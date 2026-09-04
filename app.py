import streamlit as st
import json

st.title("EduNova Learning Companion")
st.subheader("Diagnostic Test")

@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

try:
    questions = load_questions()
    for i, q in enumerate(questions, 1):
        q_id = q.get("question_id") or q.get("id") or str(i)
        topic = q.get("topic", "General")
        question_text = q.get("question", "")
        
        st.write(f"**Q{q_id}: [{topic}] {question_text}**")
        options = q.get("options", [])
        if options:
            st.radio(f"Select an answer for Q{q_id}:", options, key=f"q_{i}")
        st.write("---")
except Exception as e:
    st.error(f"Error loading questions: {e}")
