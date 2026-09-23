from sentence_transformers import SentenceTransformer
import chromadb;
from langchain_text_splitters import RecursiveCharacterTextSplitter
model=SentenceTransformer( "sentence-transformers/all-MiniLM-L6-v2");
with open("data/report.txt", "r") as file:
    text = file.read()


client=chromadb.PersistentClient("./chromadb");
collection=client.get_or_create_collection(name="medical_documents",
                                            metadata={"hnsw:space": "cosine"});
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

chunks=splitter.split_text(text);

metadatas = []

for i, chunk in enumerate(chunks):

    metadatas.append({
        "user_id": "user_123",
        "document_id": "report_001",
        "page": 1,
        "section": "unknown",
        "chunk_index": i
    })
embeddings = model.encode(chunks)

collection.add(ids=[f"i" for i in range(0,len(chunks))],
               embeddings=embeddings.tolist(),
               documents=chunks,
               metadatas=metadatas);

