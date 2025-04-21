# PowerShell-skript för att starta Streamlit-appen
# Kör med: .\start_app.ps1

Write-Host "Startar Functional Food & Longevity med Ulrika Davidsson..."
Write-Host "Förbereder miljön..."

# Kontrollera om .env-filen finns, om inte skapa en mall för den
if (-not (Test-Path ".env")) {
    Write-Host "Ingen .env-fil hittades." -ForegroundColor Yellow
    Write-Host "Se till att du har skapat en .env-fil med din OPENAI_API_KEY innan du startar appen." -ForegroundColor Yellow
    Write-Host "Du kan kopiera .env.example till .env och lägga till din API-nyckel." -ForegroundColor Yellow
}

# Starta Streamlit-appen
streamlit run app.py

# Behåll fönstret öppet om det uppstår fel
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ett fel uppstod vid start av appen. Felkod: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Tryck på valfri tangent för att stänga..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 