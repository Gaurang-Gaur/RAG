from sentence_transformers import SentenceTransformer;
import chromadb;
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
client=chromadb.PersistentClient(path="./chroma_db");
#get this collection/table that is medical_report
# ┌──────────────────────────────────┐
# │          ChromaDB                │
# ├──────────┬───────────┬───────────┤
# │ ID       │ Text      │ Vector    │
# ├──────────┼───────────┼───────────┤
# │ chunk_0  │ text...   │ [....]    │
# │ chunk_1  │ text...   │ [....]    │
# │ chunk_2  │ MMEF...   │ [....]    │
# │ chunk_3  │ text...   │ [....]    │
# └──────────┴───────────┴───────────┘
collection=client.get_collection(name="medical_reports");

query="what is my breathing test report";
query_embedding=model.encode(query).tolist();

results=collection.query(query_embeddings=query_embedding,n_results=3);
# for i, (doc, id) in enumerate(zip(results["documents"], results["ids"])):
#     print(i, doc, id)
# for document,score in zip(results["documents"][0],results["distances"][0]):
#     print(document,score)
for document, distance in zip(
    results["documents"][0],
    results["distances"][0]
):
    if distance < 1.3:
        print(document, distance)

#till here That's retrieval.