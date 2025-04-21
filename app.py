# app.py

import streamlit as st
from frontend.pages import (
    intro_page,
    livsstil_page,
    matvanor_page,
    longevity_page,
    kursplan_page
)
from frontend.navigation import create_sidebar
import requests
import os
import uuid
import io
from PIL import Image
from dotenv import load_dotenv

# Ladda miljövariabler från .env-filen
load_dotenv()

# Anpassad CSS för en fräsch, hälsosam design med gröna inslag
custom_css = """
<style>
    /* Mjukare kanter på element */
    div.stButton > button {
        border-radius: 8px;
        box-shadow: 0px 2px 5px rgba(76, 175, 80, 0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 8px rgba(76, 175, 80, 0.3);
    }
    
    /* Accentfärg på rubriker */
    h1, h2, h3 {
        color: #2E7D32;
        border-bottom: 2px solid #C8E6C9;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Kort-stil för expanders */
    .streamlit-expanderHeader {
        background-color: #F1F8E9;
        border-radius: 8px;
        border-left: 4px solid #8BC34A;
    }
    
    /* Bättre kontrast för text i sidebaren */
    section[data-testid="stSidebar"] {
        background-color: #F1F8E9;
        border-right: 1px solid #C8E6C9;
    }
    
    /* Mer naturliga widgets */
    .stTextInput, .stSelectbox, .stMultiselect {
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Generell mjuk skuggning för innehåll */
    div.block-container {
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.05);
        padding: 2rem;
        border-radius: 10px;
    }
</style>
"""

# Hämta API-nyckel från miljövariabel
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Ingen OpenAI API-nyckel hittades. Ange OPENAI_API_KEY i .env-filen eller som miljövariabel.")

def generate_vision_image(prompt):
    """Funktion för att generera målbild med DALL-E API"""
    if not API_KEY:
        st.error("Ingen OpenAI API-nyckel hittades.")
        return None
        
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # Förbättra prompten för drömska bilder
    enhanced_prompt = f"""
    {prompt}
    
    Skapa en drömsk, nästan magisk bild med mjuka, glödande färger och en känsla av transformation. 
    Bilden ska ha ett djup och en känslomässig kvalitet som inspirerar till hälsosamma val.
    Använd en ljus, varm färgpalett med subtila blå och gröna toner som representerar hälsa och förnyelse.
    """
    
    data = {
        "model": "dall-e-3",
        "prompt": enhanced_prompt,  # Här använder vi den förbättrade prompten
        "n": 1,
        "size": "1024x1024",
        "quality": "hd",
        "style": "vivid"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        image_url = response.json()['data'][0]['url']
        return image_url
    else:
        raise Exception(f"Fel vid API-anrop: {response.text}")

# Sessionhantering för att spara tidigare svar och användardata
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'intro'
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'food_analysis' not in st.session_state:
    st.session_state.food_analysis = None
if 'food_image' not in st.session_state:
    st.session_state.food_image = None
if 'manifest' not in st.session_state:
    st.session_state.manifest = None
if 'vision_image' not in st.session_state:
    st.session_state.vision_image = None
if 'custom_image_mode' not in st.session_state:
    st.session_state.custom_image_mode = False

def main():
    """
    Huvudfunktionen som hanterar sidnavigering baserat på användarens aktuella steg i processen.
    """
    # Injicera anpassad CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Skapa sidofältet för navigering
    create_sidebar()
    
    # Sidnavigering baserat på aktuellt steg
    if st.session_state.current_stage == 'intro':
        intro_page()
    elif st.session_state.current_stage == 'livsstil':
        livsstil_page()
    elif st.session_state.current_stage == 'matvanor':
        matvanor_page()
    elif st.session_state.current_stage == 'longevity':
        longevity_page()
    elif st.session_state.current_stage == 'kursplan':
        kursplan_page()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Functional Food & Longevity med Ulrika Davidsson",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()