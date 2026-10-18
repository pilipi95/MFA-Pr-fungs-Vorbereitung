import datetime
import json
import os
import random
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

# Custom CSS für modernes, angenehmes Design
st.markdown(
    """
    <style>
    /* Haupt-Hintergrund und Schriftart */
    .main {
        background-color: #F7FAFC;
    }
    
    /* Header-Styling */
    h1 {
        color: #2C5282;
        font-weight: 700;
        font-size: 2.2rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Subtitle / Captions */
    .stCaption {
        color: #4A5568;
        font-size: 1rem;
        margin-bottom: 1.5rem !important;
    }

    /* Info-Boxen & Cards */
    .css-1r6slb0, .stAlert {
        border-radius: 10px !important;
    }
    
    /* Custom Card Design */
    .custom-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.2rem;
    }

    /* Buttons Veredelung */
    .stButton>button {
        border-radius: 8px !important;
        background-color: #3182CE !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        background-color: #2B6CB0 !important;
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
    }

    /* Radio Buttons / Formulare entzerren */
    .stRadio > label {
        font-weight: 600;
        color: #2D3748;
    }
    
    /* Sidebar Optik */
    section[data-testid="stSidebar"] {
        background-color: #EDF2F7;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header-Bereich
st.title("🩺 MFA Abschlussprüfung BW")
st.caption(
    "Interaktives Lernportal für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)"
)

# Robustes Laden der fragen.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "fragen.json")


@st.cache_data
def load_questions():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Fehler beim Lesen der 'fragen.json': {e}")
            return get_fallback_questions()
    else:
        st.warning(
            f"⚠️ 'fragen.json' wurde unter `{JSON_FILE}` nicht gefunden. Nutze Notfall-Fragenkatalog."
        )
        return get_fallback_questions()


def get_fallback_questions():
    """Notfall-Fragenkatalog, falls fragen.json nicht geladen werden kann."""
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
        },
        {
            "lf": "LF 2",
            "q": "Warum muss ein Citrat-Röhrchen für Gerinnungstests exakt befüllt werden?",
            "options": [
                "Um das Mischungsverhältnis 1:9 einzuhalten",
                "Damit keine Hämolyse entsteht",
                "Damit die Zentrifuge stabil läuft",
                "Um den Blutzucker zu stabilisieren",
            ],
            "correct": "Um das Mischungsverhältnis 1:9 einzuhalten",
            "exp": "Bei abweichendem Mischungsverhältnis verfälschen sich Quick und PTT.",
        },
        {
            "lf": "LF 3",
            "q": "Wie lange dauert die Probezeit nach dem BBiG maximal?",
            "options": ["4 Monate", "1 Monat", "6 Monate", "12 Monate"],
            "correct": "4 Monate",
            "exp": "Laut BBiG gilt: mind. 1 Monat, max. 4 Monate.",
        },
    ]


ALL_QUESTIONS = load_questions()

# Sidebar Navigation
st.sidebar.header("🎯 Navigation")
mode = st.sidebar.radio(
    "Lernform wählen:",
    [
        "🎲 Dynamische Generatoren",
        "🩸 Laborwert-Diagnostiker",
        "🔄 Zuordnungs-Trainer",
        "📑 Original-Fallstudien",
        "✏️ Freitext-Trainer",
        "📝 Musterklausur",
        "📚 Gesamter Fragenkatalog",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric("📋 Geladene Fragen", len(ALL_QUESTIONS))

# ==============================================================================
# 2. DYNAMISCHE AUFGABEN-GENERATOREN
# ==============================================================================


def generate_naegele_task():
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
    base_price = round(random.uniform(10.0, 120.0), 2)
    factor = random.choice([1.0, 1.15, 1.8, 2.3, 3.5])
    total = round(base_price * factor, 2)
    return {"base": base_price, "factor": factor, "total": total}


def generate_urlaub_task():
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


def generate_lab_value():
    labs = [
        {
            "parameter": "HbA1c",
            "unit": "%",
            "norm": "4.0 - 6.0 %",
            "val": round(random.uniform(4.5, 11.0), 1),
            "low_thresh": 4.0,
            "high_thresh": 6.0,
            "diag_high": "Verdacht auf / Schlecht eingestellter Diabetes mellitus",
            "diag_low": "Physiologisch / Selten Hypoglykämie-Neigung",
        },
        {
            "parameter": "Kalium",
            "unit": "mmol/l",
            "norm": "3.5 - 5.0 mmol/l",
            "val": round(random.uniform(2.8, 6.8), 1),
            "low_thresh": 3.5,
            "high_thresh": 5.0,
            "diag_high": "Hyperkalämie (Gefahr von Herzrhythmusstörungen / Niereninsuffizienz)",
            "diag_low": "Hypokalämie (z.B. durch Diuretika, Erbrechen, Laxanzien)",
        },
        {
            "parameter": "Leukozyten",
            "unit": "/µl",
            "norm": "4.000 - 10.000 /µl",
            "val": random.randint(2000, 22000),
            "low_thresh": 4000,
            "high_thresh": 10000,
            "diag_high": "Leukozytose (Bakterielle Infektion / Entzündung)",
            "diag_low": "Leukopentie (Agranulozytose / Virale Infektion / Knochenmarkschädigung)",
        },
        {
            "parameter": "CRP (C-reaktives Protein)",
            "unit": "mg/l",
            "norm": "< 5.0 mg/l",
            "val": round(random.uniform(1.0, 85.0), 1),
            "low_thresh": 0.0,
            "high_thresh": 5.0,
            "diag_high": "Akute bakterielle Entzündung / Gewebsnekrose",
            "diag_low": "Normalbefund (keine akute Entzündung)",
        },
    ]
    return random.choice(labs)


# ==============================================================================
# 3. ZUORDNUNGS-DATENBANK & FALLSTUDIEN
# ==============================================================================
MATCHING_TASKS = [
    {
        "title": "Zuordnung: EBM vs. GOÄ Regelungen",
        "items": [
            {"term": "Versichertenpauschale 03000", "correct_cat": "EBM (GKV)"},
            {"term": "Regelhöchstsatz 2,3-fach", "correct_cat": "GOÄ (PKV)"},
            {
                "term": "Schwellenwert 1,8-fach für Sachleistungen",
                "correct_cat": "GOÄ (PKV)",
            },
            {"term": "Chronikerpauschale 03220", "correct_cat": "EBM (GKV)"},
        ],
        "categories": ["EBM (GKV)", "GOÄ (PKV)"],
    },
    {
        "title": "Zuordnung: Injektionsarten & Injektionswinkel",
        "items": [
            {"term": "Intrakutan (i.c.)", "correct_cat": "10° - 15° (Quaddel)"},
            {
                "term": "Subkutan (s.c.)",
                "correct_cat": "45° - 90° (Fettgewebe)",
            },
            {
                "term": "Intramuskulär (i.m.)",
                "correct_cat": "90° (Muskelgewebe)",
            },
        ],
        "categories": [
            "10° - 15° (Quaddel)",
            "45° - 90° (Fettgewebe)",
            "90° (Muskelgewebe)",
        ],
    },
]

CASE_STUDIES = [
    {
        "title": "Fallstudie 1: Akuter Notfall in der Praxis (Anaphylaxie)",
        "scenario": """
        **Ausgangslage:** Herr Müller (45 Jahre) erhält in Ihrer Praxis eine intramuskuläre Injektion eines Antibiotikums.
        3 Minuten nach der Injektion klagt der Patient über plötzlichen Juckreiz an den Handflächen, Atemnot, Schwindel und Hitzegefühl.
        Sein Gesicht schwillt an (Angioödem), die Haut zeigt Urtikaria.
        """,
        "questions": [
            {
                "q": "1. Welches Krankheitsbild liegt hier höchstwahrscheinlich vor?",
                "solution": "Anaphylaktischer Schock (Anaphylaxie / Schwerwiegende allergische Sofortreaktion Typ I).",
            },
            {
                "q": "2. Welche Sofortmaßnahmen müssen Sie als MFA unverzüglich einleiten?",
                "solution": "1. Arzt sofort benachrichtigen / Notruf veranlassen.\n2. Patient flach lagern, bei Atemnot Oberkörper hochlagern (bzw. Schocklagerung bei Kollaps).\n3. Atemwege freihalten und O2-Gabe vorbereiten.\n4. Notfallkoffer & Anaphylaxie-Besteck bereitstellen (Adrenalin, Antihistaminika, Glukokortikoide).",
            },
            {
                "q": "3. Welches Notfallmedikament ist das Mittel der 1. Wahl bei einer Anaphylaxie mit Atemnot/Schock?",
                "solution": "Adrenalin (Epinephrin) – vorzugsweise i.m. (z. B. in den Oberschenkel).",
            },
        ],
    },
    {
        "title": "Fallstudie 2: Arbeitsunfall & Hygiene (Nadelstichverletzung)",
        "scenario": """
        **Ausgangslage:** Während der Blutentnahme bei einem bekannten Hepatitis-C-Patienten rutscht die Auszubildende Lisa ab
        und sticht sich mit der gebrauchten Kanüle tief in den rechten Zeigefinger.
        """,
        "questions": [
            {
                "q": "1. Welche Sofortmaßnahmen am Verletzungsort sind durchzuführen?",
                "solution": "1. Wundblutung anregen (nicht quetschen!).\n2. Wunde gründlich mit hautverträglichem Antiseptikum spülen/desinfizieren (mind. 1 Minute).\n3. Wunde steril abdecken.",
            },
            {
                "q": "2. Welche Stellen/Personen müssen umgehend informiert und aufgesucht werden?",
                "solution": "1. Praxisinhaber / Sicherheitsbeauftragten informieren.\n2. Durchgangsarzt (D-Arzt) zur Unfalldokumentation aufsuchen.\n3. Eintragung in das Verbandbuch / Unfallsystem der Berufsgenossenschaft (BGW).",
            },
            {
                "q": "3. Welche Blutuntersuchungen müssen beim Indexpatienten und der MFA veranlasst werden?",
                "solution": "Bestimmung des Serologie-Status auf HBV (HBsAg, Anti-HBs), HCV (Anti-HCV) und HIV (Anti-HIV) zum Zeitpunkt 0 sowie Verlaufskontrollen.",
            },
        ],
    },
]

FREETEXT_TASKS = [
    {
        "term": "Naegele-Regel (einfach)",
        "prompt": "Geben Sie die mathematische Formel für die einfache Naegele-Regel an:",
        "keywords": ["7 tage", "3 monate", "1 jahr", "letzten regel"],
        "sample": "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr",
    },
    {
        "term": "EBM Chronikerpauschale Ziffer",
        "prompt": "Welche EBM-Ziffer wird für die Betreuung eines chronisch kranken Patienten angesetzt?",
        "keywords": ["03220", "03221"],
        "sample": "EBM 03220 (bzw. 03221)",
    },
    {
        "term": "Fachbegriff: Bluthochdruck",
        "prompt": "Wie lautet der medizinische Fachbegriff für dauerhaft erhöhten Blutdruck (≥ 140/90 mmHg)?",
        "keywords": ["hypertonie", "arterielle hypertonie"],
        "sample": "Arterielle Hypertonie",
    },
    {
        "term": "BBiG Probezeit Dauer",
        "prompt": "Wie lang muss die Probezeit im Berufsausbildungsvertrag laut BBiG mindestens und darf sie maximal sein?",
        "keywords": ["1 monat", "4 monate"],
        "sample": "Mindestens 1 Monat, maximal 4 Monate.",
    },
]

# ==============================================================================
# 4. BENUTZEROBERFLÄCHE & MODUS-STEUERUNG
# ==============================================================================

if mode == "🎲 Dynamische Generatoren":
    st.markdown("### 🎲 Dynamische Rechen- & Fallaufgaben")
    st.info("Diese Aufgaben generieren bei jedem Klick neue Zufallswerte.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="custom-card"><h4>1. Naegele-Regel (Gynäkologie)</h4>',
            unsafe_allow_html=True,
        )
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
                st.success(f"✅ Richtig! Errechnet: {n_task['correct_date']}")
            else:
                st.error(f"❌ Falsch. Richtig: {n_task['correct_date']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="custom-card"><h4>2. GOÄ-Honorare (Abrechnung)</h4>',
            unsafe_allow_html=True,
        )
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
                st.success(f"✅ Korrekt! Ergebnis: {g_task['total']:.2f} €")
            else:
                st.error(f"❌ Falsch. Richtig ist: {g_task['total']:.2f} €")
        st.markdown("</div>", unsafe_allow_html=True)

elif mode == "🩸 Laborwert-Diagnostiker":
    st.markdown("### 🩸 Interaktiver Laborwert-Diagnostiker (LF 2)")

    if "lab_task" not in st.session_state or st.button(
        "🔄 Nächster Laborbefund"
    ):
        st.session_state.lab_task = generate_lab_value()

    l_task = st.session_state.lab_task

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader(f"Laborparameter: {l_task['parameter']}")

    col_a, col_b = st.columns(2)
    col_a.metric("Gemessener Wert", f"{l_task['val']} {l_task['unit']}")
    col_b.metric("Referenzbereich (Norm)", l_task["norm"])

    user_eval = st.radio(
        "Bewertung des Messwertes:",
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
            st.success(f"✅ Richtig! Der Wert ist {correct_eval}.")
            st.info(
                f"**Klinische Einordnung:** {l_task['diag_high'] if user_eval == 'Erhöht' else (l_task['diag_low'] if user_eval == 'Erniedrigt' else 'Unauffälliger Befund')}"
            )
        else:
            st.error(f"❌ Falsch. Richtig wäre: **{correct_eval}**.")
    st.markdown("</div>", unsafe_allow_html=True)

elif mode == "🔄 Zuordnungs-Trainer":
    st.markdown("### 🔄 Zuordnungs-Trainer (Matching)")

    for m_idx, m_task in enumerate(MATCHING_TASKS):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

elif mode == "📑 Original-Fallstudien":
    st.markdown("### 📑 Original-Fallstudien & Komplexaufgaben")

    case_choice = st.selectbox(
        "Fall auswählen:", [c["title"] for c in CASE_STUDIES]
    )
    selected_case = next(c for c in CASE_STUDIES if c["title"] == case_choice)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(selected_case["scenario"])
    st.markdown("</div>", unsafe_allow_html=True)

    for idx, q_item in enumerate(selected_case["questions"]):
        st.markdown(f"**{q_item['q']}**")
        st.text_area(
            "Ihre Lösung:", key=f"cs_{case_choice}_{idx}", height=100
        )
        with st.expander("💡 Musterlösung anzeigen"):
            st.markdown(q_item["solution"])
        st.markdown("---")

elif mode == "✏️ Freitext-Trainer":
    st.markdown("### ✏️ Freitext- & Fachbegriffe-Trainer")

    for idx, ft in enumerate(FREETEXT_TASKS):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
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
            else:
                st.error("Bitte geben Sie eine Antwort ein.")
        st.markdown("</div>", unsafe_allow_html=True)

elif mode == "📝 Musterklausur":
    st.markdown("### 📝 Generierte Musterklausur")

    if not ALL_QUESTIONS:
        st.warning("Keine Fragen vorhanden.")
    else:
        if "exam_questions" not in st.session_state or st.button(
            "🔄 Neue Musterklausur erstellen"
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
                f"Antwort währen für Frage {idx+1}:",
                q["options"],
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

            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader(f"Ergebnis: {score} von {total} Punkten ({percent}%)")

            if percent >= 50:
                st.balloons()
                st.success("🎉 Bestanden! Hervorragendes Ergebnis.")
            else:
                st.error(
                    "❌ Leider nicht bestanden. Wiederholen Sie die Themen im Fragenkatalog."
                )
            st.markdown("</div>", unsafe_allow_html=True)

elif mode == "📚 Gesamter Fragenkatalog":
    st.markdown("### 📚 Vollständiger Fragenkatalog")

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
                "Antwort auswählen:", q["options"], key=f"cat_{q['lf']}_{idx}"
            )
            if st.button("Prüfen", key=f"btn_{q['lf']}_{idx}"):
                if user_sel == q["correct"]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch. Richtige Antwort: {q['correct']}")
                st.info(f"**Erklärung:** {q['exp']}")
