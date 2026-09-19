from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    "Hemoglobin is 11.2 g/dL.",
    "The patient's white blood cell count is 8040 per microliter.",
    "MMEF is 69 percent of the predicted value.",
    "Creatinine is 0.9 mg/dL.",
    "The patient has a history of allergic bronchitis."
]

print("documents dimension");
document_embeddings = model.encode(documents)

print(document_embeddings.shape)

print("Query dimension");
query = "What is my breathing test result?"

query_embedding = model.encode(query)

print(query_embedding.shape)
from sentence_transformers.util import cos_sim

scores = cos_sim(
    query_embedding,
    document_embeddings,
    
)


print(scores)
scores = scores[0]

best_index = scores.argmax()

print(documents[best_index])

from sentence_transformers.util import semantic_search

results = semantic_search(
    query_embedding,
    document_embeddings,
    top_k=3
)

print(results)