import datetime
import random
import streamlit as st

# Seiten-Konfiguration
st.set_page_config(
    page_title="MFA Prüfungs-Generator BW (Vollversion)",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 MFA Abschlussprüfung BW – XXL Prüfungs-Generator")
st.caption(
    "Umfangreicher Prüfungs- & Uebungssimulator für die Lernfelder 1 bis 5 (MFA Baden-Württemberg)."
)

# Session State Initialisierung
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Sidebar Navigation
mode = st.sidebar.radio(
    "Modus waehlen:",
    [
        "🎲 Dynamische Generatoren (Naegele, GOE, BBiG)",
        "📝 Musterklausur (Zufallsauswahl)",
        "📚 Gesamter Fragenkatalog (LF 1 – 5)",
    ],
)

# ------------------------------------------------------------------------------
# 1. DYNAMISCHE GENERATOREN
# ------------------------------------------------------------------------------


def generate_naegele_task():
    """Generiert eine dynamische Naegele-Aufgabe mit Zufallsdatum und variabler Zykluslaenge."""
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
    """Generiert eine dynamische GOAE-Abrechnungsaufgabe."""
    base_price = round(random.uniform(10.0, 120.0), 2)
    factor = random.choice([1.0, 1.15, 1.8, 2.3, 3.5])
    total = round(base_price * factor, 2)
    return {"base": base_price, "factor": factor, "total": total}


def generate_urlaub_task():
    """Generiert eine dynamische Urlaubsanspruchs-Berechnung nach JArbSchG."""
    alter = random.randint(15, 18)
    # JArbSchG § 19: <16: 30 Werktage, <17: 27 Werktage, <18: 25 Werktage, ab 18: BUrlG (24 Werktage)
    if alter < 16:
        urlaub = 30
    elif alter < 17:
        urlaub = 27
    elif alter < 18:
        urlaub = 25
    else:
        urlaub = 24

    return {"alter": alter, "urlaub": urlaub}


# ------------------------------------------------------------------------------
# 2. FRAGENDATENBANK (LF 1 BIS LF 5)
# ------------------------------------------------------------------------------
ALL_QUESTIONS = [
    # --- LERNFELD 1: Behandlungsassistenz & Medizinische Fachkunde ---
    {
        "lf": "LF 1",
        "q": "Welches Symptom gehört zur klassischen Trias des akuten Myokardinfarkts (STEMI)?",
        "options": [
            "Retrosternaler Vernichtungsschmerz, Kaltschweissigkeit und Atemnot",
            "Stechender Schmerz im rechten Unterbauch und Fieber",
            "Einseitige Pupillenerweiterung und Lähmung",
            "Plötzlicher Sehverlust auf beiden Augen",
        ],
        "correct": "Retrosternaler Vernichtungsschmerz, Kaltschweissigkeit und Atemnot",
        "exp": "Der Herzinfarkt zeigt sich klassisch durch Engegefühl (Angina Pectoris), Ausstrahlung in den linken Arm/Kiefer und Kaltschweissigkeit.",
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
        "q": "Welche Wunde darf primär NICHT durch eine Naht verschlossen werden?",
        "options": [
            "Frische Operationsinzision",
            "Hundebisswunde am Unterarm",
            "Glatte Schnittwunde am Finger (1 Stunde alt)",
            "Aseptische Wunde nach Muttermalentfernung",
        ],
        "correct": "Hundebisswunde am Unterarm",
        "exp": "Bisswunden sind hochgradig infektionsgefährdet (Mischflora) und heilen primär sekundär.",
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
        "q": "Welche Druckpunkte werden bei Verdacht auf Appendizitis geprüft?",
        "options": [
            "McBurney-Punkt, Lanz-Punkt und Blumberg-Zeichen (Loslassschmerz)",
            "Homans-Zeichen und Meyer-Zeichen",
            "Giordano-Zeichen an den Flanken",
            "Trousseau-Zeichen am Oberarm",
        ],
        "correct": "McBurney-Punkt, Lanz-Punkt und Blumberg-Zeichen (Loslassschmerz)",
        "exp": "Lanz- und McBurney-Punkt liegen im rechten Unterbauch. Das Blumberg-Zeichen bezeichnet den kontralateralen Loslassschmerz.",
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
    {
        "lf": "LF 1",
        "q": "Welche Injektionsart wird für den Tuberkulin-Hauttest bzw. Allergietests genutzt?",
        "options": [
            "Intrakutan (i.c.)",
            "Subkutan (s.c.)",
            "Intramuskulär (i.m.)",
            "Intravenös (i.v.)",
        ],
        "correct": "Intrakutan (i.c.)",
        "exp": "Intrakutane Injektionen erfolgen direkt in die Lederhaut (Cutis) unter Quaddelbildung.",
    },
    # --- LERNFELD 2: Praxislabor & Hygiene ---
    {
        "lf": "LF 2",
        "q": "Welche Reihenfolge ist bei der venösen Blutentnahme nach den Empfehlungen einzuhalten?",
        "options": [
            "Blutkultur -> Serum -> Citrat (Gerinnung) -> Heparin -> EDTA -> Fluorid",
            "EDTA -> Citrat -> Serum -> Fluorid",
            "Fluorid -> EDTA -> Heparin -> Serum",
            "Die Reihenfolge ist beliebig, solange gut gemischt wird",
        ],
        "correct": "Blutkultur -> Serum -> Citrat (Gerinnung) -> Heparin -> EDTA -> Fluorid",
        "exp": "Blutkulturen stehen an erster Stelle zur Verschleppungsvermeidung. EDTA darf nie vor Serum/Citrat entnommen werden.",
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
        "exp": "Die RiliBÄK schreibt tägliche Kontrollprobenmessungen und regelmässige Ringversuche vor.",
    },
    {
        "lf": "LF 2",
        "q": "Welche Parameter gelten für die Standard-Dampfsterilisation im Autoklaven?",
        "options": [
            "134 °C bei 2 bar Betriebsüberdruck für mindestens 5 Minuten Haltezeit",
            "100 °C bei Normaldruck für 60 Minuten",
            "180 °C Trockenhitze für 30 Minuten",
            "200 °C bei 5 bar für 1 Minute",
        ],
        "correct": "134 °C bei 2 bar Betriebsüberdruck für mindestens 5 Minuten Haltezeit",
        "exp": "Gespannter, gesättigter Wasserdampf tötet bei 134 °C selbst hochresistente Sporen zuverlässig ab.",
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
    {
        "lf": "LF 3",
        "q": "Wie lange ist die gesetzliche Mindestaufbewahrungsfrist für ärztliche Patientendokumente nach BGB (§ 630f)?",
        "options": [
            "10 Jahre nach Abschluss der Behandlung",
            "2 Jahre ab Jahresende",
            "30 Jahre für alle Dokumente ohne Ausnahme",
            "5 Jahre ab Erstellung",
        ],
        "correct": "10 Jahre nach Abschluss der Behandlung",
        "exp": "Die allgemeine BGB-Aufbewahrungsfrist für Behandlungsakten beträgt 10 Jahre (Sonderfristen wie Röntgenunterlagen beachten).",
    },
    {
        "lf": "LF 3",
        "q": "Genießt eine Auszubildende während der Probezeit Kündigungsschutz bei Schwangerschaft?",
        "options": [
            "Ja, es gilt ein absolutes Kündigungsverbot nach § 17 Mutterschutzgesetz (MuSchG)",
            "Nein, in der Probezeit kann immer fristlos ohne Grund gekündigt werden",
            "Nur, wenn die Schwangerschaft vor Ausbildungsbeginn bekannt war",
            "Ja, aber nur mit Zustimmung der zuständigen Ärztekammer",
        ],
        "correct": "Ja, es gilt ein absolutes Kündigungsverbot nach § 17 Mutterschutzgesetz (MuSchG)",
        "exp": "Der Mutterschutz hebelt die Flexibilität der Probezeitkündigung zum Schutz der Mutter aus.",
    },
    # --- LERNFELD 4: Abrechnungswesen (EBM, GOÄ & UV-GOÄ) ---
    {
        "lf": "LF 4",
        "q": "Was ist die Voraussetzung für die Abrechnung der EBM-Chronikerpauschale (03220 / 03221)?",
        "options": [
            "Mindestens 2 persönliche Arzt-Patienten-Kontakte in den letzten 4 Quartalen wegen derselben lebensverändernden Erkrankung",
            "Einmaliger Kontakt pro Kalenderjahr bei Patienten über 60 Jahren",
            "Tägliche Blutdruckmessung über einen Zeitraum von 4 Wochen",
            "Ausschliesslich die Diagnose Diabetes mellitus Typ 2",
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
    {
        "lf": "LF 4",
        "q": "Welches Muster wird für die Verordnung einer Facharztüberweisung im GKV-System genutzt?",
        "options": [
            "Muster 6",
            "Muster 16",
            "Muster 1 (AU)",
            "Muster 2 (Krankenhaus)",
        ],
        "correct": "Muster 6",
        "exp": "Muster 6 ist der Überweisungsschein für kurative/präventive Behandlungen.",
    },
    {
        "lf": "LF 4",
        "q": "Wie lange ist ein rosa Kassenrezept (Muster 16) für Arzneimittel in der Regel gültig?",
        "options": [
            "28 Tage (bzw. 1 Monat)",
            "7 Tage ab Ausstellungsdatum",
            "3 Monate ab Ausstellungsdatum",
            "Unbegrenzt gültig",
        ],
        "correct": "28 Tage (bzw. 1 Monat)",
        "exp": "Standard-Kassenrezepte müssen innerhalb von 28 Tagen in der Apotheke eingelöst werden.",
    },
    # --- LERNFELD 5: Wirtschafts- & Sozialkunde ---
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
    {
        "lf": "LF 5",
        "q": "Welches Prinzip bestimmt die Verteilung der Beiträge zur Kranken-, Renten- und Arbeitslosenversicherung?",
        "options": [
            "Paritätische Finanzierung (je 50 % Arbeitnehmer und Arbeitgeber)",
            "Vollständige Eigenfinanzierung durch den Arbeitnehmer",
            "Steuerfinanzierung durch den Bund",
            "Umlageverfahren ohne Arbeitgeberanteil",
        ],
        "correct": "Paritätische Finanzierung (je 50 % Arbeitnehmer und Arbeitgeber)",
        "exp": "Die Beiträge werden hälftig zwischen Arbeitgeber und Arbeitnehmer aufgeteilt.",
    },
]

# ------------------------------------------------------------------------------
# APP LOGIK
# ------------------------------------------------------------------------------

if mode == "🎲 Dynamische Generatoren (Naegele, GOE, BBiG)":
    st.header("🎲 Dynamische Rechen- & Fallaufgaben")
    st.info(
        "Diese Aufgaben generieren bei jedem Klick neue Zufallswerte – perfekt zum Üben von Rechenwegen!"
    )

    # Task 1: Naegele
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

    # Task 2: GOÄ
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

    # Task 3: JArbSchG
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
        "Es werden zufällig 10 Fragen aus allen Lernfeldern ausgewählt. Viel Erfolg!"
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
                "❌ Leider nicht bestanden (unter 50 %). Nutzen Sie die Fachbereichsübersicht zum Wiederholen."
            )

elif mode == "📚 Gesamter Fragenkatalog (LF 1 – 5)":
    st.header("📚 Vollständiger Fragenkatalog")
    st.write("Wählen Sie ein Lernfeld aus, um alle Fragen gezielt zu üben:")

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