import datetime
import os
import json
import asyncio
from contextlib import AsyncExitStack
# from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.sessions import InMemorySessionService, Session
from functools import wraps
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.planners import BuiltInPlanner
from google.genai import types

{$agentOpsBlock}

# Available tools for this agent
AVAILABLE_TOOLS = {$toolNames}
# 

# Map agent types to their corresponding classes
AGENT_CLASS_MAP = {
    "LlmAgent": LlmAgent,
    "SequentialAgent": SequentialAgent,
    "ParallelAgent": ParallelAgent,
    "LoopAgent": LoopAgent,
}

# Get the agent class based on execution type
AgentClass = AGENT_CLASS_MAP.get("{$executionType}")
if AgentClass is None:
    # raise RuntimeError(f"Unknown execution_type '{$executionType}'")
    raise RuntimeError(f"Unknown execution_type '{$executionType}'")


# Initialize root agent
root_agent = AgentClass(
    model="gemini-2.5-pro",
    name="{$agentName}",
    instruction="""{$agentInstruction}""",   
    
    tools=[
        MCPToolset(
            connection_params=SseConnectionParams(
                url="{$mcpServerUrl}/sse",
                headers={'Accept': 'text/event-stream'},
            ),
            tool_filter=AVAILABLE_TOOLS,
        )
    ],
) 