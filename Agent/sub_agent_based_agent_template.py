import datetime
import os
import json
import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.sessions import InMemorySessionService, Session
from functools import wraps
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any, List
from typing import Optional
from google.adk.planners import BuiltInPlanner
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

{$agentOpsBlock}

# Helper to filter tools by name
def filter_tools(tools, allowed_names):
    return [tool for tool in tools if tool.name in allowed_names]

# Map agent types to their corresponding classes
AGENT_CLASS_MAP = {
    "LlmAgent": LlmAgent,
    "SequentialAgent": SequentialAgent,
    "ParallelAgent": ParallelAgent,
    "LoopAgent": LoopAgent,
}

# Get the agent class based on execution type
execution_type = "{$executionType}"
AgentClass = AGENT_CLASS_MAP.get(execution_type)
if AgentClass is None:
    raise RuntimeError(f"Unknown execution_type '{execution_type}'")

# Create sub-agents
{$subAgentBlocks}

# Initialize root agent with sub-agents
root_agent = LlmAgent(
    model="{$agentModel}",
    name="{$agentName}",
    instruction="""{$agentInstruction}""",    
    sub_agents={$subAgentVarList}
) 