# Data

## Waar staat de data?

In `index.html` zelf, in het blok `<script id="feedforward-data" type="application/json">`.
Bewust niet in een los JSON-bestand: browsers blokkeren het ophalen van een lokaal bestand
als je de pagina met `file://` opent, en dan werkt de download-variant niet meer.

## Huidige inhoud: voorbeelddata

| | |
|---|---|
| Herkomst | Verzonnen voor dit prototype. **Geen echte bezoekersreacties.** |
| Omvang | 72 feedbackitems, 6 pagina's over reisdocumenten |
| Periode in de app | 1 mei 2026 t/m 31 augustus 2026 (fictief) |

De app toont op elk scherm een gele balk die dit benoemt. Haal die balk niet weg zolang er
voorbeelddata in staat.

## Vorm van de data

```
meta       — bron, periode, exportdatum, analysedatum, disclaimer
paginas[]  — id, titel, url, samenvatting
             oorzaken[] — titel, toelichting, citaat_ids[], suggesties[]
feedback[] — id, pagina, beantwoord (true/false), tekst
```

Een oorzaak verwijst met `citaat_ids` naar feedback-items; de citaattekst wordt niet
gekopieerd. Daardoor kán er geen citaat in de app staan dat niet in de bron voorkomt.
Aantallen ("14 van de 16") worden in de app geteld uit `feedback`, niet los opgeslagen.

## Echte Mopinion-data erin zetten

Dit mag pas als de toestemmingen rond zijn (zie het bouwplan, §7). Dan geldt:

1. **Opschonen in Excel, vóórdat het bestand een Claude Code-sessie in gaat.** Verwijder de
   kolommen met e-mailadres, naam, telefoonnummer, IP-adres en sessie-ID.
2. Lees de vrije tekst zelf na. Kolommen weghalen is niet genoeg: een zin als "ik ben 78 en
   wacht al negen weken op mijn paspoort in Alkmaar" is ook herleidbaar. Kort zulke citaten
   in tot de klacht zelf.
3. Draai de analyse met `PROMPT.md`.
4. Zet `meta.is_voorbeelddata` op `false`, vul de echte periode en exportdatum in, en pas de
   gele balk in `index.html` aan.
5. Draai `python3 controle.py` en los alles op wat eruit komt.
6. Commit **nooit** het exportbestand zelf. `.gitignore` sluit `*.csv` en `*.xlsx` uit; wat
   eenmaal gepusht is, blijft in de git-history staan.
