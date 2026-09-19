from sentence_transformers import SentenceTransformer;
import chromadb;
from langchain_google_genai import ChatGoogleGenerativeAI;
from dotenv import load_dotenv;
load_dotenv();
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

query = input("Ask your question: ");
query_embedding=model.encode(query).tolist();

results=collection.query(query_embeddings=query_embedding,n_results=3);
# for i, (doc, id) in enumerate(zip(results["documents"], results["ids"])):
#     print(i, doc, id)
# for document,score in zip(results["documents"][0],results["distances"][0]):
#     print(document,score)
# for document, distance in zip
#     results["documents"][0],
#     results["distances"][0]
# ):
#     if distance < 1.3:
#         print(document, distance)

# #till here That's retrieval.

#we will start with augementation -> the process of making something bigger and stronger and improved
#data augementation-> a process of creating a new data from existing data in order to train ai without change the core meaning of it...
#Augementation start here
retrieved_documents = results["documents"][0]

context = "\n\n".join(retrieved_documents)

# print(context)


system_prompt = """
You are a medical information assistant.

Use the provided medical report context to answer the
user's question.

Rules:
1. Use patient-specific information only when it appears
   in the provided context.
2. Never invent laboratory values or medical history.
3. Clearly distinguish report findings from general
   medical information.
4. Do not present a definitive diagnosis.
5. If the context does not contain enough information,
   say that it is insufficient.
6. Explain medical terminology in simple language.
"""

user_prompt = f"""
Medical report context:

{context}

User question:

{query}
"""

#finally Generation part'G; of rag

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

response = llm.invoke([
    ("system", system_prompt),
    ("human", user_prompt)
])

print(response.content)

