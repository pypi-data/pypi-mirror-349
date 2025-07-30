"""This module provides general helpers for traces with no dependencies on the agent evaluation harness."""

import uuid
from typing import Any, Dict, List, Optional

import mlflow
import mlflow.entities as mlflow_entities
import mlflow.tracing.constant as mlflow_tracing_constant
from mlflow.entities import trace_status


def span_is_type(
    span: mlflow_entities.Span,
    span_type: str | List[str],
) -> bool:
    """Check if the span is of a certain span type or one of the span types in the collection"""
    if span.attributes is None:
        return False
    if not isinstance(span_type, List):
        span_type = [span_type]
    return (
        span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE)
        in span_type
    )


def get_leaf_spans(trace: mlflow_entities.Trace) -> List[mlflow_entities.Span]:
    """Get all leaf spans in the trace."""
    if trace.data is None:
        return []
    spans = trace.data.spans or []
    leaf_spans_by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_id:
            leaf_spans_by_id.pop(span.parent_id, None)
    return list(leaf_spans_by_id.values())


def get_root_span(trace: mlflow_entities.Trace) -> Optional[mlflow_entities.Span]:
    """Get the root span in the trace."""
    if trace.data is None:
        return None
    spans = trace.data.spans or []
    # Root span is the span that has no parent
    return next((span for span in spans if span.parent_id is None), None)


# ================== Trace Creation/Modification ==================
def _generate_trace_id() -> str:
    """
    Generate a new trace ID. This is a 16-byte hex string.
    """
    return uuid.uuid4().hex


def _generate_span_id() -> str:
    """
    Generate a new span ID. This is a 8-byte hex string.
    """
    return uuid.uuid4().hex[:16]  # OTel span spec says it's only 8 bytes (16 hex chars)


def create_minimal_trace(
    request: Dict[str, Any],
    response: Any,
    retrieval_context: Optional[List[mlflow_entities.Document]] = None,
    status: str = trace_status.TraceStatus.OK,
) -> mlflow_entities.Trace:
    """
    Create a minimal trace object with a single span, based on given request/response. If
    retrieval context is provided, a retrieval span is added.

    :param request: The request object. This is expected to be a JSON-serializable object
    :param response: The response object. This is expected to be a JSON-serializable object, but we cannot guarantee this
    :param retrieval_context: Optional list of documents retrieved during processing
    :return: A trace object.
    """
    client = mlflow.MlflowClient()
    root_span = client.start_trace(
        name="root_span",
        inputs=request,
        attributes={
            mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE: mlflow_entities.SpanType.CHAIN
        },
    )
    trace_id = root_span.request_id

    # Add retrieval span if retrieval context is provided
    if retrieval_context is not None:
        retrieval_span = client.start_span(
            name="retrieval_span",
            request_id=trace_id,
            parent_id=root_span.span_id,
            span_type=mlflow_entities.SpanType.RETRIEVER,
        )
        retrieval_span.set_outputs([doc.to_dict() for doc in retrieval_context])
        client.end_span(
            request_id=trace_id,
            span_id=retrieval_span.span_id,
        )

    client.end_trace(
        request_id=trace_id,
        outputs=response,
        status=status,
    )
    return client.get_trace(trace_id)


def inject_experiment_run_id_to_trace(
    trace: mlflow_entities.Trace, experiment_id: str, run_id: str
) -> mlflow_entities.Trace:
    """
    Inject the experiment and run ID into the trace metadata.

    :param trace: The trace object
    :param experiment_id: The experiment ID to inject
    :param run_id: The run ID to inject
    :return: The updated trace object
    """
    if trace.info.request_metadata is None:
        trace.info.request_metadata = {}
    trace.info.request_metadata[mlflow_tracing_constant.TraceMetadataKey.SOURCE_RUN] = (
        run_id
    )
    trace.info.experiment_id = experiment_id
    return trace


def clone_trace_to_reupload(trace: mlflow_entities.Trace) -> mlflow_entities.Trace:
    """
    Prepare a trace for cloning by resetting traceId and clearing various fields.
    This has the downstream effect of causing the trace to be recreated with a new trace_id.

    :param trace: The trace to prepare
    :return: The prepared trace
    """
    prepared_trace = mlflow_entities.Trace.from_dict(trace.to_dict())

    # Since the semantics of this operation are to _clone_ the trace, and assessments are tied to
    # a specific trace, we clear assessments as well.
    prepared_trace.info.assessments = []

    # Tags and metadata also contain references to the source run, trace data artifact location, etc.
    # We clear these as well to ensure that the trace is not tied to the original source of the trace.
    for key in [k for k in prepared_trace.info.tags.keys() if k.startswith("mlflow.")]:
        prepared_trace.info.tags.pop(key)
    for key in [
        k
        for k in prepared_trace.info.request_metadata.keys()
        if k.startswith("mlflow.")
        and k
        not in [
            mlflow_tracing_constant.TraceMetadataKey.INPUTS,
            mlflow_tracing_constant.TraceMetadataKey.OUTPUTS,
        ]
    ]:
        prepared_trace.info.request_metadata.pop(key)

    prepared_trace.info.request_id = "tr-" + str(uuid.uuid4().hex)
    # We skip updating the spans here to avoid issues with blob storage retrievals
    return prepared_trace
