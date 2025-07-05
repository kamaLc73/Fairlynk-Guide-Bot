from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)

def index_data(input_path, vectorstore_path="vectorstore/db_faiss"):
    # Charger le texte
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Segmenter en chunks
    chunks = chunk_text(text)
    
    # Créer les embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Créer et sauvegarder le VectorStore FAISS
    os.makedirs(vectorstore_path, exist_ok=True)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    vectorstore.save_local(vectorstore_path)
    print(f"VectorStore FAISS sauvegardé dans {vectorstore_path}/index.faiss et {vectorstore_path}/index.pkl")
    print(f"Nombre de chunks indexés : {len(chunks)}")

if __name__ == "__main__":
    input_path = "data/guide_fairlynk.txt"
    index_data(input_path)