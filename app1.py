import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# ---------------------------------------------------------
# PAGE CONFIGURATION & ARTISTIC THEME INJECTION
# ---------------------------------------------------------
st.set_page_config(
    page_title="UIU Academic Strategy Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism UI & Google Fonts Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Title Text */
    .artistic-title {
        background: linear-gradient(135deg, #00B4DB 0%, #0083B0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }

    .artistic-sub {
        color: #6C757D;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(220, 224, 230, 0.8);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
        border-color: #00B4DB;
    }

    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(220, 224, 230, 0.6);
        background: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DUAL-ROLE AUTHENTICATION DATABASE & SESSION INITIALIZATION
# ---------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "faculty@uiu.ac.bd": {"name": "Prof. AI Evaluation", "password": "123", "role": "Faculty"},
        "student@uiu.ac.bd": {"name": "Rahim Ahmed (011241001)", "password": "123", "role": "Student"},
        "admin": {"name": "System Administrator", "password": "admin", "role": "Faculty"}
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ---------------------------------------------------------
# LOGIN & SIGN UP PAGE
# ---------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;' class='artistic-title'>🎓 UIU Academic Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;' class='artistic-sub'>Student Goal Planner & Faculty Risk Analytics Engine</p>", unsafe_allow_html=True)

    auth_tab1, auth_tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])

    with auth_tab1:
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            st.subheader("Welcome Back")
            login_user = st.text_input("Email / Username", key="login_u", placeholder="faculty@uiu.ac.bd or student@uiu.ac.bd")
            login_pass = st.text_input("Password", type="password", key="login_p")
            
            st.info("💡 **Demo Credentials:**\n- **Faculty:** `faculty@uiu.ac.bd` | Pass: `123`\n- **Student:** `student@uiu.ac.bd` | Pass: `123`")

            if st.button("Log In to Portal", type="primary", use_container_width=True):
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user]["password"] == login_pass:
                    st.session_state.authenticated = True
                    st.session_state.current_user = st.session_state.users_db[login_user]["name"]
                    st.session_state.user_role = st.session_state.users_db[login_user]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify username/password.")

    with auth_tab2:
        col_center2 = st.columns([1, 2, 1])[1]
        with col_center2:
            st.subheader("Create New Account")
            new_name = st.text_input("Full Name", key="signup_n")
            new_user = st.text_input("UIU Email", key="signup_u")
            new_role = st.selectbox("Account Type", ["Student", "Faculty"], key="signup_role")
            new_pass = st.text_input("Password", type="password", key="signup_p")
            confirm_pass = st.text_input("Confirm Password", type="password", key="signup_cp")
            
            if st.button("Register Account", type="primary", use_container_width=True):
                if new_pass != confirm_pass:
                    st.warning("Passwords do not match.")
                elif new_user in st.session_state.users_db:
                    st.error("Username/Email already exists.")
                elif new_user and new_pass and new_name:
                    st.session_state.users_db[new_user] = {"name": new_name, "password": new_pass, "role": new_role}
                    st.success("Account created successfully! Switch to 'Sign In' tab to log in.")
                else:
                    st.warning("Please fill in all required fields.")

    st.stop()

# ---------------------------------------------------------
# LOAD MODEL & SCALER ARTIFACTS
# ---------------------------------------------------------
@st.cache_resource
def load_ml_artifacts():
    try:
        model = joblib.load('log_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except Exception:
        return None, None

model, scaler = load_ml_artifacts()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & ROLE-BASED CONTROLS
# ---------------------------------------------------------
st.sidebar.title("🎓 UIU Academic Portal")
st.sidebar.markdown(f"👤 **{st.session_state.current_user}**\n\n🏷️ Role: **{st.session_state.user_role}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.user_role = None
    st.rerun()

st.sidebar.divider()

# DYNAMIC NAVIGATION MENU ACCORDING TO ROLE
if st.session_state.user_role == "Student":
    menu_choice = st.sidebar.radio(
        "Student Navigation",
        ["🎯 My Goal & Strategy Planner", "📊 My Performance Trajectory", "⚙️ System Info"]
    )
else:
    menu_choice = st.sidebar.radio(
        "Faculty Navigation",
        ["📊 Executive Class Overview", "🎯 What-If Strategy Engine", "👥 Class Section Roster", "⚙️ System Info"]
    )

st.sidebar.divider()
st.sidebar.subheader("Active Session")
selected_course = st.sidebar.selectbox("Course Code", ["CSE 412: Artificial Intelligence Lab", "CSE 411: Artificial Intelligence"])
selected_section = st.sidebar.selectbox("Section", ["Section I", "Section A", "Section B"])

# =========================================================
# STUDENT VIEW 1: MY GOAL & STRATEGY PLANNER
# =========================================================
if menu_choice == "🎯 My Goal & Strategy Planner":
    st.markdown("<h1 class='artistic-title'>🎯 Personal Academic Goal Planner</h1>", unsafe_allow_html=True)
    st.markdown("<p class='artistic-sub'>Simulate your study metrics and generate an actionable roadmap to hit your target GPA.</p>", unsafe_allow_html=True)

    col_inputs, col_results = st.columns([1, 1], gap="large")

    with col_inputs:
        st.subheader("📥 Enter Your Current Progress")
        att_val = st.slider("Current Attendance Rate (%)", 0, 100, 85)
        assign_val = st.slider("Assignment Score (%)", 0, 100, 80)
        quiz_val = st.slider("Quiz Average (%)", 0, 100, 70)
        study_val = st.slider("Weekly Study Time (hrs/wk)", 0, 30, 12)
        target_gpa_val = st.slider("Your Target GPA Goal", 2.00, 4.00, 3.50, step=0.05)

        run_btn = st.button("🚀 Generate My Improvement Plan", type="primary", use_container_width=True)

    with col_results:
        st.subheader("📊 Your Predicted Outcome")

        if run_btn or 'student_calc' in st.session_state:
            st.session_state.student_calc = True

            if model is not None and scaler is not None:
                raw_vector = pd.DataFrame([[att_val, assign_val, quiz_val, study_val]],
                                          columns=['Attendance_Rate', 'Assignment_Score', 'Quiz_Score', 'Study_Hours'])
                scaled_vector = scaler.transform(raw_vector)
                pass_prob = model.predict_proba(scaled_vector)[0][1] * 100
                proj_gpa = round((pass_prob / 100) * 4.0, 2)

                st.metric(label="Predicted GPA Trajectory", value=f"{proj_gpa:.2f} / 4.00", 
                          delta=f"Goal Gap: {proj_gpa - target_gpa_val:.2f}")

                if proj_gpa >= target_gpa_val:
                    st.success(f"🎉 **GREAT JOB!** You are currently on track to achieve your **{target_gpa_val:.2f} GPA** target.")
                else:
                    st.warning(f"⚠️ **ADJUSTMENT NEEDED:** Your current path gives a **{proj_gpa:.2f} GPA**. Here is how to reach **{target_gpa_val:.2f}**:")
                    
                    target_score = (target_gpa_val / 4.0) * 100
                    current_score = (0.3*att_val) + (0.3*assign_val) + (0.3*quiz_val) + (1.5*study_val)
                    score_gap = target_score - current_score
                    
                    needed_hours = round(study_val + (score_gap / 1.5), 1)
                    needed_quiz = round(quiz_val + (score_gap / 0.3), 1)

                    st.markdown("#### 💡 Recommended Actions:")
                    st.info(f"• **Option 1 (Study Time):** Increase self-study to **{needed_hours} hrs/week**.\n"
                            f"• **Option 2 (Quizzes & Mid):** Target **{min(100.0, needed_quiz)}%** on upcoming exams.")
            else:
                st.error("ML model files (`log_model.pkl` / `scaler.pkl`) missing in folder.")

# =========================================================
# STUDENT VIEW 2: MY PERFORMANCE TRAJECTORY
# =========================================================
elif menu_choice == "📊 My Performance Trajectory":
    st.markdown("<h1 class='artistic-title'>📈 My Learning Analytics</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='artistic-sub'>Personal dashboard for <b>{st.session_state.current_user}</b> in {selected_course}</p>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Attendance", "88%", "+2% safe zone")
    m2.metric("Assignments", "82%", "Submitted 4/4")
    m3.metric("Quiz Average", "71%", "-5% vs class avg")
    m4.metric("Study Hours", "12 hrs/wk", "Recommended: 15 hrs")

    st.divider()

    # Progress breakdown chart
    chart_data = pd.DataFrame({
        'Assessment': ['Attendance', 'Assignments', 'Quizzes', 'Midterm Prep'],
        'Your Score (%)': [88, 82, 71, 78],
        'Class Average (%)': [82, 79, 75, 72]
    })
    
    fig = px.bar(chart_data, x='Assessment', y=['Your Score (%)', 'Class Average (%)'],
                 barmode='group', height=400, title="Your Progress vs Class Benchmark")
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FACULTY VIEW 1: EXECUTIVE CLASS OVERVIEW
# =========================================================
elif menu_choice == "📊 Executive Class Overview":
    st.markdown("<h1 class='artistic-title'>Executive Academic Analytics & Visuals</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='artistic-sub'>Section overview for <b>{selected_course} ({selected_section})</b></p>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total Enrolled", value="50 Students", delta="Full Capacity")
    kpi2.metric(label="Class Average GPA", value="3.12 / 4.00", delta="+0.18 vs Prev Term")
    kpi3.metric(label="Avg Study Hours", value="14.8 hrs/wk", delta="+1.2 hrs/wk")
    kpi4.metric(label="At-Risk Rate", value="12%", delta="-4% (Low Risk)", delta_color="inverse")

    st.divider()

    np.random.seed(42)
    attendance_data = np.random.uniform(55, 98, 50)
    quiz_data = np.random.uniform(45, 95, 50)
    study_data = np.random.uniform(3, 28, 50)
    gpa_data = np.clip(np.round(((0.3*attendance_data + 0.3*quiz_data + 1.5*study_data)/100)*4.0, 2), 0.0, 4.0)

    chart_df = pd.DataFrame({
        'Student_ID': [f"011241{i:03d}" for i in range(1, 51)],
        'Attendance': attendance_data,
        'Quiz_Score': quiz_data,
        'Study_Hours': study_data,
        'Projected_GPA': gpa_data
    })

    col_chart1, col_chart2 = st.columns([1.1, 0.9], gap="medium")

    with col_chart1:
        st.markdown("##### 💎 Attendance vs. GPA Trajectory")
        fig_scatter = px.scatter(
            chart_df, x="Attendance", y="Projected_GPA", size="Study_Hours", color="Projected_GPA",
            labels={"Attendance": "Attendance Rate (%)", "Projected_GPA": "Projected GPA"},
            color_continuous_scale="Viridis", height=450
        )
        fig_scatter.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.markdown("##### 📊 Section GPA Grade Spread")
        fig_hist = px.histogram(
            chart_df, x="Projected_GPA", nbins=8, color_discrete_sequence=['#2A9D8F'],
            labels={"Projected_GPA": "GPA Ranges"}, height=450
        )
        fig_hist.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

# =========================================================
# FACULTY VIEW 2: WHAT-IF STRATEGY ENGINE
# =========================================================
elif menu_choice == "🎯 What-If Strategy Engine":
    st.markdown("<h1 class='artistic-title'>\"What-If\" Goal-Seek Strategy Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='artistic-sub'>Simulate student inputs and generate automated action plans to reach target GPAs.</p>", unsafe_allow_html=True)

    col_inputs, col_results = st.columns([1, 1], gap="large")

    with col_inputs:
        st.subheader("📥 Student Metrics Input")
        att_val = st.slider("Current Attendance Rate (%)", 0, 100, 80)
        assign_val = st.slider("Current Assignment Score (%)", 0, 100, 75)
        quiz_val = st.slider("Current Quiz Score (%)", 0, 100, 65)
        study_val = st.slider("Weekly Study Hours (hrs/wk)", 0, 30, 12)
        target_gpa_val = st.slider("Desired Target GPA Goal", 2.00, 4.00, 3.50, step=0.05)

        run_btn = st.button("🚀 Calculate Strategy Plan", type="primary", use_container_width=True)

    with col_results:
        st.subheader("🎯 Diagnostic Strategy Output")

        if run_btn or 'faculty_calc' in st.session_state:
            st.session_state.faculty_calc = True

            if model is not None and scaler is not None:
                raw_vector = pd.DataFrame([[att_val, assign_val, quiz_val, study_val]],
                                          columns=['Attendance_Rate', 'Assignment_Score', 'Quiz_Score', 'Study_Hours'])
                scaled_vector = scaler.transform(raw_vector)
                pass_prob = model.predict_proba(scaled_vector)[0][1] * 100
                proj_gpa = round((pass_prob / 100) * 4.0, 2)

                st.metric(label="Projected Current GPA", value=f"{proj_gpa:.2f} / 4.00", 
                          delta=f"Goal: {target_gpa_val:.2f} (Gap: {proj_gpa - target_gpa_val:.2f})")

                if proj_gpa >= target_gpa_val:
                    st.success(f"✅ **ON TRACK:** Trajectory meets or exceeds target goal of **{target_gpa_val:.2f} GPA**.")
                else:
                    st.warning(f"⚠️ **ACTION NEEDED:** Projected GPA ({proj_gpa:.2f}) is below target goal ({target_gpa_val:.2f}).")
                    
                    target_score = (target_gpa_val / 4.0) * 100
                    current_score = (0.3*att_val) + (0.3*assign_val) + (0.3*quiz_val) + (1.5*study_val)
                    score_gap = target_score - current_score
                    
                    needed_hours = round(study_val + (score_gap / 1.5), 1)
                    needed_quiz = round(quiz_val + (score_gap / 0.3), 1)

                    st.markdown("#### 📋 Recommended Action Plan:")
                    st.info(f"• **Option A (Study Boost):** Increase study time to **{needed_hours} hrs/wk**.\n"
                            f"• **Option B (Assessment Target):** Raise remaining quiz marks to **{min(100.0, needed_quiz)}%**.")
            else:
                st.error("Model files missing in workspace.")

# =========================================================
# FACULTY VIEW 3: CLASS SECTION ROSTER
# =========================================================
elif menu_choice == "👥 Class Section Roster":
    st.markdown("<h1 class='artistic-title'>Class Roster & Risk Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p class='artistic-sub'>Batch performance monitoring with visual progress bars and risk tiers.</p>", unsafe_allow_html=True)

    np.random.seed(101)
    roster_df = pd.DataFrame({
        'Student ID': [f"0112410{i:02d}" for i in range(1, 16)],
        'Student Name': [f"Student {i}" for i in range(1, 16)],
        'Attendance %': np.random.randint(60, 100, 15),
        'Assignment %': np.random.randint(50, 98, 15),
        'Quiz %': np.random.randint(40, 95, 15),
        'Study Hours': np.random.randint(4, 25, 15),
    })

    scores = (0.3*roster_df['Attendance %']) + (0.3*roster_df['Assignment %']) + (0.3*roster_df['Quiz %']) + (1.5*roster_df['Study Hours'])
    roster_df['Projected GPA'] = np.clip(np.round((scores / 100) * 4.0, 2), 0.0, 4.0)
    roster_df['Risk Status'] = np.where(roster_df['Projected GPA'] >= 3.0, '🟢 Safe', 
                               np.where(roster_df['Projected GPA'] >= 2.2, '🟡 Moderate', '🔴 High Risk'))

    st.dataframe(
        roster_df,
        use_container_width=True,
        hide_index=True,
        height=550,
        column_config={
            "Student ID": st.column_config.TextColumn("Student ID", width="medium"),
            "Student Name": st.column_config.TextColumn("Student Name", width="medium"),
            "Attendance %": st.column_config.ProgressColumn("Attendance", format="%d%%", min_value=0, max_value=100),
            "Assignment %": st.column_config.ProgressColumn("Assignments", format="%d%%", min_value=0, max_value=100),
            "Quiz %": st.column_config.ProgressColumn("Quizzes", format="%d%%", min_value=0, max_value=100),
            "Study Hours": st.column_config.NumberColumn("Study Time", format="%d hrs/wk"),
            "Projected GPA": st.column_config.NumberColumn("Projected GPA", format="%.2f ⭐"),
            "Risk Status": st.column_config.TextColumn("Risk Status", width="medium")
        }
    )

# =========================================================
# COMMON VIEW: SYSTEM INFO
# =========================================================
elif menu_choice == "⚙️ System Info":
    st.markdown("<h1 class='artistic-title'>System Architecture & Model Info</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### Machine Learning Backend
    * **Pipeline:** Feature extraction & $z$-score standardization (`StandardScaler`).
    * **Classifiers:** Multi-Class Logistic Regression & $k$-Nearest Neighbors ($k=5$).
    * **Role Adaptability:** Custom Student & Faculty views driven by Session State RBAC.
    """)

st.divider()
st.caption("UIU Dual-Perspective Academic Strategy & Risk Management Platform | AI Lab Project")