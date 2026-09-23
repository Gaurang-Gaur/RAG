from sentence_transformers import SentenceTransformer;
import chromadb;
from langchain_google_genai import ChatGoogleGenerativeAI;

from dotenv import load_dotenv;
load_dotenv();
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
client=chromadb.PersistentClient(path="./chroma_db");
collection=client.get_collection(name="medical_reports");

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

#This rag functions
def ask_question(question:str)->dir:
    #1 queryEmbedding
    query_embedding=model.encode(question).tolist();

    #2 retrieved from chroma db
    results=collection.query(query_embedding,n_results=3);

    
    documents=results["documents"][0];
    # print(documents);
    # build context
    context="\n\n".join(documents);

    #build system prompt or prompt template
    prompt = f"""
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
    {question}
    """
    response=llm.invoke(prompt);

    return {
        "question":question,
        "response":response.content,
        "sources":documents
    }

result = ask_question(
    "What is my kidney test result?"
)

print(result["response"])

# print("\nSources:")
# for source in result["sources"]:
#     print(source)