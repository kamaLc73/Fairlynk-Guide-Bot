from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class RAGPipeline:
    def __init__(self, groq_model="llama-3.3-70b-versatile", vectorstore_path="vectorstore/db_faiss"):
        load_dotenv()
        logging.info("Chargement du VectorStore FAISS depuis %s", vectorstore_path)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        logging.info("Initialisation du LLM Groq (%s)", groq_model)
        self.llm = ChatGroq(
            model=groq_model,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.4,
            max_tokens=700
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",  "Vous êtes un assistant intelligent et fiable. Répondez à la question dans la même langue que l'utilisateur, en vous basant uniquement sur le contexte ci-dessous. Si la réponse ne se trouve pas dans le contexte, dites-le simplement. Contexte : {context}")
            ,("human", "{question}")
        ])
        self.parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.parser

    def query(self, query, top_k=3):
        logging.info("Requête utilisateur : %s", query)
        docs = self.vectorstore.similarity_search(query, k=top_k)
        context = "\n".join([doc.page_content for doc in docs])
        logging.info("Contexte extrait : %d documents", len(docs))
        response = self.chain.invoke({"context": context, "question": query})
        logging.info("Réponse générée.")
        return response

if __name__ == "__main__":
    rag = RAGPipeline()
    query = "Comment créer un contrat dans FAIRLYNK ?"
    response = rag.query(query)
    logging.info(response)