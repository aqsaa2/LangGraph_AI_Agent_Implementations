from typing import Annotated, Dict, List, Any
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.types import Command, interrupt

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool

from langchain_core.runnables import RunnableLambda


# 1. Generalized State to handle any key-value pairs
class GeneralState(TypedDict):
    messages: Annotated[List, add_messages]
    data: Dict[str, Any]


# 2. Human assistance tool (dynamic fields)
@tool
def human_assistance(
    data: Dict[str, Any],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Request human review of arbitrary data."""
    human_response = interrupt(
        {
            "question": "Is this information correct?",
            "data": data
        }
    )
    
    if human_response.get("correct", "").lower().startswith("y"):
        verified_data = data
        response = "Verified as correct"
    else:
        # Use human-provided corrections
        verified_data = human_response.get("data", data)
        response = f"Corrections applied: {verified_data}"

    return Command(update={
        "data": verified_data,
        "messages": [ToolMessage(content=response, tool_call_id=tool_call_id)]
    })


# 3. A sample node that simulates a lookup and calls human review
def lookup_node(state: GeneralState) -> Command:
    # Simulate extracting key-value data from user question
    extracted_data = {
        "LangGraph": "Jan 17, 2024",
        "Python": "Feb 20, 1991"
    }
    return Command(
        add={
            "messages": [{"role": "system", "content": "Extracted info, sending to human_assistance"}],
        },
        invoke={
            "human_assistance": {
                "data": extracted_data
            }
        }
    )


# 4. Define the Graph
builder = StateGraph(GeneralState)

builder.add_node("lookup", lookup_node)
builder.add_node("human_assistance", human_assistance)

# Workflow: lookup -> human_assistance -> END
builder.set_entry_point("lookup")
builder.add_edge("lookup", "human_assistance")
builder.add_edge("human_assistance", END)

# 5. Build the graph
graph = builder.compile()


# 6. Run a session
config = {"configurable": {"thread_id": "1"}}
user_input = "When was Python released? Review it via human_assistance."

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)

print(">>> INITIAL STREAM")
for event in events:
    if "messages" in event:
        print(event["messages"][-1].content)

# 7. Human review command (simulating human)
human_command = Command(resume={"data": {"LangGraph": "Jan 17, 2024", "Python": "Feb 20, 1991"}})

events = graph.stream(human_command, config, stream_mode="values")

print("\n>>> AFTER HUMAN REVIEW")
for event in events:
    if "messages" in event:
        print(event["messages"][-1].content)

# 8. Inspect the final state
snapshot = graph.get_state(config)
print("\n>>> FINAL STATE DATA:")
print(snapshot.values["data"])
