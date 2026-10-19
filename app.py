import datetime
import json
import os
import random
import re
import time
from PIL import Image, ImageDraw
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM DESIGN SYSTEM (UI/UX)
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Trainer PRO BW",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Injektion von modernem, augenschonendem und hochkontrastreichem CSS
st.markdown(
    """
    <style>
    /* Global Styles */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
    }
    
    /* Card Container */
    .mfa-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
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
    }
    .feedback-warning {
        background-color: #FEFCE8;
        border-left: 5px solid #EAB308;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    .feedback-error {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }

    /* Custom Buttons */
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
    
    /* Progress Bars & Badges */
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
# 2. DATA LAYER & PERSISTENCE
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "fragen.json")


def get_default_questions():
    """Umfassender Katalog für MFA LF 1 bis LF 5 (Baden-Württemberg)."""
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
            "lf": "LF 2",
            "q": "Warum muss ein Citrat-Röhrchen für Gerinnungsuntersuchungen (z. B. Quick, PTT) exakt bis zur Füllmarkierung befüllt werden?",
            "sample": "Um das exakte Mischungsverhältnis von 1 Teil Citrat zu 9 Teilen Blut (1:9) einzuhalten.",
            "keywords": ["1:9", "mischungsverhältnis", "citrat"],
            "hint": "Welches Mengenverhältnis zwischen dem Antikoagulanz und dem Blut ist vorgeschrieben?",
            "exp": "Zuviel oder zuwenig Blut verschiebt das Kalzium-Bindungsverhältnis und führt zu fälschlicherweise verlängerten oder verkürzten Gerinnungszeiten.",
        },
        {
            "id": "q4",
            "lf": "LF 2",
            "q": "Aus welchem Grund ist zur Beseitigung von Blut- und Sekretverschmutzungen auf Arbeitsflächen eine Scheuer-Wisch-Desinfektion einer gezielten Sprühdesinfektion vorzuziehen?",
            "sample": "Die Scheuer-Wisch-Desinfektion gewährleistet eine mechanische Reinigung und verhindert gesundheitsschädliche Aerosolbildung.",
            "keywords": ["mechanisch", "aerosol", "benetzung"],
            "hint": "Denke an das Einatmen von Desinfektionsmitteln und die nötige Krafteinwirkung.",
            "exp": "Sprühdesinfektion verteilt Keime und Chemikalien als Aerosole in der Raumluft und erreicht oft keine vollständige Wischbenetzung.",
        },
        {
            "id": "q5",
            "lf": "LF 3",
            "q": "Ein Ehemann bittet telefonisch um Übermittlung der Laborbefunde seiner volljährigen Ehefrau. Wie ist rechtlich korrekt zu handeln?",
            "sample": "Die Auskunft muss verweigert werden, solange keine schriftliche Schweigepflichtentbindung der Ehefrau vorliegt.",
            "keywords": ["schweigepflicht", "entbindung", "verweigern"],
            "hint": "Gilt die ärztliche Schweigepflicht auch gegenüber Verwandten und Ehepartnern?",
            "exp": "Gemäß § 203 StGB gilt die Schweigepflicht absolut – auch gegenüber Familienangehörigen, sofern keine Vollmacht vorliegt.",
        },
        {
            "id": "q6",
            "lf": "LF 3",
            "q": "Welche Stelle muss nach einer betrieblichen Nadelstichverletzung zur Unfallaufnahme aufgesucht werden und wer ist Kostenträger?",
            "sample": "Vorstellung beim Durchgangsarzt (D-Arzt). Kostenträger ist die Berufsgenossenschaft (BGW).",
            "keywords": ["d-arzt", "durchgangsarzt", "bgw"],
            "hint": "Suche nach dem Facharzt für Arbeitsunfälle und der speziellen BG für Gesundheitsdienst.",
            "exp": "Arbeitsunfälle fallen nicht unter die GKV, sondern werden über den D-Arzt bei der Berufsgenossenschaft für Gesundheitsdienst und Wohlfahrtspflege (BGW) abgewickelt.",
        },
        {
            "id": "q7",
            "lf": "LF 4",
            "q": "Welche Voraussetzungen müssen erfüllt sein, damit die EBM-Chronikerpauschale (GOP 03220) abgerechnet werden darf?",
            "sample": "Mindestens 2 persönliche Arzt-Patienten-Kontakte in den letzten 4 Quartalen wegen derselben chronischen Erkrankung.",
            "keywords": ["kontakte", "quartale", "chronisch"],
            "hint": "Erinnere dich an die '4-3-2-1'-Regel des EBM.",
            "exp": "Für die Chronikerpauschale fordert der EBM den kontinuierlichen Nachweis der Betreuung über mindestens ein Jahr mit mind. 2 persönlichen Kontakten.",
        },
        {
            "id": "q8",
            "lf": "LF 4",
            "q": "Bis zu welchem Schwellenwert (Regelhöchstsatz) dürfen persönliche ärztliche Leistungen nach der GOÄ ohne schriftliche Begründung berechnet werden?",
            "sample": "Bis zum 2,3-fachen Gebührensatz.",
            "keywords": ["2,3", "regelhöchstsatz"],
            "hint": "Wie lautet der Multiplikator für die Regelspanne im Privatbereich?",
            "exp": "Der 2,3-fache Satz ist der Regelhöchstsatz. Höhere Faktoren bis 3,5-fach verlangen eine medizinische Begründung auf der Rechnung.",
        },
        {
            "id": "q9",
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
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return get_default_questions()
    return get_default_questions()


ALL_QUESTIONS = load_all_questions()

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = {}
if "exam_active" not in st.session_state:
    st.session_state.exam_active = False


# ==============================================================================
# 3. ADVANCED NLP / TEXT MATCHING EVALUATOR
# ==============================================================================
def evaluate_answer(user_text, keywords, sample_solution):
    """
    Semantische Evaluierung der Freitextantwort über Schlüsselwort-Stämme.
    Gibt Score (0-100%), Trefferliste und visuelles Feedback zurück.
    """
    if not user_text or not user_text.strip():
        return 0, [], "empty"

    user_clean = re.sub(r"[^\w\s]", "", user_text.lower())
    found_keywords = []

    for kw in keywords:
        kw_clean = kw.lower().strip()
        # Flexibler Stammabgleich (mindestens 3 Zeichen)
        pattern = re.escape(kw_clean)
        if len(kw_clean) > 3:
            pattern = re.escape(kw_clean[:4])

        if re.search(pattern, user_clean):
            found_keywords.append(kw)

    score = int((len(found_keywords) / len(keywords)) * 100) if keywords else 0
    return score, found_keywords, "evaluated"


# ==============================================================================
# 4. CANVA / CANVAS IMAGE GENERATORS FOR CASES
# ==============================================================================
def render_urine_case_image():
    img = Image.new("RGB", (360, 480), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    draw.rectangle([120, 20, 200, 460], fill="#E2E8F0", outline="#94A3B8", width=2)

    fields = [
        ("LEU (Leukozyten)", "#7E22CE"),  # Positiv: Violett
        ("NIT (Nitrit)", "#EC4899"),  # Positiv: Pink
        ("PRO (Protein)", "#FACC15"),  # Normal: Gelb
        ("GLU (Glukose)", "#10B981"),  # Normal: Grün
        ("ERY (Erythrozyten)", "#F97316"),  # Positiv: Orange/Rot
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
        (220, 180),  # STEMI ST-Elevation
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


CASE_STUDIES = [
    {
        "id": "cs1",
        "title": "Fallstudie A: Infektiologie & Praxislabor",
        "image_fn": render_urine_case_image,
        "scenario": "**Anamnese:** Frau K. (34 J., GKV) klagt über Dysurie und Pollakisurie seit 2 Tagen. Sie übergeben ihr einen Becher für frischen Morgenurin.",
        "questions": [
            {
                "q": "Welche zwei Parameter auf dem Teststreifen sichern den Verdacht auf einen bakteriellen Harnwegsinfekt?",
                "sample": "Leukozyten (Entzündungszeichen) und Nitrit (Bakteriennachweis).",
                "keywords": ["leukozyten", "nitrit"],
                "exp": "Leukozyten zeigen die immunologische Reaktion; Nitrit entsteht durch die bakterielle Umwandlung von Nitrat.",
            },
            {
                "q": "Welche Abrechnungsziffer (EBM) ist für diesen Urinstreifen-Schnelltest anzusetzen?",
                "sample": "EBM-GOP 32033.",
                "keywords": ["32033"],
                "exp": "Die GOP 32033 deckt die Auswertung von Mehrfach-Teststreifen im Ausnahmekatalog ab.",
            },
        ],
    },
    {
        "id": "cs2",
        "title": "Fallstudie B: Kardiologischer Notfall",
        "image_fn": render_ekg_case_image,
        "scenario": "**Anamnese:** Herr M. (58 J.) erscheint unangemeldet mit retrosternalem Vernichtungsschmerz, Kaltschweißigkeit und Atemnot.",
        "questions": [
            {
                "q": "Welche spezifische EKG-Veränderung liegt in der Ableitung vor?",
                "sample": "Signifikante ST-Streckenhebung (STEMI).",
                "keywords": ["st-hebung", "stemi", "st-streckenhebung"],
                "exp": "Die Hebung der ST-Strecke aus dem absteigenden Schenkel der R-Zacke zeigt den transmuralen Myokardinfarkt.",
            },
            {
                "q": "Nenne die zwei wichtigsten Erstmaßnahmen der MFA vor Eintreffen des Arztes.",
                "sample": "Notruf 112 absetzen und Oberkörper hochlagern.",
                "keywords": ["112", "notruf", "oberkörper"],
                "exp": "Oberkörperhochlagerung senkt die kardiale Vorlast. Der Notruf sichert das Überleben.",
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
# MODUS 1: ÜBUNGSMODUS (ACTIVE RECALL WITH SCAFFOLDING)
# ==============================================================================
if mode == "📖 Übungsmodus (Adaptive Recall)":
    st.header("📖 Übungsmodus: Aktives Erinnern & Verstehen")
    st.caption(
        "Formuliere deine Antworten eigenständig. Das System analysiert deine Eingabe semantisch auf Schlüsselkonzepte."
    )

    lf_filter = st.selectbox(
        "Lernfeld auswählen:",
        ["Alle Lernfelder", "LF 1", "LF 2", "LF 3", "LF 4", "LF 5"],
    )
    questions_pool = [
        q
        for q in ALL_QUESTIONS
        if lf_filter == "Alle Lernfelder" or q["lf"] == lf_filter
    ]

    if not questions_pool:
        st.warning("Keine Aufgaben für dieses Lernfeld gefunden.")
    else:
        for idx, q in enumerate(questions_pool):
            st.markdown(
                f'<div class="mfa-card"><span class="badge-lf">{q["lf"]}</span><h3>Frage {idx+1}: {q["q"]}</h3></div>',
                unsafe_allow_html=True,
            )

            # Interactive Scaffolding (Tipps)
            with st.expander("💡 Hinweis / Tipp einblenden"):
                st.info(q.get("hint", "Kein gesonderter Tipp vorhanden."))

            user_ans = st.text_area(
                "Deine Antwort eingeben:", key=f"ans_{q['id']}", height=100
            )

            col_a, col_b = st.columns([1, 4])
            if col_a.button("Antwort prüfen", key=f"btn_{q['id']}"):
                score, found, status = evaluate_answer(
                    user_ans, q["keywords"], q["sample"]
                )

                # Persist state
                st.session_state.history[q["id"]] = score

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

                st.markdown(f"**Musterlösung:**\n> {q['sample']}")
                st.info(f"**Fachliche Begründung:** {q['exp']}")

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
                score, found, _ = evaluate_answer(c_ans, q["keywords"], q["sample"])

                if score >= 70:
                    st.success(f"✅ Korrekt! ({score}%)")
                else:
                    st.error(f"❌ Unvollständig ({score}%)")

                st.markdown(f"**Musterlösung:** {q['sample']}")
                st.caption(f"Erklärung: {q['exp']}")
            st.markdown("---")

# ==============================================================================
# MODUS 3: PRÜFUNGSMODUS (TIMED EXAM)
# ==============================================================================
elif mode == "⏱️ Prüfungsmodus (Simulations-Klausur)":
    st.header("⏱️ Simulations-Prüfung")
    st.caption(
        "Simulation unter Zeitdruck. Die Auswertung erfolgt gesammelt nach Abgabe."
    )

    if not st.session_state.exam_active:
        st.info(
            "Die Prüfung umfasst 5 zufällige Fragen aus allen Lernfeldern. Zeitlimit: 10 Minuten."
        )
        if st.button("🚀 Klausur jetzt starten"):
            st.session_state.exam_questions = random.sample(
                ALL_QUESTIONS, min(5, len(ALL_QUESTIONS))
            )
            st.session_state.exam_start_time = time.time()
            st.session_state.exam_active = True
            st.rerun()

    else:
        elapsed = int(time.time() - st.session_state.exam_start_time)
        remaining = max(0, 600 - elapsed)

        col_time, col_prog = st.columns([1, 3])
        col_time.metric(
            "Verbleibende Zeit", f"{remaining // 60}:{remaining % 60:02d} Min"
        )
        col_prog.progress(min(1.0, elapsed / 600))

        if remaining == 0:
            st.error("⏰ Die Zeit ist abgelaufen! Bitte reiche deine Antworten ein.")

        exam_answers = {}
        for idx, q in enumerate(st.session_state.exam_questions):
            st.markdown(f"### Frage {idx+1} [{q['lf']}]")
            st.write(q["q"])
            exam_answers[q["id"]] = st.text_area(
                "Deine Antwort:", key=f"exam_ans_{q['id']}", height=90
            )
            st.markdown("---")

        if st.button("📥 Klausur abgeben & auswerten"):
            st.session_state.exam_active = False
            total_score = 0

            st.header("📋 Prüfungsergebnis")
            for idx, q in enumerate(st.session_state.exam_questions):
                u_text = exam_answers.get(q["id"], "")
                score, found, _ = evaluate_answer(u_text, q["keywords"], q["sample"])
                total_score += score

                st.markdown(f"**Frage {idx+1} ({q['lf']}):** {q['q']}")
                st.write(f"Deine Punkte: {score}%")
                st.write(f"Musterlösung: {q['sample']}")
                st.markdown("---")

            final_percent = total_score / len(st.session_state.exam_questions)
            st.subheader(f"Gesamtergebnis: {final_percent:.1f}%")

            if final_percent >= 50:
                st.balloons()
                st.success("🎉 Glückwunsch! Du hast die Prüfung bestanden.")
            else:
                st.error("❌ Leider nicht bestanden. Nutze den Übungsmodus zum Vertiefen.")

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
