import streamlit as st
import streamlit.components.v1 as components
from chatbot.rag_pipeline import RAGPipeline
import base64
import logging
import sys

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Page config
st.set_page_config(
    page_title="Chatbot Fairlynk",
    page_icon="static/icon.png",
    layout="centered"
)

# Fixer le thème par défaut à "light"
theme = "light"

# Changer le logo et la couleur du titre selon le thème (fixé ici à light)
logo_file = "static/logo_dm.png" 
title_color = "#e1e1e1"

# White-mode
# logo_file = "static/logo_dm.png"  # static/logo_wm.png
# title_color = "#29235c"         # white-mode 

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo_file, width=400)

# Affichage du titre
st.markdown(f"<h1 style='text-align: left; color: {title_color};'>Guide Chatbot</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:left;font-size:1.1rem;color:#db9804;margin-bottom:1.5em;'>"
    "Votre assistant Fairlynk, à votre écoute!"
    "</p>",
    unsafe_allow_html=True
)

# Historique de la conversation
if "history" not in st.session_state:
    st.session_state["history"] = [
        (
            "🤖",
            "Bonjour ! Je suis votre assistant Fairlynk. Posez-moi une question sur les fonctionnalités, modèles ou clauses disponibles."
        )
    ]

# Indicateur de soumission
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# Chargement du pipeline RAG
rag = RAGPipeline()

# Affichage des messages
with st.container():
    for q, r in st.session_state["history"]:
        if q != "🤖":
            st.markdown(
                f"<div style='background-color:#e53a5c;color:white;padding:14px 18px;"
                f"font-size:1.08rem;border-radius:16px 16px 0 16px;margin-bottom:4px;"
                f"width:fit-content;min-width:30%;max-width:70%;align-self:flex-end;"
                f"word-break:break-word;margin-left:auto;text-align:right;display:block;'>{q}</div>",
                unsafe_allow_html=True)
        st.markdown(
            f"<div style='background-color:#f5f5f5;color:#222;padding:10px 12px;"
            f"border-radius:12px 12px 12px 0;margin-bottom:16px;max-width:70%;"
            f"align-self:flex-start;word-break:break-word;'>{r}</div>",
            unsafe_allow_html=True)

# Champ de saisie utilisateur
st.markdown("<div id='input-anchor'></div>", unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Votre question :", key="input_field")
    submit = st.form_submit_button("Envoyer", help="Envoyer votre question")

# Bouton pour arrêter le bot
if st.button("Arrêter le bot"):
    logging.info("Arrêt du bot demandé par l'utilisateur.")
    st.stop()
    sys.exit(0)

# Traitement de la soumission
if submit and user_input:
    logging.info(f"Nouvelle question utilisateur : {user_input}")
    with open("static/icon.png", "rb") as img_file:
        icon_base64 = base64.b64encode(img_file.read()).decode()
    spinner_html = f'''
    <div id="custom-spinner" style="display:flex;flex-direction:column;justify-content:center;align-items:center;margin:20px 0;">
        <img src="data:image/png;base64,{icon_base64}" width="32" style="animation: spin 1s linear infinite; margin-bottom:8px;"/>
        <span style="color:#fff;font-weight:bold;font-size:1rem;">Génération de la réponse...</span>
    </div>
    <style>
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
    .stSpinner {{ display: none !important; }}
    </style>
    '''
    spinner_placeholder = st.empty()
    spinner_placeholder.markdown(spinner_html, unsafe_allow_html=True)
    try:
        response = rag.query(user_input)
        logging.info(f"Réponse générée : {response}")
    except Exception as e:
        logging.error(f"Erreur lors de la génération de la réponse : {e}")
        response = "Une erreur est survenue lors de la génération de la réponse."
    spinner_placeholder.empty()
    st.session_state["history"].append((user_input, response))
    st.session_state["submitted"] = True
    st.rerun()