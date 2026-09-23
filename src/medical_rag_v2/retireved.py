from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)
query = "What is my MMEF result?"

query_embedding = model.encode(query).tolist()

collection = client.get_or_create_collection(
    name="medical_reports"
)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
      where={
        "user_id": "user_123"
    }
)

if(len(results["documents"])):
    print("No entry found");
else:
    print(results["documents"][0][0])
    print(results["metadatas"][0][0])