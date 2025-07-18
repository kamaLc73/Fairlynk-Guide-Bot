import streamlit as st
from chatbot.rag_pipeline import RAGPipeline
import base64
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Page config
st.set_page_config(
    page_title="Chatbot Fairlynk",
    page_icon="static/icon.png",
    layout="centered"
)

# Initialiser le thème dans session_state
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"  # Thème par défaut

# Fonction pour basculer le thème
def toggle_theme():
    if st.session_state["theme"] == "dark":
        st.session_state["theme"] = "light"
    else:
        st.session_state["theme"] = "dark"

# Configuration du thème basée sur session_state
if st.session_state["theme"] == "dark":
    logo_file = "static/logo_dm.png"
    title_color = "#e1e1e1"
    bg_color = "#0e1117"
    user_msg_bg = "#e53a5c"
    bot_msg_bg = "#f5f5f5"
    bot_msg_color = "#222"
    spinner_color = "#fff"
else:
    logo_file = "static/logo_wm.png"
    title_color = "#29235c"
    bg_color = "#ffffff"
    user_msg_bg = "#29235c"
    bot_msg_bg = "#e8e8e8"
    bot_msg_color = "#222"
    spinner_color = "#29235c"

# CSS pour le thème
theme_css = f"""
<style>
    .stApp {{
        background-color: {bg_color};
    }}
    
    /* Styles pour les formulaires */
    .stTextInput > div > div > input {{
        background-color: {"#262730" if st.session_state["theme"] == "dark" else "#ffffff"};
        color: {"#ffffff" if st.session_state["theme"] == "dark" else "#000000"};
        border: 1px solid {"#444" if st.session_state["theme"] == "dark" else "#ccc"};
    }}
    
    /* Placeholder du champ de texte */
    .stTextInput > div > div > input::placeholder {{
        color: {"#888" if st.session_state["theme"] == "dark" else "#666"} !important;
        opacity: 1;
    }}
    
    /* Texte d'aide "Press Enter to submit" */
    .stTextInput > div > div > div[data-testid="InputInstructions"] {{
        color: {"#888" if st.session_state["theme"] == "dark" else "#666"} !important;
    }}
    
    /* Correction pour tous les éléments de texte dans le champ */
    .stTextInput * {{
        color: {"#ffffff" if st.session_state["theme"] == "dark" else "#000000"} !important;
    }}
    
    /* Spécifique pour le texte d'instruction */
    .stTextInput [data-testid="InputInstructions"] {{
        color: {"#888" if st.session_state["theme"] == "dark" else "#666"} !important;
    }}
    
    /* Label du champ de texte */
    .stTextInput > label {{
        color: {"#ffffff" if st.session_state["theme"] == "dark" else "#000000"} !important;
        font-weight: 500;
    }}
    
    /* Conteneur du formulaire */
    .stForm {{
        background-color: {"transparent" if st.session_state["theme"] == "dark" else "transparent"};
        border: {"none" if st.session_state["theme"] == "dark" else "none"};
        border-radius: 8px;
        padding: {"10px" if st.session_state["theme"] == "light" else "0px"};
    }}
    
    /* Bouton Envoyer */
    .stFormSubmitButton > button {{
        background-color: {"#e53a5c" if st.session_state["theme"] == "dark" else "#29235c"};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }}
    
    .stFormSubmitButton > button:hover {{
        background-color: {"#d12b4a" if st.session_state["theme"] == "dark" else "#1a1742"};
    }}
    
    /* Bouton Arrêter le bot */
    .stButton > button {{
        background-color: {"#444" if st.session_state["theme"] == "dark" else "#666"};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }}
    
    .stButton > button:hover {{
        background-color: {"#555" if st.session_state["theme"] == "dark" else "#777"};
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background-color: {"#262730" if st.session_state["theme"] == "dark" else "#f8f9fa"};
    }}
    
    /* Texte général */
    .stMarkdown p {{
        color: {"#ffffff" if st.session_state["theme"] == "dark" else "#000000"};
    }}
    
    /* Headers dans la sidebar */
    .css-1d391kg h3 {{
        color: {"#ffffff" if st.session_state["theme"] == "dark" else "#000000"};
    }}
    
    /* Masquer le spinner par défaut de Streamlit */
    .stSpinner {{
        display: none !important;
    }}
    
    .stSpinner > div {{
        display: none !important;
    }}
    
    /* Spinner personnalisé */
    .custom-spinner {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    
    .custom-spinner img {{
        animation: spin 1s linear infinite;
        margin-bottom: 8px;
    }}
    
    @keyframes spin {{
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Correction pour les messages du bot en mode sombre */
    .bot-message {{
        background-color: {bot_msg_bg};
        color: {bot_msg_color};
        padding: 10px 12px;
        border-radius: 12px 12px 12px 0;
        margin-bottom: 16px;
        max-width: 70%;
        align-self: flex-start;
        word-break: break-word;
    }}
    
    /* Correction spécifique pour le texte en mode sombre */
    .bot-message * {{
        color: {bot_msg_color} !important;
    }}
</style>
"""

st.markdown(theme_css, unsafe_allow_html=True)

# Bouton de basculement du thème dans la sidebar
with st.sidebar:
    st.markdown("### Paramètres")
    theme_label = "🌙 Dark Mode" if st.session_state["theme"] == "dark" else "☀️ Light Mode"
    if st.button(theme_label, key="theme_toggle", help="Basculer entre le mode sombre et clair"):
        toggle_theme()
        st.rerun()

# Affichage du logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image(logo_file, width=400)
    except FileNotFoundError:
        st.warning(f"Logo introuvable : {logo_file}")

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

# Chargement du pipeline RAG avec spinner personnalisé
@st.cache_resource
def load_rag_pipeline():
    # Affichage du spinner personnalisé pendant le chargement
    try:
        with open("static/icon.png", "rb") as img_file:
            icon_base64 = base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        icon_base64 = ""
        logging.warning("Icône introuvable pour le spinner")
    
    loading_html = f'''
    <div id="loading-spinner" style="display:flex;flex-direction:column;justify-content:center;align-items:center;margin:20px 0;">
        <img src="data:image/png;base64,{icon_base64}" width="32" style="animation: spin 1s linear infinite; margin-bottom:8px;"/>
        <span style="color:{spinner_color};font-weight:bold;font-size:1rem;">Initialisation de l'assistant...</span>
    </div>
    <style>
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
    .stSpinner {{ display: none !important; }}
    </style>
    '''
    
    # Placeholder pour le spinner
    spinner_placeholder = st.empty()
    spinner_placeholder.markdown(loading_html, unsafe_allow_html=True)
    
    # Chargement du pipeline
    pipeline = RAGPipeline()
    
    # Suppression du spinner
    spinner_placeholder.empty()
    
    return pipeline

rag = load_rag_pipeline()

# Affichage des messages avec couleurs dynamiques
with st.container():
    for q, r in st.session_state["history"]:
        if q != "🤖":
            st.markdown(
                f"<div style='background-color:{user_msg_bg};color:white;padding:14px 18px;"
                f"font-size:1.08rem;border-radius:16px 16px 0 16px;margin-bottom:4px;"
                f"width:fit-content;min-width:30%;max-width:70%;align-self:flex-end;"
                f"word-break:break-word;margin-left:auto;text-align:right;display:block;'>{q}</div>",
                unsafe_allow_html=True)
        
        # Utilisation de la classe CSS pour les messages du bot
        st.markdown(
            f"<div class='bot-message'>{r}</div>",
            unsafe_allow_html=True)

# Champ de saisie utilisateur avec styles améliorés
st.markdown("<div id='input-anchor'></div>", unsafe_allow_html=True)

# Conteneur personnalisé pour le formulaire - suppression du style en mode light
form_container_style = f"""
<div style="
    background-color: {"transparent" if st.session_state["theme"] == "dark" else "transparent"};
    border: {"none" if st.session_state["theme"] == "dark" else "none"};
    border-radius: 12px;
    padding: {"20px" if st.session_state["theme"] == "dark" else "0px"};
    margin: 20px 0;
">
"""

st.markdown(form_container_style, unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    # Style personnalisé pour le label
    st.markdown(
        f"<label style='color: {title_color}; font-weight: 500; margin-bottom: 8px; display: block;'>Votre question :</label>", 
        unsafe_allow_html=True
    )
    
    # Correction du problème du label vide et ajout du placeholder
    user_input = st.text_input("Votre question", key="input_field", label_visibility="collapsed", placeholder="Tapez votre question ici...")
    
    col1, col2 = st.columns([1, 6])
    with col1:
        submit = st.form_submit_button("Envoyer", help="Envoyer votre question")

st.markdown("</div>", unsafe_allow_html=True)

# Espace supplémentaire pour l'esthétique
st.markdown("<br>", unsafe_allow_html=True)

# Traitement de la soumission
if submit and user_input:
    logging.info(f"Nouvelle question utilisateur : {user_input}")
    
    # Spinner avec couleur adaptée au thème
    try:
        with open("static/icon.png", "rb") as img_file:
            icon_base64 = base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        icon_base64 = ""
        logging.warning("Icône introuvable pour le spinner")
    
    spinner_html = f'''
    <div class="custom-spinner">
        <img src="data:image/png;base64,{icon_base64}" width="32"/>
        <span style="color:{spinner_color};font-weight:bold;font-size:1rem;">Génération de la réponse...</span>
    </div>
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