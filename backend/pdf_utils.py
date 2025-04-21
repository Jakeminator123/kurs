# backend/pdf_utils.py

import tempfile
import os
import base64
from fpdf import FPDF
from datetime import datetime
import requests
import uuid
import io
from PIL import Image

def create_pdf_report(data, fyrfalt_text=None, fyrfalt_image=None, livsmotto=None, vision_image=None, full_analysis=False):
    """Skapar en PDF-rapport med all hälsoinformation"""
    try:
        pdf = FPDF()
        # Sätt UTF-8 som kodning för att hantera specialtecken
        pdf.add_page()
        
        # Försök lägga till Ulrikas bild som vattenmärke om den finns
        try:
            # Kontrollera sökvägen till bilden
            ulrika_image_path = "bilder/u.jpg"
            if os.path.exists(ulrika_image_path):
                # Sätt bakgrundsfärg till vit
                pdf.set_fill_color(255, 255, 255)
                pdf.rect(0, 0, 210, 297, style="F")
                
                # Lägg till bild utan alpha-parameter
                pdf.image(ulrika_image_path, x=110, y=10, w=80)
            else:
                print(f"Varning: Kunde inte hitta bilden på {ulrika_image_path}")
        except Exception as e:
            print(f"Kunde inte lägga till vattenmärke: {e}")
        
        # Sätt typsnitt
        pdf.set_font("Arial", "B", 24)
        
        # Titelrubrik
        person_name = data.get('namn', "Din personliga")
        # Konvertera eventuella problematiska tecken
        person_name = person_name.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(190, 20, f"Functional Food & Longevity", ln=True, align="C")
        pdf.set_font("Arial", "B", 18)
        pdf.cell(190, 10, f"Personlig hälsoplan för {person_name}", ln=True, align="C")
        
        # Målbild om tillgänglig
        if vision_image:
            try:
                # Ladda ner målbild
                response = requests.get(vision_image)
                if response.status_code == 200:
                    img_path = f"temp_vision_{uuid.uuid4()}.png"
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Lägg till målbilden i PDF
                    pdf.image(img_path, x=65, y=60, w=80)
                    pdf.ln(90)  # Lägg till utrymme efter bilden
                    
                    # Ta bort temp-filen
                    os.remove(img_path)
                else:
                    print(f"Kunde inte ladda ner bilden, status kod: {response.status_code}")
            except Exception as e:
                print(f"Kunde inte lägga till målbild: {e}")
        
        # Introduktionstext
        pdf.set_font("Arial", "I", 11)
        pdf.multi_cell(190, 10, f"""Den här personliga hälsorapporten är framtagen baserat på information du delat om dina livs- och matvanor. Det är en försmak på den djupa och transformativa kunskap du kan få genom Ulrika Davidssons kompletta kurs i Functional Food och Longevity. 

Med rätt kunskaper och verktyg kan du uppnå optimal hälsa och livslängd genom medvetna matval och livsstilsförändringar.""")
        pdf.ln(5)
        
        # Grundläggande information
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "Din hälsoprofil", ln=True)
        pdf.ln(5)
        
        # Tabellformat för grundläggande information
        pdf.set_font("Arial", "", 12)
        info_items = [
            ("Namn", data.get('namn', 'N/A')),
            ("Ålder", data.get('alder', 'N/A')),
            ("Aktivitetsnivå", data.get('aktivitet', 'N/A')),
            ("Stressnivå", data.get('stress', 'N/A')),
            ("Sömn", f"{data.get('somn', 'N/A')} timmar/natt"),
        ]
        
        # Lägg bara till kosthållning om den finns
        if 'kosthallning' in data:
            info_items.append(("Kosthållning", data.get('kosthallning', 'N/A')))
            
        # Lägg bara till hälsomål om de finns
        if 'halsomal' in data:
            info_items.append(("Hälsomål", data.get('halsomal', 'N/A')))
        
        for label, value in info_items:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(40, 10, label + ":", 0)
            pdf.set_font("Arial", "", 12)
            # Konvertera eventuella problematiska tecken
            value = str(value).encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(150, 10, value, ln=True)
        
        pdf.ln(10)
        
        # Hela analysen om full_analysis=True och det finns superfoods data
        if full_analysis:
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "Din detaljerade analys", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", "", 12)
            
            # Matvanor - bara om datan finns
            if 'superfoods' in data:
                superfoods_list = ", ".join(data.get('superfoods', []))
                pdf.set_font("Arial", "B", 14)
                pdf.cell(190, 10, "Dina matvanor", ln=True)
                pdf.set_font("Arial", "", 12)
                
                matvanor_text = "Dina matval inkluderar:\n\n"
                
                if 'superfoods' in data:
                    matvanor_text += f"Superfoods du äter: {superfoods_list}\n\n"
                
                if 'maltider' in data:
                    matvanor_text += f"Måltider per dag: {data.get('maltider', 'N/A')}\n\n"
                
                if 'mat_gillar' in data:
                    matvanor_text += f"Matpreferenser: {data.get('mat_gillar', 'N/A')}\n\n"
                
                if 'matlagning' in data:
                    matvanor_text += f"Matlagning från grunden: {data.get('matlagning', 'N/A')} gånger/vecka\n\n"
                
                pdf.multi_cell(190, 10, matvanor_text)
                pdf.ln(5)
            
            # Förslag på förbättringar
            pdf.set_font("Arial", "B", 14)
            pdf.cell(190, 10, "Ulrikas förslag till förbättringar", ln=True)
            pdf.set_font("Arial", "", 12)
            
            # Exempel på förbättringsförslag - ersätter punkttecken (•) med vanliga tecken (*)
            forbattringstext = """
Baserat på din profil rekommenderar Ulrika Davidsson att du fokuserar på:

1. Att öka intaget av antioxidantrika livsmedel för att motverka inflammatoriska processer i kroppen
2. Balanserad måltidsplanering som stödjer dina hälsomål
3. Regelbundna matrutiner som optimerar ditt energiflöde under dagen
4. Att prioritera fermenterade livsmedel för att stärka tarmfloran och immunförsvaret

Dessa förbättringar är bara början på din resa mot optimal hälsa och välbefinnande. För en fullständig transformation och personlig vägledning rekommenderas Ulrikas kompletta kurs.
            """
            
            pdf.multi_cell(190, 10, forbattringstext)
            pdf.ln(5)
        
        # Kursplan
        if 'kursplan' in data:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "Din personliga kursplan", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", "", 12)
            
            # Dela upp texten i stycken och lägg till i PDF
            plan_text = data.get('kursplan', '')
            # Ersätt problematiska Unicode-tecken
            plan_text = plan_text.replace('•', '*')
            # Konvertera eventuella problematiska tecken
            plan_text = plan_text.encode('latin-1', 'replace').decode('latin-1')
            paragraphs = plan_text.split('\n\n')
            
            for paragraph in paragraphs:
                # Kolla om det är en rubrik (antar att rubriker är korta rader som slutar med kolon)
                if len(paragraph) < 50 and paragraph.strip().endswith(':'):
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(190, 10, paragraph, ln=True)
                    pdf.set_font("Arial", "", 12)
                else:
                    pdf.multi_cell(190, 10, paragraph)
                    pdf.ln(5)
        
        # Fyrfältsanalys
        if fyrfalt_text:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "Fyrfältsanalys för ditt hälsosamma åldrande", ln=True)
            pdf.ln(5)
            
            # Om det finns en bild av fyrfältsdiagrammet
            if fyrfalt_image:
                try:
                    fyrfalt_img_path = f"temp_fyrfalt_{uuid.uuid4()}.png"
                    with open(fyrfalt_img_path, 'wb') as f:
                        f.write(fyrfalt_image.getvalue())
                    
                    pdf.image(fyrfalt_img_path, x=10, y=None, w=190)
                    pdf.ln(140)  # Lägg till tillräckligt med utrymme efter bilden
                    
                    # Ta bort temp-filen
                    os.remove(fyrfalt_img_path)
                except Exception as e:
                    print(f"Kunde inte lägga till fyrfältsbild: {e}")
            
            # Detaljerad fyrfältstext - Ersätt problematiska Unicode-tecken
            fyrfalt_text = fyrfalt_text.replace('•', '*')
            pdf.set_font("Arial", "", 12)
            # Konvertera eventuella problematiska tecken
            fyrfalt_text_safe = fyrfalt_text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 10, fyrfalt_text_safe)
        
        # Livsmotto (istället för företagsmanifest)
        if livsmotto:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "Ditt personliga livsmotto", ln=True)
            pdf.ln(5)
            
            # Ersätt problematiska Unicode-tecken
            livsmotto = livsmotto.replace('•', '*')
            pdf.set_font("Arial", "I", 12)
            # Konvertera eventuella problematiska tecken
            livsmotto_safe = livsmotto.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 10, livsmotto_safe)
        
        # Säljande avslutning
        pdf.add_page()
        # Försök lägga till Ulrikas bild igen
        try:
            if os.path.exists("bilder/u.jpg"):
                pdf.image("bilder/u.jpg", x=75, y=40, w=60)
                pdf.ln(70)
        except Exception as e:
            print(f"Kunde inte lägga till slutbild: {e}")
        
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "Ta nästa steg mot optimal hälsa", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "", 12)
        # Ersätt bullet points med asterisker
        avslutning_text = """
Detta är bara en försmak på vad du kan lära dig i Ulrika Davidssons kompletta kurs i Functional Food och Longevity. I den fullständiga kursen får du:

* 8 veckors intensiv kunskap och praktiska verktyg
* Personlig coachning och feedback
* Exklusiva recept utvecklade av Ulrika
* Djupgående förståelse för hur mat påverkar ditt åldrande
* Verktyg för att skapa långsiktig förändring

Kursen börjar 15 september 2023, och antalet platser är begränsat till 25 deltagare.

För att säkra din plats, besök www.ulrikadavidsson.se/longevity eller ring 070-12 34 56.

"Min mission är att hjälpa människor leva längre, friskare liv genom kunskap om matens kraft." - Ulrika Davidsson
        """
        pdf.multi_cell(190, 10, avslutning_text)
        
        # Lägg till datum och sidfot
        pdf.set_y(-15)
        pdf.set_font("Arial", "I", 8)
        now = datetime.now().strftime("%Y-%m-%d")
        pdf.cell(0, 10, f"Genererad {now} | Functional Food & Longevity med Ulrika Davidsson", 0, 0, 'C')
        
        # Spara PDF temporärt
        temp_pdf_path = f"haelsoplan_{now.replace('-', '')}.pdf"
        pdf.output(temp_pdf_path)
        
        return temp_pdf_path
        
    except Exception as e:
        # Lägg till detaljerad felhantering
        import traceback
        error_details = traceback.format_exc()
        print(f"Detaljerat fel vid skapande av PDF: {error_details}")
        raise Exception(f"Kunde inte skapa PDF: {str(e)}")

def get_pdf_download_link(file_path, text="Ladda ner PDF"):
    """Genererar en länk för att ladda ner PDF-filen"""
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{os.path.basename(file_path)}">{text}</a>'
    return href

def simple_pdf_report(title, content, output_filename="rapport.pdf"):
    """
    Skapar en enkel PDF-rapport med angivet innehåll.
    content förväntas vara en sträng eller lista av strängar.
    Returnerar sökvägen till den genererade PDF-filen.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Titeln
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, title, ln=True)
    pdf.ln(5)
    
    # Innehållet
    pdf.set_font("Arial", "", 12)
    
    if isinstance(content, list):
        for paragraph in content:
            pdf.multi_cell(190, 10, paragraph)
            pdf.ln(5)
    else:
        pdf.multi_cell(190, 10, content)
    
    # Spara PDF temporärt
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_filename.split('.')[0]}_{now}.pdf"
    pdf.output(output_path)
    
    return output_path
