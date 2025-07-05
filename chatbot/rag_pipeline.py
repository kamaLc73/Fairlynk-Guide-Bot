from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

class RAGPipeline:
    def __init__(self, groq_model="llama-3.3-70b-versatile", vectorstore_path="vectorstore/db_faiss"):
        load_dotenv()
        # Charger le VectorStore FAISS
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        
        # Initialiser le LLM Groq
        self.llm = ChatGroq(
            model=groq_model,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
            max_tokens=1000
        )
        
        # Définir le prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Vous êtes un assistant utile qui répond en français. Utilisez le contexte suivant pour répondre précisément à la question. Contexte : {context}"),
            ("human", "{question}")
        ])
        self.parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.parser

    def query(self, query, top_k=3):
        # Rechercher les documents pertinents
        docs = self.vectorstore.similarity_search(query, k=top_k)
        context = "\n".join([doc.page_content for doc in docs])
        
        # Générer la réponse
        response = self.chain.invoke({"context": context, "question": query})
        return response

if __name__ == "__main__":
    rag = RAGPipeline()
    query = "Comment créer un contrat dans FAIRLYNK ?"
    response = rag.query(query)
    print(response)