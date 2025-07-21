from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import logging
from transformers import MarianMTModel, MarianTokenizer
import langdetect

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
            max_tokens=700,
            timeout=60
        )
        self.parser = StrOutputParser()
        # Préparer les modèles de traduction
        self.translators = {
            ("fr", "en"): self._load_translator("Helsinki-NLP/opus-mt-fr-en"),
            ("en", "fr"): self._load_translator("Helsinki-NLP/opus-mt-en-fr"),
            ("es", "en"): self._load_translator("Helsinki-NLP/opus-mt-es-en"),
            ("en", "es"): self._load_translator("Helsinki-NLP/opus-mt-en-es"),
            ("fr", "es"): self._load_translator("Helsinki-NLP/opus-mt-fr-es"),
            ("es", "fr"): self._load_translator("Helsinki-NLP/opus-mt-es-fr"),
        }

    def _load_translator(self, model_name):
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return (model, tokenizer)

    def _translate(self, text, src, tgt):
        if src == tgt:
            return text
        key = (src, tgt)
        if key not in self.translators:
            return text  # Pas de traducteur, retourne le texte original
        model, tokenizer = self.translators[key]
        batch = tokenizer([text], return_tensors="pt", padding=True)
        gen = model.generate(**batch, max_length=512)
        return tokenizer.decode(gen[0], skip_special_tokens=True)

    def query(self, query, lang="fr"):
        logging.info("Requête utilisateur : %s (lang=%s)", query, lang)
        # Détecter la langue de la question (simple heuristique)
        try:
            detected_lang = langdetect.detect(query)
        except Exception:
            detected_lang = lang
        # Traduire la question si besoin
        translated_query = self._translate(query, detected_lang, lang)
        # Prompt unique par langue
        prompts = {
            "fr": "Vous êtes un assistant intelligent. Répondez uniquement en français, en vous basant sur le contexte suivant. Si la réponse n'est pas dans le contexte, dites-le simplement. Contexte : {context}",
            "en": "You are an intelligent assistant. Respond only in English, based on the following context. If the answer is not in the context, just say so. Context: {context}",
            "es": "Eres un asistente inteligente. Responde solo en español, basándote en el siguiente contexto. Si la respuesta no está en el contexto, simplemente dilo. Contexto: {context}"
        }
        system_prompt = prompts.get(lang, prompts["fr"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}")
        ])
        chain = prompt | self.llm | self.parser
        docs = self.vectorstore.similarity_search(translated_query, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        logging.info("Contexte extrait : %d documents", len(docs))
        response = chain.invoke({"context": context, "question": translated_query})
        logging.info("Réponse générée.")
        return response

if __name__ == "__main__":
    rag = RAGPipeline()
    query = "Comment créer un contrat dans FAIRLYNK ?"
    response = rag.query(query)
    logging.info(response)