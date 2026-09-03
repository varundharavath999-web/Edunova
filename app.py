import streamlit as st
import json

st.set_page_config(page_title="EduNova - Smart Education Companion", layout="wide")
st.title("🎓 EduNova: Adaptive Learning Companion")

@st.cache_data
def load_questions():
    with open('questions.json', 'r') as file:
        return json.load(file)

questions = load_questions()

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

with st.form("diagnostic_form"):
    st.subheader("📋 Step 1: Initial Diagnostic Assessment")
    for idx, q in enumerate(questions):
        st.markdown(f"**Q{idx+1}. {q['question']}** ({q['topic']})")
        options = {q['option_a']: "option_a", q['option_b']: "option_b", q['option_c']: "option_c", q['option_d']: "option_d"}
        selected = st.radio("Select option:", list(options.keys()), key=q['question_id'])
        st.session_state.user_answers[q['question_id']] = options[selected]
    submit = st.form_submit_button("Submit Diagnostic Test")

if submit:
    score = sum(1 for q in questions if st.session_state.user_answers.get(q['question_id']) == q['correct_option'])
    st.metric("Score", f"{score} / {len(questions)}")
  
