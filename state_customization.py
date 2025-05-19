# This code builds a LangGraph-powered conversational agent 
# that uses tools (search, human help), supports pausing for 
# human input, and keeps memory using a structured state.

import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_tavily import TavilySearch
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize the chat model
llm = init_chat_model("google_genai:gemini-2.0-flash")


# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

# Define the human assistance tool
# Used the human_assistance tool to introduce a controlled 
# interruption for manual human input before updating the state.
@tool
def human_assistance(
    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "name": name,
            "birthday": birthday,
        },
    )
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    else:
        verified_name = human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"

    state_update = {
        "name": verified_name,
        "birthday": verified_birthday,
        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
    }
    return Command(update=state_update)


tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]

llm_with_tools = llm.bind_tools(tools)

# Define chatbot node
def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

# Build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Now you can run the graph
user_input = (
    "Can you look up when LangGraph was released? "
    "When you have the answer, use the human_assistance tool for review."
)
config = {"configurable": {"thread_id": "1"}}
# Stream the graph with user input
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}], "name": "", "birthday": ""},
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

human_command = Command(
    resume={
        "name": "LangGraph",
        "birthday": "Jan 17, 2024",
    },
)
# The human command is used to update the state
# with the information provided by the human
# The human command is used to update the state

events = graph.stream(human_command, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
# Get the state of the graph
# after the human command
{k: v for k, v in snapshot.values.items() if k in ("name", "birthday")}

graph.update_state(config, {"name": "LangGraph (library)"})

snapshot = graph.get_state(config)

{k: v for k, v in snapshot.values.items() if k in ("name", "birthday")}