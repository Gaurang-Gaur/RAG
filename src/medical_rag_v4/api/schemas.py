from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str
    user_id: str
    document_id: str


class Source(BaseModel):
    document_id: str
    page: int | None
    chunk_index: int | None


class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    message: str
    document_id: str
    chunks_created: int