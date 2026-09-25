# from sentence_transformers import SentenceTransformer
# from medical_rag_v4.ingestion.ingestion import ingest_pdf;
# from pathlib import Path
# pdf_path = Path(__file__).parent.parent / "data" / "synthetic_single_patient_medical_record.pdf"
# #manual add of pdf after apis is create no use of this
# embedding_model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )



# collection = client.get_or_create_collection(
#     name="medical_reports"
# )
# # chunks=ingest_pdf(pdf_path,"userzyx","document_1_report")
# USER_ID = "user_123"
# DOCUMENT_ID = "report_001"

# chunks = ingest_pdf(
#     pdf_path,
#     USER_ID,
#     DOCUMENT_ID
# )

# texts = [chunk.page_content for chunk in chunks]

# metadatas = [chunk.metadata for chunk in chunks]

# chunks_embedding = embedding_model.encode(
#     texts
# ).tolist()



# ids = [f"{USER_ID}_report_{i}" for i in range(len(texts))]

# collection.add(
#     ids=ids,
#     embeddings=chunks_embedding,
#     documents=texts,
#     metadatas=metadatas
# )

import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"

)
client = chromadb.PersistentClient(
    path="././data/chroma_db"
)
collection = client.get_or_create_collection(
    name="medical_reports"
)
