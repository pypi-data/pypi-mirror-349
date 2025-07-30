import contextvars
from functools import wraps, partial
from typing import Any, Callable

from flask.app import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

from insightconnect_plugin_runtime.plugin import Plugin
from insightconnect_plugin_runtime.util import is_running_in_cloud, OTEL_ENDPOINT


def init_tracing(app: Flask, plugin: Plugin, endpoint: str) -> None:
    """
    Initialize OpenTelemetry Tracing

    The function sets up the tracer provider, span processor and exporter with auto-instrumentation

    :param app: The Flask Application
    :param plugin: The plugin to derive the service name from
    :param endpoint: The Otel Endpoint to emit traces to
    """

    if not is_running_in_cloud():
        return

    resource = Resource(attributes={"service.name": f'{plugin.name.lower().replace(" ", "_")}-{plugin.version}'})

    trace_provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint)
    trace_provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(trace_provider)

    FlaskInstrumentor().instrument_app(app)

    def requests_callback(span: trace.Span, _: Any, response: Any) -> None:
        if hasattr(response, "status_code"):
            span.set_status(Status(StatusCode.OK if response.status_code < 400 else StatusCode.ERROR))

    RequestsInstrumentor().instrument(trace_provider=trace_provider, response_hook=requests_callback)


def auto_instrument(func: Callable) -> Callable:
    """
    Decorator that auto-instruments a function with a trace

    :param func: function to instrument
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__):
            return func(*args, **kwargs)

    return wrapper


def create_post_fork(app_getter: Callable, plugin_getter: Callable, config_getter: Callable) -> Callable:
    def post_fork(server, worker):
        app = app_getter()
        plugin = plugin_getter()
        endpoint = config_getter().get(OTEL_ENDPOINT, None)
        if endpoint:
            init_tracing(app, plugin, endpoint)

    return post_fork


def with_context(context: contextvars.Context, function: Callable) -> Callable:
    """
    Creates a wrapper function that executes the target function with the specified context.

    :param context: The Context object to apply when executing the function
    :type context: contextvars.Context

    :param function: The function to wrap with the specified context
    :type function: Callable

    :return: A wrapper function that applies the context when called
    :rtype: Callable
    """

    def _wrapper(context_: contextvars.Context, function_: Callable, *args, **kwargs):
        return context_.copy().run(function_, *args, **kwargs)

    return partial(_wrapper, context, function)
