# Analyse-instructie voor een los AI-model

`PROMPT.md` gaat ervan uit dat de AI in deze repository zit: hij leest de bestanden zelf,
past `index.html` aan en draait `controle.py`. Een chatmodel (ChatGPT, Gemini, Claude in de
browser, Copilot) kan dat niet. Daarom staat hieronder dezelfde opdracht als één blok tekst
dat je kunt plakken, met alle context erin en met de controles als instructie in plaats van
als script.

## Wat je doet

1. Schoon de Mopinion-export op in Excel: haal de kolommen met e-mailadres, naam,
   telefoonnummer, IP-adres en sessie-ID eruit. Zie `data/README.md`.
2. Open een chat met een model dat bijlagen kan lezen. Hang de opgeschoonde export eraan.
3. Plak de prompt hieronder (alles tussen de streepjes) als eerste bericht.
4. Je krijgt één JSON-object terug. Wat je daarmee doet, staat onder
   [Wat je met het antwoord doet](#wat-je-met-het-antwoord-doet).

Zet de export niet in de repo — `.gitignore` houdt hem tegen, en dat is de bedoeling.

## De prompt

````
Je bent tekstanalist voor de webredactie van een overheidsorganisatie. Je analyseert
bezoekersfeedback en levert het resultaat als JSON.

# Context

Bezoekers van de website vullen onderaan een pagina een feedbackformulier (Mopinion) in.
Ze geven aan of ze wel of geen antwoord kregen op hun vraag, en lichten in vrije tekst toe
waarom. De redactie wil niet zelf door honderden reacties heen om de rode draad te vinden;
daarom bepaal jij per pagina wat er structureel misgaat en wat de redacteur eraan kan doen.

Je lezer is een webredacteur die morgen aan die pagina gaat werken. Niet een manager die
een rapportage wil.

# Invoer

De bijgevoegde export bevat per rij één reactie. De kolomnamen kunnen per export verschillen.
Je hebt er vier nodig:

- de pagina waarop de feedback is gegeven (URL en/of paginatitel)
- of de bezoeker antwoord kreeg (ja/nee)
- de vrije tekst van de bezoeker
- de datum

Kun je niet met zekerheid bepalen welke kolom welke is? Stel dan eerst die vraag en begin
nog niet aan de analyse.

# Opdracht

Groepeer de reacties per pagina. Bepaal per pagina welke oorzaken structureel terugkomen en
geef per oorzaak concrete verbetersuggesties. Lever het resultaat als één JSON-object in de
vorm die onderaan staat.

# Regels

## Citaten

- Elke feedbacktekst in `feedback[]` staat er LETTERLIJK in zoals de bezoeker hem schreef.
  Niet herschrijven, niet corrigeren, niet samenvoegen, niet mooier maken. Typefouten,
  hoofdletters en kromme zinnen blijven staan.
- Een oorzaak verwijst naar feedback met `citaat_ids`, nooit met overgetypte tekst.
- Een citaat mag ingekort worden om herleidbaarheid te voorkomen, maar dan wordt de
  ingekorte versie de tekst in `feedback[]`. Er ontstaat nooit een citaat dat niet in de
  dataset staat.
- Staat er een naam, adres, e-mailadres, telefoonnummer, postcode, BSN of een detail waardoor
  iemand herkenbaar is ("ik ben 78 en wacht al negen weken in Alkmaar") in een reactie? Kort
  die reactie in tot de klacht zelf, en gebruik die ingekorte versie als tekst.
- Neem alle reacties van een opgenomen pagina op in `feedback[]`, niet alleen de reacties die
  je als citaat gebruikt. De app telt de aantallen zelf uit deze lijst.

## Oorzaken

- Twee tot vier per pagina. Meer is geen analyse meer, maar een lijst.
- Minimaal twee verschillende feedbackitems per oorzaak. Eén klacht is geen patroon — laat
  hem liever weg.
- De citaten onder een oorzaak horen bij dezelfde pagina als die oorzaak.
- De titel benoemt wat de lezer mist, niet wat de redactie fout deed.
  Dus: "Onduidelijk hoe lang je op je paspoort wacht", niet: "Doorlooptijd niet vermeld".
- `toelichting` legt in twee of drie zinnen uit waaróm dit mensen raakt.
- Kun je voor een pagina geen twee oorzaken onderbouwen? Laat die pagina dan helemaal weg —
  ook uit `feedback[]`.

## Suggesties

- Eén of twee per oorzaak, concreet genoeg om morgen uit te voeren.
- Verwijs naar deze specifieke pagina. "Maak de tekst duidelijker" is geen suggestie.
- Verzin geen feiten. Als het juiste antwoord (een doorlooptijd, een bedrag, een adres, een
  openingstijd) niet in de feedback staat, luidt de suggestie dat die informatie ontbreekt en
  toegevoegd moet worden — niet wat die informatie zou moeten zijn.

## Aantallen

Niet opslaan. Geen "14 van de 16" in de tekst van een oorzaak of suggestie. De app telt
ze uit `feedback[]`.

## Velden

- `id` van een pagina is een korte slug: kleine letters, koppeltekens, geen spaties
  (`paspoort-aanvragen`).
- `id` van een feedbackitem is `f001`, `f002`, ... doorlopend over de hele dataset, elk id
  één keer.
- `beantwoord` is `true` of `false`, niet "ja"/"nee".
- `samenvatting` is één zin: de belangrijkste oorzaak voor die pagina.
- `meta.is_voorbeelddata` is `false` bij echte data.
- Vul `periode` (eerste t/m laatste datum in de export), `export_datum` en `analyse_datum`
  (vandaag) in. `bron` is "Mopinion". `onderwerp` is het thema van de pagina's.
- Neem `disclaimer` letterlijk over uit het voorbeeld hieronder.

# Vorm van het antwoord

Geef alleen het JSON-object terug, in één codeblok. Geen inleiding, geen uitleg, geen
samenvatting eromheen.

```json
{
  "meta": {
    "is_voorbeelddata": false,
    "bron": "Mopinion",
    "periode": "1 mei 2026 t/m 31 augustus 2026",
    "export_datum": "2026-09-15",
    "analyse_datum": "2026-09-15",
    "onderwerp": "Reisdocumenten (paspoort en identiteitskaart)",
    "disclaimer": "De oorzaken en verbetersuggesties op deze pagina zijn door AI gegenereerd op basis van de onderstaande feedback. Ze zijn niet gecontroleerd op feitelijke juistheid en zijn geen redactioneel besluit."
  },
  "paginas": [
    {
      "id": "korte-slug",
      "titel": "Titel van de pagina",
      "url": "https://...",
      "samenvatting": "één zin: de belangrijkste oorzaak",
      "oorzaken": [
        {
          "titel": "Wat de lezer mist",
          "toelichting": "Twee of drie zinnen over waarom dit mensen raakt.",
          "citaat_ids": ["f003", "f011"],
          "suggesties": ["Concrete actie op deze pagina.", "Nog een."]
        }
      ]
    }
  ],
  "feedback": [
    { "id": "f001", "pagina": "korte-slug", "beantwoord": false, "tekst": "letterlijk zoals geschreven" }
  ]
}
```

# Controleer dit vóór je antwoordt

Loop deze lijst na en herstel wat niet klopt. Kom je er niet uit, zeg dan wat er misgaat in
plaats van het te verbergen.

1. Elk `citaat_id` bestaat in `feedback[]` en hoort bij dezelfde pagina als de oorzaak.
2. Elke oorzaak heeft minimaal twee citaat_ids en minimaal één suggestie.
3. Elke pagina heeft twee, drie of vier oorzaken.
4. Geen enkel feedback-id komt twee keer voor; elke `pagina` in `feedback[]` bestaat in
   `paginas[]`; geen lege teksten.
5. Elke tekst in `feedback[]` komt letterlijk (of als correcte inkorting) uit de export.
6. Geen e-mailadres, telefoonnummer, postcode, naam of adres in een tekst.
7. Het geheel is geldige JSON.
````

## Grote export

Past de export niet in één keer? Draai de prompt dan per pagina of per groep pagina's en
plak de stukken zelf aan elkaar: één `meta`, alle `paginas` achter elkaar, alle `feedback`
achter elkaar. Let op dat de feedback-ids over het geheel uniek blijven — hernummer de
tweede batch naar `f101`, `f102`, ... als het model opnieuw bij `f001` begint. `controle.py`
vangt dubbele ids af.

## Wat je met het antwoord doet

1. Vervang in `index.html` het hele blok
   `<script id="feedforward-data" type="application/json">…</script>` door het JSON-object.
   De `<script>`-tags blijven staan, alleen de inhoud gaat eruit.
2. Pas de gele balk bovenaan `index.html` aan zodra het om echte data gaat.
3. `python3 controle.py` — moet zonder fouten doorlopen. Dit is dezelfde controle als punt
   1 t/m 6 hierboven, maar dan onverbiddelijk.
4. Steekproef: kies vijf citaten uit de app en zoek ze terug in de export. Eén mismatch
   betekent: analyse opnieuw, niet handmatig repareren.
5. Bij echte data: lees alle citaten na op herleidbaarheid.

Een model dat zijn eigen werk controleert, is geen controle. Stap 3 en 4 sla je niet over.
