import streamlit as st
import random
import numpy as np
import json
import os
import time
import pandas as pd

# --- App-Konfiguration ---
st.set_page_config(
    page_title="Zahlensystem-Entdecker",
    page_icon="🧭",
    layout="wide"
)

# --- KONSTANTEN FÜR DEN CONTEST ---
HIGHSCORE_FILE = "highscore.json"
STUDENT_LIST = [
    "Bitte Namen wählen", 
    "Jasmin Michelle Agsten", 
    "Annika Balke", 
    "Nebahat Beller", 
    "Peter Berg", 
    "Emilia Bergmann", 
    "Alessandro Dario Bonvecchi", 
    "Andrea Deschermaier", 
    "Luka Drinjak", 
    "Cora Dücker", 
    "Marcel Carsten Duve", 
    "Wilhelm Erdmann", 
    "Lazaros Gerdis", 
    "Shania Erika Margit Hienzsch", 
    "Rammon Hoch", 
    "Pia Höpfner", 
    "Nadine Klein", 
    "Sophie Louise Krämer", 
    "Natasa Petrov", 
    "Kevin Plattner", 
    "Selina Polat", 
    "Tobias Richter", 
    "Marie Robiné", 
    "Jonas Rohde", 
    "Celina Marie Ruf", 
    "Noah Schäfer", 
    "Gian-Luca Schmitt", 
    "Tobias Schütt", 
    "Noé-Li Schwab", 
    "Hannah Stein", 
    "Mery Surja-Morin", 
    "Ibtissam Taiki", 
    "Johanna Theßeling", 
    "Robin Vallei", 
    "Dimitrios Zotos", 
    "Lisa Zysk"
] # Liste der Studierenden 
CONTEST_DURATION_SECONDS = 15 * 60 # 15 Minuten

# --- App-Titel ---
st.title("🧭 Der Zahlensystem-Entdecker")
st.markdown("Lerne Schritt für Schritt, wie Zahlensysteme funktionieren und warum sie in der Informatik so wichtig sind.")

# --- Tabs für den Lernpfad ---
tab_grundlagen, tab_binaer, tab_hex, tab_training, tab_aufgaben, tab_contest = st.tabs([
    "1. Grundlagen",
    "2. Binärsystem",
    "3. Hexadezimalsystem",
    "4. Trainingsplatz",
    "5. Übungsaufgaben (Vorlesung)",
    "🏆 Powerlearning Contest"
])

# ==============================================================================
# HILFSFUNKTIONEN (werden von mehreren Tabs genutzt)
# ==============================================================================
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

def generate_question_data():
    """Generiert die Daten für eine beliebige Frage."""
    bases = ["Binär", "Dezimal", "Hexadezimal"]
    from_base, to_base = random.sample(bases, 2)
    dec_value = random.randint(10, 255)
    
    if from_base == "Binär":
        q_val, from_b_num = bin(dec_value)[2:], 2
    elif from_base == "Hexadezimal":
        q_val, from_b_num = hex(dec_value)[2:].upper(), 16
    else: # Dezimal
        q_val, from_b_num = str(dec_value), 10

    if to_base == "Binär":
        a_val, to_b_num = bin(dec_value)[2:], 2
    elif to_base == "Hexadezimal":
        a_val, to_b_num = hex(dec_value)[2:].upper(), 16
    else: # Dezimal
        a_val, to_b_num = str(dec_value), 10
        
    if from_base == "Dezimal":
        solution_path = get_dez_to_base_steps(dec_value, to_b_num)
    elif to_base == "Dezimal":
        solution_path = get_base_to_dez_steps(q_val, from_b_num)
    else:
        path1 = get_base_to_dez_steps(q_val, from_b_num)
        path2 = get_dez_to_base_steps(dec_value, to_b_num)
        solution_path = (f"**Umwandlung über das Dezimalsystem**\n\n"
                       f"**1. Schritt: {from_base} nach Dezimal**\n{path1}\n\n"
                       f"**2. Schritt: Dezimal nach {to_base}**\n{path2}")

    return {
        "question": f"Wandle **`{q_val}`** (_{from_base}_) in das **{to_base}**-System um.",
        "answer": a_val,
        "solution_path": solution_path
    }


# ==============================================================================
# TAB 1-3 (unverändert, hier zur Vollständigkeit eingeklappt)
# ==============================================================================
with tab_grundlagen:
    st.header("Alles beginnt mit dem, was du schon kennst: Das Dezimalsystem (Basis 10)")
    st.write(
        "Ein Zahlensystem ist nur eine Methode, um Zahlen darzustellen. Wir benutzen täglich das Dezimalsystem. "
        "Es hat **zehn Ziffern (0-9)** und der Wert einer Ziffer hängt von ihrer **Position** ab."
    )
    st.subheader("Interaktiver Stellenwert-Explorer")
    user_number_str = st.text_input("Gib eine Dezimalzahl ein (z.B. 253)", "253", key="grundlagen_input")
    try:
        user_number = int(user_number_str)
        st.markdown(f"Schauen wir uns die Zahl **{user_number}** genauer an:")
        cols = st.columns(len(user_number_str))
        total_sum = []
        for i, digit in enumerate(user_number_str):
            power = len(user_number_str) - 1 - i
            value = int(digit) * (10**power)
            with cols[i]:
                st.metric(label=f"10^{power}er-Stelle", value=digit)
                st.write(f"= `{digit} * {10**power}`")
            total_sum.append(f"{value}")
        st.success(f"**Zusammengesetzt ergibt das:** {' + '.join(total_sum)} = **{user_number}**")
        st.info("Dieses Prinzip des **Stellenwerts** ist der Schlüssel zu **allen** anderen Zahlensystemen!")
    except ValueError:
        st.error("Bitte gib eine gültige ganze Zahl ein.")

with tab_binaer:
    # ... (Code für Binärsystem, unverändert)
    st.header("Die Sprache der Computer: Das Binärsystem (Basis 2)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Von Dezimal zu Binär")
        dez_in = st.number_input("Dezimalzahl:", min_value=0, value=42, step=1, key="d2b")
        st.code(get_dez_to_base_steps(dez_in, 2).replace("**Rechenweg: Divisionsmethode**\n", ""), language="text")
    with col2:
        st.subheader("Von Binär zu Dezimal")
        bin_in = st.text_input("Binärzahl:", "101010", key="b2d")
        if all(c in '01' for c in bin_in) and bin_in:
            st.code(get_base_to_dez_steps(bin_in, 2).replace("**Rechenweg: Stellenwertmethode**\n", ""), language="text")
        else:
            st.error("Bitte eine gültige Binärzahl (nur 0 und 1) eingeben.")


with tab_hex:
    # ... (Code für Hexadezimalsystem, unverändert)
    st.header("Kompakt und praktisch: Das Hexadezimalsystem (Basis 16)")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Von Dezimal zu Hexadezimal")
        dez_in_hex = st.number_input("Dezimalzahl:", min_value=0, value=255, step=1, key="d2h")
        st.code(get_dez_to_base_steps(dez_in_hex, 16).replace("**Rechenweg: Divisionsmethode**\n", ""), language="text")
    with col2:
        st.subheader("Von Hexadezimal zu Dezimal")
        hex_in = st.text_input("Hex-Zahl:", "FF", key="h2d").upper()
        try:
            int(hex_in, 16)
            st.code(get_base_to_dez_steps(hex_in, 16).replace("**Rechenweg: Stellenwertmethode**\n", ""), language="text")
        except (ValueError, TypeError):
            st.error("Bitte eine gültige Hexadezimalzahl eingeben (0-9, A-F).")

# ==============================================================================
# TAB 4: TRAININGSPLATZ (unverändert)
# ==============================================================================
with tab_training:
    st.header("Teste dein Wissen!")
    st.markdown("Jetzt bist du dran! Wandle die zufällig generierten Zahlen um.")

    # Session State Initialisierung (robust)
    if 'score_correct' not in st.session_state:
        st.session_state.score_correct = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_training_question' not in st.session_state:
        st.session_state.current_training_question = None
    if 'last_answer_feedback' not in st.session_state:
        st.session_state.last_answer_feedback = None

    def generate_training_question():
        st.session_state.current_training_question = generate_question_data()
        st.session_state.last_answer_feedback = None

    col1, col2 = st.columns(2)
    col1.metric("Richtig ✅", st.session_state.score_correct)
    col2.metric("Fragen ❔", st.session_state.total_questions)
    st.divider()

    if st.session_state.last_answer_feedback:
        feedback = st.session_state.last_answer_feedback
        if feedback['correct']:
            st.success(feedback['message'])
        else:
            st.error(feedback['message'])
        
        with st.expander("Richtigen Rechenweg anzeigen"):
            st.markdown(feedback['solution_path'])
        
        if st.button("Nächste Frage ▶️", key="next_train_q"):
            generate_training_question()
            st.rerun()
    else:
        if st.session_state.current_training_question is None:
            generate_training_question()

        st.markdown(st.session_state.current_training_question["question"])
        with st.form("training_form"):
            user_answer = st.text_input("Deine Antwort:", key="train_answer")
            submitted = st.form_submit_button("Antwort prüfen")

        if submitted:
            st.session_state.total_questions += 1
            correct_answer = st.session_state.current_training_question["answer"]
            solution_path = st.session_state.current_training_question["solution_path"]

            if user_answer.strip().upper() == correct_answer:
                st.session_state.score_correct += 1
                st.session_state.last_answer_feedback = {
                    "correct": True, "message": "🎉 Korrekt! Sehr gut gemacht!", "solution_path": solution_path
                }
            else:
                st.session_state.last_answer_feedback = {
                    "correct": False, "message": f"Leider falsch. Die richtige Antwort wäre **{correct_answer}** gewesen.", "solution_path": solution_path
                }
            st.rerun()

# ==============================================================================
# NEU - TAB 5: ÜBUNGSAUFGABEN
# ==============================================================================
with tab_aufgaben:
    st.header("📝 Übungsaufgaben für die Vorlesung")
    st.markdown("Löst bitte die folgenden Aufgaben auf Papier. Wir besprechen die Lösungswege gleich gemeinsam.")

    st.subheader("Aufgabe 1: Dezimal ➔ Binär")
    st.markdown("Wandle die Dezimalzahl **147** in eine Binärzahl um.")
    
    st.subheader("Aufgabe 2: Binär ➔ Dezimal")
    st.markdown("Wandle die Binärzahl **10110101** in eine Dezimalzahl um.")

    st.subheader("Aufgabe 3: Dezimal ➔ Hexadezimal")
    st.markdown("Wandle die Dezimalzahl **498** in eine Hexadezimalzahl um.")

    st.subheader("Aufgabe 4: Hexadezimal ➔ Dezimal")
    st.markdown("Wandle die Hexadezimalzahl **1F5** in eine Dezimalzahl um.")

    st.subheader("Aufgabe 5: Binär ➔ Hexadezimal")
    st.markdown("Wandle die Binärzahl **11010110** in eine Hexadezimalzahl um. (Tipp: Der Weg über das Dezimalsystem ist eine Möglichkeit!)")

# ==============================================================================
# NEU - TAB 6: POWERLEARNING CONTEST
# ==============================================================================
with tab_contest:
    st.header("🏆 Powerlearning Contest")
    st.markdown(f"Wer löst in **{CONTEST_DURATION_SECONDS // 60} Minuten** die meisten Aufgaben? Wähle deinen Namen und leg los!")

    # --- Highscore-Funktionen ---
    def load_highscore():
        if not os.path.exists(HIGHSCORE_FILE):
            return {}
        with open(HIGHSCORE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_highscore(data):
        with open(HIGHSCORE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    # --- Session State Initialisierung für den Contest ---
    if 'contest_user' not in st.session_state:
        st.session_state.contest_user = None
    if 'contest_started' not in st.session_state:
        st.session_state.contest_started = False
    if 'contest_start_time' not in st.session_state:
        st.session_state.contest_start_time = 0
    if 'contest_score' not in st.session_state:
        st.session_state.contest_score = 0
    if 'contest_question' not in st.session_state:
        st.session_state.contest_question = None

    # --- ZUSTAND 1: NAMENSAUSWAHL (LOGIN) ---
    if not st.session_state.contest_user:
        st.subheader("Schritt 1: Wähle deinen Namen")
        selected_name = st.selectbox("Wer bist du?", options=STUDENT_LIST)

        if st.button("Das bin ich!", type="primary") and selected_name != STUDENT_LIST[0]:
            st.session_state.contest_user = selected_name
            st.rerun()

    # --- ZUSTAND 2: CONTEST LÄUFT ODER KANN GESTARTET WERDEN ---
    else:
        st.success(f"Angemeldet als: **{st.session_state.contest_user}**")
        
        # --- ZUSTAND 2A: CONTEST NOCH NICHT GESTARTET ---
        if not st.session_state.contest_started:
            st.subheader("Bist du bereit?")
            if st.button(f"Ja, {CONTEST_DURATION_SECONDS // 60}-Minuten-Challenge starten!", type="primary"):
                st.session_state.contest_started = True
                st.session_state.contest_start_time = time.time()
                st.session_state.contest_score = 0
                st.session_state.contest_question = generate_question_data()
                st.rerun()

        # --- ZUSTAND 2B: CONTEST LÄUFT ---
        else:
            elapsed_time = time.time() - st.session_state.contest_start_time
            remaining_time = CONTEST_DURATION_SECONDS - elapsed_time

            # --- ZEIT LÄUFT NOCH ---
            if remaining_time > 0:
                c1, c2 = st.columns(2)
                c1.metric("Verbleibende Zeit", f"{int(remaining_time // 60):02d}:{int(remaining_time % 60):02d}")
                c2.metric("Dein Score", f"{st.session_state.contest_score} ✅")
                
                st.markdown(st.session_state.contest_question['question'])

                with st.form("contest_form"):
                    user_answer = st.text_input("Deine schnelle Antwort:", key="contest_answer")
                    submitted = st.form_submit_button("Prüfen!")
                
                if submitted:
                    if user_answer.strip().upper() == st.session_state.contest_question['answer']:
                        st.session_state.contest_score += 1
                        st.toast("Richtig! Nächste Aufgabe...", icon="🎉")
                        # Highscore aktualisieren
                        scores = load_highscore()
                        scores[st.session_state.contest_user] = max(scores.get(st.session_state.contest_user, 0), st.session_state.contest_score)
                        save_highscore(scores)
                    else:
                        st.toast(f"Leider falsch. Richtig wäre: {st.session_state.contest_question['answer']}", icon="❌")
                    
                    st.session_state.contest_question = generate_question_data()
                    st.rerun()
            
            # --- ZEIT IST ABGELAUFEN ---
            else:
                st.balloons()
                st.header("🏁 Die Zeit ist um! 🏁")
                st.subheader(f"Super gemacht, {st.session_state.contest_user}!")
                st.metric("Dein finaler Score:", f"{st.session_state.contest_score} Aufgaben")
                st.info("Dein Ergebnis wurde im Highscore gespeichert.")
                
                if st.button("Nochmal versuchen"):
                    st.session_state.contest_started = False
                    st.rerun()

    # --- HIGHSCORE ANZEIGE (immer sichtbar, wenn eingeloggt) ---
    st.divider()
    st.header("🥇 Gruppen-Highscore")
    highscore_data = load_highscore()
    if not highscore_data:
        st.info("Noch keine Einträge im Highscore. Sei der/die Erste!")
    else:
        # Sortiere das Dictionary nach Werten (Scores) in absteigender Reihenfolge
        sorted_scores = sorted(highscore_data.items(), key=lambda item: item[1], reverse=True)
        
        # In einen Pandas DataFrame umwandeln für eine schöne Tabelle
        df = pd.DataFrame(sorted_scores, columns=['Name', 'Score'])
        df.index = df.index + 1 # Startet den Index bei 1 (für den Rang)
        st.dataframe(df, use_container_width=True)
