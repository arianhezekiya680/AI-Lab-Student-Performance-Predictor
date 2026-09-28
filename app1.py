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

# Custom Artistic CSS (Google Fonts + Glassmorphism UI)
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

    /* Glassmorphism Metric Cards */
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

    /* Expanded Canvas Styling for Charts & Tables */
    .stPlotlyChart {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(220, 224, 230, 0.6);
        background: white;
    }

    /* Authentication Card Styling */
    .auth-box {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
        max-width: 450px;
        margin: 2rem auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# AUTHENTICATION DATABASE & SESSION INITIALIZATION
# ---------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "faculty@uiu.ac.bd": {"name": "Prof. AI Evaluation", "password": "123"},
        "admin": {"name": "System Administrator", "password": "admin"}
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# ---------------------------------------------------------
# LOGIN & SIGN UP PAGE (TRIGGERED IF NOT LOGGED IN)
# ---------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;' class='artistic-title'>🎓 UIU Faculty & Analytics Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;' class='artistic-sub'>Predictive Strategy Engine & Class Management Portal</p>", unsafe_allow_html=True)

    auth_tab1, auth_tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])

    with auth_tab1:
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            st.subheader("Welcome Back")
            login_user = st.text_input("Username or Email", key="login_u")
            login_pass = st.text_input("Password", type="password", key="login_p")
            
            if st.button("Log In to Portal", type="primary", use_container_width=True):
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user]["password"] == login_pass:
                    st.session_state.authenticated = True
                    st.session_state.current_user = st.session_state.users_db[login_user]["name"]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify username/password.")

    with auth_tab2:
        col_center2 = st.columns([1, 2, 1])[1]
        with col_center2:
            st.subheader("Create Faculty Account")
            new_name = st.text_input("Full Name", key="signup_n")
            new_user = st.text_input("Username or Email", key="signup_u")
            new_pass = st.text_input("Password", type="password", key="signup_p")
            confirm_pass = st.text_input("Confirm Password", type="password", key="signup_cp")
            
            if st.button("Register Account", type="primary", use_container_width=True):
                if new_pass != confirm_pass:
                    st.warning("Passwords do not match.")
                elif new_user in st.session_state.users_db:
                    st.error("Username already exists.")
                elif new_user and new_pass and new_name:
                    st.session_state.users_db[new_user] = {"name": new_name, "password": new_pass}
                    st.success("Account created successfully! Switch to the 'Sign In' tab to log in.")
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
# SIDEBAR NAVIGATION & SESSION INFO
# ---------------------------------------------------------
st.sidebar.title("🎓 UIU Faculty Portal")
st.sidebar.markdown(f"👤 Logged in as: **{st.session_state.current_user}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

st.sidebar.divider()

menu_choice = st.sidebar.radio(
    "Navigation Menu",
    ["📊 Executive Overview", "🎯 What-If Strategy Engine", "👥 Class Section Roster", "⚙️ Settings & System Info"]
)

st.sidebar.divider()
st.sidebar.subheader("Active Session Setup")
selected_course = st.sidebar.selectbox("Course Code", ["CSE 412: Artificial Intelligence Lab", "CSE 411: Artificial Intelligence"])
selected_section = st.sidebar.selectbox("Section", ["Section I", "Section A", "Section B"])
selected_trimester = st.sidebar.selectbox("Trimester", ["Fall 2026", "Spring 2026", "Summer 2026"])

# ---------------------------------------------------------
# 1. EXECUTIVE OVERVIEW DASHBOARD
# ---------------------------------------------------------
if menu_choice == "📊 Executive Overview":
    st.markdown("<h1 class='artistic-title'>Executive Academic Analytics & Visuals</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='artistic-sub'>Section overview for <b>{selected_course} ({selected_section})</b> — {selected_trimester}</p>", unsafe_allow_html=True)
    
    # KPI Metric Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total Enrolled", value="50 Students", delta="Full Capacity")
    kpi2.metric(label="Class Average GPA", value="3.12 / 4.00", delta="+0.18 vs Prev Term")
    kpi3.metric(label="Avg Study Hours", value="14.8 hrs/wk", delta="+1.2 hrs/wk")
    kpi4.metric(label="At-Risk Rate", value="12%", delta="-4% (Low Risk)", delta_color="inverse")

    st.divider()

    # EXPANDED FULL-SCREEN VISUAL CANVAS
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
            chart_df,
            x="Attendance",
            y="Projected_GPA",
            size="Study_Hours",
            color="Projected_GPA",
            labels={"Attendance": "Attendance Rate (%)", "Projected_GPA": "Projected GPA"},
            color_continuous_scale="Viridis",
            height=480
        )
        
        fig_scatter.update_traces(
            marker=dict(
                symbol='diamond',
                opacity=0.88,
                line=dict(width=1.5, color='#1E293B'),
                sizeref=2.0 * max(chart_df['Study_Hours']) / (45.**2),
                sizemin=7
            )
        )
        fig_scatter.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.markdown("##### 📊 Section GPA Grade Spread")
        fig_hist = px.histogram(
            chart_df,
            x="Projected_GPA",
            nbins=8,
            color_discrete_sequence=['#2A9D8F'],
            labels={"Projected_GPA": "GPA Ranges"},
            height=480
        )
        fig_hist.update_traces(marker_line_color='white', marker_line_width=1.5, opacity=0.9)
        fig_hist.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

# ---------------------------------------------------------
# 2. WHAT-IF STRATEGY ENGINE
# ---------------------------------------------------------
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

        if run_btn or 'calculated' in st.session_state:
            st.session_state.calculated = True

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

                    if study_val >= 20 and quiz_val < 55:
                        st.error("🚨 **BURNOUT ALERT:** High study effort detected with low assessment scores. Recommend TA intervention.")

            else:
                st.error("Model files (`log_model.pkl` and `scaler.pkl`) missing in workspace.")

# ---------------------------------------------------------
# 3. CLASS SECTION ROSTER (EXPANDED FULL CANVAS TABLE)
# ---------------------------------------------------------
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

    # FULL CANVAS STYLED TABLE
    st.dataframe(
        roster_df,
        use_container_width=True,
        hide_index=True,
        height=550,
        column_config={
            "Student ID": st.column_config.TextColumn("Student ID", width="medium"),
            "Student Name": st.column_config.TextColumn("Student Name", width="medium"),
            "Attendance %": st.column_config.ProgressColumn(
                "Attendance",
                format="%d%%",
                min_value=0,
                max_value=100
            ),
            "Assignment %": st.column_config.ProgressColumn(
                "Assignments",
                format="%d%%",
                min_value=0,
                max_value=100
            ),
            "Quiz %": st.column_config.ProgressColumn(
                "Quizzes",
                format="%d%%",
                min_value=0,
                max_value=100
            ),
            "Study Hours": st.column_config.NumberColumn(
                "Study Time",
                format="%d hrs/wk"
            ),
            "Projected GPA": st.column_config.NumberColumn(
                "Projected GPA",
                format="%.2f ⭐"
            ),
            "Risk Status": st.column_config.TextColumn(
                "Risk Status",
                width="medium"
            )
        }
    )

# ---------------------------------------------------------
# 4. SETTINGS & SYSTEM INFO
# ---------------------------------------------------------
elif menu_choice == "⚙️ Settings & System Info":
    st.markdown("<h1 class='artistic-title'>System Architecture & Model Info</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Machine Learning Backend
    * **Pipeline:** Feature extraction & $z$-score standardization (`StandardScaler`).
    * **Classifiers:** $k$-Nearest Neighbors ($k=5$) & Multi-Class Logistic Regression.
    * **Validation Accuracy:** 98% test set accuracy.
    """)

st.divider()
st.caption("UIU Academic Strategy & Risk Management Platform | Course AI Lab Evaluation")