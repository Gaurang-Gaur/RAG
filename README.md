Medical RAG Assistant

A Retrieval-Augmented Generation application that combines a medical knowledge base with Gemini to answer questions using retrieved context.

Flow

User -> Node.js API/Auth -> RAG service -> Query embedding -> Vector search -> Relevant medical chunks -> Gemini -> Response + sources

Main components

Gemini: generates the final response.

Python + LangChain: orchestrates ingestion, chunking, retrieval, prompts and LLM calls.

Embeddings: represent documents and queries as vectors.

Vector database: finds relevant document chunks.

Node.js backend: authentication, sessions, validation and API layer.

Frontend: chat interface and source display.

Why RAG?

The LLM does not need the complete medical knowledge base inside its model weights. Relevant information is retrieved at request time and supplied to the model as context.

Why LangChain?

LangChain is an orchestration layer. It connects the different RAG components and reduces integration code. RAG itself does not require LangChain.

RAG vs Agent

Basic RAG follows a controlled retrieve -> generate pipeline. An agent adds decision-making, such as choosing between different tools or retrieval paths.

Authentication/session

A practical flow is:

Frontend -> Node.js -> validate JWT/session -> call Python RAG service with userId/sessionId -> RAG -> Gemini -> Node.js -> Frontend

Keep authentication in the Node.js layer and keep the Python service focused on RAG/AI logic.

Medical safety

Use trusted and versioned sources, return citations where possible, and clearly state that the system is educational and not a replacement for professional medical advice.

Next steps

Complete the basic RAG pipeline.

Improve retrieval and add source citations.

Expose RAG through a Python API.

Connect Node.js authentication/session handling.

Add conversation history.

Evaluate retrieval relevance and answer grounding.

Add agentic tool selection only where it is actually useful.
