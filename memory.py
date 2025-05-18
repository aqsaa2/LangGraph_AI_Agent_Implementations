#In this example, the chatbot will be able to remember the user's name 
# and provide information about LangGraph.

import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing import Annotated
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_tavily import TavilySearch

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.0-flash")

# Define the state type
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Init the graph
graph_builder = StateGraph(State)

# Tools setup
tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

# Main chatbot function
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Add nodes
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# Add edges
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

memory = MemorySaver()
# Checkpoints allow the chatbot to remember previous interactions using thread_id.
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

user_input = "Hi there! My name is Will."
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)

for event in events:
    event["messages"][-1].pretty_print()

user_input = "Remember my name?"
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)

for event in events:
    event["messages"][-1].pretty_print()

events = graph.stream(
    {"messages": [{"role": "user", "content": "Remember my name?"}]},
    {"configurable": {"thread_id": "2"}},
    stream_mode="values",
)

for event in events:
    event["messages"][-1].pretty_print()

snapshot = graph.get_state(config)
print(snapshot.values)  # Shows full conversation history

