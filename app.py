import datetime
import json
import os
import random
from PIL import Image, ImageDraw
import streamlit as st

# ==============================================================================
# 1. SEITEN-KONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Trainer BW (Freitext-Edition)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🩺 MFA Prüfungstrainer BW – Active Recall & Freitext-Evaluation")
st.caption(
    "Professionelle Software zur Vorbereitung auf die MFA-Abschlussprüfung (LF 1 - LF 5)"
)

# Pfadberechnung
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
            "sample": "Kontralateraler Loslassschmerz (Blumberg-Zeichen).",
            "keywords": ["blumberg", "loslassschmerz"],
            "exp": "Das Blumberg-Zeichen deutet auf eine Peritonealreizung hin.",
        }
    ]


ALL_QUESTIONS = load_questions()

# Navigation
st.sidebar.header("🎯 Navigation & Module")
mode = st.sidebar.radio(
    "Prüfungsmodus wählen:",
    [
        "✍️ Freitext-Fragenkatalog",
        "🖼️ Komplexe Bild- & Praxisfälle",
        "🎲 Dynamische Rechen-Generatoren",
        "🩸 Laborwert-Diagnostiker",
        "📝 Freitext-Musterklausur",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric("📋 Geladene Prüfungsfragen", len(ALL_QUESTIONS))

# ==============================================================================
# HELPER-FUNKTION: EIGENE ANTWORT GEGENPRÜFEN
# ==============================================================================
def evaluate_user_answer(user_text, keywords, sample_solution, explanation):
    """Überprüft die Freitextantwort des Nutzers auf essenzielle Schlüsselwörter."""
    if not user_text.strip():
        st.warning("⚠️ Bitte geben Sie zuerst Ihre Antwort ein.")
        return

    user_text_lower = user_text.lower()
    found_keywords = [kw for kw in keywords if kw.lower() in user_text_lower]
    score = len(found_keywords)
    total = len(keywords)

    st.markdown("#### 📊 Auswertung Ihrer Antwort:")
    if score == total:
        st.success(f"🎉 **Ausgezeichnet!** Alle essenziellen Fachbegriffe wurden erkannt ({score}/{total}).")
    elif score > 0:
        st.warning(f"⚠️ **Teilweise korrekt:** Sie haben {score} von {total} Wichtigen Schlüsselwörtern genannt.")
    else:
        st.error("❌ **Unvollständig / Unkorrekt:** Es wurden keine zentralen Fachbegriffe erkannt.")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Ihre Eingabe:**\n\n_{user_text}_")
    with col2:
        st.success(f"**Musterlösung:**\n\n{sample_solution}")

    with st.expander("💡 Detaillierte fachliche Erklärung & Hintergrundwissen"):
        st.write(explanation)


# ==============================================================================
# 2. BILD-GENERATOREN FOR KOMPLEXAUFGABEN
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
        draw.rectangle([125, y_start, 175, y_start + 40], fill=color, outline="#475569")
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
        (20, 180), (60, 180), (70, 190), (80, 180), (90, 180),
        (100, 210), (110, 80), (120, 230), (130, 110), (180, 110),
        (210, 180), (260, 180), (270, 190), (280, 180), (290, 180),
        (300, 210), (310, 80), (320, 230), (330, 110), (380, 110), (410, 180), (580, 180)
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


# ==============================================================================
# 3. KOMPLEXE PRÜFUNGS-FALLBEISPIELE (FREITEXT)
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
                "q": "1. Welche zwei Testfelder auf dem Urinstreifen weisen spezifisch auf einen bakteriellen Harnwegsinfekt hin?",
                "sample": "Leukozyten und Nitrit.",
                "keywords": ["leukozyten", "nitrit"],
                "exp": "Leukozyten zeigen die Entzündungsreaktion an; Nitrit entsteht durch nitratreduzierende Bakterien (z. B. E. coli).",
            },
            {
                "q": "2. Aus welchem Grund muss für einen verlässlichen Nitritnachweis zwingend Morgenurin verwendet werden?",
                "sample": "Bakterien benötigen mindestens 4 Stunden Verweilzeit in der Blase zur Umwandlung von Nitrat in Nitrit.",
                "keywords": ["4 stunden", "verweilzeit", "blase"],
                "exp": "Die bakterielle Nitratreduktase benötigt mehrere Stunden Kontaktzeit im Blasenurin, um nachweisbare Mengen Nitrit zu bilden.",
            },
            {
                "q": "3. Welche EBM-GOP-Ziffer rechnet die Praxis für die Durchführung des Urinstreifen-Schnelltests ab?",
                "sample": "EBM 32033.",
                "keywords": ["32033"],
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
                "q": "1. Welche pathologische EKG-Veränderung liegt vor?",
                "sample": "ST-Streckenhebung (STEMI / Akuter Herzinfarkt).",
                "keywords": ["st-streckenhebung", "stemi", "infarkt"],
                "exp": "Eine Hebung der ST-Strecke direkt aus dem absteigenden Schenkel der R-Zacke zeigt einen akuten transmuralen Infarkt.",
            },
            {
                "q": "2. Welche zwei Sofortmaßnahmen leitet die MFA unverzüglich ein?",
                "sample": "Notarzt (112) rufen und Oberkörper hochlagern (Herzentlastung).",
                "keywords": ["notarzt", "oberkörper", "112"],
                "exp": "Bei Verdacht auf STEMI gilt absolute Ruhigstellung mit Oberkörperhochlagerung zur Vorlastsenkung und sofortige Notrufabsetzung.",
            },
        ],
    },
]

# ==============================================================================
# 4. RECHEN-GENERATOREN
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

# ==============================================================================
# 5. MODUS-STEUERUNG
# ==============================================================================

if mode == "✍️ Freitext-Fragenkatalog":
    st.header("✍️ Freitext-Fragenkatalog (Eigenformulierung)")
    st.write("Formulieren Sie Ihre Antwort frei im Textfeld. Das System gleicht Ihre Antwort anschließend mit der Fachmusterlösung ab:")

    lf_filter = st.selectbox(
        "Lernfeld filtern:",
        ["Alle Lernfelder", "LF 1", "LF 2", "LF 3", "LF 4", "LF 5"],
    )
    filtered = [
        q for q in ALL_QUESTIONS
        if lf_filter == "Alle Lernfelder" or q["lf"] == lf_filter
    ]

    for idx, q in enumerate(filtered):
        with st.expander(f"Frage {idx+1} [{q['lf']}]: {q['q']}"):
            user_input = st.text_area("Ihre Antwort:", key=f"cat_txt_{q['lf']}_{idx}", height=90)
            if st.button("Antwort einreichen & Gegenprüfen", key=f"btn_cat_{q['lf']}_{idx}"):
                evaluate_user_answer(user_input, q["keywords"], q["sample"], q["exp"])

elif mode == "🖼️ Komplexe Bild- & Praxisfälle":
    st.header("🖼️ Komplexe Praxis-Fallstudien")
    st.write("Analysieren Sie das Befundbild und beantworten Sie die praxisnahen Prüfungsfragen:")

    case_title = st.selectbox(
        "Wählen Sie einen Fall aus:",
        [c["title"] for c in IMAGE_CASE_STUDIES],
    )
    selected_case = next(c for c in IMAGE_CASE_STUDIES if c["title"] == case_title)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(selected_case["generator"](), caption=selected_case["caption"], use_container_width=True)

    with col2:
        st.markdown(selected_case["scenario"])
        st.markdown("---")

        for q_idx, q_item in enumerate(selected_case["questions"]):
            st.markdown(f"**{q_item['q']}**")
            u_ans = st.text_area("Ihre Lösung:", key=f"img_txt_{case_title}_{q_idx}", height=80)
            if st.button("Lösung überprüfen", key=f"img_btn_{case_title}_{q_idx}"):
                evaluate_user_answer(u_ans, q_item["keywords"], q_item["sample"], q_item["exp"])
            st.markdown("---")

elif mode == "🎲 Dynamische Rechen-Generatoren":
    st.header("🎲 Dynamische Rechen- & Fallaufgaben")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Naegele-Regel (Gynäkologie)")
        if "naegele" not in st.session_state or st.button("🔄 Neue Naegele-Aufgabe"):
            st.session_state.naegele = generate_naegele_task()
        n_task = st.session_state.naegele
        st.write(f"**Letzte Regel (LMP):** {n_task['lmp']}")
        st.write(f"**Zykluslänge:** {n_task['cycle']} Tage")
        u_date = st.text_input("Berechneter Entbindungstermin (TT.MM.YYYY):", key="naegele_in")
        if st.button("Termin prüfen"):
            if u_date.strip() == n_task["correct_date"]:
                st.success(f"✅ Richtig! Berechneter Termin: {n_task['correct_date']}")
            else:
                st.error(f"❌ Falsch. Korrekter Termin: {n_task['correct_date']}")

    with col2:
        st.subheader("2. GOÄ-Honorare (Abrechnung)")
        if "goae" not in st.session_state or st.button("🔄 Neue GOÄ-Aufgabe"):
            st.session_state.goae = generate_goae_task()
        g_task = st.session_state.goae
        st.write(f"**Einfacher Satz:** {g_task['base']:.2f} €")
        st.write(f"**Steigerungsfaktor:** {g_task['factor']:.2f}")
        u_price = st.number_input("Rechnungsbetrag (€):", step=0.01, format="%.2f", key="goae_in")
        if st.button("GOÄ Betrag prüfen"):
            if abs(u_price - g_task["total"]) < 0.05:
                st.success(f"✅ Korrekt! Rechnungsbetrag: {g_task['total']:.2f} €")
            else:
                st.error(f"❌ Falsch. Korrekter Betrag: {g_task['total']:.2f} €")

elif mode == "🩸 Laborwert-Diagnostiker":
    st.header("🩸 Interaktiver Laborwert-Diagnostiker")
    st.write("Analysieren Sie den Befund und formulieren Sie Ihre Verdachtsdiagnose frei:")

    lab_param = "HbA1c"
    lab_val = 8.5
    st.metric("Gemessener HbA1c-Wert", f"{lab_val} %", "Norm: 4.0 - 6.0 %")

    u_diag = st.text_area("Ihre medizinische Bewertung & Verdachtsdiagnose:", height=100)
    if st.button("Befund-Auswertung einreichen"):
        evaluate_user_answer(
            u_diag,
            ["diabetes", "erhöht", "blutzucker"],
            "Deutlich erhöhter HbA1c-Wert: Verdacht auf Diabetes mellitus bzw. unzureichend eingestellter Blutzucker.",
            "Der HbA1c-Wert spiegelt den durchschnittlichen Blutzuckerspiegel der letzten 8 bis 12 Wochen wider."
        )

elif mode == "📝 Freitext-Musterklausur":
    st.header("📝 Generierte Freitext-Musterklausur")
    if not ALL_QUESTIONS:
        st.warning("Keine Fragen vorhanden.")
    else:
        if "exam_questions" not in st.session_state or st.button("🔄 Neue Musterklausur zusammenstellen"):
            st.session_state.exam_questions = random.sample(ALL_QUESTIONS, min(5, len(ALL_QUESTIONS)))

        exam_q = st.session_state.exam_questions
        for idx, q in enumerate(exam_q):
            st.markdown(f"### Frage {idx+1} [{q['lf']}]: {q['q']}")
            u_ans = st.text_area("Ihre Ausarbeitung:", key=f"ex_txt_{idx}", height=100)
            if st.button(f"Frage {idx+1} gegenprüfen", key=f"ex_btn_{idx}"):
                evaluate_user_answer(u_ans, q["keywords"], q["sample"], q["exp"])
            st.markdown("---")
