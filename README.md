# Functional Food & Longevity med Ulrika Davidsson

En interaktiv Streamlit-applikation för hälsovägledning med fokus på functional food och longevity. Appen vägleder användaren genom olika steg för att skapa en personlig hälsoplan.

## Funktioner

- **Interaktiv livsstilsanalys**: Guidar användaren genom olika hälsorelaterade frågor
- **Matvanor och råd**: Analyser och rekommendationer kring matvanor
- **Longevitystrategi**: Långsiktiga strategier för hälsosamt åldrande
- **Personlig hälsoplan**: Genererar en skräddarsydd hälsoplan baserad på användarens svar
- **AI-genererade bilder**: Skapar inspirerande visualiseringar
- **PDF-export**: Exportera den kompletta hälsoplanen som en professionell PDF-rapport

## Projektstruktur

Projektet är organiserat i frontend- och backend-moduler för bättre struktur:

```
.
├── app.py                  # Huvudapplikationsfil
├── frontend/               # Frontend kod för UI
│   ├── pages.py            # Sidkomponenter
│   └── navigation.py       # Navigeringsfunktioner
├── backend/                # Backend kod för affärslogik
│   ├── openai_utils.py     # Funktioner för OpenAI-interaktion
│   ├── pdf_utils.py        # Funktioner för PDF-generering
│   └── session_utils.py    # Funktioner för sessionshantering
├── .streamlit/             # Streamlit-konfiguration
├── requirements.txt        # Projektberoenden
├── render.yaml             # Konfiguration för Render-hosting
└── .env                    # Miljövariabler (skapa från .env.example)
```

## Installation och körning

### Lokal installation

1. Klona detta repository
2. Installera beroenden:
```
pip install -r requirements.txt
```
3. Skapa en .env-fil och lägg till din OpenAI API-nyckel:
```
OPENAI_API_KEY=din_openai_api_nyckel_här
```
4. Kör appen:
```
streamlit run app.py
```

### Driftsättning på Render

För att driftsätta appen på Render:

1. Skapa ett konto på [Render](https://render.com)
2. Länka ditt GitHub-repository
3. Klicka på "New Web Service"
4. Välj ditt repository och Render kommer automatiskt att upptäcka `render.yaml`
5. Lägg till din OpenAI API-nyckel som miljövariabel i Render-gränssnittet
6. Klicka på "Create Web Service"

## Krav

- Python 3.9+
- Streamlit 1.23.0+
- OpenAI API-nyckel 