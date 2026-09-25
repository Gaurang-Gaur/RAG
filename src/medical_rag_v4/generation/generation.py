from medical_rag_v4.embeddings.embeddings import embedding_model,collection;
# i didn't expose complete path of file from where I am importing this because I am 
#using __init_file in that folder so, clearner imports in other files.
from dotenv import load_dotenv;
from medical_rag_v4.retrieval.retrieval import retrieval;
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv();
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
def ask_question(
    question: str,
    user_id: str,
    document_id: str
)->str:


    # -----------------------------
    # 3. Get documents + metadata
    # -----------------------------
    results=retrieval(question,user_id,document_id);
    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            f"""
            Source:
            Document: {metadata.get("document_id")}
            Page: {metadata.get("page")}

            Content:
            {document}
            """
        )

    context = "\n\n".join(context_parts);
    prompt = f"""
                    You are a medical information assistant.

                    Use the provided medical document context
                    to answer the user's question.

                    Rules:

                    1. Use the provided context as the primary
                       source of patient-specific information.

                    2. Do not invent patient information.

                    3. If the answer cannot be found in the
                       provided context, clearly say that the
                       information is not available in the
                       provided document.

                    4. Do not claim to diagnose the patient.

                    5. Explain medical terminology in simple
                       language when useful.

                    6. If you provide general medical information,
                       clearly distinguish it from the patient's
                       documented results.

                    7. When possible, mention the source page.

                    Medical document context:

                    {context}

                    User question:

                    {question}
                    """
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": metadatas
    }
    