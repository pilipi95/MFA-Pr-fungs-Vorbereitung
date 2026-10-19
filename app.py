import datetime
import json
import os
import random
import re
import time
from PIL import Image, ImageDraw
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM DESIGN SYSTEM (HOCHKONTRAST & BARRIEREFREI)
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Trainer PRO BW",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Global Background & Base Text */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Headers im Hauptbereich */
    h1, h2, h3 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
    }

    /* ---------------------------------------------------------------------- */
    /* STYLING FÜR DIE NAVIGATIONSLEISTE (SIDEBAR) - OPTIMALE LESBARKEIT     */
    /* ---------------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #EDF2F7 !important;
        border-right: 2px solid #CBD5E1 !important;
    }

    section[data-testid="stSidebar"] *, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
        margin-bottom: 4px !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
    }

    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: #DBEAFE !important;
        border-color: #2563EB !important;
    }
    
    /* KONTRAST-FIX FÜR TEXTFELDER & EINGABEN IM HAUPTBEREICH */
    textarea, input, select, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #64748B !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    textarea:focus, input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }
    
    label, .stTextArea label, .stTextInput label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* Card Container */
    .mfa-card {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Feedback Containers */
    .feedback-success {
        background-color: #F0FDF4;
        border-left: 5px solid #22C55E;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        color: #14532D !important;
    }
    .feedback-warning {
        background-color: #FEFCE8;
        border-left: 5px solid #EAB308;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        color: #713F12 !important;
    }
    .feedback-error {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        color: #7F1D1D !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Badges */
    .badge-lf {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. DATA LAYER & VOLLSTÄNDIGER KATALOG (LF 1 BIS LF 5)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "fragen.json")


def get_default_questions():
    """Umfassender Prüfungsfragen-Katalog (MFA Baden-Württemberg, LF 1 - LF 5)."""
    return [
        {
            "id": "q1",
            "lf": "LF 1",
            "q": "Eine Patientin klagt über stechende Schmerzen im rechten Unterbauch. Welches Schmerzzeichen bei der Palpation des linken Unterbauchs deutet typischerweise auf eine Appendizitis hin?",
            "sample": "Kontralateraler Loslassschmerz (Blumberg-Zeichen).",
            "keywords": ["blumberg", "loslassschmerz", "kontralateral"],
            "hint": "Denke an den Schmerz, der erst beim plötzlichen Loslassen der Hand auf der Gegenseite auftritt.",
            "exp": "Das Blumberg-Zeichen entsteht durch die plötzliche Entlastung und darauffolgende Erschütterung des gereizten Peritoneums.",
        },
        {
            "id": "q2",
            "lf": "LF 1",
            "q": "Nenne die drei Leitsymptome der klassischen Symptomtrias beim akuten ST-Hebungsinfarkt (STEMI).",
            "sample": "Retrosternaler Vernichtungsschmerz, Kaltschweißigkeit und Atemnot (Dyspnoe).",
            "keywords": ["schmerz", "kaltschweiß", "atemnot"],
            "hint": "Ein Symptom betrifft die Brust, eines die Haut/Schweißdrüsen, eines die Lunge.",
            "exp": "Der STEMI zeigt sich durch Engegefühl/Schmerz (Angina Pectoris), Sympathikusaktivierung (Kaltschweiß) und Ausfall von Auswurfleistung (Dyspnoe).",
        },
        {
            "id": "q3",
            "lf": "LF 1",
            "q": "Wie wird der voraussichtliche Geburtstermin nach der erweiterten Naegele-Regel berechnet, wenn die Patientin einen Zyklus von 31 Tagen angibt?",
            "sample": "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr + 3 Tage (Zyklusabweichung von 28 Tagen).",
            "keywords": ["7 tage", "3 monate", "1 jahr", "3 tage"],
            "hint": "Rechne erst die Grundformel und korrigiere dann die Differenz zum Standardzyklus (28 Tage).",
            "exp": "Die Standardformel lautet: LMP + 7 Tage - 3 Monate + 1 Jahr. Bei einem 31-Tage-Zyklus werden +3 Tage hinzugefügt.",
        },
        {
            "id": "q4",
            "lf": "LF 2",
            "q": "Warum muss ein Citrat-Röhrchen für Gerinnungsuntersuchungen (z. B. Quick, PTT) exakt bis zur Füllmarkierung befüllt werden?",
            "sample": "Um das exakte Mischungsverhältnis von 1 Teil Citrat zu 9 Teilen Blut (1:9) einzuhalten.",
            "keywords": ["1:9", "mischungsverhältnis", "citrat"],
            "hint": "Welches Mengenverhältnis zwischen dem Antikoagulanz und dem Blut ist vorgeschrieben?",
            "exp": "Zuviel oder zuwenig Blut verschiebt das Kalzium-Bindungsverhältnis und führt zu fälschlicherweise verlängerten oder verkürzten Gerinnungszeiten.",
        },
        {
            "id": "q5",
            "lf": "LF 2",
            "q": "Aus welchem Grund ist zur Beseitigung von Blut- und Sekretverschmutzungen auf Arbeitsflächen eine Scheuer-Wisch-Desinfektion einer gezielten Sprühdesinfektion vorzuziehen?",
            "sample": "Die Scheuer-Wisch-Desinfektion gewährleistet eine mechanische Reinigung und verhindert gesundheitsschädliche Aerosolbildung.",
            "keywords": ["mechanisch", "aerosol", "benetzung"],
            "hint": "Denke an das Einatmen von Desinfektionsmitteln und die nötige Krafteinwirkung.",
            "exp": "Sprühdesinfektion verteilt Keime und Chemikalien als Aerosole in der Raumluft und erreicht oft keine vollständige Wischbenetzung.",
        },
        {
            "id": "q6",
            "lf": "LF 2",
            "q": "Warum muss für den verlässlichen Nachweis von Nitrit im Urin bevorzugt Morgenurin verwendet werden?",
            "sample": "Weil Bakterien eine Verweilzeit von mindestens 4 Stunden in der Blase benötigen, um Nitrat zu Nitrit zu reduzieren.",
            "keywords": ["4 stunden", "verweilzeit", "blase", "nitrat"],
            "hint": "Denke an die Dauer, die Bakterien im Blasenurin benötigen, um biochemisch aktiv zu werden.",
            "exp": "Die bakterielle Nitratreduktase benötigt mehrere Stunden Verweilzeit im Blasenurin, um nachweisbare Mengen Nitrit zu bilden.",
        },
        {
            "id": "q7",
            "lf": "LF 3",
            "q": "Ein Ehemann bittet telefonisch um Übermittlung der Laborbefunde seiner volljährigen Ehefrau. Wie ist rechtlich korrekt zu handeln?",
            "sample": "Die Auskunft muss verweigert werden, solange keine schriftliche Schweigepflichtentbindung der Ehefrau vorliegt.",
            "keywords": ["schweigepflicht", "entbindung", "verweigern"],
            "hint": "Gilt die ärztliche Schweigepflicht auch gegenüber Verwandten und Ehepartnern?",
            "exp": "Gemäß § 203 StGB gilt die Schweigepflicht absolut – auch gegenüber Familienangehörigen, sofern keine Vollmacht vorliegt.",
        },
        {
            "id": "q8",
            "lf": "LF 3",
            "q": "Welche Stelle muss nach einer betrieblichen Nadelstichverletzung zur Unfallaufnahme aufgesucht werden und wer ist Kostenträger?",
            "sample": "Vorstellung beim Durchgangsarzt (D-Arzt). Kostenträger ist die Berufsgenossenschaft (BGW).",
            "keywords": ["d-arzt", "durchgangsarzt", "bgw"],
            "hint": "Suche nach dem Facharzt für Arbeitsunfälle und der speziellen BG für Gesundheitsdienst.",
            "exp": "Arbeitsunfälle fallen nicht unter die GKV, sondern werden über den D-Arzt bei der Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege (BGW) abgewickelt.",
        },
        {
            "id": "q9",
            "lf": "LF 4",
            "q": "Welche Voraussetzungen müssen erfüllt sein, damit die EBM-Chronikerpauschale (GOP 03220) abgerechnet werden darf?",
            "sample": "Mindestens 2 persönliche Arzt-Patienten-Kontakte in den letzten 4 Quartalen wegen derselben chronischen Erkrankung.",
            "keywords": ["kontakte", "quartale", "chronisch"],
            "hint": "Erinnere dich an die Regelung bezüglich Kontakten pro Jahr/Quartalen.",
            "exp": "Für die Chronikerpauschale fordert der EBM den kontinuierlichen Nachweis der Betreuung über mindestens ein Jahr mit mind. 2 persönlichen Kontakten.",
        },
        {
            "id": "q10",
            "lf": "LF 4",
            "q": "Bis zu welchem Schwellenwert (Regelhöchstsatz) dürfen persönliche ärztliche Leistungen nach der GOÄ ohne schriftliche Begründung berechnet werden?",
            "sample": "Bis zum 2,3-fachen Gebührensatz.",
            "keywords": ["2,3", "regelhöchstsatz"],
            "hint": "Wie lautet der Multiplikator für die Regelspanne im Privatbereich?",
            "exp": "Der 2,3-fache Satz ist der Regelhöchstsatz. Höhere Faktoren bis 3,5-fach verlangen eine medizinische Begründung auf der Rechnung.",
        },
        {
            "id": "q11",
            "lf": "LF 4",
            "q": "Was bedeutet die Zusatzkennzeichnung 'G' hinter einem ICD-10-Diagnosecode im ambulanten Bereich?",
            "sample": "G steht für 'Gesicherte Diagnose'.",
            "keywords": ["gesichert", "gesicherte diagnose"],
            "hint": "Unterscheide zwischen gesichert, Verdacht, Ausschluss und symptomfreiem Zustand.",
            "exp": "In der ambulanten Abrechnung steht 'G' für gesichert, 'V' für Verdacht auf, 'A' für Ausschluss und 'Z' für symptomfreien Zustand nach.",
        },
        {
            "id": "q12",
            "lf": "LF 5",
            "q": "Ein 16-jähriger Auszubildender kauft von seinem ersparten Geld ein Tablet für 300 €. Welcher Paragraf des BGB regelt die Wirksamkeit dieses Kaufs?",
            "sample": "§ 110 BGB ('Taschengeldparagraf').",
            "keywords": ["110", "taschengeld"],
            "hint": "Wie heißt die Ausnahmeregelung für beschränkt Geschäftsfähige?",
            "exp": "Nach § 110 BGB ist ein Vertrag ohne Zustimmung der Eltern wirksam, wenn der Minderjährige die Leistung mit Mitteln bewirkt, die ihm zur freien Verfügung überlassen wurden.",
        },
    ]


@st.cache_data
def load_all_questions():
    questions = []
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                questions = json.load(f)
        except Exception:
            questions = get_default_questions()
    else:
        questions = get_default_questions()

    for idx, q in enumerate(questions):
        if "id" not in q or not q["id"]:
            q["id"] = f"q_{idx}_{hash(q.get('q', ''))}"

    return questions


ALL_QUESTIONS = load_all_questions()

if "history" not in st.session_state:
    st.session_state.history = {}
if "exam_active" not in st.session_state:
    st.session_state.exam_active = False


# ==============================================================================
# 3. ADVANCED NLP / SEMANTISCHER EVALUATOR
# ==============================================================================
def evaluate_answer(user_text, keywords, sample_solution):
    """Semantische Evaluierung der Freitextantwort über Schlüsselwörter und Wortstämme."""
    if not user_text or not user_text.strip():
        return 0, [], "empty"

    user_clean = re.sub(r"[^\w\s]", "", user_text.lower())
    found_keywords = []

    for kw in keywords:
        kw_clean = str(kw).lower().strip()
        pattern = re.escape(kw_clean)
        if len(kw_clean) > 3:
            pattern = re.escape(kw_clean[:4])

        if re.search(pattern, user_clean):
            found_keywords.append(kw)

    score = int((len(found_keywords) / len(keywords)) * 100) if keywords else 0
    return score, found_keywords, "evaluated"


# ==============================================================================
# 4. CANVA / CANVAS BILD-GENERATOREN FÜR FALLSTUDIEN
# ==============================================================================
def render_urine_case_image():
    img = Image.new("RGB", (360, 480), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    draw.rectangle([120, 20, 200, 460], fill="#E2E8F0", outline="#94A3B8", width=2)

    fields = [
        ("LEU (Leukozyten)", "#7E22CE"),
        ("NIT (Nitrit)", "#EC4899"),
        ("PRO (Protein)", "#FACC15"),
        ("GLU (Glukose)", "#10B981"),
        ("ERY (Erythrozyten)", "#F97316"),
    ]

    y = 40
    for name, color in fields:
        draw.rectangle([135, y, 185, y + 45], fill=color, outline="#475569")
        draw.text((210, y + 15), name, fill="#0F172A")
        y += 85
    return img


def render_ekg_case_image():
    img = Image.new("RGB", (650, 280), color="#FFF5F5")
    draw = ImageDraw.Draw(img)
    for x in range(0, 650, 25):
        draw.line([(x, 0), (x, 280)], fill="#FCA5A5", width=1)
    for y in range(0, 280, 25):
        draw.line([(0, y), (650, y)], fill="#FCA5A5", width=1)

    points = [
        (20, 180),
        (60, 180),
        (75, 195),
        (85, 180),
        (95, 180),
        (105, 220),
        (115, 60),
        (125, 240),
        (135, 110),
        (190, 110),
        (220, 180),
        (280, 180),
        (295, 195),
        (305, 180),
        (315, 180),
        (325, 220),
        (335, 60),
        (345, 240),
        (355, 110),
        (410, 110),
        (440, 180),
        (630, 180),
    ]
    draw.line(points, fill="#DC2626", width=3)
    draw.text((20, 15), "12-Kanal-EKG Ableitung II - Akut-Befund", fill="#7F1D1D")
    return img


def render_au_form_image():
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
    draw.text(
        (40, 138),
        "N39.0 G (Harnwegsinfektion, Lokalisation nicht näher bezeichnet)",
        fill="#0F172A",
    )
    draw.text((30, 185), "Arbeitsunfähig seit: 14.10.2026", fill="#166534")
    draw.text((30, 210), "Voraussichtlich bis: 20.10.2026", fill="#166534")
    draw.text((30, 235), "Festgestellt am: 14.10.2026", fill="#166534")
    return img


CASE_STUDIES = [
    {
        "id": "cs1",
        "lf": "LF 2 / LF 4",
        "title": "Fallstudie A: Infektiologie & Praxislabor",
        "image_fn": render_urine_case_image,
        "scenario": "**Anamnese:** Frau K. (34 J., GKV) klagt über Dysurie und Pollakisurie seit 2 Tagen. Sie übergeben ihr einen Becher für frischen Morgenurin.",
        "questions": [
            {
                "id": "cs1_q1",
                "q": "Welche zwei Parameter auf dem Teststreifen sichern den Verdacht auf einen bakteriellen Harnwegsinfekt?",
                "sample": "Leukozyten (Entzündungszeichen) und Nitrit (Bakteriennachweis).",
                "keywords": ["leukozyten", "nitrit"],
                "exp": "Leukozyten zeigen die immunologische Reaktion; Nitrit entsteht durch die bakterielle Umwandlung von Nitrat.",
            },
            {
                "id": "cs1_q2",
                "q": "Welche Abrechnungsziffer (EBM) ist für diesen Urinstreifen-Schnelltest anzusetzen?",
                "sample": "EBM-GOP 32033.",
                "keywords": ["32033"],
                "exp": "Die GOP 32033 deckt die Auswertung von Mehrfach-Teststreifen im Ausnahmekatalog ab.",
            },
        ],
    },
    {
        "id": "cs2",
        "lf": "LF 1 / LF 2",
        "title": "Fallstudie B: Kardiologischer Notfall",
        "image_fn": render_ekg_case_image,
        "scenario": "**Anamnese:** Herr M. (58 J.) erscheint unangemeldet mit retrosternalem Vernichtungsschmerz, Kaltschweißigkeit und Atemnot.",
        "questions": [
            {
                "id": "cs2_q1",
                "q": "Welche spezifische EKG-Veränderung liegt in der Ableitung vor?",
                "sample": "Signifikante ST-Streckenhebung (STEMI).",
                "keywords": ["st-hebung", "stemi", "st-streckenhebung"],
                "exp": "Die Hebung der ST-Strecke aus dem absteigenden Schenkel der R-Zacke zeigt den transmuralen Myokardinfarkt.",
            },
            {
                "id": "cs2_q2",
                "q": "Nenne die zwei wichtigsten Erstmaßnahmen der MFA vor Eintreffen des Arztes.",
                "sample": "Notruf 112 absetzen und Oberkörper hochlagern.",
                "keywords": ["112", "notruf", "oberkörper"],
                "exp": "Oberkörperhochlagerung senkt die kardiale Vorlast. Der Notruf sichert das Überleben.",
            },
        ],
    },
    {
        "id": "cs3",
        "lf": "LF 3 / LF 4",
        "title": "Fallstudie C: Formularkunde & Arbeitsunfähigkeit",
        "image_fn": render_au_form_image,
        "scenario": "**Anamnese:** Ein GKV-Patient verlangt nach Feststellung eines HWI eine Arbeitsunfähigkeitsbescheinigung (Muster 1).",
        "questions": [
            {
                "id": "cs3_q1",
                "q": "Was bedeutet der Zusatzbuchstabe 'G' hinter dem ICD-10 Code N39.0 auf dem Formular?",
                "sample": "Gesicherte Diagnose.",
                "keywords": ["gesichert", "gesicherte diagnose"],
                "exp": "Im ambulanten Bereich steht 'G' für eine gesicherte Diagnose.",
            },
            {
                "id": "cs3_q2",
                "q": "Unter welcher Voraussetzung darf der AU-Beginn ausnahmsweise rückdatiert werden?",
                "sample": "Maximal 3 Tage nach eingehender ärztlicher Untersuchung.",
                "keywords": ["3 tage", "ausnahmsweise"],
                "exp": "Nach den AU-Richtlinien ist eine Rückdatierung nur ausnahmsweise und bis zu 3 Tage zulässig.",
            },
        ],
    },
]

# ==============================================================================
# 5. NAVIGATION & APP STRUCTURE
# ==============================================================================
st.sidebar.title("🩺 MFA Trainer PRO")
st.sidebar.markdown("**Lernfeld-Navigator Baden-Württemberg**")

mode = st.sidebar.radio(
    "Modus wählen:",
    [
        "📖 Übungsmodus (Adaptive Recall)",
        "🖼️ Interaktive Bild-Fallstudien",
        "⏱️ Prüfungsmodus (Simulations-Klausur)",
        "📊 Lernfortschritt & Analysen",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Status: 100% Offline-fähig & DSGVO-konform")

# ==============================================================================
# MODUS 1: ÜBUNGSMODUS
# ==============================================================================
if mode == "📖 Übungsmodus (Adaptive Recall)":
    st.header("📖 Übungsmodus: Aktives Erinnern & Verstehen")
    st.caption(
        "Formuliere deine Antworten eigenständig im Freitextfeld. Das System analysiert deine Eingabe."
    )

    lf_filter = st.selectbox(
        "Lernfeld auswählen:",
        ["Alle Lernfelder", "LF 1", "LF 2", "LF 3", "LF 4", "LF 5"],
    )
    questions_pool = [
        q
        for q in ALL_QUESTIONS
        if lf_filter == "Alle Lernfelder" or q.get("lf") == lf_filter
    ]

    if not questions_pool:
        st.warning("Keine Aufgaben für dieses Lernfeld gefunden.")
    else:
        for idx, q in enumerate(questions_pool):
            q_id = q.get("id", f"gen_id_{idx}")
            st.markdown(
                f'<div class="mfa-card"><span class="badge-lf">{q.get("lf", "LF")}</span><h3>Frage {idx+1}: {q["q"]}</h3></div>',
                unsafe_allow_html=True,
            )

            with st.expander("💡 Hinweis / Tipp einblenden"):
                st.info(q.get("hint", "Kein gesonderter Tipp vorhanden."))

            user_ans = st.text_area(
                "Deine Antwort eingeben:", key=f"ans_{q_id}", height=100
            )

            col_a, col_b = st.columns([1, 4])
            if col_a.button("Antwort prüfen", key=f"btn_{q_id}"):
                score, found, status = evaluate_answer(
                    user_ans, q.get("keywords", []), q.get("sample", "")
                )

                st.session_state.history[q_id] = score

                if score >= 80:
                    st.markdown(
                        f'<div class="feedback-success"><b>✅ Hervorragend! ({score}%)</b><br>Erkannte Kernbegriffe: {", ".join(found)}</div>',
                        unsafe_allow_html=True,
                    )
                elif score >= 40:
                    st.markdown(
                        f'<div class="feedback-warning"><b>⚠️ Teilweise korrekt ({score}%)</b><br>Fehlende Schlüsselbegriffe vorhanden. Erkannte Begriffe: {", ".join(found)}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="feedback-error"><b>❌ Unvollständig ({score}%)</b><br>Es wurden keine zentralen Fachbegriffe erkannt.</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(f"**Musterlösung:**\n> {q.get('sample', 'Keine Musterlösung hinterlegt.')}")
                st.info(f"**Fachliche Begründung:** {q.get('exp', '')}")

            st.markdown("---")

# ==============================================================================
# MODUS 2: INTERAKTIVE BILD-FALLSTUDIEN
# ==============================================================================
elif mode == "🖼️ Interaktive Bild-Fallstudien":
    st.header("🖼️ Komplexe Bild- & Praxisfälle")
    st.caption("Prüfungsrelevante Befundanalyse und Fallbeispiele.")

    case_titles = [cs["title"] for cs in CASE_STUDIES]
    selected_title = st.selectbox("Fallstudie wählen:", case_titles)
    cs = next(c for c in CASE_STUDIES if c["title"] == selected_title)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            cs["image_fn"](), caption="Befundunterlage / Dokumentation", use_container_width=True
        )

    with col2:
        st.markdown(cs["scenario"])
        st.markdown("---")

        for q_idx, q in enumerate(cs["questions"]):
            st.subheader(f"Teilaufgabe {q_idx+1}")
            st.write(q["q"])

            c_ans = st.text_area(
                "Lösungsansatz:", key=f"cs_ans_{cs['id']}_{q_idx}", height=80
            )
            if st.button("Teilaufgabe auswerten", key=f"cs_btn_{cs['id']}_{q_idx}"):
                score, found, _ = evaluate_answer(c_ans, q.get("keywords", []), q.get("sample", ""))

                if score >= 70:
                    st.success(f"✅ Korrekt! ({score}%)")
                else:
                    st.error(f"❌ Unvollständig ({score}%)")

                st.markdown(f"**Musterlösung:** {q.get('sample', '')}")
                st.caption(f"Erklärung: {q.get('exp', '')}")
            st.markdown("---")

# ==============================================================================
# MODUS 3: PRÜFUNGSMODUS (SIMULATIONS-KLAUSUR INKL. FALLSTUDIEN)
# ==============================================================================
elif mode == "⏱️ Prüfungsmodus (Simulations-Klausur)":
    st.header("⏱️ Simulations-Prüfung")
    st.caption(
        "Prüfungssimulation unter Zeitdruck: Enthält Wissensfragen & komplexe Fallstudien."
    )

    if not st.session_state.exam_active:
        st.info(
            "Die Simulation besteht aus 4 Wissensfragen sowie 1 komplexe Fallstudie inklusive Befundmaterial. Zeitlimit: 15 Minuten."
        )
        if st.button("🚀 Prüfung jetzt starten"):
            st.session_state.exam_questions = random.sample(
                ALL_QUESTIONS, min(4, len(ALL_QUESTIONS))
            )
            st.session_state.exam_case = random.choice(CASE_STUDIES)
            st.session_state.exam_start_time = time.time()
            st.session_state.exam_active = True
            st.rerun()

    else:
        elapsed = int(time.time() - st.session_state.exam_start_time)
        remaining = max(0, 900 - elapsed)

        col_time, col_prog = st.columns([1, 3])
        col_time.metric(
            "Verbleibende Zeit", f"{remaining // 60}:{remaining % 60:02d} Min"
        )
        col_prog.progress(min(1.0, elapsed / 900))

        if remaining == 0:
            st.error("⏰ Die Zeit ist abgelaufen! Bitte reiche deine Antworten ein.")

        exam_answers = {}

        # TEIL 1: WISSENSFRAGEN
        st.markdown("---")
        st.subheader("Teil A: Wissensfragen")
        for idx, q in enumerate(st.session_state.exam_questions):
            q_id = q.get("id", f"exam_q_{idx}")
            st.markdown(f"**Frage {idx+1} [{q.get('lf', 'LF')}]:** {q['q']}")
            exam_answers[q_id] = st.text_area(
                "Deine Ausarbeitung:", key=f"exam_ans_{q_id}", height=90
            )
            st.markdown("---")

        # TEIL 2: FALLSTUDIE
        st.subheader("Teil B: Komplexe Fallstudie")
        cs = st.session_state.exam_case
        st.markdown(f"**{cs['title']} [{cs.get('lf', 'Praxis')}]**")
        
        col_img, col_scen = st.columns([1, 1])
        with col_img:
            st.image(cs["image_fn"](), caption="Prüfungsdokument / Befund", use_container_width=True)
        with col_scen:
            st.markdown(cs["scenario"])

        for q_idx, q in enumerate(cs["questions"]):
            cs_q_id = q["id"]
            st.markdown(f"**Teilaufgabe B.{q_idx+1}:** {q['q']}")
            exam_answers[cs_q_id] = st.text_area(
                "Lösungsansatz zur Fallstudie:", key=f"exam_ans_{cs_q_id}", height=90
            )
            st.markdown("---")

        if st.button("📥 Gesamte Prüfung abgeben & auswerten"):
            st.session_state.exam_active = False
            total_score = 0
            total_items = len(st.session_state.exam_questions) + len(cs["questions"])

            st.header("📋 Gesamtes Prüfungsergebnis")
            
            st.subheader("Auswertung Teil A: Wissensfragen")
            for idx, q in enumerate(st.session_state.exam_questions):
                q_id = q.get("id", f"exam_q_{idx}")
                u_text = exam_answers.get(q_id, "")
                score, found, _ = evaluate_answer(u_text, q.get("keywords", []), q.get("sample", ""))
                total_score += score

                st.markdown(f"**Frage {idx+1} ({q.get('lf', 'LF')}):** {q['q']}")
                st.write(f"Erreichte Erfüllung: **{score}%**")
                st.write(f"Musterlösung: _{q.get('sample', '')}_")
                st.markdown("---")

            st.subheader("Auswertung Teil B: Fallstudie")
            for q_idx, q in enumerate(cs["questions"]):
                cs_q_id = q["id"]
                u_text = exam_answers.get(cs_q_id, "")
                score, found, _ = evaluate_answer(u_text, q.get("keywords", []), q.get("sample", ""))
                total_score += score

                st.markdown(f"**Teilaufgabe B.{q_idx+1}:** {q['q']}")
                st.write(f"Erreichte Erfüllung: **{score}%**")
                st.write(f"Musterlösung: _{q.get('sample', '')}_")
                st.markdown("---")

            final_percent = total_score / total_items
            st.subheader(f"📊 Gesamtergebnis der Prüfung: {final_percent:.1f}%")

            if final_percent >= 50:
                st.balloons()
                st.success("🎉 Herzlichen Glückwunsch! Du hast die Prüfungssimulation bestanden.")
            else:
                st.error("❌ Das erforderliche Ziel wurde nicht erreicht. Nutze den Übungsmodus zum gezielten Nacharbeiten.")

# ==============================================================================
# MODUS 4: LERNFORTSCHRITT & ANALYSEN
# ==============================================================================
elif mode == "📊 Lernfortschritt & Analysen":
    st.header("📊 Deine Lernstatistik")

    if not st.session_state.history:
        st.info(
            "Nimm am Übungsmodus teil, um Daten für deinen Lernfortschritt zu sammeln."
        )
    else:
        scores = list(st.session_state.history.values())
        avg_score = sum(scores) / len(scores)

        col1, col2, col3 = st.columns(3)
        col1.metric("Bearbeitete Aufgaben", len(scores))
        col2.metric("Durchschnittliche Korrektheit", f"{avg_score:.1f}%")
        col3.metric(
            "Meisterungsgrad", f"{sum(1 for s in scores if s >= 80)} Aufgaben"
        )

        st.subheader("Detailübersicht der Aufgaben")
        for q_id, sc in st.session_state.history.items():
            st.progress(sc / 100)
            st.caption(f"Aufgaben-ID: {q_id} — Erfolgsquote: {sc}%")
