from sentence_transformers import SentenceTransformer

with open("data/report.txt", "r") as file:
    text = file.read()



def check_text(text,chunk_size=300):
    chunks=[];
    start=0;
    while start<len(text):
        end=start+chunk_size;
        chunks.append(text[start:end]);
        start=end;
    return chunks;

chunks=check_text(text);

for i ,chunk in enumerate(chunks):
    print(f"{i}----------------------------------------------------------------------------");
    print(chunk)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

print(embeddings[0]);