import streamlit as st
import random

# --- App-Konfiguration ---
st.set_page_config(
    page_title="Zahlen-Konverter-Coach",
    page_icon="🧠",
    layout="centered"
)

# --- Hilfsfunktionen für die Konvertierung ---
def generate_question(difficulty):
    """Generiert eine zufällige Frage und die dazugehörige Antwort."""
    bases = {
        "Dezimal": 10,
        "Binär": 2,
        "Oktal": 8,
        "Hexadezimal": 16
    }
    
    # Wähle zufällige Start- und Zielbasis
    from_name, to_name = random.sample(list(bases.keys()), 2)
    from_base, to_base = bases[from_name], bases[to_name]

    # Generiere eine zufällige Zahl basierend auf der Schwierigkeit
    if difficulty == "Einfach":
        decimal_number = random.randint(10, 100)
    else: # Schwer
        decimal_number = random.randint(101, 500)

    # Konvertiere die Dezimalzahl in die Startbasis für die Frage
    if from_base == 2:
        question_val = bin(decimal_number)[2:]
    elif from_base == 8:
        question_val = oct(decimal_number)[2:]
    elif from_base == 16:
        question_val = hex(decimal_number)[2:].upper()
    else: # Dezimal
        question_val = str(decimal_number)

    # Berechne die korrekte Antwort in der Zielbasis
    if to_base == 2:
        correct_answer = bin(decimal_number)[2:]
    elif to_base == 8:
        correct_answer = oct(decimal_number)[2:]
    elif to_base == 16:
        correct_answer = hex(decimal_number)[2:].upper()
    else: # Dezimal
        correct_answer = str(decimal_number)
        
    question_text = f"Wandle die **{from_name}**-Zahl **`{question_val}`** in das **{to_name}**-System um."
    
    # Erklärung des Lösungswegs
    explanation = f"""
    **Lösungsweg:**

    1.  **Umwandlung in Dezimal (falls nötig):**
        Die Zahl `{question_val}` (Basis {from_base}) entspricht der Dezimalzahl `{decimal_number}`.
        
    2.  **Umwandlung von Dezimal in die Zielbasis ({to_name}):**
        Um `{decimal_number}` in das {to_name}-System (Basis {to_base}) umzuwandeln, teilt man die Zahl wiederholt durch {to_base} und notiert die Reste von unten nach oben.
        
    **Ergebnis:** Die korrekte Antwort ist **`{correct_answer}`**.
    """

    st.session_state.question_data = {
        "text": question_text,
        "answer": correct_answer,
        "explanation": explanation
    }


# --- Initialisierung des Session State ---
if 'score_correct' not in st.session_state:
    st.session_state.score_correct = 0
    st.session_state.total_questions = 0
    st.session_state.last_answer_state = None # None, "correct", "incorrect"
    st.session_state.show_explanation = False

# --- App-Oberfläche ---

# Titel
st.title("🧠 Der Zahlen-Konverter-Coach")
st.markdown("Trainiere hier deine Fähigkeiten im Umrechnen von Zahlensystemen!")

# Seitenleiste für Einstellungen und Score
with st.sidebar:
    st.header("Einstellungen")
    difficulty = st.radio(
        "Wähle deine Schwierigkeit:",
        ("Einfach", "Schwer"),
        key="difficulty_selector"
    )
    
    st.header("Dein Spielstand")
    # Verwende Spalten für eine saubere Darstellung
    col1, col2 = st.columns(2)
    col1.metric("Richtig", f"{st.session_state.score_correct}")
    col2.metric("Fragen", f"{st.session_state.total_questions}")

    if st.button("Spielstand zurücksetzen"):
        st.session_state.score_correct = 0
        st.session_state.total_questions = 0
        st.session_state.last_answer_state = None
        st.experimental_rerun()

# Generiere eine neue Frage, falls keine existiert
if 'question_data' not in st.session_state:
    generate_question(difficulty)

# --- Hauptbereich: Frage und Antwort ---
st.subheader(f"Frage #{st.session_state.total_questions + 1}")
st.markdown(st.session_state.question_data["text"])

# Antwortformular, um ein Neuladen bei jeder Eingabe zu verhindern
with st.form(key="answer_form"):
    user_answer = st.text_input("Deine Antwort:", placeholder="Gib hier deine Lösung ein")
    submit_button = st.form_submit_button("Antwort prüfen")

# Logik nach dem Absenden des Formulars
if submit_button:
    # Antworten sind nicht case-sensitive (wichtig für Hexadezimal)
    if user_answer.strip().lower() == st.session_state.question_data["answer"].lower():
        st.session_state.last_answer_state = "correct"
        st.session_state.score_correct += 1
    else:
        st.session_state.last_answer_state = "incorrect"
    
    st.session_state.total_questions += 1
    st.session_state.show_explanation = True # Zeige Erklärung nach jeder Antwort

# Feedback anzeigen
if st.session_state.last_answer_state == "correct":
    st.success("🎉 Richtig! Super gemacht!")
elif st.session_state.last_answer_state == "incorrect":
    st.error(f"Leider falsch. Die richtige Antwort lautet: **{st.session_state.question_data['answer']}**")
    
# Erklärung anzeigen (falls gewünscht)
if st.session_state.show_explanation and st.session_state.last_answer_state == "incorrect":
     with st.expander("💡 Wie kommt man darauf? (Lösungsweg)"):
         st.markdown(st.session_state.question_data["explanation"])


# Button für die nächste Frage
if st.button("Nächste Frage"):
    generate_question(difficulty)
    st.session_state.last_answer_state = None
    st.session_state.show_explanation = False
    st.experimental_rerun()
