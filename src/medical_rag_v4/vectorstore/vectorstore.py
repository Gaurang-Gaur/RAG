from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
from medical_rag_v4.embeddings.embeddings import embedding_model;

chroma_path = Path(__file__).parent.parent / "data" / "chroma_db"

client = chromadb.PersistentClient(
    path=str(chroma_path)
)

collection = client.get_or_create_collection(
    name="medical_reports"
)


def add_chunks(chunks):
    texts = [chunk.page_content for chunk in chunks]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts
    ).tolist()

    ids = [
        f"{chunk.metadata['user_id']}_"
        f"{chunk.metadata['document_id']}_"
        f"{chunk.metadata['chunk_index']}"
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    return len(chunks)