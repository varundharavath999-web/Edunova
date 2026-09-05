import streamlit as st
import json

st.set_page_config(page_title="EduNova Day 3 MVP", layout="wide")

st.title("EduNova Learning Companion")
st.subheader("Day 3 Core Build — Smart Education Diagnostic & Testing Engine")

@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

try:
    questions = load_questions()
    
    # Session state initialization for re-testing flow
    if "stage" not in st.session_state:
        st.session_state.stage = "DIAGNOSTIC"
    if "weak_topics" not in st.session_state:
        st.session_state.weak_topics = []

    # ---------------------------------------------------------
    # STAGE 1: DIAGNOSTIC ASSESSMENT
    # ---------------------------------------------------------
    if st.session_state.stage == "DIAGNOSTIC":
        st.write("### 1. Diagnostic Assessment")
        with st.form("diagnostic_form"):
            user_answers = {}
            for i, q in enumerate(questions):
                q_id = q.get("question_id", str(i+1))
                topic = q.get("topic", "General")
                q_text = q.get("question", "")
                
                # Construct option map
                options_map = {
                    "A": f"A) {q.get('option_a', '')}",
                    "B": f"B) {q.get('option_b', '')}",
                    "C": f"C) {q.get('option_c', '')}",
                    "D": f"D) {q.get('option_d', '')}"
                }
                
                st.write(f"**[{q_id}] [{topic}] ({q.get('difficulty', 'Medium')}) {q_text}**")
                selected_letter = st.radio(
                    f"Select answer for {q_id}:",
                    options=list(options_map.keys()),
                    format_func=lambda x: options_map[x],
                    key=f"q_{i}",
                    index=None
                )
                user_answers[i] = selected_letter
                st.write("---")
                
            submit_btn = st.form_submit_button("Submit Diagnostic Test")

        if submit_btn:
            if None in user_answers.values():
                st.warning("Please answer all questions before submitting!")
            else:
                topic_stats = {}
                total_correct = 0
                
                for i, q in enumerate(questions):
                    topic = q.get("topic", "General")
                    correct_opt = q.get("correct_option", "A")
                    selected_opt = user_answers[i]
                    
                    if topic not in topic_stats:
                        topic_stats[topic] = {"correct": 0, "total": 0}
                    topic_stats[topic]["total"] += 1
                    
                    if selected_opt == correct_opt:
                        total_correct += 1
                        topic_stats[topic]["correct"] += 1
                
                st.session_state.weak_topics = []
                st.header("Results & Weakness Detection")
                overall_pct = (total_correct / len(questions)) * 100
                st.metric("Overall Score", f"{total_correct}/{len(questions)} ({overall_pct:.1f}%)")
                
                st.write("#### Topic Performance Breakdown:")
                for topic, stats in topic_stats.items():
                    pct = (stats["correct"] / stats["total"]) * 100
                    st.write(f"- **{topic}**: {stats['correct']}/{stats['total']} ({pct:.0f}%)")
                    if pct < 60.0:
                        st.session_state.weak_topics.append(topic)
                
                if st.session_state.weak_topics:
                    st.error(f"⚠️ Weak Topics Detected (<60%): {', '.join(st.session_state.weak_topics)}")
                    st.header("Personalized Learning Roadmap")
                    for idx, wt in enumerate(st.session_state.weak_topics, 1):
                        st.write(f"**Step {idx}: Target Weak Area → [{wt}]**")
                    
                    if st.button("Proceed to Targeted Practice & Re-test"):
                        st.session_state.stage = "PRACTICE"
                        st.rerun()
                else:
                    st.success("🎉 No weak topics detected! High performance across all concepts.")

    # ---------------------------------------------------------
    # STAGE 2: TARGETED PRACTICE & RE-TEST
    # ---------------------------------------------------------
    elif st.session_state.stage == "PRACTICE":
        st.header("2. Targeted Practice & Re-test")
        st.info(f"Targeting Weak Topics: {', '.join(st.session_state.weak_topics)}")
        
        practice_questions = [q for q in questions if q.get("topic") in st.session_state.weak_topics]
        
        with st.form("retest_form"):
            retest_answers = {}
            for i, q in enumerate(practice_questions):
                q_id = q.get("question_id")
                q_text = q.get("question")
                options_map = {
                    "A": f"A) {q.get('option_a', '')}",
                    "B": f"B) {q.get('option_b', '')}",
                    "C": f"C) {q.get('option_c', '')}",
                    "D": f"D) {q.get('option_d', '')}"
                }
                st.write(f"**[RE-TEST {q_id}] {q_text}**")
                retest_answers[i] = st.radio(
                    f"Select answer for {q_id}:",
                    options=list(options_map.keys()),
                    format_func=lambda x: options_map[x],
                    key=f"rq_{i}",
                    index=None
                )
                st.write("---")
            retest_submit = st.form_submit_button("Submit Re-test")

        if retest_submit:
            if None in retest_answers.values():
                st.warning("Please answer all re-test questions!")
            else:
                rt_correct = 0
                for i, q in enumerate(practice_questions):
                    if retest_answers[i] == q.get("correct_option", "A"):
                        rt_correct += 1
                rt_pct = (rt_correct / len(practice_questions)) * 100
                st.success(f"Re-test Complete! New Score on Weak Topics: {rt_correct}/{len(practice_questions)} ({rt_pct:.0f}%)")
                if rt_pct >= 60.0:
                    st.balloons()
                    st.success("Weak topic successfully remediated!")
                if st.button("Restart Diagnostic Loop"):
                    st.session_state.stage = "DIAGNOSTIC"
                    st.rerun()

except Exception as e:
    st.error(f"Error loading questions: {e}")