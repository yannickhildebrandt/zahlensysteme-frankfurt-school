import streamlit as st
import random
import numpy as np # Wird für die bin->dez-Konvertierung genutzt

# --- App-Konfiguration ---
st.set_page_config(
    page_title="Zahlensystem-Entdecker",
    page_icon="🧭",
    layout="wide"
)

# --- App-Titel ---
st.title("🧭 Der Zahlensystem-Entdecker")
st.markdown("Lerne Schritt für Schritt, wie Zahlensysteme funktionieren und warum sie in der Informatik so wichtig sind.")

# --- Tabs für den Lernpfad ---
tab_grundlagen, tab_binaer, tab_hex, tab_training = st.tabs([
    "1. Grundlagen: Was ist ein Zahlensystem?",
    "2. Das Binärsystem (Basis 2)",
    "3. Das Hexadezimalsystem (Basis 16)",
    "4. Dein Trainingsplatz"
])

# ==============================================================================
# TAB 1: GRUNDLAGEN
# ==============================================================================
with tab_grundlagen:
    st.header("Alles beginnt mit dem, was du schon kennst: Das Dezimalsystem (Basis 10)")
    st.write(
        "Ein Zahlensystem ist nur eine Methode, um Zahlen darzustellen. Wir benutzen täglich das Dezimalsystem. "
        "Es hat **zehn Ziffern (0-9)** und der Wert einer Ziffer hängt von ihrer **Position** ab."
    )
    st.subheader("Interaktiver Stellenwert-Explorer")
    user_number_str = st.text_input("Gib eine Dezimalzahl ein (z.B. 253)", "253")
    try:
        user_number = int(user_number_str)
        st.markdown(f"Schauen wir uns die Zahl **{user_number}** genauer an:")
        cols = st.columns(len(user_number_str))
        total_sum = []
        for i, digit in enumerate(user_number_str):
            power = len(user_number_str) - 1 - i
            value = int(digit) * (10**power) # KORRIGIERT: ** für Potenz
            with cols[i]:
                st.metric(label=f"10^{power}er-Stelle", value=digit)
                st.write(f"= `{digit} * {10**power}`")
            total_sum.append(f"{value}")
        st.success(f"**Zusammengesetzt ergibt das:** {' + '.join(total_sum)} = **{user_number}**")
        st.info("Dieses Prinzip des **Stellenwerts** ist der Schlüssel zu **allen** anderen Zahlensystemen!")
    except ValueError:
        st.error("Bitte gib eine gültige ganze Zahl ein.")

# ==============================================================================
# TAB 2: BINÄRSYSTEM
# ==============================================================================
with tab_binaer:
    st.header("Die Sprache der Computer: Das Binärsystem (Basis 2)")
    st.markdown(
        "Computer kennen nur zwei Zustände: Strom an (1) und Strom aus (0). Daher arbeiten sie mit dem Binärsystem. "
        "Es hat nur **zwei Ziffern (0 und 1)**. Das Prinzip des Stellenwerts bleibt aber dasselbe, nur mit der **Basis 2**."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Von Dezimal zu Binär: Die Divisionsmethode")
        dez_in = st.number_input("Dezimalzahl zum Umwandeln:", min_value=0, value=42, step=1, key="d2b")
        if dez_in >= 0:
            steps = []
            remains = []
            num = dez_in
            if num == 0:
                st.code("0 / 2 = 0 Rest 0\n\nErgebnis (Reste von unten nach oben): 0", language="text")
            else:
                while num > 0:
                    remainder = num % 2
                    steps.append(f"{num: >3} / 2 = {num // 2: >3}   Rest: {remainder}")
                    remains.append(str(remainder))
                    num //= 2
                result_binary = "".join(reversed(remains))
                steps_text = "\n".join(steps)
                st.code(f"{steps_text}\n\nErgebnis (Reste von unten nach oben gelesen): {result_binary}", language="text")
    with col2:
        st.subheader("Von Binär zu Dezimal: Die Stellenwertmethode")
        bin_in = st.text_input("Binärzahl zum Umwandeln:", "101010", key="b2d")
        if all(c in '01' for c in bin_in) and bin_in:
            steps = []
            total = 0
            for i, digit in enumerate(reversed(bin_in)):
                power = i
                value = int(digit) * (2**power) # KORRIGIERT: ** für Potenz
                steps.append(f"{digit} * 2^{power} = {value}")
                total += value
            st.code("\n".join(steps) + f"\n\nSumme: {total}", language="text")
        else:
            st.error("Bitte eine gültige Binärzahl (nur 0 und 1) eingeben.")

# ==============================================================================
# TAB 3: HEXADEZIMALSYSTEM
# ==============================================================================
with tab_hex:
    st.header("Kompakt und praktisch: Das Hexadezimalsystem (Basis 16)")
    st.markdown(
        "Das Hexadezimalsystem ist in der Informatik beliebt, weil es eine sehr kompakte Schreibweise für lange Binärzahlen ist (eine Hex-Ziffer = vier Binär-Ziffern). "
        "Es hat **16 Ziffern**: `0-9` und zusätzlich `A, B, C, D, E, F` für die Werte 10 bis 15."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Von Dezimal zu Hexadezimal")
        dez_in_hex = st.number_input("Dezimalzahl zum Umwandeln:", min_value=0, value=255, step=1, key="d2h")
        if dez_in_hex >= 0:
            hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
            steps = []
            remains_str = []
            num = dez_in_hex
            if num == 0:
                 st.code("0 / 16 = 0 Rest 0\n\nErgebnis: 0", language="text")
            else:
                while num > 0:
                    remainder = num % 16
                    remainder_char = str(remainder) if remainder < 10 else hex_map[remainder]
                    steps.append(f"{num: >4} / 16 = {num // 16: >4}   Rest: {remainder} ({remainder_char})")
                    remains_str.append(remainder_char)
                    num //= 16
                result_hex = "".join(reversed(remains_str))
                st.code("\n".join(steps) + f"\n\nErgebnis (Reste von unten nach oben): {result_hex}", language="text")
    with col2:
        st.subheader("Von Hexadezimal zu Dezimal")
        hex_in = st.text_input("Hex-Zahl zum Umwandeln:", "FF", key="h2d").upper()
        try:
            # Teste, ob es eine gültige Hex-Zahl ist, indem wir sie konvertieren.
            int(hex_in, 16)
            steps = []
            total = 0
            for i, digit_char in enumerate(reversed(hex_in)):
                power = i
                # Konvertiere A-F in 10-15
                value_dez = int(digit_char, 16)
                value = value_dez * (16**power) # KORRIGIERT: ** für Potenz
                steps.append(f"{digit_char} * 16^{power} (= {value_dez} * {16**power}) = {value}")
                total += value
            st.code("\n".join(steps) + f"\n\nSumme: {total}", language="text")
        except (ValueError, TypeError):
            st.error("Bitte eine gültige Hexadezimalzahl eingeben (0-9, A-F).")

# ==============================================================================
# TAB 4: TRAININGSPLATZ
# ==============================================================================
with tab_training:
    st.header("Teste dein Wissen!")
    st.markdown("Jetzt bist du dran! Wandle die zufällig generierten Zahlen um.")

    # --- HILFSFUNKTIONEN FÜR DEN RECHENWEG ---
    def get_dez_to_base_steps(num, base):
        """Generiert den Rechenweg für Dezimal zu Binär/Hex."""
        if base not in [2, 16]: return ""
        hex_map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
        steps = ["**Rechenweg: Divisionsmethode**"]
        remains = []
        if num == 0:
            return "**Rechenweg:** Die Dezimalzahl 0 ist in jedem System 0."
        
        n = num
        while n > 0:
            remainder = n % base
            if base == 16:
                remainder_char = str(remainder) if remainder < 10 else hex_map[remainder]
                steps.append(f"`{n: >4} / {base} = {n // base: >4}`   Rest: **{remainder}** ({remainder_char})")
                remains.append(remainder_char)
            else: # base == 2
                steps.append(f"`{n: >3} / {base} = {n // base: >3}`   Rest: **{remainder}**")
                remains.append(str(remainder))
            n //= base
        result = "".join(reversed(remains))
        steps.append(f"\nReste von unten nach oben lesen: **{result}**")
        return "\n".join(steps)

    def get_base_to_dez_steps(num_str, base):
        """Generiert den Rechenweg für Binär/Hex zu Dezimal."""
        if base not in [2, 16]: return ""
        steps = ["**Rechenweg: Stellenwertmethode**"]
        total = 0
        for i, digit_char in enumerate(reversed(num_str)):
            power = i
            value_dez = int(digit_char, base)
            value = value_dez * (base**power)
            steps.append(f"`{digit_char} * {base}^{power}` (= {value_dez} * {base**power}) = **{value}**")
            total += value
        steps.append(f"\nAlle Werte summieren: **{total}**")
        return "\n".join(steps)

    # Session State für den Spielstand
    if 'score_correct' not in st.session_state:
        st.session_state.score_correct = 0
        st.session_state.total_questions = 0
        st.session_state.current_question = None
        st.session_state.last_answer_feedback = None # Hinzugefügt, um Feedback zu speichern

    def generate_training_question():
        bases = ["Binär", "Dezimal", "Hexadezimal"]
        from_base, to_base = random.sample(bases, 2)
        dec_value = random.randint(10, 255)
        
        # Frage und Antwort generieren
        if from_base == "Binär":
            q_val = bin(dec_value)[2:]
            from_b_num = 2
        elif from_base == "Hexadezimal":
            q_val = hex(dec_value)[2:].upper()
            from_b_num = 16
        else: # Dezimal
            q_val = str(dec_value)
            from_b_num = 10

        if to_base == "Binär":
            a_val = bin(dec_value)[2:]
            to_b_num = 2
        elif to_base == "Hexadezimal":
            a_val = hex(dec_value)[2:].upper()
            to_b_num = 16
        else: # Dezimal
            a_val = str(dec_value)
            to_b_num = 10
            
        # Rechenweg generieren
        solution_path = ""
        if from_base == "Dezimal":
            solution_path = get_dez_to_base_steps(dec_value, to_b_num)
        elif to_base == "Dezimal":
            solution_path = get_base_to_dez_steps(q_val, from_b_num)
        else: # z.B. Binär -> Hexadezimal
            path1 = get_base_to_dez_steps(q_val, from_b_num)
            path2 = get_dez_to_base_steps(dec_value, to_b_num)
            solution_path = (f"**Umwandlung über das Dezimalsystem**\n\n"
                           f"**1. Schritt: {from_base} nach Dezimal**\n{path1}\n\n"
                           f"**2. Schritt: Dezimal nach {to_base}**\n{path2}")

        st.session_state.current_question = {
            "question": f"Wandle **`{q_val}`** (_{from_base}_) in das **{to_base}**-System um.",
            "answer": a_val,
            "solution_path": solution_path
        }
        # Altes Feedback löschen, wenn eine neue Frage generiert wird
        st.session_state.last_answer_feedback = None

    # Initialisiere die erste Frage oder wenn "überspringen" geklickt wird
    if st.session_state.current_question is None:
        generate_training_question()

    # Score anzeigen
    col1, col2 = st.columns(2)
    col1.metric("Richtig ✅", st.session_state.score_correct)
    col2.metric("Fragen ❔", st.session_state.total_questions)

    # --- NEUE LOGIK: Feedback vom letzten Versuch anzeigen ---
    if st.session_state.last_answer_feedback:
        feedback = st.session_state.last_answer_feedback
        if feedback['correct']:
            st.success(feedback['message'])
        else:
            st.error(feedback['message'])
        
        with st.expander("Richtigen Rechenweg anzeigen"):
            st.markdown(feedback['solution_path'])

    # Frage anzeigen
    st.markdown(st.session_state.current_question["question"])

    # Antwortformular
    with st.form("training_form"):
        user_answer = st.text_input("Deine Antwort:", key="train_answer")
        submitted = st.form_submit_button("Antwort prüfen")

    if submitted:
        st.session_state.total_questions += 1
        correct_answer = st.session_state.current_question["answer"]
        solution_path = st.session_state.current_question["solution_path"]

        # Antwort prüfen und Feedback im session_state speichern
        if user_answer.strip().upper() == correct_answer:
            st.session_state.score_correct += 1
            st.session_state.last_answer_feedback = {
                "correct": True,
                "message": "🎉 Korrekt! Sehr gut gemacht!",
                "solution_path": solution_path
            }
        else:
            st.session_state.last_answer_feedback = {
                "correct": False,
                "message": f"Leider falsch. Die richtige Antwort wäre **{correct_answer}** gewesen.",
                "solution_path": solution_path
            }
        
        # Nächste Frage generieren für den nächsten Durchlauf
        generate_training_question()
        # Seite neu laden, um das Feedback und die neue Frage anzuzeigen
        st.rerun()

    if st.button("Neue Frage (überspringen)"):
        generate_training_question()
        st.rerun()
