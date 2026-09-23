from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="medical_reports"
)
chunks = [
    "Hemoglobin: 11.2 g/dL.",
    "White Blood Cell Count: 8040 /µL.",
    "MMEF: 69% of predicted value.",
    "FEV1: 82% of predicted value."
]

metadatas = [
    {
        "user_id": "user_123",
        "document_id": "report_001",
        "page": 1,
        "section": "Complete Blood Count",
        "chunk_index": 0
    },
    {
        "user_id": "user_223",
        "document_id": "report_001",
        "page": 1,
        "section": "Complete Blood Count",
        "chunk_index": 1
    },
    {
        "user_id": "user_123",
        "document_id": "report_001",
        "page": 2,
        "section": "Pulmonary Function Test",
        "chunk_index": 2
    },
    {
        "user_id": "user_123",
        "document_id": "report_001",
        "page": 2,
        "section": "Pulmonary Function Test",
        "chunk_index": 3
    }
]

embeddings = model.encode(chunks);

collection.add(
    ids=[
        "report_001_chunk_0",
        "report_001_chunk_1",
        "report_001_chunk_2",
        "report_001_chunk_3"
    ],

    documents=chunks,

    embeddings=embeddings.tolist(),

    metadatas=metadatas
)

# ┌──────────────────────────────────────────────┐
# │ ChromaDB                                     │
# ├──────────────────────────────────────────────┤
# │ ID                                           │
# │ report_001_chunk_2                           │
# │                                              │
# │ Document                                     │
# │ "MMEF: 69% of predicted value."              │
# │                                              │
# │ Embedding                                    │
# │ [0.023, -0.182, 0.091, ...]                  │
# │                                              │
# │ Metadata                                     │
# │ user_id = user_123                           │
# │ document_id = report_001                     │
# │ page = 2                                     │
# │ section = Pulmonary Function Test             │
# │ chunk_index = 2                              │
# └──────────────────────────────────────────────┘