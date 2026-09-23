from sentence_transformers import SentenceTransformer
import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI;
from dotenv import load_dotenv;
load_dotenv();
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)
query = "What is my MMEF result? and FEV1 meaning?Is my FEV1 is ok?"

query_embedding = model.encode(query).tolist()

collection = client.get_or_create_collection(
    name="medical_reports"
)

# Semantic similarity tells us "what is relevant?" Metadata filtering tells us "whose/document's data are we allowed to search?"
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
      where={
        "$and": [
            {"user_id": "user_123"},
            {"document_id": "report_001"}
        ]
    }
)


if(len(results["documents"][0])==0):
    print("No entry found");
# else:
#     print(results["documents"][0][0])
#     print(results["metadatas"][0][0])
    
    
contextpart=[];

for document,metadata in zip(results["documents"][0],results["metadatas"][0]):
    contextpart.append(
                f"""
                    Source:"medical_reports"
                    Document: {metadata['document_id']}
                    Page: {metadata['page']}
                    Section: {metadata['section']}

                    Content:
                    {document}
                    
                """
    )

context="\n\n".join(contextpart);


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


system_prompt=f"""
    You are a medical information assistant.
    
        Answer the user's question using ONLY the
        provided medical report context.
    
        Rules:
        - Do not invent patient information.
        - If the answer is not present, say so.
        - Clearly distinguish report findings from
          general medical information.
        - Do not provide a definitive diagnosis.
        - Explain medical terms in simple language.
    
        Medical report context:
        {context}
    
        User question:
        {query}

        """


results = llm.invoke(system_prompt);

print(results.content);