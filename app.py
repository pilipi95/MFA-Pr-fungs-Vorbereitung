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

st.title("🩺 MFA Abschlussprüfung BW – Mit Bild-Fallbeispielen")
st.caption(
    "Interaktives Lernportal für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)"
)

# Robuste absolute Pfadberechnung für fragen.json
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

# Navigation
st.sidebar.header("🎯 Navigation")
mode = st.sidebar.radio(
    "Lernform wählen:",
    [
        "🖼️ Bild-Fallbeispiele (Komplex)",
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

# ==============================================================================
# 2. BILD-FALLBEISPIELE (DATENBANK)
# ==============================================================================
IMAGE_CASE_STUDIES = [
    {
        "id": "fall_1",
        "title": "Fallbeispiel 1: Urindiagnostik bei Harnwegsinfekt",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Urine_test_strip.jpg/640px-Urine_test_strip.jpg",
        "caption": "Abb. 1: Ausgewerteter Urin-Teststreifen aus der Praxis (Morgenurin).",
        "scenario": """
        **Patientenanamnese:**
        Frau Weber (38 Jahre) kommt mit brennenden Schmerzen beim Wasserlassen (Dysurie) und ständigem Harndrang (Pollakisurie) in die Praxis. 
        Sie führen eine Urinuntersuchung mittels Teststreifen durch.
        """,
        "questions": [
            {
                "q": "1. Welche zwei Testfelder sind bei einem bakteriellen Harnwegsinfekt klassischerweise positiv?",
                "options": [
                    "Leukozyten und Nitrit",
                    "Glukose und Ketone",
                    "Bilirubin und Urobilinogen",
                    "Protein und pH-Wert 9.0",
                ],
                "correct": "Leukozyten und Nitrit",
                "exp": "Leukozyten weisen auf eine Entzündungsreaktion hin; Nitrit zeigt die Anwesenheit nitratreduzierender Bakterien (z.B. E. coli) an.",
            },
            {
                "q": "2. Welche Bedingung muss für eine verlässliche Nitritbestimmung im Urin erfüllt sein?",
                "options": [
                    "Der Urin muss mindestens 4 Stunden in der Blase verweilt haben (Morgenurin).",
                    "Der Urin muss vor der Messung auf 37 °C erwärmt werden.",
                    "Es muss zwingend Katheterurin verwendet werden.",
                    "Die Patientin muss zuvor 1 Liter Wasser trinken.",
                ],
                "correct": "Der Urin muss mindestens 4 Stunden in der Blase verweilt haben (Morgenurin).",
                "exp": "Bakterien benötigen Zeit, um im Urin vorhandenes Nitrat zu Nitrit zu reduzieren.",
            },
            {
                "q": "3. Welche EBM-Ziffer rechnet die Hausarztpraxis für den Urinstreifen-Schnelltest ab?",
                "options": ["EBM 32033", "EBM 03000", "EBM 03220", "EBM 32001"],
                "correct": "EBM 32033",
                "exp": "Die EBM 32033 ist die Gebührenordnungsposition für den Harnstreifentest in der Kassenpraxis.",
            },
        ],
    },
    {
        "id": "fall_2",
        "title": "Fallbeispiel 2: EKG-Befundung bei Brustschmerz",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Anterior_AMI.svg/640px-Anterior_AMI.svg.png",
        "caption": "Abb. 2: 12-Kanal-EKG bei Ankunft des Patienten.",
        "scenario": """
        **Patientenanamnese:**
        Herr Huber (58 Jahre) klagt über plötzlich aufgetretenen, retrosternalen Vernichtungsschmerz mit Ausstrahlung in den linken Arm und Kaltschweißigkeit. 
        Sie schreiben unverzüglich ein 12-Kanal-EKG.
        """,
        "questions": [
            {
                "q": "1. Welche Pathologie zeigt das EKG im Falle eines akuten Herzinfarkts?",
                "solution": "ST-Streckenhebung in mindestens zwei korrespondierenden Ableitungen (STEMI).",
            },
            {
                "q": "2. Welche Erstmaßnahmen leiten Sie als MFA unverzüglich ein?",
                "solution": "1. Notarzt rufen (112).\n2. Oberkörper hochlagern (Herzentlastung).\n3. Vitalwerte (BD, Puls, SpO2) überwachen.\n4. Sauerstoffgabe vorbereiten & Notfallkoffer bereitstellen.",
            },
        ],
    },
    {
        "title": "Fallbeispiel 3: Wundversorgung & Tetanusschutz",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Laceration_of_the_finger_with_stictches.jpg/640px-Laceration_of_the_finger_with_stictches.jpg",
        "caption": "Abb. 3: Versorgte Schnittwunde am Finger.",
        "scenario": """
        **Patientenanamnese:**
        Ein 24-jähriger Patient hat sich bei Gartenarbeiten an einer verschmutzten Gartenhalle tief am Zeigefinger geschnitten. Die Wunde ist glattrandig und 2 Stunden alt.
        """,
        "questions": [
            {
                "q": "1. Welches Zeitfenster gilt maximal für eine primäre Wundnaht?",
                "options": [
                    "Innerhalb von 6 Stunden",
                    "Innerhalb von 12 Stunden",
                    "Innerhalb von 24 Stunden",
                    "Immer möglich unabhängig von der Zeit",
                ],
                "correct": "Innerhalb von 6 Stunden",
                "exp": "Nach 6 Stunden gilt eine Wunde als primär besiedelt/infiziert und darf nicht mehr primär verschlossen werden.",
            },
            {
                "q": "2. Welche Impfung muss bei verunreinigten Wunden zwingend im Impfpass überprüft werden?",
                "solution": "Tetanus-Impfschutz (Wundstarrkrampf). Bei unvollständigem Schutz oder > 10 Jahren Auffrischung ggf. Simultanimpfung (Aktiv + Passiv).",
            },
        ],
    },
]

# ==============================================================================
# 3. HELPER-FUNKTIONEN FÜR ANDERE MODI
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
        ],
        "categories": ["EBM (GKV)", "GOÄ (PKV)"],
    }
]

FREETEXT_TASKS = [
    {
        "term": "Naegele-Regel (einfach)",
        "prompt": "Formel für die einfache Naegele-Regel:",
        "keywords": ["7 tage", "3 monate", "1 jahr"],
        "sample": "1. Tag der letzten Regel + 7 Tage - 3 Monate + 1 Jahr",
    }
]

# ==============================================================================
# 4. MODUS-STEUERUNG
# ==============================================================================

if mode == "🖼️ Bild-Fallbeispiele (Komplex)":
    st.header("🖼️ Bild-Fallbeispiele aus der Praxis")
    st.write(
        "Analysieren Sie das Befundbild und beantworten Sie die dazugehörigen Prüfungsfragen:"
    )

    case_title = st.selectbox(
        "Wählen Sie ein Bild-Fallbeispiel aus:",
        [c["title"] for c in IMAGE_CASE_STUDIES],
    )
    selected_img_case = next(
        c for c in IMAGE_CASE_STUDIES if c["title"] == case_title
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(
            selected_img_case["image_url"],
            caption=selected_img_case["caption"],
            use_container_width=True,
        )

    with col2:
        st.markdown(selected_img_case["scenario"])
        st.markdown("---")

        for q_idx, q_item in enumerate(selected_img_case["questions"]):
            st.markdown(f"**{q_item['q']}**")

            # Unterscheidung Multiple Choice vs. Freitext
            if "options" in q_item:
                user_ans = st.radio(
                    "Antwort wählen:",
                    q_item["options"],
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
