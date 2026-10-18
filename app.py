import datetime
import io
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont
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

# Robuste absolute Pfadberechnung
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
# 2. BILD-GENERATOREN (DYNAMISCHE BILDERZEUGUNG MIT PILLOW)
# ==============================================================================


def create_urine_strip_image():
    """Erzeugt ein Bild eines Urin-Teststreifens mit positiven Feldern."""
    img = Image.new("RGB", (300, 500), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    # Teststreifen-Körper
    draw.rectangle([110, 20, 190, 480], fill="#E2E8F0", outline="#94A3B8")

    # Testfelder (von oben nach unten)
    fields = [
        ("LEU (Leukozyten)", "#8B5CF6"),  # Positiv (Lila)
        ("NIT (Nitrit)", "#EC4899"),  # Positiv (Pink/Rosa)
        ("PRO (Protein)", "#FACC15"),  # Negativ (Gelb)
        ("GLU (Glukose)", "#10B981"),  # Negativ (Grün)
        ("BLO (Blut)", "#F97316"),  # Leicht positiv (Orange)
    ]

    y_start = 50
    for name, color in fields:
        draw.rectangle(
            [125, y_start, 175, y_start + 40], fill=color, outline="#475569"
        )
        draw.text((195, y_start + 12), name, fill="#1E293B")
        y_start += 80

    return img


def create_ekg_image():
    """Erzeugt ein EKG-Bild mit ST-Hebung (STEMI)."""
    img = Image.new("RGB", (600, 300), color="#FFF5F5")
    draw = ImageDraw.Draw(img)

    # EKG-Gitter zeichnen
    for x in range(0, 600, 20):
        draw.line([(x, 0), (x, 300)], fill="#FED7D7", width=1)
    for y in range(0, 300, 20):
        draw.line([(0, y), (600, y)], fill="#FED7D7", width=1)

    # EKG-Linie mit ST-Hebung
    points = [
        (20, 180),
        (60, 180),
        (70, 190),
        (80, 180),
        (90, 180),  # P-Welle
        (100, 210),
        (110, 80),
        (120, 230),  # QRS
        (130, 120),
        (180, 120),  # ST-Hebung (Elevated)
        (210, 180),
        (260, 180),  # T-Welle / Isoelektrisch
        # Wiederholung
        (270, 190),
        (280, 180),
        (290, 180),
        (300, 210),
        (310, 80),
        (320, 230),
        (330, 120),
        (380, 120),
        (410, 180),
        (580, 180),
    ]

    draw.line(points, fill="#DC2626", width=3)
    draw.text((20, 20), "Ableitung II - Akuter Befund", fill="#991B1B")

    return img


def create_au_form_image():
    """Erzeugt eine schematische Muster-1 Arbeitsunfähigkeitsbescheinigung."""
    img = Image.new("RGB", (500, 350), color="#F0FDF4")
    draw = ImageDraw.Draw(img)

    # Formular-Rahmen
    draw.rectangle([10, 10, 490, 340], fill="#DCFCE7", outline="#16A34A", width=2)
    draw.text((20, 20), "Muster 1: Arbeitsunfähigkeitsbescheinigung", fill="#15803D")

    # Kästchen Erst-/Folgemeldung
    draw.rectangle([30, 60, 150, 90], outline="#16A34A")
    draw.text((35, 68), "[X] Erstbescheinigung", fill="#166534")

    draw.rectangle([170, 60, 290, 90], outline="#16A34A")
    draw.text((175, 68), "[ ] Folgebescheinigung", fill="#166534")

    # Diagnosenfeld
    draw.text((30, 120), "AU begründende Diagnose (ICD-10):", fill="#166534")
    draw.rectangle([30, 145, 470, 185], fill="#FFFFFF", outline="#16A34A")
    draw.text((40, 158), "J06.9 G (Akute Infektion der oberen Atemwege)", fill="#0F172A")

    draw.text((30, 210), "Arbeitsunfähig seit: 12.10.2026", fill="#166534")
    draw.text((30, 235), "Voraussichtlich bis: 18.10.2026", fill="#166534")
    draw.text((30, 260), "Festgestellt am: 12.10.2026", fill="#166534")

    return img


# ==============================================================================
# 3. BILD-FALLBEISPIELE (DATENBANK)
# ==============================================================================
IMAGE_CASE_STUDIES = [
    {
        "id": "fall_1",
        "title": "Fallbeispiel 1: Urindiagnostik bei Harnwegsinfekt",
        "generator": create_urine_strip_image,
        "caption": "Abb. 1: Ausgewerteter Urin-Teststreifen der Patientin (Morgenurin).",
        "scenario": """
        **Patientenanamnese:**
        Frau Weber (38 Jahre) kommt mit brennenden Schmerzen beim Wasserlassen (Dysurie) und ständigem Harndrang (Pollakisurie) in die Praxis. 
        Sie führen eine Urinuntersuchung mittels Teststreifen durch.
        """,
        "questions": [
            {
                "q": "1. Welche zwei Testfelder sind auf dem Teststreifen oben eindeutig positiv verändert?",
                "options": [
                    "Leukozyten und Nitrit",
                    "Glukose und Ketone",
                    "Bilirubin und Urobilinogen",
                    "Protein und pH-Wert",
                ],
                "correct": "Leukozyten und Nitrit",
                "exp": "Leukozyten zeigen die Entzündung an; Nitrit weist auf nitratreduzierende Bakterien (z.B. E. coli) hin.",
            },
            {
                "q": "2. Welche Bedingung muss für eine verlässliche Nitritbestimmung erfüllt sein?",
                "options": [
                    "Der Urin muss mindestens 4 Stunden in der Blase verweilt haben (Morgenurin).",
                    "Der Urin muss vor der Messung auf 37 °C erwärmt werden.",
                    "Es muss zwingend Katheterurin verwendet werden.",
                    "Die Patientin muss zuvor 1 Liter Wasser trinken.",
                ],
                "correct": "Der Urin muss mindestens 4 Stunden in der Blase verweilt haben (Morgenurin).",
                "exp": "Bakterien benötigen Verweilzeit im Urin, um Nitrat zu Nitrit zu reduzieren.",
            },
            {
                "q": "3. Welche EBM-Ziffer rechnet die Hausarztpraxis für den Urinstreifen-Schnelltest ab?",
                "options": ["EBM 32033", "EBM 03000", "EBM 03220", "EBM 32001"],
                "correct": "EBM 32033",
                "exp": "Die EBM 32033 ist die Gebührenordnungsposition für den Harnstreifentest.",
            },
        ],
    },
    {
        "id": "fall_2",
        "title": "Fallbeispiel 2: EKG-Befundung bei Brustschmerz",
        "generator": create_ekg_image,
        "caption": "Abb. 2: 12-Kanal-EKG bei Ankunft des Patienten (Ausschnitt Ableitung II).",
        "scenario": """
        **Patientenanamnese:**
        Herr Huber (58 Jahre) klagt über plötzlich aufgetretenen, retrosternalen Vernichtungsschmerz mit Ausstrahlung in den linken Arm und Kaltschweißigkeit. 
        Sie schreiben unverzüglich ein 12-Kanal-EKG.
        """,
        "questions": [
            {
                "q": "1. Welche auffällige Pathologie zeigt das EKG im Kurvenverlauf?",
                "options": [
                    "Signifikante ST-Streckenhebung (STEMI)",
                    "Verlängerte PQ-Zeit (AV-Block I°)",
                    "Absolute Arrhythmie bei Vorhofflimmern",
                    "Ablaufende Ventrikuläre Tachykardie",
                ],
                "correct": "Signifikante ST-Streckenhebung (STEMI)",
                "exp": "Die Hebung der ST-Strecke direkt aus dem absteigenden Schenkel der R-Zacke zeigt einen akuten Infarkt.",
            },
            {
                "q": "2. Welche Erstmaßnahmen leiten Sie als MFA unverzüglich ein?",
                "solution": "1. Notarzt rufen (112).\n2. Oberkörper hochlagern (Herzentlastung).\n3. Vitalwerte (BD, Puls, SpO2) überwachen.\n4. Sauerstoffgabe vorbereiten & Notfallkoffer bereitstellen.",
            },
        ],
    },
    {
        "id": "fall_3",
        "title": "Fallbeispiel 3: Formularkunde & AU-Bescheinigung (Muster 1)",
        "generator": create_au_form_image,
        "caption": "Abb. 3: Ausgestelltes Muster 1 Formular zur Überprüfung.",
        "scenario": """
        **Patientenanamnese:**
        Ein Patient erscheint am Freitag in der Praxis zur Verlängerung seiner Arbeitsunfähigkeit. Im System liegt bereits eine Erstbescheinigung vor.
        """,
        "questions": [
            {
                "q": "1. Welche Zusatzbuchstabe im ICD-10-Code bedeutet 'Gesicherte Diagnose'?",
                "options": ["G (Gesichert)", "V (Verdacht)", "A (Ausschluss)", "G (Grad)"],
                "correct": "G (Gesichert)",
                "exp": "In der ambulanten Versorgung steht 'G' für gesichert, 'V' für Verdacht auf und 'A' für Ausschluss.",
            },
            {
                "q": "2. Bis zu wie vielen Tagen darf eine AU-Bescheinigung in Ausnahmefällen rückdatiert werden?",
                "options": [
                    "Maximal 3 Tage nach gründlicher ärztlicher Untersuchung",
                    "Bis zu 7 Tage",
                    "Rückdatierung ist gesetzlich streng verboten",
                    "Unbegrenzt nach Ermessen des Arztes",
                ],
                "correct": "Maximal 3 Tage nach gründlicher ärztlicher Untersuchung",
                "exp": "Eine Rückdatierung ist nur ausnahmsweise und nach ärztlicher Rücksprache für max. 3 Tage zulässig.",
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
        }
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
# 5. MODUS-STEUERUNG
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
        # Dynamisch erzeugtes Bild anzeigen
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
            user_sel = st.radio(
                "Antwort auswählen:", q["options"], key=f"cat_{q['lf']}_{idx}"
            )
            if st.button("Prüfen", key=f"btn_{q['lf']}_{idx}"):
                if user_sel == q["correct"]:
                    st.success("✅ Richtig!")
                else:
                    st.error(f"❌ Falsch. Richtig: {q['correct']}")
                st.info(f"**Erklärung:** {q['exp']}")
