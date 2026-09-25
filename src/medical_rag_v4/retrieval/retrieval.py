from medical_rag_v4.embeddings.embeddings import embedding_model,collection;
def retrieval(question: str,user_id: str,document_id: str):

    query_embedding = embedding_model.encode(
        question
    ).tolist()
    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=1,

        where={
            "$and": [
                {"user_id": user_id},
                {"document_id": document_id}
            ]
        }
    )
    
    # print("\n========== RETRIEVAL DEBUG ==========")

    # print("\nDocuments:")
    # print(results["documents"])

    # print("\nMetadatas:")
    # print(results["metadatas"])

    # print("\nDistances:")
    # print(results["distances"])

    # print("\n======================================\n")
    
    return results;