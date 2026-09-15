# Feedforward

AI-interpretatie van bezoekersfeedback (Mopinion) die per webpagina laat zien wat er
structureel misgaat en wat je eraan kunt doen. Zie [`STRATEGY.md`](STRATEGY.md) voor het
waarom.

**Dit is een prototype dat draait op voorbeelddata.** De feedback in de app is verzonnen en
is niet afkomstig van echte bezoekers.

## Bekijken

- Gepubliceerd: `https://nww-team.github.io/feedforward/` (nadat GitHub Pages is aangezet)
- Of: `index.html` downloaden en dubbelklikken. Werkt ook zonder internet.

## Hoe het in elkaar zit

Eén bestand, `index.html`, zonder build en zonder dependencies. De analyse zit erin als een
`<script id="feedforward-data" type="application/json">`-blok. Er is geen server, geen
database en geen API-sleutel — daarom kan het bestand ook los geopend worden.

| Bestand | Wat het is |
|---|---|
| `index.html` | De app én de data |
| `PROMPT.md` | De instructie waarmee de analyse opnieuw te maken is (Claude Code) |
| `PROMPT-CHAT.md` | Dezelfde instructie als losse prompt, voor een chatmodel |
| `controle.py` | Controleert dat elk citaat in de app echt in de dataset staat |
| `data/README.md` | Herkomst van de data en hoe je echte data erin zet |
| `STRATEGY.md` | De strategie achter het product |

## GitHub Pages aanzetten

Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)`. De URL is binnen
een paar minuten bereikbaar. **Let op:** bij een publieke repo is alles wat in `index.html`
staat voor iedereen op internet leesbaar, inclusief de citaten.

## Controle draaien

```
python3 controle.py
```

Faalt als een citaat niet letterlijk in de dataset voorkomt, als een oorzaak minder dan twee
citaten heeft, of als er een CSV/XLSX in de repo staat.
