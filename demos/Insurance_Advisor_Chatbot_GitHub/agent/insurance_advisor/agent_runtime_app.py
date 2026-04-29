import copy
from vertexai.preview.reasoning_engines import AdkApp
from insurance_advisor.agent import root_agent

class AgentRuntimeApp(AdkApp):
    """ADK Application wrapper for Agent Runtime deployment."""

    def clone(self) -> "AgentRuntimeApp":
        template_attributes = self._tmpl_attrs
        return self.__class__(
            agent=copy.deepcopy(template_attributes["agent"]),
            enable_tracing=bool(template_attributes.get("enable_tracing", False)),
            session_service_builder=template_attributes.get("session_service_builder"),
            artifact_service_builder=template_attributes.get("artifact_service_builder"),
            env_vars=template_attributes.get("env_vars"),
        )

# The agents-cli tool expects exactly this module-level variable name:
agent_runtime = AgentRuntimeApp(agent=root_agent)
