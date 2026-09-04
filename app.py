import json
import streamlit as st

st.set_page_config(page_title="EduNova Diagnostic", layout="centered")

@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

st.title("EduNova Learning Companion")
st.header("Diagnostic Test")

questions = load_questions()
user_answers = {}

with st.form("diagnostic_form"):
    for q in questions:
        st.write(f"*Q{q['question_id']}: [{q['topic']}] {q['question']}*")
        options = {
            "A": q["option_a"],
            "B": q["option_b"],
            "C": q["option_c"],
            "D": q["option_d"]
        }
        
        user_answers[q["question_id"]] = st.radio(
            "Select your answer:",
            options=list(options.keys()),
            format_func=lambda opt: f"{opt}) {options[opt]}",
            key=f"q_{q['question_id']}"
        )
        st.write("---")

    submitted = st.form_submit_button("Submit Diagnostic Test")

if submitted:
    total_score = 0
    topic_scores = {}

    for q in questions:
        topic = q["topic"]
        if topic not in topic_scores:
            topic_scores[topic] = {"correct": 0, "total": 0}
            
        topic_scores[topic]["total"] += 1

        if user_answers[q["question_id"]] == q["correct_option"]:
            total_score += 1
            topic_scores[topic]["correct"] += 1

    st.success(f"Overall Score: {total_score} / {len(questions)}")
    st.write("*Topic Breakdown:*")
    
    for topic, stats in topic_scores.items():
        pct = (stats["correct"] / stats["total"]) * 100
        st.write(f"* *{topic}*: {stats['correct']}/{stats['total']} ({pct:.0f}%)")
        st.progress(pct / 100)
        