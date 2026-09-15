# Analyse-instructie

Hiermee maak je het datablok in `index.html` opnieuw. Gebruik dit in een Claude Code-sessie
op deze repository. Werk je met een chatmodel dat deze bestanden niet kan lezen, gebruik dan
[`PROMPT-CHAT.md`](PROMPT-CHAT.md): dezelfde opdracht, maar als één blok tekst om te plakken.

## Wat je aanlevert

Een **opgeschoonde** Mopinion-export (CSV of Excel): kolommen met e-mailadres, naam,
telefoonnummer, IP-adres en sessie-ID zijn er al uit, vóórdat het bestand de sessie in gaat.
Zie `data/README.md`.

Zet het bestand niet in de repo — `.gitignore` houdt het tegen, en dat is de bedoeling.

## De opdracht

> Lees de aangeleverde feedback-export. Analyseer per webpagina wat er structureel misgaat.
> Vervang daarna het blok `<script id="feedforward-data" type="application/json">` in
> `index.html` door het resultaat, in exact dezelfde vorm. Houd je aan de regels hieronder
> en draai `python3 controle.py` voordat je iets commit.

## Regels voor de analyse

**Citaten.**
- Een oorzaak verwijst naar feedback met `citaat_ids`, nooit met overgetypte tekst.
- Elke feedbacktekst in `feedback[]` staat er **letterlijk** in zoals de bezoeker hem schreef.
  Niet herschrijven, niet corrigeren, niet samenvoegen, niet mooier maken.
- Een citaat mag ingekort worden om herleidbaarheid te voorkomen, maar dan wordt de
  ingekorte versie de tekst in `feedback[]`. Er ontstaat nooit een citaat dat niet in de
  dataset staat.

**Oorzaken.**
- Twee tot vier per pagina. Meer is geen analyse meer, maar een lijst.
- Minimaal twee verschillende feedbackitems per oorzaak. Eén klacht is geen patroon — laat
  hem liever weg.
- De titel benoemt wat de lezer mist, niet wat de redactie fout deed.
- `toelichting` legt uit waaróm dit mensen raakt, in twee of drie zinnen.

**Suggesties.**
- Eén of twee per oorzaak, concreet genoeg om morgen uit te voeren.
- Verwijs naar deze specifieke pagina. "Maak de tekst duidelijker" is geen suggestie.
- Verzin geen feiten. Als het juiste antwoord (een doorlooptijd, een bedrag, een adres) niet
  in de feedback staat, luidt de suggestie dat die informatie ontbreekt en toegevoegd moet
  worden — niet wat die informatie zou moeten zijn.

**Aantallen.** Niet opslaan. De app telt ze uit `feedback[]`.

**Meta.** Vul `periode`, `export_datum` en `analyse_datum` in. Zet `is_voorbeelddata` op
`false` zodra het om echte data gaat, en pas dan ook de gele balk bovenaan `index.html` aan.

## Vorm

```json
{
  "meta": { "is_voorbeelddata": false, "bron": "...", "periode": "...",
            "export_datum": "...", "analyse_datum": "...", "onderwerp": "...",
            "disclaimer": "..." },
  "paginas": [
    { "id": "korte-slug", "titel": "...", "url": "https://...",
      "samenvatting": "één zin: de belangrijkste oorzaak",
      "oorzaken": [
        { "titel": "...", "toelichting": "...",
          "citaat_ids": ["f003", "f011"],
          "suggesties": ["...", "..."] }
      ] }
  ],
  "feedback": [
    { "id": "f001", "pagina": "korte-slug", "beantwoord": false, "tekst": "letterlijk" }
  ]
}
```

## Vóór het committen

1. `python3 controle.py` — moet zonder fouten doorlopen.
2. Steekproef: kies vijf citaten uit de app en zoek ze terug in de export. Eén mismatch
   betekent: analyse opnieuw, niet handmatig repareren.
3. Bij echte data: lees alle citaten na op herleidbaarheid.
