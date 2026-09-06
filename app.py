import streamlit as st
import json

# ---------------------------------------------------------
# PAGE CONFIGURATION & STYLING (Sai Teja's UI Wireframes)
# ---------------------------------------------------------
st.set_page_config(page_title="EduNova - Adaptive Learning Companion", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main-header {font-size: 2.2rem; color: #1E3A8A; font-weight: 700; text-align: center; margin-bottom: 0.5rem;}
    .sub-header {font-size: 1.1rem; color: #4B5563; text-align: center; margin-bottom: 2rem;}
    .card {background-color: #F3F4F6; padding: 1.2rem; border-radius: 10px; border-left: 5px solid #2563EB; margin-bottom: 1rem;}
    .metric-card {background-color: #EFF6FF; padding: 1rem; border-radius: 8px; text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🎓 EduNova Learning Companion</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Adaptive Diagnostic Test, Weakness Detection & Progress Tracking</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA LOADER (Raj's Question Bank)
# ---------------------------------------------------------
@st.cache_data
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)

try:
    questions = load_questions()
except Exception as e:
    st.error(f"Error loading questions.json: {e}")
    st.stop()

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION (Adaptive Flow Engine)
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = "DIAGNOSTIC"
if "diagnostic_score" not in st.session_state:
    st.session_state.diagnostic_score = 0
if "topic_performance" not in st.session_state:
    st.session_state.topic_performance = {}
if "weak_topics" not in st.session_state:
    st.session_state.weak_topics = []
if "retest_score" not in st.session_state:
    st.session_state.retest_score = 0

# ---------------------------------------------------------
# NAVIGATION SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("📌 Student Journey")
steps = ["1. Diagnostic Test", "2. Performance & Weakness", "3. Personalized Roadmap", "4. Targeted Practice", "5. Progress Tracking"]
current_idx = {"DIAGNOSTIC": 0, "RESULTS": 1, "ROADMAP": 2, "PRACTICE": 3, "PROGRESS": 4}.get(st.session_state.step, 0)
st.sidebar.radio("Current Phase", steps, index=current_idx, disabled=True)

# ---------------------------------------------------------
# STEP 1: DIAGNOSTIC TEST
# ---------------------------------------------------------
if st.session_state.step == "DIAGNOSTIC":
    st.subheader("📋 Phase 1: Diagnostic Assessment")
    st.write("Answer all questions to analyze your strengths and weak topics.")
    
    with st.form("diagnostic_form"):
        user_answers = {}
        for i, q in enumerate(questions):
            q_id = q.get("question_id", str(i+1))
            topic = q.get("topic", "General")
            opts = {
                "A": f"A) {q.get('option_a', '')}",
                "B": f"B) {q.get('option_b', '')}",
                "C": f"C) {q.get('option_c', '')}",
                "D": f"D) {q.get('option_d', '')}"
            }
            st.write(f"**Q{i+1} [{q_id}] [{topic}]: {q.get('question')}**")
            user_answers[i] = st.radio(
                f"Select answer for Q{i+1}:",
                options=list(opts.keys()),
                format_func=lambda x: opts[x],
                key=f"diag_{i}",
                index=None
            )
            st.write("---")
            
        submit_diag = st.form_submit_button("Submit Diagnostic Test")

    if submit_diag:
        if None in user_answers.values():
            st.warning("⚠️ Please answer all questions before submitting!")
        else:
            topic_stats = {}
            total_correct = 0
            
            for i, q in enumerate(questions):
                topic = q.get("topic", "General")
                correct = q.get("correct_option", "A")
                selected = user_answers[i]
                
                if topic not in topic_stats:
                    topic_stats[topic] = {"correct": 0, "total": 0}
                topic_stats[topic]["total"] += 1
                
                if selected == correct:
                    total_correct += 1
                    topic_stats[topic]["correct"] += 1

            # Store metrics in session state
            st.session_state.diagnostic_score = round((total_correct / len(questions)) * 100, 1)
            st.session_state.topic_performance = {
                t: round((s["correct"] / s["total"]) * 100, 1) for t, s in topic_stats.items()
            }
            st.session_state.weak_topics = [
                t for t, score in st.session_state.topic_performance.items() if score < 60.0
            ]
            st.session_state.step = "RESULTS"
            st.rerun()

# ---------------------------------------------------------
# STEP 2: PERFORMANCE ANALYSIS & WEAKNESS DETECTION
# ---------------------------------------------------------
elif st.session_state.step == "RESULTS":
    st.subheader("📊 Phase 2: Diagnostic Results & Weakness Detection")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Overall Score", f"{st.session_state.diagnostic_score}%")
    with col2:
        st.write("#### Topic Mastery Breakdown")
        for topic, score in st.session_state.topic_performance.items():
            st.progress(score / 100, text=f"{topic}: {score}%")

    st.write("---")
    st.write("#### 🔍 Weak Topic Detection (< 60% Threshold)")
    if st.session_state.weak_topics:
        st.error(f"Detected {len(st.session_state.weak_topics)} Weak Topic(s): " + ", ".join(st.session_state.weak_topics))
    else:
        st.success("🎉 Great job! No weak topics detected.")

    if st.button("Generate Personalized Roadmap ➡️"):
        st.session_state.step = "ROADMAP"
        st.rerun()

# ---------------------------------------------------------
# STEP 3: PERSONALIZED LEARNING ROADMAP
# ---------------------------------------------------------
elif st.session_state.step == "ROADMAP":
    st.subheader("🗺️ Phase 3: Personalized Learning Roadmap")
    
    if st.session_state.weak_topics:
        st.info("The adaptive engine prioritizes topics where your score was below 60%:")
        for idx, wt in enumerate(st.session_state.weak_topics, 1):
            st.markdown(f"""
                <div class='card'>
                    <h4>Step {idx}: Remediate [{wt}]</h4>
                    <p>Current Score: <b>{st.session_state.topic_performance[wt]}%</b></p>
                    <p><i>Recommendation:</i> Complete targeted practice modules to build core understanding.</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("You have mastered all diagnostic concepts! Proceeding to advanced practice.")

    if st.button("Start Targeted Practice ➡️"):
        st.session_state.step = "PRACTICE"
        st.rerun()

# ---------------------------------------------------------
# STEP 4: TARGETED PRACTICE & RE-TEST
# ---------------------------------------------------------
elif st.session_state.step == "PRACTICE":
    st.subheader("🎯 Phase 4: Targeted Practice & Re-test")
    
    # Filter questions matching weak topics, or use all if no weak topics
    practice_qs = [q for q in questions if q.get("topic") in st.session_state.weak_topics]
    if not practice_qs:
        practice_qs = questions[:3] # Fallback sample

    st.write(f"Re-testing focused on: **{', '.join(st.session_state.weak_topics or ['General Mastery'])}**")
    
    with st.form("retest_form"):
        retest_answers = {}
        for i, q in enumerate(practice_qs):
            q_id = q.get("question_id", str(i+1))
            opts = {
                "A": f"A) {q.get('option_a', '')}",
                "B": f"B) {q.get('option_b', '')}",
                "C": f"C) {q.get('option_c', '')}",
                "D": f"D) {q.get('option_d', '')}"
            }
            st.write(f"**[RE-TEST Q{i+1}] [{q_id}]: {q.get('question')}**")
            retest_answers[i] = st.radio(
                f"Select answer for Q{i+1}:",
                options=list(opts.keys()),
                format_func=lambda x: opts[x],
                key=f"re_{i}",
                index=None
            )
            st.write("---")
            
        submit_retest = st.form_submit_button("Submit Re-test")

    if submit_retest:
        if None in retest_answers.values():
            st.warning("⚠️ Please answer all re-test questions!")
        else:
            rt_correct = sum(1 for i, q in enumerate(practice_qs) if retest_answers[i] == q.get("correct_option", "A"))
            st.session_state.retest_score = round((rt_correct / len(practice_qs)) * 100, 1)
            st.session_state.step = "PROGRESS"
            st.rerun()

# ---------------------------------------------------------
# STEP 5: PROGRESS TRACKING & RETEST COMPARISON
# ---------------------------------------------------------
elif st.session_state.step == "PROGRESS":
    st.subheader("📈 Phase 5: Progress Tracking & Learning Comparison")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Initial Diagnostic Score", f"{st.session_state.diagnostic_score}%")
    with c2:
        st.metric("Targeted Re-test Score", f"{st.session_state.retest_score}%", 
                  delta=f"{round(st.session_state.retest_score - st.session_state.diagnostic_score, 1)}%")

    st.write("---")
    if st.session_state.retest_score >= 60.0:
        st.balloons()
        st.success("🎉 **Adaptive Loop Complete!** Weak topic successfully remediated.")
    else:
        st.warning("⚠️ Further review recommended for remaining weak areas.")

    if st.button("🔄 Restart Diagnostic Cycle"):
        st.session_state.step = "DIAGNOSTIC"
        st.rerun()