
# LangGraph RAG Chatbot

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot using **LangGraph**, **LangChain**, and **OpenAI**. It supports conversational memory and document-based retrieval using a PDF, allowing natural language querying over documents.

---

## 🚀 Features

- ✅ Conversational chatbot with memory (via `ConversationBufferMemory`)
- ✅ PDF ingestion using LangChain's `PyPDFLoader`
- ✅ Vector-based retrieval using `FAISS`
- ✅ Custom RAG flow using LangGraph's stateful nodes and graph-based control
- ✅ Integration with OpenAI's GPT models (GPT-4, GPT-3.5)

---

## 🛠️ Technologies Used

- Python 3.10+
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- FAISS for vector similarity search
- OpenAI (for LLM)
- tiktoken (for token counting)

---

## 📁 Folder Structure

```
langgraph_chatbot/
├── main.py             # Main file to run the chatbot
├── state.py            # Defines the State object for LangGraph
├── nodes.py            # Contains graph nodes for RAG and conversation
├── graph.py            # Builds and compiles the LangGraph graph
├── ingest.py           # Loads PDF, chunks it, and creates FAISS retriever
├── utils.py            # Utility functions for setup and environment
├── README.md           # This file
└── .env                # Contains API keys (not included in repo)
```

---

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/langgraph_chatbot.git
cd langgraph_chatbot
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the dependencies**

```bash
pip install -r requirements.txt
```

> You can also install manually:
```bash
pip install langchain langgraph openai faiss-cpu tiktoken python-dotenv
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## 📄 Add Your Document

Place your PDF file in the root directory (e.g., `sample.pdf`), or change the path inside `ingest.py`.

---

## ▶️ Running the Chatbot

To run the chatbot:

```bash
python main.py
```

You’ll enter a command-line interface (CLI) where you can chat with your document-based assistant.

---

## 🧠 Key Implementation Details

- **Graph-based Flow**: LangGraph lets us build a directed graph of nodes:
  - `ingest.py`: Loads and processes the PDF.
  - `nodes.py`: Defines two nodes:
    - `retrieve_docs`: Uses the retriever to fetch top-k relevant chunks.
    - `call_rag_chain`: Constructs the prompt and calls OpenAI GPT model.
  - `graph.py`: Builds the flow:
    ```
    user_input → retrieve_docs → call_rag_chain → output
    ```
- **Memory**: Uses `ConversationBufferMemory` to maintain context between user messages.
- **Document Ingestion**:
  - Splits PDF into ~800 token chunks with 50-token overlap.
  - Embeds chunks using OpenAI Embeddings.
  - Stores vectors in FAISS index.

---

## 🧩 Optional Enhancements

- 🔧 Add Streamlit or Gradio frontend
- 🧠 Replace `ConversationBufferMemory` with `ConversationSummaryBufferMemory` for long chats
- 💾 Save and load vectorstore from disk
- 📊 Add analytics like token usage or response times
- 📚 Allow multiple document ingestion

---

## 📬 Contact

For support or questions, open an issue or contact the maintainer at [your-email@example.com].

---

## 📜 License

This project is licensed under the MIT License.
