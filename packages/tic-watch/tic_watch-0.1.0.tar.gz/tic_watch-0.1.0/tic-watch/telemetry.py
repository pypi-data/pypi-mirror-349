from fastapi import FastAPI
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry import trace

def init_monitoring(app: FastAPI, service_name: str, connection_string: str):
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()

    exporter = AzureMonitorTraceExporter(connection_string=connection_string)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

    FastAPIInstrumentor.instrument_app(app)
    app.add_middleware(OpenTelemetryMiddleware)

    @app.on_event("startup")
    async def startup_event():
        print(f"✅ Monitoring initialized for: {service_name}")
