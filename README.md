# Chatbot FAIRLYNK basé sur RAG avec Groq et LangChain

Ce projet implémente un chatbot RAG pour répondre aux questions sur FAIRLYNK, utilisant un document LaTeX comme base de connaissances, Groq pour l’inférence rapide, et LangChain avec FAISS VectorStore pour la recherche sémantique.

## Prérequis

- Python 3.8+
- `texlive-full` pour compiler le fichier LaTeX
- Clé API Groq (obtenez-la sur https://console.groq.com)
- Fichier `fairlynk_guide_rag.pdf` généré à partir de `fairlynk_guide_rag.tex`

## Commandes
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1
   python -m streamlit run .\app.py
   ```