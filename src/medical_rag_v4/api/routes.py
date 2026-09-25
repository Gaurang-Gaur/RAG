import hashlib
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
)

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
    tags=["RAG"],
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask(request: QuestionRequest):

    result = ask_question(
        question=request.question,
        user_id=request.user_id,
        document_id=request.document_id,
    )

    return result


@router.post(
    "/documents/upload",
    response_model=UploadResponse,
)
def upload_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):

    # Read PDF once
    file_bytes = file.file.read()

    # Generate deterministic document ID
    document_hash = hashlib.sha256(
        file_bytes
    ).hexdigest()

    document_id = document_hash

    # Save PDF
    pdf_path = (
        UPLOAD_DIR /
        f"{document_id}.pdf"
    )

    with open(pdf_path, "wb") as buffer:
        buffer.write(file_bytes)

    # Ingest
    chunks = ingest_pdf(
        pdf_path,
        user_id,
        document_id,
    )

    # Store in Chroma
    chunks_created = add_chunks(chunks)

    return {
        "message": "Document uploaded successfully",
        "document_id": document_id,
        "chunks_created": chunks_created,
    }