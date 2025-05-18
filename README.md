
# LangGraph Chatbot with Memory, Tools Integration, and Custom Post-Processing

## Overview

This project implements an intelligent chatbot using **LangGraph** and **LangChain**, designed to:

- Remember user information dynamically using conversation memory.
- Integrate external tools (TavilySearch) for enhanced responses.
- Support custom post-processing steps on chatbot outputs.
- Manage multi-threaded conversations with state persistence.

---

## Features

### 1. Memory Support with LangGraph

- The chatbot remembers previous interactions, such as the user's name.
- Conversations are stored and retrieved using a persistent checkpoint (`MemorySaver`).
- Supports multiple conversation threads using `thread_id` configuration.

### 2. Tool Integration

- The chatbot is enhanced with **TavilySearch**, a web search tool to fetch real-time information.
- Tools are integrated and conditionally triggered based on user input.

### 3. Custom Post-Processing

- A custom `postprocess` node modifies chatbot output dynamically.
- Example post-processing appends a confirmation emoji (`✅`) to all chatbot responses.
- This step can be customized for filtering, formatting, or any transformation logic.

---

## Setup

### Prerequisites

- Python 3.8+
- `langchain`, `langgraph`, `langchain_tavily`, `python-dotenv` packages
- Google GenAI API access with Gemini 2.0 Flash model
- Environment variables configured in `.env`

### Installation

```bash
pip install langchain langgraph langchain_tavily python-dotenv
```

Set your API keys in `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Usage

Run the chatbot script:

```bash
python memory.py
```

Example interaction:

```
User: Hi there! My name is Will.
Bot: Hi Will, nice to meet you! How can I help you today? ✅

User: Remember my name?
Bot: Yes, your name is Will. ✅
```

---

## Code Structure

- **State Definition:** Defines conversation state structure (`messages` list).
- **Graph Setup:** Initializes LangGraph `StateGraph` and adds nodes.
- **Chatbot Node:** Invokes LLM with integrated tools.
- **Postprocess Node:** Applies custom transformations to LLM output.
- **Tool Node:** Wraps TavilySearch tool.
- **Edges:** Defines graph flow including conditional routing to tools.
- **Memory:** Uses `MemorySaver` to persist conversation history.
- **Multi-thread Support:** `thread_id` config enables multiple independent chat sessions.

---

## Extending Post-Processing

To customize post-processing logic, modify the `postprocess` function:

```python
def postprocess(state: State) -> State:
    messages = state["messages"]
    # Example: Append emoji
    messages[-1].content += " ✅"
    return {"messages": messages}
```

This function receives and returns the chatbot state, allowing full control over responses before they are sent to the user.

---

## License

MIT License © 2025 Your Name or Organization

---

## Contact

For questions or contributions, please open an issue or contact via email: youremail@example.com

---
