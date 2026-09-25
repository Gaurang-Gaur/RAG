
# from medical_rag_v4.generation.generation import ask_question
# result = ask_question(
#     question="What is my MMEF result?",
#     user_id="user_123",
#     document_id="report_001"
# )



# print("ANSWER:")
# print(result["answer"])


# print("\nSOURCES:")

# for source in result["sources"]:
#     print(
#         f"Page: {source.get('page')}"
#     )

from fastapi import FastAPI

from medical_rag_v4.api.routes import router

app = FastAPI(
    title="Medical RAG API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }