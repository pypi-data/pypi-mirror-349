"""ML Observability package for monitoring and analyzing machine learning models."""

from .observability import monitor, agent, tool, identify

# Import integrations
try:
    from .integrations.langchain import MLObservabilityCallbackHandler
except ImportError:
    # LangChain integration is optional
    pass