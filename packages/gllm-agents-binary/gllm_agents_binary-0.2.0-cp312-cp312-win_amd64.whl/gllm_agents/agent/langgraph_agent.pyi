from gllm_agents.agent.interface import AgentInterface as AgentInterface
from langchain_core.messages import BaseMessage as BaseMessage
from langchain_core.runnables import Runnable as Runnable
from typing import Any, AsyncGenerator

class LangGraphAgent(AgentInterface):
    """An agent that wraps a compiled LangGraph graph.

    This class implements AgentInterface and uses a LangGraph `Graph`
    (typically a compiled `StateGraph`) to manage execution flow.
    """
    agent_executor: Runnable
    thread_id_key: str
    def __init__(self, name: str, instruction: str, model: Any, tools: list[Any], description: str | None = None, thread_id_key: str = 'thread_id', verbose: bool = False, mcp_config: dict[str, Any] | None = None, a2a_config: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """Initializes the LangGraphAgent.

        Args:
            name: The name of this agent.
            instruction: The system instruction for the agent, used if no initial
                         messages are provided in `arun` or `stream`.
            model: The language model instance to be used by the agent.
            tools: A list of tools the agent can use.
            description: An optional human-readable description.
            thread_id_key: The key used in the `configurable` dict to pass the thread ID
                           to the LangGraph methods (ainvoke, astream_events).
            verbose: If True, sets langchain.debug = True for verbose LangChain logs.
            mcp_config: Configuration for MCP support.
            a2a_config: Configuration for A2A support.
            **kwargs: Additional keyword arguments passed to the parent `__init__`.
        """
    def run(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Synchronously runs the LangGraph agent by wrapping `arun`.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
            **kwargs: Additional keyword arguments passed to `arun`.

        Returns:
            A dictionary containing the agent's response.

        Raises:
            RuntimeError: If `asyncio.run()` is called from an already running event loop.
        """
    async def arun(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Asynchronously runs the LangGraph agent.

        Prepares input messages (including system instruction if no messages are provided)
        and invokes the graph using `ainvoke`.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
                          The `thread_id_key` defined in `__init__` is expected here.
            **kwargs: Additional keyword arguments, including `messages` if providing
                      a full message history instead of a single query.

        Returns:
            A dictionary containing the agent's output and the full final state from the graph.
        """
    async def arun_stream(self, query: str, configurable: dict[str, Any] | None = None, **kwargs: Any) -> AsyncGenerator[str | dict[str, Any], None]:
        """Asynchronously streams the LangGraph agent's response.

        Prepares input messages and streams events from the graph using `astream_events`.
        Yields content chunks from `on_chat_model_stream` events.

        Args:
            query: The input query for the agent.
            configurable: Optional dictionary for LangGraph configuration (e.g., thread_id).
            **kwargs: Additional keyword arguments, including `messages` if providing
                      a full message history instead of a single query.

        Yields:
            Text chunks from the language model's streaming response.
        """
