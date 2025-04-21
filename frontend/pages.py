# frontend/pages.py

import streamlit as st
from backend.openai_utils import (
    generate_chatgpt_response, 
    search_web, 
    generate_logo, 
    generate_swot_analysis, 
    create_swot_diagram, 
    generate_company_manifest
)
from backend.pdf_utils import create_pdf_report, get_pdf_download_link
import os

def intro_page():
    st.title("Välkommen till Functional Food & Longevity")
    st.write("Hej! Jag är din digitala guide inför Ulrika Davidssons exklusiva kurs om Functional Food och Longevity. Jag kommer att hjälpa dig att utvärdera dina nuvarande livsvanor och förbereda en skräddarsydd kursplan.")
    
    namn = st.text_input("Vad heter du?")
    if namn:
        st.session_state.user_data["namn"] = namn
        st.write(f"Hej {namn}! Spännande att du vill lära dig mer om hur mat kan förlänga ditt liv och förbättra din hälsa. Klicka på knappen nedan för att börja din resa.")
        
        if st.button("Starta utvärderingen"):
            st.session_state.current_stage = "livsstil"
            st.rerun()

def livsstil_page():
    st.title(f"Dina livsvanor - {st.session_state.user_data.get('namn', 'Din')} personliga profil")
    st.write("Först behöver vi förstå dina nuvarande livsvanor för att kunna ge de bästa rekommendationerna.")
    
    # Ålder
    alder = st.slider("Hur gammal är du?", 18, 100, 40)
    if alder:
        st.session_state.user_data["alder"] = alder
    
    # Aktivitetsnivå
    aktivitet_options = ["Låg (mest stillasittande)", "Måttlig (någon träning/vecka)", "Aktiv (3-5 träningspass/vecka)", "Mycket aktiv (daglig träning)"]
    aktivitet = st.selectbox("Hur skulle du beskriva din aktivitetsnivå?", aktivitet_options)
    if aktivitet:
        st.session_state.user_data["aktivitet"] = aktivitet
    
    # Stress
    stress_options = ["Låg (sällan stressad)", "Måttlig (ibland stressad)", "Hög (ofta stressad)", "Mycket hög (konstant stressad)"]
    stress = st.selectbox("Hur skulle du beskriva din stressnivå?", stress_options)
    if stress:
        st.session_state.user_data["stress"] = stress
    
    # Sömn
    somn = st.slider("Hur många timmar sover du i genomsnitt per natt?", 4, 12, 7)
    if somn:
        st.session_state.user_data["somn"] = somn
    
    # Hälsomål
    halsomal = st.text_area("Beskriv dina främsta hälsomål:", placeholder="T.ex. gå ner i vikt, få mer energi, leva längre, förbättra matsmältningen...")
    if halsomal:
        st.session_state.user_data["halsomal"] = halsomal
    
    # Hälsoutmaningar
    halsoutmaningar = st.multiselect(
        "Har du några specifika hälsoutmaningar?",
        ["Inflammation", "Matsmältningsproblem", "Högt blodtryck", "Högt kolesterol", "Diabetes/pre-diabetes", "Ledbesvär", "Trötthet/energibrist", "Sömnproblem", "Stressrelaterade problem", "Viktproblem", "Hudproblem", "Inga specifika utmaningar", "Annat"]
    )
    if halsoutmaningar:
        st.session_state.user_data["halsoutmaningar"] = halsoutmaningar
    
    if st.button("Fortsätt till matvanor"):
        st.session_state.current_stage = "matvanor"
        st.rerun()

def matvanor_page():
    st.title("Dina matvanor")
    st.write("Nu ska vi utforska dina matvanor för att kunna ge personliga rekommendationer inom functional food.")
    
    # Visa tidigare svar
    with st.expander("Sammanfattning av dina livsvanor"):
        for key, value in st.session_state.user_data.items():
            if key not in ["namn", "halsomal", "halsoutmaningar"]:
                st.write(f"**{key.capitalize()}:** {value}")
    
    # Kosthållning
    kosthallning = st.selectbox(
        "Vilken kosthållning följer du främst?",
        ["Blandkost", "Vegetarisk", "Vegansk", "Pescetarian", "Lågkolhydrat/LCHF", "Ketogen", "Paleo", "Medelhavsmat", "Periodisk fasta", "Annat/Ingen specifik"]
    )
    if kosthallning:
        st.session_state.user_data["kosthallning"] = kosthallning
    
    # Måltidsfrekvens
    maltider = st.slider("Hur många måltider äter du vanligtvis per dag?", 1, 8, 3)
    if maltider:
        st.session_state.user_data["maltider"] = maltider
    
    # Matlagning
    matlagning = st.slider("Hur många gånger i veckan lagar du mat från grunden?", 0, 21, 7)
    if matlagning:
        st.session_state.user_data["matlagning"] = matlagning
    
    # Nya frågor om matvanor
    vattenmangd = st.slider("Hur många glas vatten dricker du per dag?", 0, 15, 6)
    if vattenmangd:
        st.session_state.user_data["vattenmangd"] = vattenmangd
        
    # Frukost
    frukost_vanor = st.radio(
        "Hur ser dina frukostvanor ut?",
        ["Äter alltid frukost", "Äter oftast frukost", "Äter ibland frukost", "Äter sällan frukost", "Äter aldrig frukost"]
    )
    if frukost_vanor:
        st.session_state.user_data["frukost_vanor"] = frukost_vanor
    
    frukost_exempel = st.text_area("Beskriv din typiska frukost (om du äter frukost):")
    if frukost_exempel:
        st.session_state.user_data["frukost_exempel"] = frukost_exempel
    
    # Kvällsrutiner
    kvallsmat = st.radio(
        "Äter du något innan du går och lägger dig?",
        ["Ja, alltid", "Ja, ofta", "Ibland", "Sällan", "Aldrig"]
    )
    if kvallsmat:
        st.session_state.user_data["kvallsmat"] = kvallsmat
    
    kvall_tid = st.slider("Hur lång tid innan sänggåendet äter du din sista måltid/snack?", 0, 6, 2, format="%d timmar")
    if kvall_tid:
        st.session_state.user_data["kvall_tid"] = kvall_tid
    
    # Matpreferenser
    mat_gillar = st.text_area("Vilka livsmedel äter du mycket av och uppskattar?")
    if mat_gillar:
        st.session_state.user_data["mat_gillar"] = mat_gillar
    
    mat_ogillar = st.text_area("Vilka livsmedel undviker du eller tycker mindre om?")
    if mat_ogillar:
        st.session_state.user_data["mat_ogillar"] = mat_ogillar
    
    # Matutmaningar
    matutmaningar = st.multiselect(
        "Vilka utmaningar har du med din kost?",
        ["Hinner inte laga mat", "Svårt att planera måltider", "Hedonistisk hunger/sockersug", "Äter för mycket", 
         "Äter för lite", "Äter för snabbt", "Äter ofta ute", "Ekonomiska begränsningar", 
         "Matallergi/intolerans", "Svårt att variera kosten", "Svårt att hitta inspiration", "Inga specifika utmaningar"]
    )
    if matutmaningar:
        st.session_state.user_data["matutmaningar"] = matutmaningar
    
    # Superfoods
    superfoods = st.multiselect(
        "Vilka av dessa superfoods äter du regelbundet?",
        ["Bär (blåbär, goji, etc)", "Gröna bladgrönsaker", "Nötter och frön", "Fettig fisk", "Fermenterade livsmedel", 
         "Ingefära", "Gurkmeja", "Spirulina/Alger", "Broccoli/kålväxter", "Avokado", "Kokosolja", "Ägg", 
         "Grönt te", "Kakao/mörk choklad", "Olivolja", "Ingen av dessa"]
    )
    if superfoods:
        st.session_state.user_data["superfoods"] = superfoods
    
    # Aptitregler
    aptit_regler = st.multiselect(
        "Vilka 'regler' tenderar du att följa för ditt ätande?",
        ["Undviker processad mat", "Undviker socker", "Undviker gluten", "Undviker mejeriprodukter", 
         "Äter bara ekologiskt", "Periodisk fasta", "Äter efter vissa tider", "Begränsar kolhydrater", 
         "Räknar kalorier", "Äter efter hunger", "Följer strikta måltidstider", "Inga specifika regler"]
    )
    if aptit_regler:
        st.session_state.user_data["aptit_regler"] = aptit_regler
    
    # Målbild - uppdaterad prompt för mer drömsk bild
    st.subheader("Din målbild")
    if st.button("Generera personlig målbild"):
        with st.spinner("Skapar din hälsomålbild..."):
            try:
                from app import generate_vision_image
                prompt = f"""Skapa en drömsk, magisk och inspirerande bild som representerar en optimal hälsosam livsstil för {st.session_state.user_data.get('namn', 'en person')} som vill {st.session_state.user_data.get('halsomal', 'leva hälsosamt')}. 
                
                Bilden ska vara fantasifull och nästan spirituell med en känsla av transformation. Inkludera vackra, vibrerande färger, mjukt ljus och en känsla av välbefinnande. Visa näringsrika, levande råvaror som strålar av energi, där varje ingrediens verkar ha en glödande aura.
                
                Inkludera subtila symboler för longevity och livskraft som en strömmande källa av klart vatten, spirande växter, och kanske ett vackert träd som representerar livets resa. Atmosfären ska vara lugnande och hoppfull, som en perfekt drömbild av hur functional food och rätt livsstil kan transformera ens hälsa och liv."""
                
                image_url = generate_vision_image(prompt)
                st.session_state.vision_image = image_url
                st.image(image_url, caption="Din personliga hälsomålbild", width=400)
                st.success("Din målbild är klar! Reflektera över hur denna vision kan bli din verklighet med rätt kunskap och vägledning.")
            except Exception as e:
                st.error(f"Kunde inte generera målbild: {str(e)}")
    
    if st.button("Fortsätt till longevitetsanalys"):
        st.session_state.current_stage = "longevity"
        st.rerun()

def longevity_page():
    st.title("Longevitetsanalys")
    st.write("Nu ska vi utforska hur dina livsvanor och matval påverkar din långsiktiga hälsa och livslängd.")
    
    # "Fyrfältare" istället för SWOT-analys
    st.subheader("Fyrfältsanalys för ditt hälsosamma åldrande")
    if st.button("Generera fyrfältsanalys"):
        with st.spinner("Analyserar dina vanor för optimal livslängd..."):
            from backend.openai_utils import generate_longevity_analysis, create_longevity_diagram
            
            # Generera textanalys
            fyrfalt_text = generate_longevity_analysis(st.session_state.user_data)
            st.session_state.fyrfalt_analys = fyrfalt_text
            
            # Visa textanalys
            st.write(fyrfalt_text)
            
            # Skapa och visa diagram
            fyrfalt_image = create_longevity_diagram(fyrfalt_text)
            st.session_state.fyrfalt_image = fyrfalt_image
            st.image(fyrfalt_image, caption="Din personliga fyrfältsanalys", use_column_width=True)
    
    # Livsmotto istället för företagsmanifest
    st.subheader("Ditt personliga livsmotto")
    if st.button("Skapa livsmotto"):
        with st.spinner("Skapar ditt personliga livsmotto..."):
            from backend.openai_utils import generate_life_motto
            
            livsmotto = generate_life_motto(st.session_state.user_data)
            st.session_state.livsmotto = livsmotto
            
            st.markdown("### Ditt livsmotto")
            st.markdown(f"<div style='padding: 20px; border-radius: 10px; background-color: #F1F8E9; border-left: 4px solid #2E7D5A;'>{livsmotto}</div>", unsafe_allow_html=True)
    
    # Livslängdsuppskattning
    st.subheader("Dina longevitetsfaktorer")
    if st.button("Analysera longevitetsfaktorer"):
        with st.spinner("Analyserar faktorer som påverkar din potentiella livslängd..."):
            from backend.openai_utils import generate_chatgpt_response
            
            data = st.session_state.user_data
            longevity_prompt = (
                f"Baserat på följande information om {data.get('namn', 'personen')}: "
                f"Ålder: {data.get('alder', 'N/A')}, Aktivitetsnivå: {data.get('aktivitet', 'N/A')}, "
                f"Stressnivå: {data.get('stress', 'N/A')}, Sömnmängd: {data.get('somn', 'N/A')}, "
                f"Kosthållning: {data.get('kosthallning', 'N/A')}, "
                f"Regelbundna superfoods: {', '.join(data.get('superfoods', ['N/A']))}, "
                f"Identifiera de tre viktigaste faktorerna som påverkar personens potentiella livslängd positivt "
                f"och de tre faktorer som bör förbättras. Ge konkreta och personliga rekommendationer om hur dessa förbättringar "
                f"kan göras med hjälp av functional food principer enligt Ulrika Davidssons filosofi. "
                f"Var specifik och personlig i dina rekommendationer."
            )
            longevity_analys = generate_chatgpt_response(longevity_prompt)
            st.write(longevity_analys)
    
    if st.button("Skapa din personliga kursplan"):
        st.session_state.current_stage = "kursplan"
        st.rerun()

def kursplan_page():
    st.title("Din personliga kursplan med Ulrika Davidsson")
    
    # Lägg till en bild av Ulrika i header
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image("bilder/u.jpg", width=150)
        except:
            st.write("(Bild på Ulrika Davidsson)")
    
    with col2:
        st.markdown("""
        ### Transformera din hälsa med expertkunskap
        
        Ulrika Davidsson är Sveriges ledande expert inom functional food och longevity. 
        Hennes kurser har hjälpt tusentals människor att förbättra sin hälsa, 
        öka sin energi och förlänga sitt liv genom smarta matval.
        """)

    # Visa sammanfattning
    with st.expander("Översikt över din hälsoprofil", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Din information")
            st.write(f"**Namn:** {st.session_state.user_data.get('namn', 'Ej angivet')}")
            st.write(f"**Ålder:** {st.session_state.user_data.get('alder', 'Ej angivet')}")
            st.write(f"**Kosthållning:** {st.session_state.user_data.get('kosthallning', 'Ej angivet')}")
            st.write(f"**Hälsomål:** {st.session_state.user_data.get('halsomal', 'Ej angivet')}")
            
        with col2:
            st.subheader("Status")
            if 'vision_image' in st.session_state and st.session_state.vision_image:
                st.write("✅ Målbild genererad")
                st.image(st.session_state.vision_image, width=100)
            else:
                st.write("❌ Målbild ej genererad")
                
            if 'fyrfalt_analys' in st.session_state and st.session_state.fyrfalt_analys:
                st.write("✅ Fyrfältsanalys klar")
            else:
                st.write("❌ Fyrfältsanalys ej genomförd")
                
            if 'livsmotto' in st.session_state and st.session_state.livsmotto:
                st.write("✅ Livsmotto skapat")
            else:
                st.write("❌ Livsmotto ej skapat")
                
            if 'kursplan' in st.session_state.user_data:
                st.write("✅ Personlig kursplan genererad")
            else:
                st.write("❌ Personlig kursplan ej genererad")
    
    # Generera personlig kursplan med säljfokus
    st.subheader("Din personliga kursplan")
    if st.button("Generera kursplan"):
        data = st.session_state.user_data
        prompt = (
            f"Skapa en personlig 8-veckors kursplan inom Functional Food och Longevity för {data.get('namn', 'kursdeltagaren')}. "
            f"Personen är {data.get('alder', 'N/A')} år, har aktivitetsnivån {data.get('aktivitet', 'N/A')}, "
            f"följer en {data.get('kosthallning', 'blandad')} kost, "
            f"har specifika hälsoutmaningar som {', '.join(data.get('halsoutmaningar', ['inga speciella']))}. "
            f"Deras hälsomål är att {data.get('halsomal', 'förbättra sin hälsa')}. "
            f"Kursen ska innehålla veckovisa fokusområden med: "
            f"1. Ett tema för veckan "
            f"2. Tre superfoods att fokusera på "
            f"3. En praktisk utmaning "
            f"4. Ett recept att testa "
            f"5. En insikt från Ulrika Davidsson "
            f"6. En försmak på vad den fullständiga kursen skulle fördjupa sig i "
            f"Gör planen personlig baserat på den information som givits om personen, och gör det klart att detta bara är en introduktion "
            f"och att den fullständiga kursen med Ulrika skulle innehålla mycket mer djupgående information, personlig coachning och "
            f"verktyg för transformation. Avsluta med en uppmuntrande inbjudan till den fullständiga kursen."
        )
        
        with st.spinner("Genererar din personliga kursplan... (detta kan ta upp till 30 sekunder)"):
            from backend.openai_utils import generate_chatgpt_response
            kursplan = generate_chatgpt_response(prompt, temperature=0.7)
            st.session_state.user_data["kursplan"] = kursplan
        
        st.markdown(kursplan)
    
    # Visa kursplanen om den redan har genererats
    if 'kursplan' in st.session_state.user_data:
        with st.expander("Visa tidigare genererad kursplan"):
            st.markdown(st.session_state.user_data["kursplan"])
    
    # Säljande box
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; background-color: #EBF5EE; border-left: 4px solid #2E7D5A; margin: 30px 0;">
        <h3 style="color: #2E7D5A; margin-top: 0;">Ta nästa steg mot optimal hälsa</h3>
        <p>Detta är bara en försmak på vad du kan uppnå med rätt kunskap och vägledning. 
        Ulrika Davidssons kompletta kurs ger dig alla verktyg du behöver för att:</p>
        <ul>
            <li>Minska inflammation i kroppen</li>
            <li>Öka din energinivå dramatiskt</li>
            <li>Förbättra din mentala klarhet</li>
            <li>Förebygga åldersrelaterade sjukdomar</li>
            <li>Optimera ditt matspektrum för longevity</li>
        </ul>
        <p><strong>Kursen börjar 15 september 2023. Endast 25 platser tillgängliga.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Knapp för att skapa PDF
    st.subheader("PDF-rapport")
    if st.button("Skapa PDF-rapport"):
        with st.spinner("Skapar din personliga hälsorapport..."):
            try:
                from backend.pdf_utils import create_pdf_report
                pdf_path = create_pdf_report(
                    st.session_state.user_data,
                    fyrfalt_text=st.session_state.get('fyrfalt_analys', None),
                    fyrfalt_image=st.session_state.get('fyrfalt_image', None),
                    livsmotto=st.session_state.get('livsmotto', None),
                    vision_image=st.session_state.get('vision_image', None),
                    full_analysis=True  # Lägg till hela analysen
                )
                st.session_state.pdf_path = pdf_path
                st.success(f"PDF skapad! Filnamn: {pdf_path}")
                
                # Visa länk för att ladda ner PDF
                from backend.pdf_utils import get_pdf_download_link
                download_link = get_pdf_download_link(pdf_path, "Klicka här för att ladda ner din personliga hälsorapport som PDF")
                st.markdown(download_link, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Ett fel uppstod när PDF-filen skulle skapas: {str(e)}")
    
    # Frågesektion
    st.subheader("Har du frågor om functional food eller longevity?")
    user_question = st.text_input("Ställ en fråga till Ulrika Davidsson:")
    
    if user_question and st.button("Få svar"):
        from backend.openai_utils import generate_chatgpt_response
        
        # Lägg till frågan i konversationshistoriken
        st.session_state.conversation_history.append({"role": "user", "content": user_question})
        
        # Generera svar
        answer = generate_chatgpt_response(
            f"Fråga om functional food och longevity: {user_question}. Ge ett informativt men också säljande svar som väcker intresse för hela kursen.", 
            history=st.session_state.conversation_history[-10:] if len(st.session_state.conversation_history) > 0 else []
        )
        
        # Lägg till svaret i konversationshistoriken
        st.session_state.conversation_history.append({"role": "assistant", "content": answer})
        
        # Visa svaret
        st.write("**Ulrika Davidsson svarar:**")
        st.write(answer)

def display_chat_history():
    """Visar konversationshistoriken"""
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.write(f"**Du:**")
            st.write(message["content"])
        else:
            st.write(f"**Affärsrådgivaren:**")
            st.write(message["content"])
        st.write("---") 