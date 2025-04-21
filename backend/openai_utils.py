# backend/openai_utils.py

import os
import json
import requests
import openai
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import io
import matplotlib.pyplot as plt
import numpy as np

# Ladda miljövariabler från .env-filen
load_dotenv()

# Ställ in OpenAI API-nyckel från miljövariabel
openai.api_key = os.getenv("OPENAI_API_KEY")

# Skapa OpenAI-klienten
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", None))

def generate_chat_response(messages, model="gpt-4o", temperature=0.7, max_tokens=1000):
    """
    Anropar OpenAI ChatCompletion och returnerar svar som en sträng.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ett fel uppstod i GPT-anropet: {e}")
        return f"Kunde inte generera svar p.g.a. fel: {e}"

def generate_chatgpt_response(prompt, history=None, temperature=0.7):
    """
    Anropar OpenAI ChatCompletion och returnerar ChatGPT:s svar som en sträng.
    """
    if history is None:
        history = []
    
    messages = [
        {"role": "system", "content": "Du är Ulrika Davidsson, en känd svensk hälsokock och expert på functional food och longevity. Du är inspirerande, kunnig om näringslära och ger personliga råd om hälsosam kost för att förlänga livet och öka välbefinnandet. Använd aktuella forskning om longevity, blå zoner och functional food när du ger råd. Var personlig och hänvisa till din egen erfarenhet som hälsokock."}
    ]
    
    # Lägg till konversationshistorik
    messages.extend(history)
    
    # Lägg till aktuell fråga
    messages.append({"role": "user", "content": prompt})
    
    return generate_chat_response(messages, temperature=temperature)

def search_web(query):
    """
    Söker på webben efter relevant information
    """
    try:
        search_term = f"{query} site:.se"
        url = f"https://api.duckduckgo.com/?q={search_term}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"Error": "Kunde inte hämta sökresultat"}
    except Exception as e:
        return {"Error": str(e)}

def generate_logo(business_name, business_type):
    """Genererar en logotyp baserat på företagsnamn och typ"""
    try:
        prompt = f"Skapa en minimalistisk, modern logotyp för ett företag som heter '{business_name}' som säljer {business_type}. Använd enkla former och max 3 färger. Gör den i vektorstil med transparent bakgrund. Logotypen ska vara professionell och lätt att känna igen."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Returnera URL till bilden
        return response.data[0].url
    except Exception as e:
        return f"Kunde inte generera logotyp: {str(e)}"

def generate_swot_analysis(data):
    """Genererar en SWOT-analys baserat på affärsdata"""
    prompt = f"""
    Gör en detaljerad SWOT-analys för ett företag som säljer {data.get('produktutbud', 'produkter')} 
    i {data.get('stad', 'en stad')} med målgruppen {data.get('malgrupp', 'konsumenter')} 
    och en {data.get('strategi', 'ospecificerad')}-strategi.
    
    Ge minst 5 punkter för varje kategori:
    1. Styrkor (Strengths)
    2. Svagheter (Weaknesses)
    3. Möjligheter (Opportunities)
    4. Hot (Threats)
    
    Basera analysen på konkret marknadsinformation och branschinsikter.
    """
    
    swot_text = generate_chatgpt_response(prompt)
    return swot_text

def create_swot_diagram(swot_text):
    """Skapar en visuell SWOT-diagram från text"""
    # Extrahera sektioner från SWOT-texten
    sections = {}
    current_section = None
    current_content = []
    
    for line in swot_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if any(keyword in line.lower() for keyword in ['styrkor', 'strength']):
            current_section = 'Styrkor'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['svagheter', 'weakness']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Svagheter'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['möjligheter', 'opportunit']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Möjligheter'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['hot', 'threat']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Hot'
            current_content = []
        elif current_section and line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            # Rensa bort punktlistetecken
            item = line.lstrip('•-*123456789. ')
            current_content.append(item)
    
    # Lägg till den sista sektionen
    if current_section and current_content:
        sections[current_section] = current_content
    
    # Skapa en figur med 2x2 rutnät
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.patch.set_facecolor('#f0f0f0')
    
    # Definiera färger för varje sektion
    colors = {
        'Styrkor': '#4CAF50',      # Grön
        'Svagheter': '#F44336',    # Röd
        'Möjligheter': '#2196F3',  # Blå
        'Hot': '#FF9800'           # Orange
    }
    
    # Titlar och innehåll för varje kvadrant
    sections_order = ['Styrkor', 'Svagheter', 'Möjligheter', 'Hot']
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for (section, pos) in zip(sections_order, positions):
        i, j = pos
        ax = axs[i, j]
        
        # Sätt bakgrundsfärg
        ax.set_facecolor(colors.get(section, '#EEEEEE') + '22')  # Lägg till transparens
        
        # Sätt titel
        ax.set_title(section, fontsize=14, fontweight='bold', color=colors.get(section, '#333333'))
        
        # Lägg till innehåll
        content = sections.get(section, ['Ingen information tillgänglig'])
        y_pos = 0.9
        for item in content[:7]:  # Begränsa till max 7 punkter
            if len(item) > 60:
                item = item[:57] + '...'  # Begränsa textlängd för visning
            ax.text(0.1, y_pos, f"• {item}", fontsize=10, va='top', wrap=True)
            y_pos -= 0.12
        
        # Ta bort axlar
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    
    # Spara figuren till en buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    
    return buf

def generate_company_manifest(data):
    """Genererar ett företagsmanifest"""
    prompt = f"""
    Skapa ett inspirerande och kraftfullt företagsmanifest för ett företag som säljer {data.get('produktutbud', 'produkter')} 
    med fokus på {data.get('malgrupp', 'kunder')} och en {data.get('strategi', 'ospecificerad')}-strategi.
    
    Manifestet ska inkludera:
    1. En inspirerande vision
    2. 3-5 kärnvärderingar med korta förklaringar
    3. Ett löfte till kunderna
    4. En kort beskrivning av företagets syfte och betydelse
    
    Skriv i en inspirerande, kraftfull ton som förmedlar företagets passion och ambition. 
    Manifestet ska vara omkring 250-300 ord långt.
    """
    
    manifest = generate_chatgpt_response(prompt)
    return manifest

def generate_food_vision(name, goal):
    """Genererar en målbild baserat på namn och hälsomål"""
    try:
        prompt = f"Skapa en vacker, inspirerande bild som representerar hälsosam mat och livsstil för {name} som vill {goal}. Inkludera färgglada, naturliga ingredienser som symboliserar hälsa och vitalitet. Gör bilden ljus, positiv och motiverande - en perfekt målbild för en hälsosam livsstil."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Returnera URL till bilden
        return response.data[0].url
    except Exception as e:
        return f"Kunde inte generera bild: {str(e)}"

def generate_food_analysis(data):
    """Genererar en näringsanalys baserat på användardata"""
    prompt = f"""
    Skapa en detaljerad "fyrfältare" (liknande SWOT-analys) för en person som har följande hälsomål och preferenser:
    Hälsomål: {data.get('halsomal', 'bli hälsosammare')}
    Matpreferenser: {data.get('matpreferenser', 'blandad kost')}
    Aktivitetsnivå: {data.get('aktivitet', 'medel')}
    Matfilosofi: {data.get('filosofi', 'balanserad')}
    
    Ge minst 4 punkter för varje kategori:
    1. Styrkor (nuvarande hälsosamma vanor att bygga på)
    2. Svagheter (utmaningar att övervinna)
    3. Möjligheter (sätt att förbättra kost och hälsa)
    4. Visdomsinsikter (djupare insikter om mat, hälsa och välbefinnande)
    
    Basera analysen på Ulrika Davidssons filosofi om functional food och näringsrik kost.
    """
    
    food_text = generate_chatgpt_response(prompt)
    return food_text

def create_food_diagram(food_text):
    """Skapar en visuell fyrfältare från text om mat och hälsa"""
    # Funktionen är liknande som create_swot_diagram men med ändrade titlar och färger
    # Anpassad för mat och hälsotema
    # ...fortsättning på implementation...

def generate_longevity_analysis(data):
    """Genererar en longevitetsanalys baserat på användardata"""
    prompt = f"""
    Skapa en detaljerad "fyrfältare" för {data.get('namn', 'en person')} som har följande livsvanor:
    Ålder: {data.get('alder', 'N/A')}
    Aktivitetsnivå: {data.get('aktivitet', 'N/A')}
    Stressnivå: {data.get('stress', 'N/A')}
    Sömn: {data.get('somn', 'N/A')} timmar/natt
    Kosthållning: {data.get('kosthallning', 'N/A')}
    Superfoods som äts regelbundet: {', '.join(data.get('superfoods', ['Inga angivna']))}
    Hälsoutmaningar: {', '.join(data.get('halsoutmaningar', ['Inga angivna']))}
    
    Ge minst 4 punkter för varje kategori:
    1. Styrkefaktorer (befintliga vanor som främjar långt liv)
    2. Utmaningar (vanor som kan minska livslängden)
    3. Möjligheter (functional food och vanor att införa)
    4. Livsvisdom (djupare insikter om mat, hälsa och longevity)
    
    Basera analysen på forskning om blå zoner, longevity och functional food kopplat till den information som personen delat.
    """
    
    longevity_text = generate_chatgpt_response(prompt)
    return longevity_text

def create_longevity_diagram(longevity_text):
    """Skapar en visuell fyrfältare från text om longevity"""
    # Extrahera sektioner från texten
    sections = {}
    current_section = None
    current_content = []
    
    # Ändrade sektionsnamn jämfört med SWOT
    for line in longevity_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if any(keyword in line.lower() for keyword in ['styrk', 'befintliga']):
            current_section = 'Styrkefaktorer'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['utmaning', 'minska']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Utmaningar'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['möjlighet', 'införa']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Möjligheter'
            current_content = []
        elif any(keyword in line.lower() for keyword in ['visdom', 'insikt']):
            if current_section and current_content:
                sections[current_section] = current_content
            current_section = 'Livsvisdom'
            current_content = []
        elif current_section and line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            # Rensa bort punktlistetecken
            item = line.lstrip('•-*123456789. ')
            current_content.append(item)
    
    # Lägg till den sista sektionen
    if current_section and current_content:
        sections[current_section] = current_content
    
    # Skapa en figur med 2x2 rutnät - resten av funktionen är samma som SWOT-diagramfunktionen men med uppdaterade färger
    import matplotlib.pyplot as plt
    import io
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.patch.set_facecolor('#f0f0f0')
    
    # Definiera färger för varje sektion - anpassade till longevity-tema
    colors = {
        'Styrkefaktorer': '#388E3C',   # Mörkgrön
        'Utmaningar': '#F57C00',       # Orange
        'Möjligheter': '#1976D2',      # Blå
        'Livsvisdom': '#7B1FA2'        # Lila
    }
    
    # Titlar och innehåll för varje kvadrant
    sections_order = ['Styrkefaktorer', 'Utmaningar', 'Möjligheter', 'Livsvisdom']
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for (section, pos) in zip(sections_order, positions):
        i, j = pos
        ax = axs[i, j]
        
        # Sätt bakgrundsfärg
        ax.set_facecolor(colors.get(section, '#EEEEEE') + '22')  # Lägg till transparens
        
        # Sätt titel
        ax.set_title(section, fontsize=14, fontweight='bold', color=colors.get(section, '#333333'))
        
        # Lägg till innehåll
        content = sections.get(section, ['Ingen information tillgänglig'])
        y_pos = 0.9
        for item in content[:7]:  # Begränsa till max 7 punkter
            if len(item) > 60:
                item = item[:57] + '...'  # Begränsa textlängd för visning
            ax.text(0.1, y_pos, f"• {item}", fontsize=10, va='top', wrap=True)
            y_pos -= 0.12
        
        # Ta bort axlar
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    
    # Spara figuren till en buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    
    return buf

def generate_life_motto(data):
    """Genererar ett personligt livsmotto"""
    prompt = f"""
    Skapa ett inspirerande och kraftfullt personligt livsmotto för {data.get('namn', 'en person')} 
    som fokuserar på longevity, hälsosam livsstil och functional food.
    
    Personen har följande egenskaper:
    Ålder: {data.get('alder', 'N/A')}
    Hälsomål: {data.get('halsomal', 'bli hälsosammare')}
    Kosthållning: {data.get('kosthallning', 'blandkost')}
    
    Motton ska vara personligt, inspirerande och reflektera Ulrika Davidssons filosofi om att mat är medicin. 
    Avsluta med en kort reflektion om hur detta motto kan guida personen i vardagen.
    """
    
    motto = generate_chatgpt_response(prompt)
    return motto
