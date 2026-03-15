# NyayaMitra AI - Legal & CA Agentic Assistant

NyayaMitra AI is an intelligent, multi-agent assistant designed for Indian users. It leverages state-of-the-art LLMs (powered by Groq) to provide expert legal insights, draft documents, perform risk analysis, and answer tax and compliance-related queries.

## 🚀 Key Features

*   **Multi-Agent Architecture**: Built with LangChain, assigning specific queries to specialized agents:
    *   **⚖️ Legal Agent**: Handles Indian Penal Code (IPC), labor laws, and legal rights.
    *   **💼 Tax Agent (CA)**: Provides insights on GST, Income Tax slabs, and corporate compliance.
    *   **📝 Draft Agent**: Generates legal notices, NDAs, and formal corporate emails.
    *   **⚠️ Risk Agent**: Evaluates contracts or disputes to identify potential risk and legal exposure.
    *   **📄 Document Agent**: Analyzes uploaded PDFs/Contracts and extracts key clauses.
*   **Intelligent Query Routing**: The **Router Agent** acts as an AI supervisor, automatically classifying and dispatching the user's input to the most qualified backend agent.
*   **Fast & Cost-Effective Inference**: Runs entirely on **Groq's LLaMA-3 models** (`llama-3.3-70b-versatile` & `llama-3.1-8b-instant`), bypassing the high costs and quotas of traditional APIs.
*   **RAG (Retrieval-Augmented Generation)**: Uses FAISS and HuggingFace embeddings to ground AI responses in actual procedural facts and documents.
*   **Modern Web Interface**: A clean, responsive React frontend.

## 🛠️ Technology Stack

*   **Backend**: Python, FastAPI, LangChain, Groq API, Uvicorn, FAISS, SQLAlchemy.
*   **Frontend**: React (Vite), TailwindCSS, Axios.

---

## 💻 Local Quickstart Guide

### 1. Prerequisites
You must have Python 3.9+ and Node.js installed. Ensure you have generated a free API key from [Groq Console](https://console.groq.com/keys).

### 2. Backend Setup
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables:
   Open `backend/.env` and ensure you have either `GROQ_API_KEY`, `OPENAI_API_KEY`, or `OPGROQ_API_KEY` set to your `gsk_...` key. The server dynamically resolves it.
   ```env
   GROQ_API_KEY="gsk_YourRealGroqKeyHere..."
   ```
5. Start the FastAPI Development Server:
   ```bash
   export PYTHONPATH=. 
   uvicorn app.main:app --reload
   ```
   *The backend will be running at http://localhost:8000.*

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite Development Server:
   ```bash
   npm run dev
   ```
   *The frontend will be running at http://localhost:5173/.*

## 📋 Example Queries to Try
- *"What is the penalty for late audit report filing under section 44AB?"* (Routes to Tax)
- *"Draft a formal legal notice to a vendor for failing to deliver raw materials on time, causing a loss of 2 lakh rupees."* (Routes to Draft)
- *"What is the difference between a bailable and non-bailable offense under the IPC?"* (Routes to Legal)

## 🎥 Project Demo

Watch the demo video on LinkedIn:
https://www.linkedin.com/posts/selva-nidharshana-s-4a9b332a7_aiprojects-artificialintelligence-rag-activity-7438903901497544704-Lxpv?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEoHPgEBYn1wP1Js5ROeoShcvpTbPeztQI0