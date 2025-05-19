# Working!!!

# Task: building a chatbot, adding tools, memory, 
# human-in-the-loop capabilities, state customization, and time travel.

import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]
# It's the core building block in LangGraph,
# defines how the flow of actions occurs.
# We define it with a custom State, which is like a 
# schema for what your graph will carry (e.g., messages).

graph_builder = StateGraph(State)
# Here we are using the Google Gemini model.
# The temperature parameter controls the randomness of the model's output.
# A higher temperature (e.g., 0.7) makes the output more random
llm = init_chat_model("google_genai:gemini-2.0-flash", temperature=0.7)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
# The chatbot function takes the current state as input
# and returns a new state with the chatbot's response.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
# Save the graph visualization to a PNG file
png_data = graph.get_graph().draw_mermaid_png()
with open("graph_visualization.png", "wb") as f:
    f.write(png_data)

print("Graph visualization saved to graph_visualization.png")
