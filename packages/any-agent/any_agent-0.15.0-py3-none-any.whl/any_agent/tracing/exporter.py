import json
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Protocol, assert_never

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SpanExportResult,
)
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from any_agent import AgentFramework, TracingConfig
from any_agent.logging import logger

from .processors import TracingProcessor
from .trace import AgentSpan, AgentTrace

if TYPE_CHECKING:
    from opentelemetry.sdk.trace import ReadableSpan


class AnyAgentExporter(SpanExporter):
    """Build an `AgentTrace` and export to the different outputs."""

    def __init__(  # noqa: D107
        self,
        agent_framework: AgentFramework,
        tracing_config: TracingConfig,
    ):
        self.agent_framework = agent_framework
        self.tracing_config = tracing_config
        self.traces: dict[int, AgentTrace] = {}
        self.processor: TracingProcessor | None = TracingProcessor.create(
            agent_framework
        )
        self.console: Console | None = None
        self.run_trace_mapping: dict[str, int] = {}

        if self.tracing_config.console:
            self.console = Console()

    def print_to_console(self, span_kind: str, interaction: Mapping[str, Any]) -> None:
        """Print the span to the console."""
        if not self.console:
            msg = "Console is not initialized"
            raise RuntimeError(msg)
        style = getattr(self.tracing_config, span_kind.lower(), None)
        if not style or interaction == {}:
            return

        self.console.rule(span_kind, style=style)

        for key, value in interaction.items():
            if key == "output":
                self.console.print(
                    Panel(
                        Markdown(str(value or "")),
                        title="Output",
                    ),
                )
            else:
                self.console.print(f"{key}: {value}")

        self.console.rule(style=style)

    def export(self, spans: Sequence["ReadableSpan"]) -> SpanExportResult:  # noqa: D102
        if not self.processor:
            return SpanExportResult.SUCCESS

        for readable_span in spans:
            # Check if this span belongs to our run
            if not readable_span.attributes:
                continue
            agent_run_id = readable_span.attributes.get("any_agent.run_id")
            trace_id = readable_span.context.trace_id
            if agent_run_id is not None:
                assert isinstance(agent_run_id, str)
                self.run_trace_mapping[agent_run_id] = trace_id
            span = AgentSpan.from_readable_span(readable_span)
            if not self.traces.get(trace_id):
                self.traces[trace_id] = AgentTrace()
            try:
                span.attributes["service.name"] = (
                    self.processor._get_agent_framework().value
                )
                span_kind, interaction = self.processor.extract_interaction(span)
                if span_kind == "LLM" and self.tracing_config.cost_info:
                    span.add_cost_info()

                self.traces[trace_id].add_span(span)

                if self.tracing_config.console and self.console:
                    self.print_to_console(span_kind, interaction)

            except (json.JSONDecodeError, TypeError, AttributeError) as e:
                logger.warning("Failed to parse span data, %s, %s", span, e)
                continue
        return SpanExportResult.SUCCESS

    def pop_trace(
        self,
        agent_run_id: str,
    ) -> AgentTrace:
        """Pop the trace for the given agent run ID."""
        trace_id = self.run_trace_mapping.pop(agent_run_id, None)
        if trace_id is None:
            msg = f"Trace ID not found for agent run ID: {agent_run_id}"
            raise ValueError(msg)
        trace = self.traces.pop(trace_id, None)
        if trace is None:
            msg = f"Trace not found for trace ID: {trace_id}"
            raise ValueError(msg)
        return trace


class Instrumenter(Protocol):  # noqa: D101
    def instrument(self, *, tracer_provider: TracerProvider) -> None: ...  # noqa: D102

    def uninstrument(self) -> None: ...  # noqa: D102


def get_instrumenter_by_framework(framework: AgentFramework) -> Instrumenter:
    """Get the instrumenter for the given agent framework."""
    if framework is AgentFramework.OPENAI:
        from openinference.instrumentation.openai_agents import (
            OpenAIAgentsInstrumentor,
        )

        return OpenAIAgentsInstrumentor()

    if framework is AgentFramework.SMOLAGENTS:
        from openinference.instrumentation.smolagents import SmolagentsInstrumentor

        return SmolagentsInstrumentor()

    if framework is AgentFramework.LANGCHAIN:
        from openinference.instrumentation.langchain import LangChainInstrumentor

        return LangChainInstrumentor()

    if framework is AgentFramework.LLAMA_INDEX:
        from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

        return LlamaIndexInstrumentor()

    if (
        framework is AgentFramework.GOOGLE
        or framework is AgentFramework.AGNO
        or framework is AgentFramework.TINYAGENT
    ):
        msg = f"{framework} tracing is not supported."
        raise NotImplementedError(msg)

    assert_never(framework)
