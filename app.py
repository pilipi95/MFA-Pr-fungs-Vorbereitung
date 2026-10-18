import datetime
import random
import streamlit as st

# ==============================================================================
# 1. SEITEN-KONFIGURATION & SETUP
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Generator BW (Vollversion)",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 MFA Abschlussprüfung BW – XXL Prüfungs-Generator")
st.caption(
    "Interaktiver Simulator für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)."
)

# Session State Initialisierung
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Sidebar Navigation
mode = st.sidebar.radio(
    "Modus wählen:",
    [
        "🎲 Dynamische Generatoren (Naegele, GOÄ, BBiG)",
        "📝 Musterklausur (Zufallsauswahl)",
        "📚 Gesamter Fragenkatalog (LF 1 – 5)",
    ],
)

# ==============================================================================
# 2. DYNAMISCHE AUFGABEN-GENERATOREN
# ==============================================================================


def generate_naegele_task():
    """Generiert eine dynamische Naegele-Aufgabe mit Zufallsdatum und variabler Zykluslänge."""
    start_date = datetime.date(2025, 1, 1)
    random_days = random.randint(1, 300)
    lmp = start_date + datetime.timedelta(days=random_days)
    cycle_length = random.choice([25, 26, 27, 28, 29, 30, 31, 32, 35])

    days_diff = 7 + (cycle_length - 28)
    edd_base = lmp + datetime.timedelta(days=days_diff)

    year = edd_base.year + 1
    month = edd_base.month - 3
    if month <= 0:
        month += 12
        year -= 1

    try:
        correct_edd = datetime.date(year, month, edd_base.day)
    except ValueError:
        correct_edd = datetime.date(year, month, 28)

    return {
        "lmp": lmp.strftime("%d.%m.%Y"),
        "cycle": cycle_length,
        "correct_date": correct_edd.strftime("%d.%m.%Y"),
    }


def generate_goae_task():
    """Generiert eine dynamische GOÄ-Abrechnungsaufgabe."""
    base_price = round(random.uniform(10.0, 120.0), 2)
    factor = random.choice([1.0, 1.15, 1.8, 2.3, 3.5])
    total = round(base_price * factor, 2)
    return {"base": base_price, "factor": factor, "total": total}


def generate_urlaub_task():
    """Generiert eine dynamische Urlaubsanspruchs-Berechnung nach JArbSchG."""
    alter = random.randint(15, 18)
    if alter < 16:
        urlaub = 30
    elif alter < 17:
        urlaub = 27
    elif alter < 18:
        urlaub = 25
    else:
        urlaub = 24

    return {"alter": alter, "urlaub": urlaub}


# ==============================================================================
# 3. KONSOLIDIERTER FRAGENDATENBANK (LF 1 BIS LF 5)
# ==============================================================================
ALL_QUESTIONS = [
    # --- LERNFELD 1: Behandlungsassistenz & Medizinische Fachkunde ---
    {
        "lf": "LF 1",
        "q": "Eine Patientin klagt über stechende Schmerzen im rechten Unterbauch. Welches Schmerzzeichen deutet typischerweise auf eine Appendizitis hin?",
        "options": [
            "Kontralateraler Loslassschmerz (Blumberg-Zeichen)",
            "Positive Homans-Zeichen am Unterschenkel",
            "Mundwinkelasymmetrie und Zungenabweichung",
            "Einseitige Schwellung und Rötung der Fußsohle",
        ],
        "correct": "Kontralateraler Loslassschmerz (Blumberg-Zeichen)",
        "exp": "Das Blumberg-Zeichen (Loslassschmerz nach Druck auf den linken Unterbauch) ist ein klassisches Indiz für eine Reizung des Peritoneums bei Appendizitis.",
    },
    {
        "lf": "LF 1",
        "q": "Wie wird der voraussichtliche Geburtstermin berechnet, wenn die Patientin einen regelmäßigen Zyklus von 30 Tagen angibt?",
        "options": [
            "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr + 2 Tage",
            "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr - 2 Tage",
            "1. Tag der letzten Regel + 14 Tage - 3 Monate + 1 Jahr",
            "1. Tag der letzten Regel + 7 Tage - 4 Monate + 1 Jahr",
        ],
        "correct": "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr + 2 Tage",
        "exp": "Bei einem 30-Tage-Zyklus werden zur erweiterten Naegele-Regel zusätzlich 2 Tage hinzugerechnet (+2 Tage Abweichung vom 28-Tage-Standard).",
    },
    {
        "lf": "LF 1",
        "q": "Welche Erstreaktion ist bei einem Patienten mit Verdacht auf einen akuten ST-Hebungsinfarkt (STEMI) korrekt?",
        "options": [
            "Notarzt (112) rufen, Oberkörper hochlagern, EKG schreiben, Vitalwerte überwachen",
            "Patienten flach auf den Rücken legen und Beine hochlagern (Schocklage)",
            "Sofortige Durchführung eines Belastungs-EKGs zur Bestätigung",
            "Patienten nach Hause schicken und zur Blutabnahme am Folgetag einbestellen",
        ],
        "correct": "Notarzt (112) rufen, Oberkörper hochlagern, EKG schreiben, Vitalwerte überwachen",
        "exp": "Bei Herzinfarkt gilt Herzentlastung durch Oberkörperhochlagerung, sofortiger Notruf und engmaschige Überwachung (EKG, SpO2, BD).",
    },
    {
        "lf": "LF 1",
        "q": "Welches Symptom gehört zur klassischen Trias des akuten Myokardinfarkts (STEMI)?",
        "options": [
            "Retrosternaler Vernichtungsschmerz, Kaltschweißigkeit und Atemnot",
            "Stechender Schmerz im rechten Unterbauch und Fieber",
            "Einseitige Pupillenerweiterung und Lähmung",
            "Plötzlicher Sehverlust auf beiden Augen",
        ],
        "correct": "Retrosternaler Vernichtungsschmerz, Kaltschweißigkeit und Atemnot",
        "exp": "Der Herzinfarkt zeigt sich klassisch durch Engegefühl (Angina Pectoris), Ausstrahlung in den linken Arm/Kiefer und Kaltschweißigkeit.",
    },
    {
        "lf": "LF 1",
        "q": "Welche EKG-Veränderung ist pathognomonisch für einen akuten ST-Hebungsinfarkt?",
        "options": [
            "ST-Streckenhebung in mindestens zwei korrespondierenden Ableitungen",
            "Verlängerte PQ-Zeit über 0,20 Sekunden",
            "Fehlen von P-Zacken bei absoluter Arrhythmie",
            "Negative T-Welle in allen Ableitungen",
        ],
        "correct": "ST-Streckenhebung in mindestens zwei korrespondierenden Ableitungen",
        "exp": "Eine Hebung der ST-Strecke aus dem absteigenden Schenkel der R-Zacke weist auf einen transmuralen Infarkt hin.",
    },
    {
        "lf": "LF 1",
        "q": "Welche Injektionsart wird gewählt, wenn ein Arzneimittel besonders langsam und gleichmäßig ins Fettgewebe aufgenommen werden soll?",
        "options": [
            "Subkutane Injektion (s.c.)",
            "Intramuskuläre Injektion (i.m.)",
            "Intrakutane Injektion (i.c.)",
            "Intraarterielle Injektion (i.a.)",
        ],
        "correct": "Subkutane Injektion (s.c.)",
        "exp": "Subkutan gespritzte Substanzen (z. B. Heparin, Insulin) werden aus dem gut durchbluteten Fettgewebe langsam resorbiert.",
    },
    {
        "lf": "LF 1",
        "q": "Wann darf eine frische Wunde per primärer Wundnaht verschlossen werden?",
        "options": [
            "Bei glatten, sauberen Wundrändern und einer Verletzungsdauer unter 6 Stunden",
            "Bei stark zerklüfteten und verschmutzten Bisswunden",
            "Bei infizierten Wunden mit eitriger Sekretion",
            "Ausschließlich bei Verletzungen, die älter als 24 Stunden sind",
        ],
        "correct": "Bei glatten, sauberen Wundrändern und einer Verletzungsdauer unter 6 Stunden",
        "exp": "Die primäre Wundheilung erfordert saubere Wundverhältnisse und ein Wundalter unter 6 Stunden (ohne Infektionszeichen).",
    },
    {
        "lf": "LF 1",
        "q": "Wann muss eine Rhesus-Prophylaxe bei einer schwangeren Frau durchgeführt werden?",
        "options": [
            "Rh-negative Mutter mit Rh-positivem Kind in der 28.–30. SSW und < 72h post partum",
            "Rh-positive Mutter mit Rh-negativem Kind direkt nach der Geburt",
            "Bei allen Schwangeren unabhängig vom Rhesusfaktor in der 12. SSW",
            "Nur bei Nachweis von Anti-D-Antikörpern im mütterlichen Blut",
        ],
        "correct": "Rh-negative Mutter mit Rh-positivem Kind in der 28.–30. SSW und < 72h post partum",
        "exp": "Anti-D-Immunglobulin verhindert die Sensibilisierung der Rhesus-negativen Mutter gegen Rh-positive fötale Erythrozyten.",
    },
    {
        "lf": "LF 1",
        "q": "Was unterscheidet Asthma bronchiale klinisch von einer COPD?",
        "options": [
            "Asthma zeigt eine reversible Atemwegsobstruktion; COPD ist weitgehend irreversibel und progredient",
            "COPD tritt nur bei Kindern auf; Asthma nur im Alter",
            "Asthma wird mit Antibiotika geheilt; COPD durch Impfungen",
            "Bei COPD gibt es keine Atemnot bei Belastung",
        ],
        "correct": "Asthma zeigt eine reversible Atemwegsobstruktion; COPD ist weitgehend irreversibel und progredient",
        "exp": "Asthma verläuft anfallsartig und ist medikamentös reversibel, während die COPD eine chronisch fortschreitende Einengung zeigt.",
    },

    # --- LERNFELD 2: Praxislabor & Hygiene ---
    {
        "lf": "LF 2",
        "q": "Welche Monovette muss bei der venösen Blutentnahme zwingend als ERSTE entnommen werden, wenn ein kompletter Satz gefordert ist?",
        "options": [
            "Blutkultur (falls angeordnet), gefolgt von Serum / Citrat",
            "EDTA-Monovette für das kleine Blutbild",
            "Fluorid-Monovette für Glukose",
            "Die Reihenfolge spielt laborchemisch keine Rolle",
        ],
        "correct": "Blutkultur (falls angeordnet), gefolgt von Serum / Citrat",
        "exp": "Blutkulturen stehen wegen Kontaminationsgefahr an erster Stelle. EDTA darf nie vor Serum oder Citrat gezogen werden (Verschleppung von K-EDTA).",
    },
    {
        "lf": "LF 2",
        "q": "Aus welchem Grund ist eine zu lange Venenstauung (> 1 Minute) vor der Blutentnahme unbedingt zu vermeiden?",
        "options": [
            "Hämokonzentration führt zu fälschlicherweise erhöhten Werten von Kalium, Proteinen und Enzymen",
            "Das Blut gerinnt sofort in der Vene und verstopft die Kanüle",
            "Der Blutzuckerspiegel fällt schlagartig ab",
            "Es bildet sich zwingend eine Lungenembolie",
        ],
        "correct": "Hämokonzentration führt zu fälschlicherweise erhöhten Werten von Kalium, Proteinen und Enzymen",
        "exp": "Durch den Flüssigkeitsaustritt ins Gewebe steigen intravasale Zell- und Eiweißkonzentrationen verfälscht an (Kaliumanstieg durch Hämolyse).",
    },
    {
        "lf": "LF 2",
        "q": "Welche Vorbereitung ist für die korrekte Bestimmung von Nitrit im Urin-Teststreifen essenziell?",
        "options": [
            "Verwendung von Morgenurin, der mindestens 4 Stunden in der Blase verweilte",
            "Verwendung von Spontanurin direkt nach der Nahrungsaufnahme",
            "Der Urin muss vor dem Test 10 Minuten lang aufgekocht werden",
            "Es darf ausschließlich Katheterurin genutzt werden",
        ],
        "correct": "Verwendung von Morgenurin, der mindestens 4 Stunden in der Blase verweilte",
        "exp": "Bakterien benötigen ausreichend Verweilzeit in der Blase, um Nitrat aus der Nahrung zu Nitrit zu reduzieren.",
    },
    {
        "lf": "LF 2",
        "q": "Welche Parameter müssen bei der Freigabe eines Dampfsterilisators (Autoklav) nach dem Sterilisationsprozess dokumentiert werden?",
        "options": [
            "Temperatur, Druck, Haltezeit und das Ergebnis des Indikatorstreifens",
            "Nutzungsdauer der Praxisräumlichkeiten und Raumtemperatur",
            "Name des Patienten und seine Versichertennummer",
            "Uhrzeit des Praxisbeginns und Alter der MFA",
        ],
        "correct": "Temperatur, Druck, Haltezeit und das Ergebnis des Indikatorstreifens",
        "exp": "Zur Chargenfreigabe nach RiliBÄK / Hygieneplan gehören Temperatur (z. B. 134 °C), Druck (2 bar), Zeit (5 Min) und Farbumschlag des Prozessindikators.",
    },
    {
        "lf": "LF 2",
        "q": "Warum muss ein Citrat-Röhrchen für die Gerinnungsdiagnostik (Quick/PTT) exakt befüllt werden?",
        "options": [
            "Um das Mischungsverhältnis von 1 Teil Natriumcitrat zu 9 Teilen Blut exakt einzuhalten",
            "Damit das Röhrchen in der Zentrifuge keine Unwucht erzeugt",
            "Weil sonst die Erythrozyten hämolysieren",
            "Damit der pH-Wert des Blutes nicht unter 5,0 fällt",
        ],
        "correct": "Um das Mischungsverhältnis von 1 Teil Natriumcitrat zu 9 Teilen Blut exakt einzuhalten",
        "exp": "Ein abweichendes Mischungsverhältnis verändert die Kalziumbindung und führt zu falsch-langen Gerinnungszeiten.",
    },
    {
        "lf": "LF 2",
        "q": "Was versteht man unter der RiliBÄK im Praxislabor?",
        "options": [
            "Richtlinie der Bundesärztekammer zur Qualitätssicherung laboratoriumsmedizinischer Untersuchungen",
            "Rechtsverordnung über die Abrechnung von Laborleistungen",
            "Richtlinie zur Biologischen Abfallentsorgung in Krankenhäusern",
            "Reichsordnung für Infektionskrankheiten und Bakteriologie",
        ],
        "correct": "Richtlinie der Bundesärztekammer zur Qualitätssicherung laboratoriumsmedizinischer Untersuchungen",
        "exp": "Die RiliBÄK schreibt tägliche Kontrollprobenmessungen und regelmäßige Ringversuche vor.",
    },
    {
        "lf": "LF 2",
        "q": "Wie verhalten Sie sich unmittelbar nach einer Nadelstichverletzung mit einer potenziell kontaminierten Kanüle?",
        "options": [
            "Blutung anregen (nicht quetschen), gründlich desinfizieren/spülen, D-Arzt aufsuchen & Vorfall melden",
            "Wunde sofort mit einem Pflaster abkleben und normal weiterarbeiten",
            "Ein Oral-Antibiotikum einnehmen und die Einstichstelle abbinden",
            "Die Verletzung verschweigen, um Probleme im Betrieb zu vermeiden",
        ],
        "correct": "Blutung anregen (nicht quetschen), gründlich desinfizieren/spülen, D-Arzt aufsuchen & Vorfall melden",
        "exp": "Erste Hilfe durchführen, D-Arzt aufsuchen (Dokumentation & ggf. HIV-Postexpositionsprophylaxe) und Indexpatienten prüfen.",
    },

    # --- LERNFELD 3: Betriebsorganisation, QM & Recht ---
    {
        "lf": "LF 3",
        "q": "Eine 17-jährige Auszubildende arbeitet in einer Arztpraxis. Wie viele Pausenminuten stehen ihr laut JArbSchG bei einer Arbeitszeit von 7,5 Stunden zu?",
        "options": [
            "Mindestens 60 Minuten Ruhepause",
            "Mindestens 30 Minuten Ruhepause",
            "Pausen sind bei Jugendlichen freiwillig",
            "Exakt 15 Minuten am Ende des Arbeitstages",
        ],
        "correct": "Mindestens 60 Minuten Ruhepause",
        "exp": "Nach JArbSchG § 11 stehen Jugendlichen bei einer Arbeitszeit von mehr als 6 Stunden mindestens 60 Minuten Pause zu (bei Erwachsenen 30 Min).",
    },
    {
        "lf": "LF 3",
        "q": "Wann ist ein Kündigungsschreiben im Arbeitsverhältnis rechtlich wirksam?",
        "options": [
            "Sobald es dem Empfänger in schriftlicher Form (mit eigenhändiger Unterschrift) zugeht",
            "Sobald eine E-Mail oder WhatsApp-Nachricht gelesen wurde",
            "Wenn eine mündliche Absichtserklärung unter Zeugen ausgesprochen wird",
            "Ausschließlich nach Bestätigung durch das Arbeitsamt",
        ],
        "correct": "Sobald es dem Empfänger in schriftlicher Form (mit eigenhändiger Unterschrift) zugeht",
        "exp": "Gemäß § 623 BGB bedarf die Kündigung eines Arbeitsverhältnisses zwingend der Schriftform (elektronische Form ist ausgeschlossen).",
    },
    {
        "lf": "LF 3",
        "q": "Welche Maßnahme im Qualitätsmanagement (QM) beschreibt eine 'SOP' (Standard Operating Procedure)?",
        "options": [
            "Eine verbindliche schriftliche Arbeitsanweisung für wiederkehrende Abläufe",
            "Die jährliche Abrechnung mit der Kassenärztlichen Vereinigung",
            "Die Anmeldung eines Arbeitsunfalls bei der Berufsgenossenschaft",
            "Ein Behandlungsfehler-Protokoll zur Einreichung beim Gericht",
        ],
        "correct": "Eine verbindliche schriftliche Arbeitsanweisung für wiederkehrende Abläufe",
        "exp": "Standard Operating Procedures (SOPs) sichern als Standard-Arbeitsanweisungen die Qualitätsstandards in Diagnostik und Verwaltung.",
    },
    {
        "lf": "LF 3",
        "q": "Wofür steht das Akronym PDCA im Qualitätsmanagement einer Arztpraxis?",
        "options": [
            "Plan - Do - Check - Act",
            "Practice - Doctor - Care - Action",
            "Patient - Diagnosis - Cure - Assessment",
            "Prevention - Documentation - Control - Analysis",
        ],
        "correct": "Plan - Do - Check - Act",
        "exp": "Der Deming-Kreislauf beschreibt den kontinuierlichen Verbesserungsprozess im QM.",
    },
    {
        "lf": "LF 3",
        "q": "Ein Ehemann ruft an und bittet um Herausgabe der Befunde seiner volljährigen Ehefrau. Wie reagieren Sie rechtlich korrekt?",
        "options": [
            "Auskunft verweigern, solange keine schriftliche Schweigepflichtentbindung der Ehefrau vorliegt",
            "Die Befunde sofort vorlesen, da Eheleute ein gegenseitiges Auskunftsrecht haben",
            "Auskunft geben, wenn der Ehemann das Geburtsdatum der Frau nennen kann",
            "Den Ehemann an die Krankenkasse verweisen",
        ],
        "correct": "Auskunft verweigern, solange keine schriftliche Schweigepflichtentbindung der Ehefrau vorliegt",
        "exp": "Die ärztliche Schweigepflicht (§ 203 StGB) gilt ausnahmslos auch gegenüber Familienangehörigen.",
    },

    # --- LERNFELD 4: Abrechnungswesen (EBM, GOÄ & UV-GOÄ) ---
    {
        "lf": "LF 4",
        "q": "Unter welcher Voraussetzung kann die EBM-Gebrauchsgebühr für ein Langzeit-EKG (03241 / 18400) abgerechnet werden?",
        "options": [
            "Wenn eine Aufzeichnungsdauer von mindestens 18 Stunden kontinuierlich erfolgt ist",
            "Bereits ab einer Messdauer von 30 Minuten in der Praxis",
            "Nur wenn der Patient während der Messung stationär aufgenommen wurde",
            "Bei jeder normalen EKG-Abrechnung ohne Zeiteinschränkung",
        ],
        "correct": "Wenn eine Aufzeichnungsdauer von mindestens 18 Stunden kontinuierlich erfolgt ist",
        "exp": "Für das Langzeit-EKG fordert der EBM eine kontinuierliche Aufzeichnung von mindestens 18 Stunden.",
    },
    {
        "lf": "LF 4",
        "q": "Ein Privatpatient erhält eine eingehende Beratung (GOÄ-Ziffer 3). Welche Mindestdauer verlangt die Legende der GOÄ?",
        "options": [
            "Mindestens 10 Minuten Dauer",
            "Mindestens 20 Minuten Dauer",
            "Mindestens 5 Minuten Dauer",
            "Es gibt keine zeitliche Mindestvorgabe",
        ],
        "correct": "Mindestens 10 Minuten Dauer",
        "exp": "GOÄ Ziffer 3 definiert eine eingehende Beratung, die mindestens 10 Minuten gedauert haben muss.",
    },
    {
        "lf": "LF 4",
        "q": "Welches Muster kommt zum Einsatz, wenn ein gesetzlich versicherter Patient wegen eines Arbeitsunfalls behandelt werden muss?",
        "options": [
            "Es wird kein GKV-Formular genutzt, die Abrechnung erfolgt über die D-Arzt-Formulare der Berufsgenossenschaft (UV-GOÄ)",
            "Muster 16 (Arzneiverordnungsblatt)",
            "Muster 6 (Überweisungsschein)",
            "Muster 10 (Laboranforderung)",
        ],
        "correct": "Es wird kein GKV-Formular genutzt, die Abrechnung erfolgt über die D-Arzt-Formulare der Berufsgenossenschaft (UV-GOÄ)",
        "exp": "Arbeits- und Wegeunfälle fallen nicht unter die GKV, sondern unter die gesetzliche Unfallversicherung (D-Arzt-Abrechnung nach UV-GOÄ).",
    },
    {
        "lf": "LF 4",
        "q": "Was ist die Voraussetzung für die Abrechnung der EBM-Chronikerpauschale (03220 / 03221)?",
        "options": [
            "Mindestens 2 persönliche Arzt-Patienten-Kontakte in den letzten 4 Quartalen wegen derselben lebensverändernden Erkrankung",
            "Einmaliger Kontakt pro Kalenderjahr bei Patienten über 60 Jahren",
            "Tägliche Blutdruckmessung über einen Zeitraum von 4 Wochen",
            "Ausschließlich die Diagnose Diabetes mellitus Typ 2",
        ],
        "correct": "Mindestens 2 persönliche Arzt-Patienten-Kontakte in den letzten 4 Quartalen wegen derselben lebensverändernden Erkrankung",
        "exp": "Die 4-3-2-1 Regel bestimmt die kontinuierliche Betreuung chronisch Kranker im EBM.",
    },
    {
        "lf": "LF 4",
        "q": "Welcher Schwellenwert (Regelhöchstsatz) gilt in der GOÄ für persönliche ärztliche Leistungen ohne schriftliche Begründung?",
        "options": ["2,3-fach", "1,8-fach", "3,5-fach", "1,0-fach"],
        "correct": "2,3-fach",
        "exp": "Der 2,3-fache Satz ist der Regelhöchstsatz. Überschreitungen bis 3,5-fach erfordern eine schriftliche Begründung auf der Rechnung.",
    },

    # --- LERNFELD 5: Wirtschafts- & Sozialkunde ---
    {
        "lf": "LF 5",
        "q": "Ein 16-jähriger Azubi kauft sich von seinem gesparten Taschengeld ohne Wissen der Eltern ein Fahrrad für 200 €. Ist der Kaufvertrag wirksam?",
        "options": [
            "Ja, der Kaufvertrag ist nach § 110 BGB ('Taschengeldparagraf') von Anfang an wirksam",
            "Nein, Verträge Minderjähriger sind immer absolut nichtig",
            "Der Vertrag wird erst mit Vollendung des 18. Lebensjahres wirksam",
            "Nein, Käufe über 50 € sind für Jugendliche gesetzlich verboten",
        ],
        "correct": "Ja, der Kaufvertrag ist nach § 110 BGB ('Taschengeldparagraf') von Anfang an wirksam",
        "exp": "Wird die Leistung mit Mitteln bewirkt, die dem Minderjährigen zur freien Verfügung überlassen wurden, gilt der Vertrag als von Anfang an wirksam.",
    },
    {
        "lf": "LF 5",
        "q": "Welche Körperschaft ist der Träger der Gesetzlichen Unfallversicherung für medizinische Praxisbetriebe?",
        "options": [
            "Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege (BGW)",
            "Deutsche Rentenversicherung Bund",
            "Kassenärztliche Vereinigung Baden-Württemberg (KVBW)",
            "AOK Baden-Württemberg",
        ],
        "correct": "Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege (BGW)",
        "exp": "Die BGW ist die zuständige Berufsgenossenschaft für nicht-staatliche Einrichtungen im Gesundheitssystem.",
    },
    {
        "lf": "LF 5",
        "q": "Welche Säule der gesetzlichen Sozialversicherung wird zu 100 % vom Arbeitgeber finanziert?",
        "options": [
            "Gesetzliche Unfallversicherung (Berufsgenossenschaft)",
            "Gesetzliche Krankenversicherung",
            "Rentenversicherung",
            "Pflegeversicherung",
        ],
        "correct": "Gesetzliche Unfallversicherung (Berufsgenossenschaft)",
        "exp": "Die Beitragslast der Unfallversicherung trägt allein der Arbeitgeber zur Absicherung von Arbeits- und Wegeunfällen.",
    },
    {
        "lf": "LF 5",
        "q": "In welchem Alter ist eine Person nach dem BGB beschränkt geschäftsunfähig?",
        "options": [
            "Vom vollendeten 7. bis zum vollendeten 18. Lebensjahr",
            "Von der Geburt bis zum 7. Lebensjahr",
            "Ab dem vollendeten 18. Lebensjahr",
            "Ab dem 21. Lebensjahr",
        ],
        "correct": "Vom vollendeten 7. bis zum vollendeten 18. Lebensjahr",
        "exp": "Kinder unter 7 sind geschäftsunfähig, Jugendliche von 7 bis 17 sind beschränkt geschäftsfähig (§ 106 BGB).",
    },
]

# ==============================================================================
# 4. BENUTZEROBERFLÄCHE & STEUERUNG
# ==============================================================================

if mode == "🎲 Dynamische Generatoren (Naegele, GOÄ, BBiG)":
    st.header("🎲 Dynamische Rechen- & Fallaufgaben")
    st.info(
        "Diese Aufgaben generieren bei jedem Klick neue Zufallswerte – perfekt zum Einüben von Rechenwegen!"
    )

    # Generator 1: Naegele
    st.subheader("1. Naegele-Regel (LF 1 - Gynäkologie)")
    if "naegele" not in st.session_state or st.button(
        "🔄 Neue Naegele-Aufgabe"
    ):
        st.session_state.naegele = generate_naegele_task()

    n_task = st.session_state.naegele
    st.write(
        f"**Fallbeispiel:** Der 1. Tag der letzten Regel (LMP) war der **{n_task['lmp']}**."
    )
    st.write(
        f"Die Patientin hat einen regelmäßigen Zyklus von **{n_task['cycle']} Tagen**."
    )

    u_date = st.text_input(
        "Berechnen Sie den voraussichtlichen Entbindungstermin (Format: TT.MM.YYYY):"
    )
    if st.button("Termin prüfen"):
        if u_date.strip() == n_task["correct_date"]:
            st.success(
                f"✅ Richtig! Der errechnete Geburtstermin ist der {n_task['correct_date']}."
            )
        else:
            st.error(
                f"❌ Falsch. Richtig wäre: {n_task['correct_date']}."
            )
            st.info(
                f"**Rechenweg:** {n_task['lmp']} + 7 Tage - 3 Monate + 1 Jahr + ({n_task['cycle']} - 28) Tage."
            )

    st.markdown("---")

    # Generator 2: GOÄ
    st.subheader("2. GOÄ-Honorare (LF 4 - Abrechnung)")
    if "goae" not in st.session_state or st.button("🔄 Neue GOÄ-Aufgabe"):
        st.session_state.goae = generate_goae_task()

    g_task = st.session_state.goae
    st.write(f"Einfacher Gebührensatz der Ziffer: **{g_task['base']:.2f} €**")
    st.write(f"Angewandter Steigerungsfaktor: **{g_task['factor']:.2f}**")

    u_price = st.number_input(
        "Berechnen Sie den Rechnungsbetrag (€):", step=0.01, format="%.2f"
    )
    if st.button("GOÄ Betrag prüfen"):
        if abs(u_price - g_task["total"]) < 0.05:
            st.success(
                f"✅ Korrekt! Der Rechnungsbetrag ist {g_task['total']:.2f} €."
            )
        else:
            st.error(
                f"❌ Falsch. Richtig ist: {g_task['base']:.2f} € × {g_task['factor']} = {g_task['total']:.2f} €."
            )

    st.markdown("---")

    # Generator 3: JArbSchG
    st.subheader("3. Urlaubsanspruch nach JArbSchG (LF 3 / LF 5)")
    if "urlaub" not in st.session_state or st.button(
        "🔄 Neue Urlaubs-Aufgabe"
    ):
        st.session_state.urlaub = generate_urlaub_task()

    u_task = st.session_state.urlaub
    st.write(
        f"**Fallbeispiel:** Ein Auszubildender ist zu Beginn des Kalenderjahres **{u_task['alter']} Jahre** alt."
    )

    u_ans = st.number_input(
        "Wie viele Werktage Mindesturlaub stehen ihm laut JArbSchG pro Jahr zu?",
        step=1,
    )
    if st.button("Urlaub prüfen"):
        if u_ans == u_task["urlaub"]:
            st.success(
                f"✅ Richtig! Mit {u_task['alter']} Jahren stehen ihm mindestens {u_task['urlaub']} Werktage zu."
            )
        else:
            st.error(
                f"❌ Falsch. Der gesetzliche Mindestanspruch beträgt {u_task['urlaub']} Werktage."
            )

elif mode == "📝 Musterklausur (Zufallsauswahl)":
    st.header("📝 Generierte Musterklausur")
    st.write(
        "Es werden zufällig 10 Fragen aus allen 5 Lernfeldern ausgewählt. Viel Erfolg!"
    )

    if "exam_questions" not in st.session_state or st.button(
        "🔄 Neue Musterklausur zusammenstellen"
    ):
        st.session_state.exam_questions = random.sample(
            ALL_QUESTIONS, min(10, len(ALL_QUESTIONS))
        )

    exam_q = st.session_state.exam_questions
    form = st.form(key="exam_form_xxl")
    user_answers = {}

    for idx, q in enumerate(exam_q):
        form.markdown(f"**Frage {idx+1} [{q['lf']}]:** {q['q']}")
        user_answers[idx] = form.radio(
            f"Antworten für Frage {idx+1}:",
            q["options"],
            key=f"ex_{idx}",
            label_visibility="collapsed",
        )
        form.markdown("---")

    submitted = form.form_submit_button("Klausur auswerten")

    if submitted:
        score = 0
        total = len(exam_q)

        for idx, q in enumerate(exam_q):
            if user_answers[idx] == q["correct"]:
                score += 1

        percent = round((score / total) * 100)
        st.subheader(f"Ergebnis: {score} von {total} Punkten ({percent}%)")

        if percent >= 50:
            st.balloons()
            st.success("🎉 Bestanden! Hervorragendes Ergebnis.")
        else:
            st.error(
                "❌ Leider nicht bestanden (unter 50 %). Nutzen Sie den Fragenkatalog zum gezielten Wiederholen."
            )

elif mode == "📚 Gesamter Fragenkatalog (LF 1 – 5)":
    st.header("📚 Vollständiger Fragenkatalog")
    st.write("Wählen Sie ein Lernfeld aus, um alle verfügbaren Prüfungsfragen gezielt zu üben:")

    lf_filter = st.selectbox(
        "Lernfeld filtern:",
        ["Alle Lernfelder", "LF 1", "LF 2", "LF 3", "LF 4", "LF 5"],
    )

    filtered = [
        q
        for q in ALL_QUESTIONS
        if lf_filter == "Alle Lernfelder" or q["lf"] == lf_filter
    ]

    for idx, q in enumerate(filtered):
        with st.expander(f"Frage {idx+1} [{q['lf']}]: {q['q']}"):
            user_sel = st.radio(
                "Wählen Sie eine Antwort:",
                q["options"],
                key=f"cat_{q['lf']}_{idx}",
            )
            if st.button("Antwort kontrollieren", key=f"btn_{q['lf']}_{idx}"):
                if user_sel == q["correct"]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch. Richtige Antwort: {q['correct']}")
                st.info(f"**Erklärung:** {q['exp']}")
