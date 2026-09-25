from pathlib import Path

import chromadb

from medical_rag_v4.embeddings.embeddings import embedding_model


# Keep Chroma data outside the source package
chroma_path = Path(__file__).parent.parent / "data" / "chroma_db"

client = chromadb.PersistentClient(
    path=str(chroma_path)
)

collection = client.get_or_create_collection(
    name="medical_reports"
)


def add_chunks(chunks):
    if not chunks:
        return 0

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    metadatas = [
        chunk.metadata
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts
    ).tolist()

    user_id = chunks[0].metadata["user_id"]
    document_id = chunks[0].metadata["document_id"]

    ids = [
        f"{user_id}_{document_id}_{chunk.metadata['chunk_index']}"
        for chunk in chunks
    ]

    # Remove previous version of this document.
    # This makes re-uploading the same document safe.
    collection.delete(
        where={
            "$and": [
                {"user_id": user_id},
                {"document_id": document_id},
            ]
        }
    )

    # Insert the fresh chunks
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

    return len(chunks)