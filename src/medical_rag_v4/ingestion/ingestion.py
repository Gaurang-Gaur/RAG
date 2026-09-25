from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



def ingest_pdf(
    file_path: str,
    user_id: str,
    document_id: str
):

    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # 2. Recursive chunking
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

    chunks = splitter.split_documents(pages)

    # 3. Add application metadata
    for i, chunk in enumerate(chunks):

        chunk.metadata["user_id"] = user_id
        chunk.metadata["document_id"] = document_id
        chunk.metadata["chunk_index"] = i

    return chunks




