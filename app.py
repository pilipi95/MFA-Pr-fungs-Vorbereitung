import datetime
import json
import os
import random
import streamlit as st

# ==============================================================================
# 1. SEITEN-KONFIGURATION & SETUP
# ==============================================================================
st.set_page_config(
    page_title="MFA Prüfungs-Generator BW (XXL Interaktiv)",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 MFA Abschlussprüfung BW – XXL Prüfungs-Generator")
st.caption(
    "Interaktiver Simulator mit allen Übungsformen für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)."
)

# Robustes Laden der fragen.json (speziell für Streamlit Cloud & Linux)
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

# Session State Initialisierung
if "score" not in st.session_state:
    st.session_state.score = 0

# Sidebar Navigation (Erweitert um Zuordnungen & Labor-Diagnostik)
mode = st.sidebar.radio(
    "Lernform / Modus wählen:",
    [
        "🎲 Dynamische Generatoren (Naegele, GOÄ, BBiG)",
        "🩸 Interaktiver Laborwert-Diagnostiker",
        "🔄 Zuordnungs-Trainer (Matching)",
        "📑 Original-Fallstudien (Komplexaufgaben)",
        "✏️ Freitext- & Fachbegriffe-Trainer",
        "📝 Musterklausur (Zufallsauswahl)",
        "📚 Gesamter Fragenkatalog (LF 1 – 5)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric("Geladene Multiple-Choice Fragen", len(ALL_QUESTIONS))

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
    """Generiert zufällige Patientendaten und Laborwerte für die Diagnostik."""
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
# 3. ZUORDNUNGS-DATENBANK (MATCHING)
# ==============================================================================
MATCHING_TASKS = [
    {
        "title": "Zuordnung: EBM vs. GOÄ Regelungen",
        "items": [
            {
                "term": "Versichertenpauschale 03000",
                "correct_cat": "EBM (GKV)",
            },
            {
                "term": "Regelhöchstsatz 2,3-fach",
                "correct_cat": "GOÄ (PKV)",
            },
            {
                "term": "Schwellenwert 1,8-fach für Sachleistungen",
                "correct_cat": "GOÄ (PKV)",
            },
            {
                "term": "Chronikerpauschale 03220",
                "correct_cat": "EBM (GKV)",
            },
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

# ==============================================================================
# 4. KOMPLEXE FALLSTUDIEN & FREITEXT
# ==============================================================================
CASE_STUDIES = [
    {
        "title": "Fallstudie 1: Akuter Notfall in der Praxis (Anaphylaxie)",
        "scenario": """
        **Ausgangslage:** Herr Müller (45 Jahre) erhält in Ihrer Praxis eine intramuskuläre Injektion eines Antibiotikums.
        3 Minuten nach der Injektion klagt der Patient über plötzlichen Juckreiz an den Handflächen, Atemnot, Schwindel und Hitzegefühl.
        Sein Gesicht wächst an (Angioödem), die Haut zeigt Urtikaria.
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
# 5. BENUTZEROBERFLÄCHE & MODUS-STEUERUNG
# ==============================================================================

if mode == "🎲 Dynamische Generatoren (Naegele, GOÄ, BBiG)":
    st.header("🎲 Dynamische Rechen- & Fallaufgaben")
    st.info(
        "Diese Aufgaben generieren bei jedem Klick neue Zufallswerte – perfekt zum Einüben von Rechenwegen!"
    )

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
            st.error(f"❌ Falsch. Richtig wäre: {n_task['correct_date']}.")
            st.info(
                f"**Rechenweg:** {n_task['lmp']} + 7 Tage - 3 Monate + 1 Jahr + ({n_task['cycle']} - 28) Tage."
            )

    st.markdown("---")

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

elif mode == "🩸 Interaktiver Laborwert-Diagnostiker":
    st.header("🩸 Interaktiver Laborwert-Diagnostiker (LF 2)")
    st.write(
        "Bewerten Sie den vorgegebenen Befund und wählen Sie die passende Verdachtsdiagnose:"
    )

    if "lab_task" not in st.session_state or st.button(
        "🔄 Neubeitrag / Nächster Laborbefund"
    ):
        st.session_state.lab_task = generate_lab_value()

    l_task = st.session_state.lab_task

    st.subheader(f"Laborparameter: {l_task['parameter']}")
    col1, col2 = st.columns(2)
    col1.metric("Gemessener Wert", f"{l_task['val']} {l_task['unit']}")
    col2.metric("Referenzbereich (Norm)", l_task["norm"])

    user_eval = st.radio(
        "1. Bewertung des Meßwertes:",
        ["Erhöht", "Erniedrigt", "Normalbefund"],
        key="lab_eval",
    )

    if user_eval == "Erhöht":
        correct_eval = "Erhöht" if l_task["val"] > l_task["high_thresh"] else ("Erniedrigt" if l_task["val"] < l_task["low_thresh"] else "Normalbefund")
    elif user_eval == "Erniedrigt":
        correct_eval = "Erniedrigt" if l_task["val"] < l_task["low_thresh"] else ("Erhöht" if l_task["val"] > l_task["high_thresh"] else "Normalbefund")
    else:
        correct_eval = "Normalbefund" if l_task["low_thresh"] <= l_task["val"] <= l_task["high_thresh"] else ("Erhöht" if l_task["val"] > l_task["high_thresh"] else "Erniedrigt")

    if st.button("Befund-Bewertung überprüfen"):
        if (
            (l_task["val"] > l_task["high_thresh"] and user_eval == "Erhöht")
            or (l_task["val"] < l_task["low_thresh"] and user_eval == "Erniedrigt")
            or (l_task["low_thresh"] <= l_task["val"] <= l_task["high_thresh"] and user_eval == "Normalbefund")
        ):
            st.success(f"✅ Richtig! Der Wert ist {correct_eval}.")
            st.info(
                f"**Klinische Einordnung:** {l_task['diag_high'] if user_eval == 'Erhöht' else (l_task['diag_low'] if user_eval == 'Erniedrigt' else 'Unauffälliger Befund')}"
            )
        else:
            st.error(f"❌ Falsch. Der Wert ist physiologisch: **{correct_eval}**.")

elif mode == "🔄 Zuordnungs-Trainer (Matching)":
    st.header("🔄 Zuordnungs-Trainer (Matching)")
    st.write(
        "Ordnen Sie die Begriffe den passenden Oberkategorien zu:"
    )

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
            correct_count = 0
            for item_idx, item in enumerate(m_task["items"]):
                if user_matches[item_idx] == item["correct_cat"]:
                    correct_count += 1

            if correct_count == len(m_task["items"]):
                st.success("🎉 Perfekt! Alle Zuordnungen sind richtig.")
            else:
                st.warning(
                    f"Sie haben {correct_count} von {len(m_task['items'])} Zuordnungen richtig."
                )
        st.markdown("---")

elif mode == "📑 Original-Fallstudien (Komplexaufgaben)":
    st.header("📑 Original-Fallstudien & Komplexaufgaben")
    st.write(
        "Wie in der praktischen & schriftlichen Prüfung: Bearbeiten Sie zusammenhängende Praxisfälle Schritt für Schritt."
    )

    case_choice = st.selectbox(
        "Wählen Sie einen Fall zur Bearbeitung aus:",
        [c["title"] for c in CASE_STUDIES],
    )
    selected_case = next(c for c in CASE_STUDIES if c["title"] == case_choice)

    st.markdown(selected_case["scenario"])
    st.markdown("---")

    for idx, q_item in enumerate(selected_case["questions"]):
        st.markdown(f"**{q_item['q']}**")
        user_input = st.text_area(
            "Ihre Lösung / Vorgehensweise:", key=f"cs_{case_choice}_{idx}"
        )

        with st.expander("💡 Musterlösung & Prüfungskriterien anzeigen"):
            st.markdown(q_item["solution"])

elif mode == "✏️ Freitext- & Fachbegriffe-Trainer":
    st.header("✏️ Freitext- & Fachbegriffe-Trainer")
    st.write(
        "Testen Sie Ihr Wissen ohne vorgegebene Antwortmöglichkeiten. Geben Sie die Antwort frei ein:"
    )

    for idx, ft in enumerate(FREETEXT_TASKS):
        st.subheader(f"Aufgabe {idx+1}: {ft['term']}")
        st.write(ft["prompt"])
        user_txt = st.text_input("Ihre Antwort:", key=f"ft_in_{idx}")

        if st.button("Antwort auswerten", key=f"ft_btn_{idx}"):
            if user_txt.strip() != "":
                found_keywords = [
                    kw for kw in ft["keywords"] if kw in user_txt.lower()
                ]
                if len(found_keywords) > 0:
                    st.success("✅ Sehr gut! Kernbegriffe richtig erkannt.")
                else:
                    st.warning(
                        "⚠️ Überprüfen Sie Ihre Eingabe anhand der Musterlösung."
                    )
                st.info(f"**Musterlösung:** {ft['sample']}")
            else:
                st.error("Bitte geben Sie zuerst eine Antwort ein.")
        st.markdown("---")

elif mode == "📝 Musterklausur (Zufallsauswahl)":
    st.header("📝 Generierte Musterklausur")
    st.write(
        "Es werden zufällig 10 Fragen aus allen 5 Lernfeldern ausgewählt. Viel Erfolg!"
    )

    if len(ALL_QUESTIONS) == 0:
        st.warning("Keine Fragen vorhanden.")
    else:
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
    st.write(
        "Wählen Sie ein Lernfeld aus, um alle verfügbaren Prüfungsfragen gezielt zu üben:"
    )

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
