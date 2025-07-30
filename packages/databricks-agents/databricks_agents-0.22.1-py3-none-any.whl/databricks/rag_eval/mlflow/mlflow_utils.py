"""Helper functions to convert RagEval entities to MLflow entities."""

import time
from typing import List, Optional, Union

import mlflow
import numpy as np
import pandas as pd
from mlflow import MlflowClient, MlflowException
from mlflow import entities as mlflow_entities
from mlflow import evaluation as mlflow_eval
from mlflow.deployments import get_deploy_client, get_deployments_target
from mlflow.entities import metric as mlflow_metric
from mlflow.models import evaluation as mlflow_models_evaluation

from databricks.rag_eval import env_vars, schemas
from databricks.rag_eval.evaluation import datasets, entities
from databricks.rag_eval.utils import collection_utils, enum_utils, error_utils

_DEFAULT_MLFLOW_DEPLOYMENT_TARGET = "databricks"


class EvaluationErrorCode(enum_utils.StrEnum):
    MODEL_ERROR = "MODEL_ERROR"


def eval_result_to_mlflow_evaluation(
    eval_result: entities.EvalResult,
) -> mlflow_eval.Evaluation:
    """
    Convert an EvalResult object to an MLflow Evaluation object.

    :param eval_result: EvalResult object
    :return: MLflow Evaluation object
    """
    eval_item = eval_result.eval_item
    # Inputs
    inputs = {}
    # In either case, "custom_inputs" are a key inside raw_request, as a sister of "messages".
    if eval_item.has_inputs_outputs:
        # True if the user used inputs/outputs schema. raw_request is guaranteed to be a dict.
        inputs = eval_item.raw_request
    else:  # The user used request/response schema.
        # If the user used custom_inputs, display the whole request instead of just the question.
        if eval_item.custom_inputs:
            inputs["messages"] = eval_item.raw_request.get("messages")
            inputs[schemas.CUSTOM_INPUTS_COL] = eval_item.custom_inputs
        else:
            inputs[schemas.REQUEST_COL] = eval_item.question or eval_item.raw_request

    outputs = {}
    if eval_item.retrieval_context:
        outputs[schemas.RETRIEVED_CONTEXT_COL] = (
            eval_item.retrieval_context.to_output_dict()
        )

    # Outputs are higher-level than trace.outputs. It includes extracted information about retrieved
    # docs, tool calls, etc, thus we always store the trace.outputs under "response".

    # If the user used inputs/outputs schema, or has custom outputs, display the whole response.
    if eval_item.has_inputs_outputs or eval_item.custom_outputs:
        outputs[schemas.RESPONSE_COL] = eval_item.raw_response
    else:
        outputs[schemas.RESPONSE_COL] = eval_item.answer or eval_item.raw_response

    if eval_item.tool_calls:
        outputs[schemas.TOOL_CALLS_COL] = eval_item.tool_calls
    if eval_item.custom_outputs:
        outputs[schemas.CUSTOM_OUTPUTS_COL] = eval_item.custom_outputs

    # Targets
    targets = {}
    if eval_item.ground_truth_answer:
        targets[schemas.EXPECTED_RESPONSE_COL] = eval_item.ground_truth_answer
    if eval_item.ground_truth_retrieval_context:
        targets[schemas.EXPECTED_RETRIEVED_CONTEXT_COL] = (
            eval_item.ground_truth_retrieval_context.to_output_dict()
        )
    if eval_item.expected_facts:
        targets[schemas.EXPECTED_FACTS_COL] = eval_item.expected_facts
    if eval_item.guidelines:
        targets[schemas.GUIDELINES_COL] = eval_item.guidelines
    if eval_item.custom_expected:
        targets[schemas.CUSTOM_EXPECTED_COL] = eval_item.custom_expected

    # Assessments
    assessments = []
    for assessment_result in eval_result.assessment_results:
        assessments.extend(
            collection_utils.to_list(
                assessment_result_to_mlflow_assessments(assessment_result)
            )
        )
    # Overall assessment
    if eval_result.overall_assessment is not None:
        assessments.append(
            mlflow_assessment_v3_to_v2(
                eval_result.overall_assessment.to_mlflow_assessment()
            )
        )
    # Assessments from custom metrics
    assessments.extend(
        [
            mlflow_assessment_v3_to_v2(assessment=assessment)
            for assessment in _get_mlflow_assessment_to_log_from_metric_results(
                eval_result.metric_results
            )
        ]
    )

    # Metrics
    metrics = eval_result_to_mlflow_metrics(eval_result)

    # Tags
    tags = {}
    if eval_item.managed_evals_eval_id:
        tags[schemas.MANAGED_EVALS_EVAL_ID_COL] = eval_item.managed_evals_eval_id
    if eval_item.managed_evals_dataset_id:
        tags[schemas.MANAGED_EVALS_DATASET_ID_COL] = eval_item.managed_evals_dataset_id
    if eval_item.source_id:
        tags[schemas.SOURCE_ID_COL] = eval_item.source_id

    error_message = None
    error_code = None
    if eval_item.model_error_message:
        error_code = EvaluationErrorCode.MODEL_ERROR
        error_message = eval_item.model_error_message

    evaluation = mlflow_eval.Evaluation(
        inputs=inputs,
        outputs=outputs,
        inputs_id=eval_item.question_id,
        request_id=eval_item.trace.info.request_id if eval_item.trace else None,
        targets=targets,
        error_code=error_code,
        error_message=error_message,
        assessments=assessments,
        metrics=metrics,
        tags=tags,
    )
    return evaluation


def eval_result_to_mlflow_metrics(
    eval_result: entities.EvalResult,
) -> List[mlflow_metric.Metric]:
    """Get a list of MLflow Metric objects from an EvalResult object."""
    return [
        _construct_mlflow_metrics(
            key=k,
            value=v,
        )
        for k, v in eval_result.get_metrics_dict().items()
        # Do not log metrics with non-numeric-or-boolean values
        if isinstance(v, (int, float, bool))
    ]


def _construct_mlflow_metrics(
    key: str, value: Union[int, float, bool]
) -> mlflow_metric.Metric:
    """
    Construct an MLflow Metric object from key and value.
    Timestamp is the current time and step is 0.
    """
    return mlflow_metric.Metric(
        key=key,
        value=value,
        timestamp=int(time.time() * 1000),
        step=0,
    )


# TODO(ML-52850): Remove this function when we remove AssessmentV2
def mlflow_assessment_v3_to_v2(
    assessment: mlflow_entities.Assessment,
    assessment_name: Optional[str] = None,
    assessment_source: Optional[mlflow_eval.AssessmentSource] = None,
) -> mlflow_eval.Assessment:
    """
    Convert an MLflow AssessmentV3 object to an MLflow AssessmentV2 object.
    :param assessment: MLflow AssessmentV3 object
    :param assessment_name: (Optional) Name of the assessment
    :param assessment_source: (Optional) Source of the assessment
    :return: MLflow AssessmentV2 object
    """
    # Convert the source type from V2 to V3
    source_type = {
        mlflow_entities.AssessmentSourceType.LLM_JUDGE: mlflow_eval.AssessmentSourceType.LLM_JUDGE,
        mlflow_entities.AssessmentSourceType.CODE: mlflow_eval.AssessmentSourceType.CODE,
        mlflow_entities.AssessmentSourceType.HUMAN: mlflow_eval.AssessmentSourceType.HUMAN,
    }.get(
        assessment.source.source_type,
        mlflow_eval.AssessmentSourceType.CODE,
    )

    assessment_source = assessment_source or mlflow_eval.AssessmentSource(
        source_type=source_type,
        source_id=assessment.source.source_id,
    )

    # Backwards compatibility for the chunk index key (used in AssessmentV2) from the span output key (used in AssessmentV3)
    if (
        assessment.metadata is not None
        and entities._SPAN_OUTPUT_KEY in assessment.metadata
    ):
        assessment.metadata[entities._CHUNK_INDEX_KEY] = int(
            assessment.metadata.pop(entities._SPAN_OUTPUT_KEY)
        )

    return mlflow_eval.Assessment(
        name=assessment_name or assessment.name,
        source=assessment_source,
        value=(
            assessment.feedback.value
            if assessment.feedback.value is not None and assessment.feedback.value != ""
            else None
        ),
        rationale=assessment.rationale,
        metadata=assessment.metadata,
        error_code=(
            assessment.error.error_code if assessment.error is not None else None
        ),
        error_message=(
            assessment.error.error_message if assessment.error is not None else None
        ),
    )


def assessment_result_to_mlflow_assessments(
    assessment_result: entities.AssessmentResult,
    assessment_name: Optional[str] = None,
    assessment_source: Optional[mlflow_eval.AssessmentSource] = None,
) -> Union[mlflow_eval.Assessment, List[mlflow_eval.Assessment]]:
    """
    Convert an AssessmentResult object to MLflow AssessmentV2 objects.
    :param assessment_result: AssessmentResult object
    :return: one or a list of MLflow Assessment objects
    """
    if not (
        isinstance(assessment_result, entities.PerRequestAssessmentResult)
        or isinstance(assessment_result, entities.PerChunkAssessmentResult)
    ):
        raise ValueError(
            f"Unsupported assessment result type: {type(assessment_result)}"
        )
    mlflow_assessments = assessment_result.to_mlflow_assessment()
    if isinstance(mlflow_assessments, list):
        return [
            mlflow_assessment_v3_to_v2(
                assessment=assessment,
                assessment_name=assessment_name,
                assessment_source=assessment_source,
            )
            for assessment in mlflow_assessments
        ]
    else:
        return mlflow_assessment_v3_to_v2(
            assessment=mlflow_assessments,
            assessment_name=assessment_name,
            assessment_source=assessment_source,
        )


def _get_mlflow_assessment_to_log_from_metric_results(
    metric_results: List[entities.MetricResult],
) -> List[mlflow_entities.Assessment]:
    """Get a list of MLflow Assessment objects from a list of MetricResult objects."""
    return [
        assessment
        for metric in metric_results
        if not metric.legacy_metric and (assessment := metric.to_mlflow_assessment())
    ]


def _cast_to_pandas_dataframe(
    data: Union[pd.DataFrame, np.ndarray], flatten: bool = True
) -> pd.DataFrame:
    """
    Cast data to a pandas DataFrame. If already a pandas DataFrame, passes the data through.
    :param data: Data to cast to a pandas DataFrame
    :param flatten: Whether to flatten the data from 2d to 1d
    :return: A pandas DataFrame
    """
    if isinstance(data, pd.DataFrame):
        return data

    data = data.tolist()
    if flatten:
        data = [item for feature in data for item in feature]
    try:
        return pd.DataFrame(data)
    except Exception as e:
        raise error_utils.ValidationError(
            f"Data must be a DataFrame or a list of dictionaries. Got: {type(data[0])}"
        ) from e


def _validate_mlflow_dataset(ds: mlflow_models_evaluation.EvaluationDataset):
    """Validates an MLflow evaluation dataset."""
    features_df = _cast_to_pandas_dataframe(ds.features_data)

    # Validate max number of rows in the eval dataset
    if len(features_df) > env_vars.RAG_EVAL_MAX_INPUT_ROWS.get():
        raise error_utils.ValidationError(
            f"The number of rows in the dataset exceeds the maximum: {env_vars.RAG_EVAL_MAX_INPUT_ROWS.get()}. "
            f"Got {len(features_df)} rows." + error_utils.CONTACT_FOR_LIMIT_ERROR_SUFFIX
        )
    if ds.predictions_data is not None:
        # Predictions data is one-dimensional so it does not need to be flattened
        predictions_df = _cast_to_pandas_dataframe(ds.predictions_data, flatten=False)
        assert features_df.shape[0] == predictions_df.shape[0], (
            f"Features data and predictions must have the same number of rows. "
            f"Features: {features_df.shape[0]}, Predictions: {predictions_df.shape[0]}"
        )


def mlflow_dataset_to_evaluation_dataset(
    ds: mlflow_models_evaluation.EvaluationDataset,
) -> datasets.EvaluationDataframe:
    """Creates an instance of the class from an MLflow evaluation dataset and model predictions."""
    _validate_mlflow_dataset(ds)
    df = _cast_to_pandas_dataframe(ds.features_data).copy()
    if ds.predictions_data is not None:
        # Predictions data is one-dimensional so it does not need to be flattened
        df[schemas.RESPONSE_COL] = _cast_to_pandas_dataframe(
            ds.predictions_data, flatten=False
        )
    return datasets.EvaluationDataframe(df)


def infer_experiment_from_endpoint(endpoint_name: str) -> mlflow.entities.Experiment:
    deploy_client = get_deploy_client(resolve_deployments_target())
    try:
        endpoint = deploy_client.get_endpoint(endpoint_name)
        served_models = endpoint.get("config", endpoint.get("pending_config", {})).get(
            "served_models", []
        )
        if not served_models:
            raise ValueError(f"No served models found for endpoint '{endpoint_name}'.")
        served_model = served_models[0]
        model_name = served_model.get("model_name")
        model_version = served_model.get("model_version")
        client = MlflowClient()
        model_info = client.get_model_version(model_name, model_version)
        experiment_id = client.get_run(model_info.run_id).info.experiment_id
        return mlflow.get_experiment(experiment_id)
    except Exception as e:
        raise Exception(
            f"Failed to infer the experiment for endpoint '{endpoint_name}'. "
            f"Please provide 'experiment_id' explicitly:\n{e}"
        ) from e


def resolve_deployments_target() -> str:
    """
    Resolve the current deployment target for MLflow deployments.

    If the deployment target is not set, use the default deployment target.

    We need this because user might set the deployment target explicitly using `set_deployments_target` to use
    endpoints from another workspace. We want to respect that config.
    """
    try:
        return get_deployments_target()
    except MlflowException:
        return _DEFAULT_MLFLOW_DEPLOYMENT_TARGET
