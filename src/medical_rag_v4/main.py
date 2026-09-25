
from medical_rag_v4.generation.generation import ask_question
result = ask_question(
    question="What is my MMEF result?",
    user_id="user_123",
    document_id="report_001"
)



print("ANSWER:")
print(result["answer"])


print("\nSOURCES:")

for source in result["sources"]:
    print(
        f"Page: {source.get('page')}"
    )