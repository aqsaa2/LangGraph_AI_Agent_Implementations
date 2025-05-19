# 🧠 Mastering LangGraph Basics

This project is a hands-on exploration of the **LangGraph** framework based on its official documentation. The implementation covers fundamental modules such as building a chatbot, adding tools and memory, incorporating human-in-the-loop workflows, customizing state, and exploring time travel functionalities.

---

## 📌 Objective

Gain a deep understanding of LangGraph by reading the official documentation and implementing the core examples from the "LangGraph basics" section.

---

## 🚀 Key Features Implemented

### 1. **Build a Basic Chatbot**
- Simple conversational bot using LangGraph nodes and edges.
- Demonstrates how to define a state and respond to user inputs.

### 2. **Add Tools**
- Integrated external tools into the LangGraph workflow.
- Example includes using a calculator or search function as part of the response generation.

### 3. **Add Memory**
- Enabled conversational memory to retain context over multiple turns.
- Showcases LangGraph’s compatibility with memory modules like LangChain’s memory systems.

### 4. **Human-in-the-Loop**
- Added decision points where human feedback or input is required.
- Demonstrates branching logic for manual control.

### 5. **Customize State**
- Custom state management logic implemented.
- Flexible handling of structured and dynamic state transitions.

### 6. **Time Travel**
- Utilized LangGraph’s state checkpoint and rollback features.
- Allows reverting to previous states for testing and debugging.

---

## 📁 Folder Structure

```
langgraph-basics/
│
├── chatbot.ipynb
├── add_tools.ipynb
├── memory.ipynb
├── human_loop.ipynb
├── customize_state.ipynb
├── time_travel.ipynb
└── README.md
```

---

## 🛠️ How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/langgraph-basics.git
   cd langgraph-basics
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Jupyter Notebooks**
   ```bash
   jupyter notebook
   ```
   Open and run each notebook (`*.ipynb`) sequentially.

---

## 🧠 Key Takeaways

- LangGraph provides a graph-based approach to building LLM workflows.
- It supports modular, transparent design and stateful execution.
- Easily integrates with LangChain for tools, memory, and agents.


