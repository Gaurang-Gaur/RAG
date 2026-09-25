from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form

from medical_rag_v4.generation.generation import ask_question
from medical_rag_v4.ingestion.ingestion import ingest_pdf
from medical_rag_v4.vectorstore.vectorstore import add_chunks

from .schemas import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse,
)


router = APIRouter(
    prefix="/api",
    tags=["RAG"]
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest):

    result = ask_question(
        question=request.question,
        user_id=request.user_id,
        document_id=request.document_id
    )

    return result


@router.post("/documents/upload", response_model=UploadResponse)
def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):

    # 1. Backend generates document ID
    document_id = str(uuid4())

    # 2. Create path for uploaded PDF
    pdf_path = UPLOAD_DIR / f"{document_id}.pdf"

    # 3. Save uploaded PDF
    with open(pdf_path, "wb") as buffer:
        buffer.write(file.file.read())

    # 4. Read PDF and create chunks
    chunks = ingest_pdf(
        pdf_path,
        user_id,
        document_id
    )

    # 5. Create embeddings and store chunks in Chroma
    chunks_created = add_chunks(chunks)

    # 6. Return document ID to frontend
    return {
        "message": "Document uploaded successfully",
        "document_id": document_id,
        "chunks_created": chunks_created
    }