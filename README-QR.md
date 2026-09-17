# V4.5 – kort och krypterad QR-överföring

Den här versionen använder inte längre QR-koden för att bära hela listan.

## Hur det fungerar
1. Datorn krypterar listan lokalt med AES-GCM.
2. Endast den krypterade datan lagras tillfälligt i Netlify Blobs.
3. QR-koden innehåller en kort engångslänk med ett slumpmässigt ID och krypteringsnyckeln.
4. Mobilen hämtar den krypterade datan och dekrypterar lokalt.
5. Efter lyckad återställning begär mobilen att posten raderas.
6. Posten upphör att gälla efter 20 minuter även om den inte används.

Krypteringsnyckeln ligger i URL-fragmentet (`#k=...`). URL-fragment skickas inte till servern när sidan hämtas.

## GitHub / Netlify
Lägg upp hela strukturen:

/
  index.html
  package.json
  netlify.toml
  netlify/
    functions/
      transfer.mjs

Netlify installerar `@netlify/blobs` och publicerar funktionen på `/api/transfer`.

## Test
1. Vänta tills Netlify-deployen är klar.
2. Öppna appen på datorn.
3. Registrera/sök hos några bolag.
4. Min lista → Spara för senare → Till mobilen med QR-kod.
5. QR-koden ska vara liten och skanningsbar.
6. På mobilen ska listan återställas automatiskt.

Om Netlify-funktionen inte är publicerad visar appen att QR-överföringen inte kunde skapas och användaren kan fortfarande välja Spara fil.
