import streamlit as st
from chatbot.rag_pipeline import RAGPipeline

st.title("Chatbot FAIRLYNK (propulsé par Groq et LangChain)")
st.write("Posez vos questions sur FAIRLYNK, ses fonctionnalités, ses contrats, modèles, ou clauses.")

rag = RAGPipeline()
query = st.text_input("Votre question :")
if query:
    with st.spinner("Génération de la réponse..."):
        response = rag.query(query)
        st.write("**Réponse :**")
        st.write(response)