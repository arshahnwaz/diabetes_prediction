from gc import enable

import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from google import genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Health Dashboard", layout="wide")

# ---------------- CSS (FULL UI) ----------------
st.markdown("""
<style>

/* 🌈 Animated Multicolor Background */
.stApp {
    background: linear-gradient(
        -45deg,
        #4f46e5,
        #7c3aed,
        #9333ea,
        #3b82f6,
        #22c55e
    );
    background-size: 400% 400%;
    animation: gradientMove 5s ease infinite;
    color: white;
}

/* Gradient Animation */
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a,#1e293b);
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(20px);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}

/* Hover Glow */
.card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 0 30px rgba(124,58,237,0.8);
}

/* KPI Cards (colorful) */
.kpi {
    background: linear-gradient(135deg,#22c55e,#3b82f6,#7c3aed);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    font-weight: bold;
    color: white;
    box-shadow: 0 5px 25px rgba(124,58,237,0.5);
}

/* Title gradient text */
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#3b82f6,#7c3aed);
    border-radius: 12px;
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px 20px;
}

/* Hover */
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#16a34a,#2563eb,#6d28d9);
}

/* Inputs */
input, .stTextInput, .stNumberInput {
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #7c3aed;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI ----------------
client = genai.Client(api_key="AIzaSyAs9sdSCCiYikiTtmFQ91uhIeEbNzqA9I0")

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------------- LOGIN PAGE ----------------
def login():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)

        st.markdown("<div class='title'>🔐 Login</div>", unsafe_allow_html=True)

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u == "admin" and p == "1234":
                st.session_state.page = "dashboard"
            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- DASHBOARD ----------------
def dashboard():
    # Sidebar
    st.sidebar.markdown("## 🩺 AI Health")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966483.png", width=60)

    st.sidebar.markdown("<div class='sidebar-card'>👤 Admin User</div>", unsafe_allow_html=True)

    page = st.sidebar.radio("", ["🏠 Home", "🧠 Prediction", "📄 Report"], label_visibility="collapsed")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "login"

    model = pickle.load(open("diabetes.pkl", "rb"))


    def ai(glucose, bmi, bp, age, prob):

        prompt = f"""
        Patient:
        Glucose={glucose}, BMI={bmi}, BP={bp}, Age={age}
        Risk={round(prob * 100, 2)}%

        Give:
            1. English Summary
            2. Hindi Summary
            3. Diagnosis
            4. Precautions

            Hindi simple aur easy ho
        """

        try:
            res = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )

            try:
                return res.text
            except:
                return res.candidates[0].content.parts[0].text

        except Exception as e:
            return "⚠️ AI service is currently busy. Please try again in a few seconds."


    # Diet plan
    def ai_diet(glucose, bmi, prob):

        prompt = f"""
        Patient:
        Glucose={glucose}, BMI={bmi}, Risk={round(prob * 100, 2)}%

            Provide diet in:
                1. English
                2. Hindi

                Include:
                    - Breakfast
                    - Lunch
                    - Dinner
                    - Foods to avoid
            """

        try:
            res = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt
            )
            return res.text
        except:
            return "Eat low sugar, high fiber, balanced meals."

    # ---------------- HOME ----------------
    if page == "🏠 Home":

        st.markdown("<div class='title'>🩺 Welcome to AI Health System</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 This system predicts diabetes risk using Machine Learning and AI.</div>",
                    unsafe_allow_html=True)

        st.subheader("🚀 Features")

        col1, col2, col3 = st.columns(3)

        col1.markdown("""
        <div class='card'>
        🧠 <b>AI Diagnosis</b><br>
        Smart ML-based prediction
        </div>
        """, unsafe_allow_html=True)

        col2.markdown("""
        <div class='card'>
        📊 <b>Dashboard</b><br>
        Graph + analytics view
        </div>
        """, unsafe_allow_html=True)

        col3.markdown("""
        <div class='card'>
        🎯 <b>Risk Meter</b><br>
        Speedometer risk %
        </div>
        """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)

        col4.markdown("""
        <div class='card'>
        🤖 <b>AI Summary</b><br>
        English + Hindi medical report
        </div>
        """, unsafe_allow_html=True)

        col5.markdown("""
        <div class='card'>
        🥗 <b>Diet Plan</b><br>
        Personalized meal suggestions
        </div>
        """, unsafe_allow_html=True)

        col6.markdown("""
        <div class='card'>
        📄 <b>PDF Report</b><br>
        Download full report
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.success("👉 Go to Prediction tab to analyze your health")

    # ---------------- PREDICTION ----------------
    elif page == "🧠 Prediction":

        st.markdown("<div class='title'>🧠 AI Based Diabetes Prediction</div>", unsafe_allow_html=True)

        with st.form("form"):

            st.markdown("<div class='card'>", unsafe_allow_html=True)

            name = st.text_input("Name")
            gender = st.selectbox("Gender", ["Male", "Female"])
            age = st.number_input("Age", 1, 100, 25)

            col1, col2 = st.columns(2)

            with col1:
                # Session init
                if "preg" not in st.session_state:
                    st.session_state.preg = 1

                if gender == "Female":
                    preg = st.number_input("Pregnancies", 1, 17, 1)
                if gender == "Male":
                    preg = st.number_input("Pregnancies", 0, 17, 0)

                glucose = st.slider("Glucose", 50, 200, 120)
                bp = st.slider("BP", 40, 122, 70)

            with col2:
                insulin = st.slider("Insulin", 15, 846, 80)
                bmi = st.slider("BMI", 10.0, 67.0, 25.0)
                dpf = st.slider("DPF", 0.0, 2.5, 0.5)

            st.markdown("</div>", unsafe_allow_html=True)

            submit = st.form_submit_button("Predict")

        if submit:


            features = [
                preg, glucose, bp, 20, insulin, bmi, dpf, age,
                1 if 30 <= bmi < 35 else 0,
                1 if 35 <= bmi < 40 else 0,
                1 if bmi >= 40 else 0,
                1 if 25 <= bmi < 30 else 0,
                1 if bmi < 18.5 else 0,
                1 if 16 <= insulin <= 166 else 0,
                1 if glucose < 70 else 0,
                1 if 70 <= glucose < 100 else 0,
                1 if 100 <= glucose < 126 else 0,
                1 if glucose >= 126 else 0
            ]


            data = np.array([features])
            pred = model.predict(data)
            prob = model.predict_proba(data)[0][1]

            # KPI
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div class='kpi'>💉 Glucose<br>{glucose}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='kpi'>⚖️ BMI<br>{bmi}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='kpi'>🎯 Risk<br>{round(prob * 100, 2)}%</div>", unsafe_allow_html=True)

            # Gauge
            # -------- PLOTLY GRAPH --------
            fig = go.Figure()

            # Bar (user values)
            fig.add_trace(go.Bar(
                x=["Glucose", "BP", "BMI", "Age"],
                y=[glucose, bp, bmi, age],
                name="Your Values",
                marker=dict(color="#6366f1")
            ))

            # Line (normal values)
            fig.add_trace(go.Scatter(
                x=["Glucose", "BP", "BMI", "Age"],
                y=[100, 80, 25, 30],
                mode="lines+markers",
                name="Normal Range",
                line=dict(color="#22c55e", width=3)
            ))

            fig.update_layout(
                title="📊 Health Comparison",
                template="plotly_dark"
            )

            # -------- SPEEDOMETER (GAUGE) --------
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={'text': "🎯 Diabetes Risk %"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#ef4444" if prob > 0.7 else "#22c55e"},
                    'steps': [
                        {'range': [0, 30], 'color': "#22c55e"},
                        {'range': [30, 70], 'color': "#facc15"},
                        {'range': [70, 100], 'color': "#ef4444"}
                    ],
                }
            ))

            # -------- SIDE-BY-SIDE LAYOUT --------
            colL, colR = st.columns([2, 1])

            with colL:
                st.plotly_chart(fig, use_container_width=True)

            with colR:
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Result
            if pred[0] == 1:
                st.markdown("<div class='card'>⚠️ High Risk</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='card'>✅ Low Risk</div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write(ai(glucose, bmi, bp, age, prob))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🥗 AI Diet Plan")

            with st.spinner("Generating diet plan..."):
                st.write(ai_diet(glucose, bmi, prob))

            st.markdown("</div>", unsafe_allow_html=True)


    # ---------------- REPORT ----------------
    elif page == "📄 Report":

        st.markdown("<div class='title'>📄 Report</div>", unsafe_allow_html=True)

        st.write("Generate report after prediction")


# ---------------- ROUTER ----------------
if st.session_state.page == "login":
    login()
else:
    dashboard()