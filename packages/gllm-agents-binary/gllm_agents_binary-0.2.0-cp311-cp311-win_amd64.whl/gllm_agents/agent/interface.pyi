import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator

class AgentInterface(ABC, metaclass=abc.ABCMeta):
    """A general and minimal interface for agent implementations.

    Defines core execution methods (`__init__`, `run`, `arun`, `arun_stream`).
    Concrete subclasses must implement all abstract methods.
    """
    name: str
    instruction: str
    description: str | None
    mcp_config: Incomplete
    a2a_config: Incomplete
    def __init__(self, name: str, instruction: str, description: str | None = None, mcp_config: dict[str, Any] | None = None, a2a_config: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """Initializes the agent.

        Args:
            name: The name of the agent.
            instruction: The core directive or system prompt for the agent.
            description: Human-readable description. Defaults to instruction if not provided.
            mcp_config: Configuration for MCP (e.g., endpoint, auth tokens).
            a2a_config: Configuration for A2A (e.g., registry URL, credentials).
            **kwargs: Additional keyword arguments for concrete implementations.
        """
    @abstractmethod
    def run(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Synchronously runs the agent.

        Args:
            query: The input query for the agent.
            **kwargs: Additional keyword arguments for execution.

        Returns:
            Dict containing at least {'output': ...}.
        """
    @abstractmethod
    async def arun(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Asynchronously runs the agent.

        Args:
            query: The input query for the agent.
            **kwargs: Additional keyword arguments for execution.

        Returns:
            Dict containing at least {'output': ...}.
        """
    @abstractmethod
    async def arun_stream(self, query: str, **kwargs: Any) -> AsyncGenerator[str | dict[str, Any], None]:
        """Asynchronously streams the agent's response.

        Args:
            query: The input query.
            **kwargs: Extra parameters for execution.

        Yields:
            Chunks of output (strings or dicts).
        """
