# frontend/navigation.py

import streamlit as st
from backend.session_utils import save_progress, load_progress

def create_sidebar():
    """Skapar sidofältet med navigationsknappar och information"""
    
    # Lägg till logotyp i sidebaren
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #2E7D32; font-family: 'Arial', sans-serif; font-weight: 600;">
                <span style="font-size: 32px;">🥗</span> Functional Food
            </h2>
            <p style="color: #666; font-style: italic; font-size: 14px;">
                Med Ulrika Davidsson
            </p>
            <div style="height: 2px; background: linear-gradient(90deg, #4CAF50, #F1F8E9); margin: 15px 0;"></div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Navigationsknappar
    stages = {
        'intro': '🏠 Introduktion',
        'basic_info': '📝 Dina hälsomål',
        'deep_dive': '🔍 Fördjupad analys',
        'financial': '🌱 Hälsobudget',
        'business_plan': '🥗 Din matplan'
    }
    
    # Visa var användaren befinner sig
    current_stage = st.session_state.current_stage
    st.sidebar.markdown("### Din position")
    
    for stage, title in stages.items():
        if stage == current_stage:
            st.sidebar.markdown(
                f"""
                <div style="
                    padding: 10px; 
                    border-radius: 8px; 
                    background-color: rgba(76, 175, 80, 0.2); 
                    border-left: 4px solid #4CAF50;
                    margin-bottom: 8px;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                ">
                    <span style="margin-right: 8px;">➡️</span>
                    {title}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.sidebar.markdown(
                f"""
                <div style="
                    padding: 10px; 
                    border-radius: 8px; 
                    background-color: #F8F9FA; 
                    margin-bottom: 8px;
                    color: #666;
                ">
                    {title}
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    # Information om appen
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='font-size: 0.9em; color: #666; margin-top: 20px;'>
            <p style='margin-bottom: 8px;'>Version 1.0</p>
            <p>En interaktiv hälsoguide baserad på Ulrika Davidssons filosofi.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Kontaktinformation
    st.sidebar.markdown("---")
    st.sidebar.info("Har du frågor? Klicka på '🥗 Din matplan' och ställ frågor direkt till din hälsocoach.")

def reset_session():
    """Återställer sessionen till ursprungsläget"""
    st.session_state.user_data = {}
    st.session_state.conversation_history = []
    st.session_state.current_stage = 'intro'
    st.session_state.pdf_path = None
    st.session_state.swot_analysis = None
    st.session_state.swot_image = None
    st.session_state.manifest = None
    st.session_state.logo_url = None

def get_current_stage_name():
    """Konverterar det tekniska stegnamnet till ett användarvänligt namn"""
    stage_map = {
        "intro": "Välkommen",
        "livsstil": "Dina livsvanor",
        "matvanor": "Dina matvanor",
        "longevity": "Livslängdsanalys",
        "kursplan": "Din personliga kursplan"
    }
    return stage_map.get(st.session_state.current_stage, "Okänt steg")

def determine_stage_from_data(user_data):
    """Bestämmer lämpligt steg baserat på data som laddats"""
    if 'kursplan' in user_data:
        return 'kursplan'
    elif user_data.get('superfoods') or user_data.get('kosthallning'):
        return 'longevity'
    elif user_data.get('alder') and user_data.get('aktivitet'):
        return 'matvanor'
    elif user_data.get('namn'):
        return 'livsstil'
    else:
        return 'intro' 