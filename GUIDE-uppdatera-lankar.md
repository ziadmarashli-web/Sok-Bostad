# Uppdatera hyresvärdar och länkar

Det här GitHub-paketet använder **`bolag.json` som enda fil du ska redigera för bolagsuppgifter**.
`index.html` och `lankkontroll.html` genereras från samma lista.

## Filer

- `index.html` – den publika appen (GitHub Pages startsida)
- `bolag.json` – **enda källan för hyresvärdar, orter och länkar**
- `lankkontroll.html` – enkel manuell kontroll av länkar
- `uppdatera-app.py` – för över ändringar från `bolag.json` till båda HTML-filerna

## 1. Kontrollera länkar

Öppna `lankkontroll.html` i webbläsaren. Klicka **Öppna ↗** för varje bolag och markera:

- **Fungerar** – länken går till rätt officiella webbplats
- **Trasig** – sidan saknas, är fel eller leder till fel företag

Markeringarna sparas bara i den webbläsaren.

## 2. Ändra bara `bolag.json`

Exempel:

```json
{
  "name": "Alebyggen",
  "url": "https://www.alebyggen.se/",
  "orter": ["Ale"],
  "note": "kommunal"
}
```

Fält:

- `name` – hyresvärdens namn
- `url` – officiell HTTPS-adress
- `orter` – orter i **Västra Götaland** som appen ska visa bolaget för
- `note` – valfritt: `kommunal` eller `formedling`. Utan `note` visas bolaget som privat.

Lägg inte in orter utanför Västra Götaland i den här versionen. Skriptet stoppar uppdateringen om en sådan ort finns.

## 3. Bygg om appen

Alla filer ska ligga i samma mapp.

### Windows

Öppna mappen i Utforskaren, skriv `cmd` i adressfältet och tryck Enter. Kör:

```text
python uppdatera-app.py
```

### Mac / Linux

```text
python3 uppdatera-app.py
```

När allt är rätt visas exempelvis:

```text
KLART! 67 bolag har skrivits till index.html och lankkontroll.html.
```

Skriptet skapar även `.backup`-filer innan det skriver över HTML-filerna.

## 4. Ladda upp till GitHub

Efter en ändring laddar du upp/committar minst:

- `bolag.json`
- `index.html`
- `lankkontroll.html`

`uppdatera-app.py` och den här guiden behöver bara laddas upp igen om de själva ändrats.

## GitHub Pages

Första gången: öppna repositoryts **Settings → Pages**, välj publicering från den branch/mapp där `index.html` ligger (vanligen `main` och `/root`).

## Viktigt

Redigera inte bolagslistan manuellt i `index.html` eller `lankkontroll.html`. Nästa körning av skriptet skriver ändå över den. Ändra alltid `bolag.json`.

*Senast uppdaterad: 16 september 2026.*
