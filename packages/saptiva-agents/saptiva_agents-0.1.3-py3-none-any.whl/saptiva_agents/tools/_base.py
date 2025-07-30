from autogen_ext.tools.mcp._base import McpToolAdapter
from autogen_core.tools import BaseToolWithState, BaseTool, Tool, ToolSchema


class McpToolAdapter(McpToolAdapter):
    """
    Base adapter class for MCP tools to make them compatible with AutoGen.
    """
    pass


class Tool(Tool):
    pass


class BaseTool(BaseTool):
    pass


class BaseToolWithState(BaseToolWithState):
    pass

