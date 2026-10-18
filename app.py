import datetime
import json
import os
import random
from PIL import Image, ImageDraw
import streamlit as st

# ==============================================================================
# 1. SEITEN-KONFIGURATION & SETUP
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Trainer BW",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🩺 MFA Abschlussprüfung BW – Komplex- & Bildfälle")
st.caption(
    "Prüfungsnaher Simulator für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)"
)

# Robuste absolute Pfadberechnung
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "fragen.json")


@st.cache_data
def load_questions():
    """Lädt die Rohdaten aus der fragen.json."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Fehler beim Lesen der 'fragen.json': {e}")
            return get_fallback_questions()
    else:
        return get_fallback_questions()


def get_fallback_questions():
    return [
        {
            "lf": "LF 1",
            "q": "Welches Schmerzzeichen deutet typischerweise auf eine Appendizitis hin?",
            "options": [
                "Kontralateraler Loslassschmerz (Blumberg-Zeichen)",
                "Homans-Zeichen",
                "Mundwinkelasymmetrie",
                "Pupillendifferenz",
            ],
            "correct": "Kontralateraler Loslassschmerz (Blumberg-Zeichen)",
            "exp": "Das Blumberg-Zeichen deutet auf eine Peritonealreizung hin.",
        }
    ]


ALL_QUESTIONS = load_questions()

# Navigation
st.sidebar.header("🎯 Navigation")
mode = st.sidebar.radio(
    "Lernform wählen:",
    [
        "🖼️ Bild- & Komplexaufgaben (Prüfungsnah)",
        "🎲 Dynamische Generatoren",
        "🩸 Laborwert-Diagnostiker",
        "🔄 Zuordnungs-Trainer",
        "✏️ Freitext-Trainer",
        "📝 Musterklausur",
        "📚 Gesamter Fragenkatalog",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric("📋 Geladene Fragen", len(ALL_QUESTIONS))

# Helper-Funktion zum Mischen von Optionen ohne Cache-Probleme
def get_shuffled_options(options_list, key_identifier):
    """Mische Optionen für eine spezifische Frage und speichere sie pro Session."""
    state_key = f"shuffled_opt_{key_identifier}"
    if state_key not in st.session_state:
        opts = list(options_list)
        random.shuffle(opts)
        st.session_state[state_key] = opts
    return st.session_state[state_key]


# ==============================================================================
# 2. BILD-GENERATOREN
# ==============================================================================


def create_urine_strip_image():
    img = Image.new("RGB", (320, 480), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    draw.rectangle([110, 20, 190, 460], fill="#E2E8F0", outline="#94A3B8")

    fields = [
        ("LEU (Leukozyten)", "#8B5CF6"),
        ("NIT (Nitrit)", "#EC4899"),
        ("PRO (Protein)", "#FACC15"),
        ("GLU (Glukose)", "#10B981"),
        ("BLO (Erythrozyten)", "#F97316"),
    ]

    y_start = 40
    for name, color in fields:
        draw.rectangle(
            [125, y_start, 175, y_start + 40], fill=color, outline="#475569"
        )
        draw.text((190, y_start + 12), name, fill="#1E293B")
        y_start += 80
    return img


def create_ekg_image():
    img = Image.new("RGB", (600, 280), color="#FFF5F5")
    draw = ImageDraw.Draw(img)
    for x in range(0, 600, 20):
        draw.line([(x, 0), (x, 280)], fill="#FED7D7", width=1)
    for y in range(0, 280, 20):
        draw.line([(0, y), (600, y)], fill="#FED7D7", width=1)

    points = [
        (20, 180),
        (60, 180),
        (70, 190),
        (80, 180),
        (90, 180),
        (100, 210),
        (110, 80),
        (120, 230),
        (130, 110),
        (180, 110),
        (210, 180),
        (260, 180),
        (270, 190),
        (280, 180),
        (290, 180),
        (300, 210),
        (310, 80),
        (320, 230),
        (330, 110),
        (380, 110),
        (410, 180),
        (580, 180),
    ]
    draw.line(points, fill="#DC2626", width=3)
    draw.text((20, 15), "12-Kanal-EKG (Ableitung II) - Notfall", fill="#991B1B")
    return img


def create_au_form_image():
    img = Image.new("RGB", (520, 320), color="#F0FDF4")
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 510, 310], fill="#DCFCE7", outline="#16A34A", width=2)
    draw.text((20, 20), "Muster 1: Arbeitsunfähigkeitsbescheinigung", fill="#15803D")

    draw.rectangle([30, 55, 160, 85], outline="#16A34A")
    draw.text((35, 63), "[X] Erstbescheinigung", fill="#166534")

    draw.rectangle([180, 55, 310, 85], outline="#16A34A")
    draw.text((185, 63), "[ ] Folgebescheinigung", fill="#166534")

    draw.text((30, 105), "Diagnose (ICD-10-Schlüssel):", fill="#166534")
    draw.rectangle([30, 125, 490, 165], fill="#FFFFFF", outline="#16A34A")
    draw.text((40, 138), "N39.0 G (Harnwegsinfektion, Lokalisation nicht näher bezeichnet)", fill="#0F172A")

    draw.text((30, 185), "Arbeitsunfähig seit: 14.10.2026", fill="#166534")
    draw.text((30, 210), "Voraussichtlich bis: 20.10.2026", fill="#166534")
    draw.text((30, 235), "Festgestellt am: 14.10.2026", fill="#166534")
    return img


def create_impfpass_image():
    img = Image.new("RGB", (520, 320), color="#FEF3C7")
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 510, 310], fill="#FFFBEB", outline="#D97706", width=2)
    draw.text((20, 20), "INTERNATIONALER IMPFAUSWEIS - Tetanus/Diphtherie/Pertussis", fill="#B45309")

    draw.rectangle([30, 60, 490, 280], outline="#D97706")
    draw.text((40, 75), "Datum       | Impfstoff / Ch.-B.       | Arzt / Stempel", fill="#B45309")
    draw.line([(30, 95), (490, 95)], fill="#D97706")

    draw.text((40, 110), "12.05.2005  | Td-PUR (Ch. 40221)      | Dr. Med. Fischer", fill="#1E293B")
    draw.text((40, 140), "18.06.2005  | Td-PUR (Ch. 41102)      | Dr. Med. Fischer", fill="#1E293B")
    draw.text((40, 170), "20.07.2006  | Td-PUR (Ch. 45091)      | Dr. Med. Fischer", fill="#1E293B")
    draw.text((40, 200), "15.09.2013  | TdaP-IMMUN (Ch. 8812)   | Dr. Med. Fischer", fill="#1E293B")
    draw.text((40, 240), "[Letzte Eintragung vor über 12 Jahren]", fill="#DC2626")
    return img


def create_nadelstich_image():
    img = Image.new("RGB", (520, 300), color="#EFF6FF")
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 510, 290], fill="#DBEAFE", outline="#2563EB", width=2)
    draw.text((20, 20), "UNFALLANZEIGE / UNFALLMELDEBOGEN (BGW)", fill="#1E40AF")

    draw.rectangle([30, 55, 490, 260], fill="#FFFFFF", outline="#2563EB")
    draw.text((40, 70), "Unfallhergang: Nadelstichverletzung nach venöser Blutentnahme", fill="#1E293B")
    draw.text((40, 100), "Verletzte Person: MFA Auszubildende (17 Jahre)", fill="#1E293B")
    draw.text((40, 130), "Indexpatient: Bekannter Hepatitis-B-Träger", fill="#DC2626")
    draw.text((40, 160), "Erstmaßnahme: Wundblutung angeregt, Desinfektion (5 Min.)", fill="#1E293B")
    draw.text((40, 190), "Zuständige BG: Berufsgenossenschaft für Gesundheitsdienst (BGW)", fill="#1E40AF")
    return img


# ==============================================================================
# 3. KOMPLEXE PRÜFUNGS-FALLBEISPIELE (DATENBANK)
# ==============================================================================
IMAGE_CASE_STUDIES = [
    {
        "id": "fall_1",
        "title": "Fallbeispiel 1: Urindiagnostik & Abrechnung bei HWI (LF 2 & LF 4)",
        "generator": create_urine_strip_image,
        "caption": "Abb. 1: Ausgewerteter Urin-Teststreifen aus der Hausarztpraxis.",
        "scenario": """
        **Patientenanamnese & Befund:**
        Frau Schneider (42 Jahre, GKV-versichert) stellt sich in der Praxis vor. Sie klagt seit zwei Tagen über brennende Schmerzen beim Wasserlassen (Dysurie) und krampfartige Unterbauchschmerzen. 
        Die MFA führt einen Urinstreifentest mit frischem Morgenurin durch.
        """,
        "questions": [
            {
                "q": "1. Welche Befundkonstellation auf dem Teststreifen ist pathognomonisch für einen bakteriellen Harnwegsinfekt?",
                "options": [
                    "Bilirubin und Urobilinogen positiv",
                    "Leukozyten und Nitrit positiv",
                    "Glukose und Ketone positiv",
                    "Ausschließlich pH-Wert von 8,0",
                ],
                "correct": "Leukozyten und Nitrit positiv",
                "exp": "Leukozyten zeigen die Entzündung der Ableitenden Harnwege; Nitrit entsteht durch die Reduktion von pflanzlichem Nitrat durch nitratreduzierende Bakterien (z. B. E. coli).",
            },
            {
                "q": "2. Aus welchem Grund muss für einen verlässlichen Nitritnachweis zwingend Morgenurin verwendet werden?",
                "options": [
                    "Bakterien benötigen mindestens 4 Stunden Verweilzeit in der Blase zur Nitratumwandlung.",
                    "Der pH-Wert fällt morgens schlagartig unter 4,0.",
                    "Glukose stört nachmittags die Enzymreaktion des Teststreifens.",
                    "Weil der Urin morgens absolut steril sein muss.",
                ],
                "correct": "Bakterien benötigen mindestens 4 Stunden Verweilzeit in der Blase zur Nitratumwandlung.",
                "exp": "Die bakterielle Nitratreduktase benötigt mehrere Stunden Verweilzeit im Blasenurin, um nachweisbare Mengen Nitrit zu bilden.",
            },
            {
                "q": "3. Welcher EBM-GOP-Ziffer rechnet die Praxis für die Durchführung des Urinstreifen-Schnelltests ab?",
                "options": ["EBM 03000", "EBM 32033", "EBM 32001", "EBM 03220"],
                "correct": "EBM 32033",
                "exp": "Die EBM 32033 deckt die Auswertung von Harn-Mehrfach-Teststreifen im Praxislabor ab.",
            },
        ],
    },
    {
        "id": "fall_2",
        "title": "Fallbeispiel 2: Akuter Brustschmerz / Notfallmanagement (LF 1 & LF 2)",
        "generator": create_ekg_image,
        "caption": "Abb. 2: Erstes 12-Kanal-EKG bei Eintreffen des Patienten.",
        "scenario": """
        **Patientenanamnese & Notfall:**
        Herr Kowalski (56 Jahre) betritt bleich und kaltschweißig die Praxis. Er greift sich an die Brust und klagt über Vernichtungsschmerz mit Ausstrahlung in den Unterkiefer und den linken Arm. 
        Die MFA schreibt sofort ein 12-Kanal-EKG.
        """,
        "questions": [
            {
                "q": "1. Welche Befundveränderung zeigt das EKG im Kurvenverlauf?",
                "options": [
                    "Verlängerung der PQ-Zeit über 0,22 Sekunden",
                    "Signifikante ST-Streckenhebung (STEMI)",
                    "Vollständiges Fehlen von P-Zacken bei absoluter Arrhythmie",
                    "Schenkelblock mit sägezahnartigen Flatterwellen",
                ],
                "correct": "Signifikante ST-Streckenhebung (STEMI)",
                "exp": "Die Hebung der ST-Strecke aus dem absteigenden Schenkel der R-Zacke zeigt einen transmuralen Herzinfarkt.",
            },
            {
                "q": "2. Welche Maßnahme steht bei dieser Erstdiagnose an allererster Stelle?",
                "options": [
                    "Unverzügliche Alarmierung des Notarztes (112) und Oberkörperhochlagerung",
                    "Durchführung eines Belastungs-EKGs zur Leistungsmessung",
                    "Beine hochlagern (Schocklage) und Patient alleine ruhen lassen",
                    "Blutentnahme für das Labor abwarten, bevor Maßnahmen ergriffen werden",
                ],
                "correct": "Unverzügliche Alarmierung des Notarztes (112) und Oberkörperhochlagerung",
                "exp": "Bei Verdacht auf STEMI hat die Notrufabsetzung und Herzentlastung durch Oberkörperhochlagerung oberste Priorität.",
            },
            {
                "q": "3. Welcher Laborwert gilt im Kliniklabor als hochspezifischer Goldstandard zum Nachweis von Herzmuskelschäden?",
                "options": ["Troponin T / I", "HbA1c", "Gamma-GT", "Quick-Wert / INR"],
                "correct": "Troponin T / I",
                "exp": "Kardiologisches Troponin T und I steigt bei Herzmuskelnekrosen hochspezifisch an.",
            },
        ],
    },
    {
        "id": "fall_3",
        "title": "Fallbeispiel 3: Arbeitsunfähigkeit & Formularkunde Muster 1 (LF 3 & LF 4)",
        "generator": create_au_form_image,
        "caption": "Abb. 3: Vorgelegtes Formular Muster 1.",
        "scenario": """
        **Patientenanamnese:**
        Ein GKV-Patient erscheint in der Sprechstunde. Der Arzt stellt eine akute Harnwegsinfektion fest und schreibt den Patienten arbeitsunfähig.
        """,
        "questions": [
            {
                "q": "1. Was bedeutet die Zusatzkennzeichnung 'G' hinter dem ICD-10-Diagnosecode N39.0?",
                "options": [
                    "Ausschluss der Diagnose",
                    "Gesicherte Diagnose",
                    "Verdacht auf Diagnose",
                    "Zustand nach Ausheilung",
                ],
                "correct": "Gesicherte Diagnose",
                "exp": "In der ambulanten Abrechnung steht 'G' für gesichert, 'V' für Verdacht auf, 'A' für Ausschluss und 'Z' für symptomfreien Zustand nach.",
            },
            {
                "q": "2. Unter welcher Bedingung darf eine Rückdatierung des AU-Beginns ausnahmsweise erfolgen?",
                "options": [
                    "Unbegrenzt, wenn der Patient krank war",
                    "Maximal 3 Tage nach eingehender ärztlicher Begründung",
                    "Rückdatierungen sind gesetzlich absolut verboten",
                    "Immer bis zu 14 Tage rückwirkend",
                ],
                "correct": "Maximal 3 Tage nach eingehender ärztlicher Begründung",
                "exp": "Nach den Arbeitsunfähigkeits-Richtlinien ist eine Rückdatierung nur ausnahmsweise und nur bis zu 3 Tage zulässig.",
            },
        ],
    },
    {
        "id": "fall_4",
        "title": "Fallbeispiel 4: Impfmanagement & Tetanus-Schutz (LF 1 & LF 3)",
        "generator": create_impfpass_image,
        "caption": "Abb. 4: Einträge im Impfausweis eines 35-jährigen Patienten.",
        "scenario": """
        **Patientenanamnese:**
        Herr Bauer (35 Jahre) hat sich bei Gartenarbeiten an einem verrosteten Draht eine tiefere Schnittwunde am Unterarm zugezogen. Er legt seinen Impfpass vor.
        """,
        "questions": [
            {
                "q": "1. Wie ist der aktuelle Tetanus-Impfschutz des Patienten laut Ausweis zu beurteilen?",
                "options": [
                    "Ablaufender Schutz: Die letzte Auffrischung liegt über 10 Jahre zurück.",
                    "Perfekt geschützt: Tetanus hält lebenslang nach Grundimmunisierung.",
                    "Kein Schutz: Es liegt überhaupt keine Grundimmunisierung vor.",
                    "Sofortige Quarantäne notwendig.",
                ],
                "correct": "Ablaufender Schutz: Die letzte Auffrischung liegt über 10 Jahre zurück.",
                "exp": "Tetanus-Auffrischimpfungen sind regulär alle 10 Jahre erforderlich. Bei verschmutzten Wunden gilt die Auffrischung bereits ab 5 Jahren.",
            },
            {
                "q": "2. Welche Impfmaßnahme ist bei dieser tiefen, verschmutzten Wunde indiziert?",
                "options": [
                    "Sofortige Auffrischimpfung mit einem Tetanus-Kombinationsimpfstoff (Td / TdaP)",
                    "Keine Impfung notwendig, Wundsalbe reicht aus",
                    "Nur Gabe von Schmerzmitteln",
                    "Ausschließliche Gabe von Penicillin",
                ],
                "correct": "Sofortige Auffrischimpfung mit einem Tetanus-Kombinationsimpfstoff (Td / TdaP)",
                "exp": "Bei Verletzungen und einer Impfung, die länger als 5 Jahre zurückliegt, muss unverzüglich aufgefrischt werden.",
            },
        ],
    },
    {
        "id": "fall_5",
        "title": "Fallbeispiel 5: Nadelstichverletzung & BG-Unfallmeldung (LF 3 & LF 5)",
        "generator": create_nadelstich_image,
        "caption": "Abb. 5: Dokumentation der Unfallanzeige im Praxislabor.",
        "scenario": """
        **Unfallereignis:**
        Eine 17-jährige MFA-Auszubildende sticht sich nach einer Blutentnahme versehentlich an einer gebrauchten Kanüle in den Finger. Der Patient ist als Hepatitis-B-Träger bekannt.
        """,
        "questions": [
            {
                "q": "1. Welche Sofortmaßnahme muss direkt an der Einstichstelle durchgeführt werden?",
                "options": [
                    "Blutung anregen (nicht quetschen) und gründlich desinfizieren/spülen",
                    "Wunde sofort fest abbinden und abwarten",
                    "Wunde mit Eisspray kühlen und weiterarbeiten",
                    "Einstichstelle tief aufschneiden",
                ],
                "correct": "Blutung anregen (nicht quetschen) und gründlich desinfizieren/spülen",
                "exp": "Der Blutfluss schwemmt Erreger aus. Quetschen ist verboten, da Gewebe geschädigt wird und Erreger tiefer ins Gewebe gedrückt werden.",
            },
            {
                "q": "2. Welcher Arzt muss nach einer Nadelstichverletzung im Betrieb zwingend aufgesucht werden?",
                "options": [
                    "Durchgangsarzt (D-Arzt)",
                    "Amtsarzt des Gesundheitsamts",
                    "Zahnarzt",
                    "Radiologe",
                ],
                "correct": "Durchgangsarzt (D-Arzt)",
                "exp": "Arbeits- und Wegeunfälle müssen zur Absicherung über die Berufsgenossenschaft durch den D-Arzt dokumentiert werden.",
            },
            {
                "q": "3. Welche Körperschaft ist der Träger der gesetzlichen Unfallversicherung für Arztpraxen?",
                "options": [
                    "BGW (Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege)",
                    "AOK Baden-Württemberg",
                    "Deutsche Rentenversicherung Bund",
                    "Kassenärztliche Vereinigung (KV)",
                ],
                "correct": "BGW (Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege)",
                "exp": "Die BGW ist die zuständige Berufsgenossenschaft für medizinische und pflegerische Berufe.",
            },
        ],
    },
]

# ==============================================================================
# 4. HELPER-FUNKTIONEN FÜR ANDERE MODI
# ==============================================================================


def generate_naegele_task():
    start_date = datetime.date(2025, 1, 1)
    lmp = start_date + datetime.timedelta(days=random.randint(1, 300))
    cycle_length = random.choice([25, 26, 27, 28, 29, 30, 31, 32, 35])
    edd_base = lmp + datetime.timedelta(days=7 + (cycle_length - 28))

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
    base_price = round(random.uniform(10.0, 120.0), 2)
    factor = random.choice([1.0, 1.15, 1.8, 2.3, 3.5])
    return {
        "base": base_price,
        "factor": factor,
        "total": round(base_price * factor, 2),
    }


def generate_lab_value():
    labs = [
        {
            "parameter": "HbA1c",
            "unit": "%",
            "norm": "4.0 - 6.0 %",
            "val": round(random.uniform(4.5, 11.0), 1),
            "low_thresh": 4.0,
            "high_thresh": 6.0,
            "diag_high": "Verdacht auf / Schlecht eingestellten Diabetes mellitus",
            "diag_low": "Physiologisch / Selten Hypoglykämie-Neigung",
        },
        {
            "parameter": "Kalium",
            "unit": "mmol/l",
            "norm": "3.5 - 5.0 mmol/l",
            "val": round(random.uniform(2.8, 6.8), 1),
            "low_thresh": 3.5,
            "high_thresh": 5.0,
            "diag_high": "Hyperkalämie (Gefahr von Herzrhythmusstörungen)",
            "diag_low": "Hypokalämie (z.B. durch Diuretika, Erbrechen)",
        },
    ]
    return random.choice(labs)


MATCHING_TASKS = [
    {
        "title": "Zuordnung: EBM vs. GOÄ Regelungen",
        "items": [
            {"term": "Versichertenpauschale 03000", "correct_cat": "EBM (GKV)"},
            {"term": "Regelhöchstsatz 2,3-fach", "correct_cat": "GOÄ (PKV)"},
            {"term": "Schwellenwert 1,8-fach für Sachleistungen", "correct_cat": "GOÄ (PKV)"},
            {"term": "Chronikerpauschale 03220", "correct_cat": "EBM (GKV)"},
        ],
        "categories": ["EBM (GKV)", "GOÄ (PKV)"],
    }
]

FREETEXT_TASKS = [
    {
        "term": "Naegele-Regel (erweitert)",
        "prompt": "Formel für die erweiterte Naegele-Regel bei abweichender Zykluslänge:",
        "keywords": ["7 tage", "3 monate", "1 jahr", "zyklus"],
        "sample": "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr +/- Abweichung von 28 Tagen",
    }
]

# ==============================================================================
# 5. MODUS-STEUERUNG
# ==============================================================================

if mode == "🖼️ Bild- & Komplexaufgaben (Prüfungsnah)":
    st.header("🖼️ Komplexe Fallbeispiele aus der Praxis")
    st.write(
        "Analysieren Sie die Situation und das Befundbild, um die Prüfungsfragen zu lösen:"
    )

    case_title = st.selectbox(
        "Wählen Sie einen Fall aus:",
        [c["title"] for c in IMAGE_CASE_STUDIES],
    )
    selected_img_case = next(
        c for c in IMAGE_CASE_STUDIES if c["title"] == case_title
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        generated_img = selected_img_case["generator"]()
        st.image(
            generated_img,
            caption=selected_img_case["caption"],
            use_container_width=True,
        )

    with col2:
        st.markdown(selected_img_case["scenario"])
        st.markdown("---")

        for q_idx, q_item in enumerate(selected_img_case["questions"]):
            st.markdown(f"**{q_item['q']}**")

            if "options" in q_item:
                # Optionen dynamsich mischen
                shuffled_opts = get_shuffled_options(q_item["options"], f"{case_title}_{q_idx}")
                user_ans = st.radio(
                    "Antwort wählen:",
                    shuffled_opts,
                    key=f"img_q_{case_title}_{q_idx}",
                )
                if st.button(
                    "Antwort prüfen", key=f"img_btn_{case_title}_{q_idx}"
                ):
                    if user_ans == q_item["correct"]:
                        st.success("✅ Richtig!")
                    else:
                        st.error(f"❌ Falsch. Richtig ist: {q_item['correct']}")
                    st.info(f"**Erklärung:** {q_item['exp']}")
            else:
                st.text_area(
                    "Ihre Antwort:",
                    key=f"img_txt_{case_title}_{q_idx}",
                    height=80,
                )
                with st.expander("💡 Musterlösung anzeigen"):
                    st.markdown(q_item["solution"])

            st.markdown("---")

elif mode == "🎲 Dynamische Generatoren":
    st.header("🎲 Dynamische Rechen- & Fallaufgaben")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Naegele-Regel (Gynäkologie)")
        if "naegele" not in st.session_state or st.button(
            "🔄 Neue Naegele-Aufgabe"
        ):
            st.session_state.naegele = generate_naegele_task()
        n_task = st.session_state.naegele
        st.write(f"**Letzte Regel (LMP):** {n_task['lmp']}")
        st.write(f"**Zykluslänge:** {n_task['cycle']} Tage")
        u_date = st.text_input(
            "Entbindungstermin (TT.MM.YYYY):", key="naegele_in"
        )
        if st.button("Termin prüfen"):
            if u_date.strip() == n_task["correct_date"]:
                st.success(f"✅ Richtig! {n_task['correct_date']}")
            else:
                st.error(f"❌ Falsch. Richtig: {n_task['correct_date']}")

    with col2:
        st.subheader("2. GOÄ-Honorare (Abrechnung)")
        if "goae" not in st.session_state or st.button("🔄 Neue GOÄ-Aufgabe"):
            st.session_state.goae = generate_goae_task()
        g_task = st.session_state.goae
        st.write(f"**Einfacher Satz:** {g_task['base']:.2f} €")
        st.write(f"**Steigerungsfaktor:** {g_task['factor']:.2f}")
        u_price = st.number_input(
            "Rechnungsbetrag (€):", step=0.01, format="%.2f", key="goae_in"
        )
        if st.button("GOÄ Betrag prüfen"):
            if abs(u_price - g_task["total"]) < 0.05:
                st.success(f"✅ Korrekt! {g_task['total']:.2f} €")
            else:
                st.error(f"❌ Falsch. Richtig: {g_task['total']:.2f} €")

elif mode == "🩸 Laborwert-Diagnostiker":
    st.header("🩸 Interaktiver Laborwert-Diagnostiker")
    if "lab_task" not in st.session_state or st.button(
        "🔄 Nächster Laborbefund"
    ):
        st.session_state.lab_task = generate_lab_value()
    l_task = st.session_state.lab_task

    st.subheader(f"Laborparameter: {l_task['parameter']}")
    col_a, col_b = st.columns(2)
    col_a.metric("Gemessener Wert", f"{l_task['val']} {l_task['unit']}")
    col_b.metric("Referenzbereich (Norm)", l_task["norm"])

    user_eval = st.radio(
        "Bewertung:",
        ["Erhöht", "Erniedrigt", "Normalbefund"],
        key="lab_eval",
        horizontal=True,
    )
    if st.button("Befund bewerten"):
        correct_eval = (
            "Erhöht"
            if l_task["val"] > l_task["high_thresh"]
            else (
                "Erniedrigt"
                if l_task["val"] < l_task["low_thresh"]
                else "Normalbefund"
            )
        )
        if user_eval == correct_eval:
            st.success(f"✅ Richtig! Wert ist {correct_eval}.")
        else:
            st.error(f"❌ Falsch. Richtig: **{correct_eval}**.")

elif mode == "🔄 Zuordnungs-Trainer":
    st.header("🔄 Zuordnungs-Trainer (Matching)")
    for m_idx, m_task in enumerate(MATCHING_TASKS):
        st.subheader(f"{m_idx+1}. {m_task['title']}")
        user_matches = {}
        for item_idx, item in enumerate(m_task["items"]):
            user_matches[item_idx] = st.selectbox(
                f"Kategorie für **{item['term']}**:",
                m_task["categories"],
                key=f"match_{m_idx}_{item_idx}",
            )
        if st.button("Zuordnungen prüfen", key=f"btn_match_{m_idx}"):
            correct_count = sum(
                1
                for item_idx, item in enumerate(m_task["items"])
                if user_matches[item_idx] == item["correct_cat"]
            )
            if correct_count == len(m_task["items"]):
                st.success("🎉 Perfekt! Alle Zuordnungen stimmen.")
            else:
                st.warning(
                    f"{correct_count} von {len(m_task['items'])} richtig."
                )
        st.markdown("---")

elif mode == "✏️ Freitext-Trainer":
    st.header("✏️ Freitext- & Fachbegriffe-Trainer")
    for idx, ft in enumerate(FREETEXT_TASKS):
        st.subheader(f"Aufgabe {idx+1}: {ft['term']}")
        st.write(ft["prompt"])
        user_txt = st.text_input("Ihre Antwort:", key=f"ft_in_{idx}")
        if st.button("Antwort auswerten", key=f"ft_btn_{idx}"):
            if user_txt.strip():
                found_keywords = [
                    kw for kw in ft["keywords"] if kw in user_txt.lower()
                ]
                if found_keywords:
                    st.success("✅ Kernbegriffe erkannt!")
                else:
                    st.warning("⚠️ Überprüfen Sie Ihre Eingabe.")
                st.info(f"**Musterlösung:** {ft['sample']}")
        st.markdown("---")

elif mode == "📝 Musterklausur":
    st.header("📝 Generierte Musterklausur")
    if not ALL_QUESTIONS:
        st.warning("Keine Fragen vorhanden.")
    else:
        if "exam_questions" not in st.session_state or st.button(
            "🔄 Neue Musterklausur erstellen"
        ):
            # Lösche alte Mischergebnisse beim Erstellen einer neuen Klausur
            for k in list(st.session_state.keys()):
                if k.startswith("shuffled_opt_"):
                    del st.session_state[k]
            st.session_state.exam_questions = random.sample(
                ALL_QUESTIONS, min(10, len(ALL_QUESTIONS))
            )

        exam_q = st.session_state.exam_questions
        form = st.form(key="exam_form_xxl")
        user_answers = {}

        for idx, q in enumerate(exam_q):
            form.markdown(f"**Frage {idx+1} [{q['lf']}]:** {q['q']}")
            shuffled_opts = get_shuffled_options(q["options"], f"exam_{idx}")
            user_answers[idx] = form.radio(
                f"Antworten für Frage {idx+1}:",
                shuffled_opts,
                key=f"ex_{idx}",
                label_visibility="collapsed",
            )
            form.markdown("---")

        submitted = form.form_submit_button("Klausur auswerten")
        if submitted:
            score = sum(
                1
                for idx, q in enumerate(exam_q)
                if user_answers[idx] == q["correct"]
            )
            total = len(exam_q)
            percent = round((score / total) * 100)

            st.subheader(f"Ergebnis: {score} von {total} Punkten ({percent}%)")
            if percent >= 50:
                st.balloons()
                st.success("🎉 Bestanden!")
            else:
                st.error("❌ Nicht bestanden. Bitte wiederholen.")

elif mode == "📚 Gesamter Fragenkatalog":
    st.header("📚 Vollständiger Fragenkatalog")
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
            shuffled_opts = get_shuffled_options(q["options"], f"cat_{q['lf']}_{idx}")
            user_sel = st.radio(
                "Antwort auswählen:", shuffled_opts, key=f"cat_{q['lf']}_{idx}"
            )
            if st.button("Prüfen", key=f"btn_{q['lf']}_{idx}"):
                if user_sel == q["correct"]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch. Richtig: {q['correct']}")
                st.info(f"**Erklärung:** {q['exp']}")
