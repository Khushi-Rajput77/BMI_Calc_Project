import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── FULL CSS + ANIMATIONS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── HIDE ALL STREAMLIT CHROME ── */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stDeployButton"],
button[title="View fullscreen"],
.stActionButton,
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebarNav"],
div[data-testid="stSidebarNav"],
.css-1rs6os, .css-17ziqus,
iframe[title="st_mods"],
#bui3, .eyeIcon,
div[aria-label="More options"],
div[aria-label="Deploy"],
[data-testid="baseButton-headerNoPadding"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
}

/* ── ROOT ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container {
    background: #0b0f0e !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, rgba(46,204,113,0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(39,174,96,0.04) 0%, transparent 50%),
                #0b0f0e !important;
}

.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1200px !important;
}

/* ── ANIMATED PARTICLES BACKGROUND ── */
body::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        radial-gradient(circle, rgba(46,204,113,0.15) 1px, transparent 1px),
        radial-gradient(circle, rgba(46,204,113,0.08) 1px, transparent 1px);
    background-size: 60px 60px, 120px 120px;
    background-position: 0 0, 30px 30px;
    animation: gridFloat 20s linear infinite;
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

@keyframes gridFloat {
    0%   { transform: translateY(0px); }
    100% { transform: translateY(-60px); }
}

/* ── HEADER HERO ── */
.hero-header {
    text-align: center;
    padding: 3rem 1rem 2.5rem;
    position: relative;
    overflow: hidden;
}

.hero-glow {
    position: absolute;
    top: -40px; left: 50%; transform: translateX(-50%);
    width: 500px; height: 200px;
    background: radial-gradient(ellipse, rgba(46,204,113,0.25) 0%, transparent 70%);
    pointer-events: none;
    animation: pulseGlow 4s ease-in-out infinite;
}

@keyframes pulseGlow {
    0%, 100% { opacity: 0.6; transform: translateX(-50%) scale(1); }
    50%       { opacity: 1;   transform: translateX(-50%) scale(1.1); }
}

.hero-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.6rem;
    animation: iconBounce 3s ease-in-out infinite;
}

@keyframes iconBounce {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}

.hero-title {
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #2ecc71 0%, #52e890 40%, #27ae60 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    animation: fadeSlideDown 0.8s cubic-bezier(.16,1,.3,1) both;
}

.hero-sub {
    color: #5a7a65;
    font-size: 1rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    animation: fadeSlideDown 0.8s 0.15s cubic-bezier(.16,1,.3,1) both;
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: none; }
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(46,204,113,0.1) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 4px !important;
    margin-bottom: 1.5rem !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4a7a5a !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    transition: all 0.25s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
    color: #0b0f0e !important;
    box-shadow: 0 4px 20px rgba(46,204,113,0.4) !important;
}

/* ── CARDS ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(46,204,113,0.12);
    border-radius: 20px;
    padding: 28px;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s cubic-bezier(.16,1,.3,1) both;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(46,204,113,0.4), transparent);
}

.card:hover {
    border-color: rgba(46,204,113,0.3);
    box-shadow: 0 8px 40px rgba(46,204,113,0.08);
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: none; }
}

.card-title {
    color: #2ecc71;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── BMI RESULT DISPLAY ── */
.bmi-result-card {
    background: linear-gradient(145deg, rgba(46,204,113,0.06), rgba(39,174,96,0.03));
    border: 1px solid rgba(46,204,113,0.25);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s cubic-bezier(.16,1,.3,1) both;
}

.bmi-result-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(46,204,113,0.5), transparent);
}

.bmi-number {
    font-size: 5rem;
    font-weight: 900;
    letter-spacing: -3px;
    line-height: 1;
    background: linear-gradient(135deg, #2ecc71, #52e890);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: countUp 0.8s cubic-bezier(.16,1,.3,1) both;
}

@keyframes countUp {
    from { opacity: 0; transform: scale(0.7); }
    to   { opacity: 1; transform: scale(1); }
}

.bmi-category {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 8px;
    color: #e0ffe8;
}

.bmi-emoji { font-size: 1.6rem; }

/* ── BMI SCALE BAR ── */
.bmi-scale {
    margin: 20px 0;
    position: relative;
}

.bmi-scale-bar {
    height: 10px;
    border-radius: 10px;
    background: linear-gradient(90deg,
        #3498db 0%, #3498db 22%,       /* underweight */
        #2ecc71 22%, #2ecc71 48%,      /* normal */
        #f39c12 48%, #f39c12 67%,      /* overweight */
        #e74c3c 67%, #e74c3c 100%);    /* obese */
    position: relative;
    overflow: visible;
}

.bmi-scale-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 22px; height: 22px;
    background: #fff;
    border: 3px solid #2ecc71;
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(46,204,113,0.3), 0 4px 12px rgba(0,0,0,0.4);
    transition: left 0.8s cubic-bezier(.16,1,.3,1);
}

.bmi-scale-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 0.72rem;
    color: #4a7a5a;
    font-weight: 500;
}

/* ── RANGE CARD ── */
.range-card {
    background: rgba(46,204,113,0.04);
    border: 1px solid rgba(46,204,113,0.12);
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 16px;
}

.range-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.88rem;
    color: #8ab89a;
}

.range-item:last-child { border-bottom: none; }
.range-value { color: #2ecc71; font-weight: 700; }
.range-highlight { color: #fff; font-weight: 600; }

/* ── INPUTS ── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stTextInput input,
input[type="text"],
input[type="number"] {
    background: #1a2620 !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(46,204,113,0.25) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    caret-color: #2ecc71 !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus,
input[type="text"]:focus,
input[type="number"]:focus {
    border-color: rgba(46,204,113,0.6) !important;
    box-shadow: 0 0 0 3px rgba(46,204,113,0.12) !important;
    outline: none !important;
    color: #ffffff !important;
    background: #1e2e28 !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
input[type="text"]::placeholder {
    color: #4a6a56 !important;
    opacity: 1 !important;
}

/* Selectbox text */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background: #1a2620 !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(46,204,113,0.25) !important;
    border-radius: 12px !important;
}

/* Selectbox dropdown option text */
[data-baseweb="menu"] li,
[role="option"] {
    background: #131f1a !important;
    color: #e0ffe8 !important;
}

[data-baseweb="menu"] li:hover,
[role="option"]:hover {
    background: rgba(46,204,113,0.15) !important;
    color: #ffffff !important;
}

/* Number input +/- buttons */
.stNumberInput button {
    background: #1e3028 !important;
    color: #2ecc71 !important;
    border: 1px solid rgba(46,204,113,0.2) !important;
}

.stNumberInput button:hover {
    background: rgba(46,204,113,0.2) !important;
}

label, .stNumberInput label, .stTextInput label, .stSelectbox label {
    color: #52a870 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
    color: #0b0f0e !important;
    border: none !important;
    padding: 14px 32px !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(46,204,113,0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.25s;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(46,204,113,0.5) !important;
}

.stButton > button:hover::after { opacity: 1 !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── ALERTS ── */
.stSuccess {
    background: rgba(46,204,113,0.08) !important;
    border-left: 4px solid #2ecc71 !important;
    border-radius: 10px !important;
    color: #a0ffb8 !important;
}

.stInfo {
    background: rgba(52,152,219,0.08) !important;
    border-left: 4px solid #3498db !important;
    border-radius: 10px !important;
    color: #a0d4ff !important;
}

.stError {
    background: rgba(231,76,60,0.08) !important;
    border-left: 4px solid #e74c3c !important;
    border-radius: 10px !important;
    color: #ffb3b3 !important;
}

.stWarning {
    background: rgba(243,156,18,0.08) !important;
    border-left: 4px solid #f39c12 !important;
    border-radius: 10px !important;
    color: #ffd999 !important;
}

/* ── METRICS ── */
[data-testid="stMetricValue"] {
    color: #2ecc71 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #4a7a5a !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(46,204,113,0.1) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(46,204,113,0.1) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ── TIPS GRID ── */
.tips-grid { display: flex; flex-direction: column; gap: 10px; margin-top: 12px; }

.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: rgba(46,204,113,0.04);
    border: 1px solid rgba(46,204,113,0.1);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.9rem;
    color: #9abfab;
    animation: fadeInUp 0.5s cubic-bezier(.16,1,.3,1) both;
}

.tip-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }

/* ── GUIDE SECTION ── */
.guide-section {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(46,204,113,0.08);
    border-radius: 16px;
    padding: 24px 28px;
    margin-top: 20px;
}

.guide-title {
    color: #2ecc71;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.guide-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    font-size: 0.875rem;
    color: #6a9a7a;
    line-height: 1.5;
}

.guide-item:last-child { border-bottom: none; }
.guide-dot { color: #2ecc71; font-size: 0.5rem; margin-top: 6px; flex-shrink: 0; }

/* ── DIVIDER ── */
.green-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(46,204,113,0.3), transparent);
    margin: 24px 0;
}

/* ── HEADING OVERRIDE ── */
h1, h2, h3 {
    font-family: 'Inter', sans-serif !important;
}

h2 {
    color: #2ecc71 !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 1.2rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 1px solid rgba(46,204,113,0.15) !important;
}

h3 {
    color: #52e890 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.8rem !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0b0f0e; }
::-webkit-scrollbar-thumb { background: rgba(46,204,113,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(46,204,113,0.5); }

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 1.2rem 1rem 3rem !important; }
    .hero-title { font-size: 2.2rem !important; }
    .bmi-number { font-size: 3.5rem; }
}
</style>
""", unsafe_allow_html=True)


# ── FUNCTIONS ────────────────────────────────────────────────────────────────
def calculate_bmi(weight, height):
    if height <= 0:
        return None
    return round(weight / (height ** 2), 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "You may need to gain weight. Consider consulting a nutritionist.", "🔵", "#3498db"
    elif bmi < 25:
        return "Normal Weight", "Excellent! You have a healthy weight. Keep it up!", "🟢", "#2ecc71"
    elif bmi < 30:
        return "Overweight", "Consider a balanced diet and regular physical activity.", "🟡", "#f39c12"
    else:
        return "Obese", "Please consult a healthcare professional for guidance.", "🔴", "#e74c3c"

def bmi_to_scale_pct(bmi):
    # Map BMI 10–40 → 0–100% on bar
    bmi_clamped = max(10, min(40, bmi))
    return (bmi_clamped - 10) / 30 * 100

def get_health_tips(bmi):
    if bmi < 18.5:
        return [
            ("🥑", "Eat calorie-dense, nutrient-rich foods like nuts, avocado, and legumes"),
            ("💪", "Include resistance and strength training to build lean muscle"),
            ("🥛", "Prioritize high-protein foods in every meal"),
            ("🩺", "Consult a nutritionist for a personalized plan"),
        ]
    elif bmi < 25:
        return [
            ("🏃", "Maintain 150 min of moderate cardio per week"),
            ("🥦", "Keep eating balanced, whole-food meals"),
            ("💧", "Stay well-hydrated — aim for 2–3 litres daily"),
            ("😴", "Prioritize 7–9 hours of quality sleep"),
        ]
    elif bmi < 30:
        return [
            ("🚶", "Start with 30 minutes of daily walking"),
            ("🥤", "Replace sugary drinks with water or herbal tea"),
            ("🥗", "Increase vegetables and reduce processed foods"),
            ("📓", "Track meals to build awareness of your habits"),
        ]
    else:
        return [
            ("🩺", "Consult a doctor before starting any new program"),
            ("🏊", "Begin with low-impact exercise like swimming or cycling"),
            ("📊", "Track food intake to identify patterns"),
            ("👥", "Consider joining a structured health program"),
        ]

DATA_FILE = "bmi_data.json"

def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_bmi_record(username, weight, height, bmi, category):
    data = load_user_data()
    if username not in data:
        data[username] = {"records": []}
    data[username]["records"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "category": category
    })
    save_user_data(data)

def get_user_records(username):
    data = load_user_data()
    return data.get(username, {}).get("records", [])

def get_all_users():
    return list(load_user_data().keys())

def styled_chart(fig, ax_list=None):
    fig.patch.set_facecolor('#0d1410')
    axes = ax_list if ax_list else [fig.get_axes()[0]]
    for ax in axes:
        ax.set_facecolor('#111a14')
        ax.tick_params(colors='#4a7a5a', labelsize=9)
        ax.xaxis.label.set_color('#4a7a5a')
        ax.yaxis.label.set_color('#4a7a5a')
        ax.title.set_color('#2ecc71')
        for spine in ax.spines.values():
            spine.set_edgecolor('#1e3328')
        ax.grid(True, alpha=0.12, color='#2ecc71', linestyle='--', linewidth=0.5)
    return fig


# ── HERO HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-glow"></div>
    <span class="hero-icon">💚</span>
    <div class="hero-title">BMI Calculator</div>
    <div class="hero-sub">Track, analyse & improve your body mass index</div>
</div>
""", unsafe_allow_html=True)


# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊  Calculator", "📈  History", "📉  Statistics", "❤️  Health Tips"])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – CALCULATOR
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Calculate Your BMI")

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card"><div class="card-title">👤 Your Information</div>', unsafe_allow_html=True)

        users = get_all_users()
        if users:
            username_choice = st.selectbox("User Profile", ["➕ Create New User"] + users, key="user_select")
            if username_choice == "➕ Create New User":
                username = st.text_input("New Username", placeholder="e.g. Alex", key="new_user")
            else:
                username = username_choice
        else:
            username = st.text_input("Your Username", value="User1", key="username_input")

        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.5)
        height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, value=1.75, step=0.01)

        save_btn = st.button("💾  Save Record", key="save_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if username and weight > 0 and height > 0:
            bmi = calculate_bmi(weight, height)
            category, advice, emoji, color = get_bmi_category(bmi)
            pct = bmi_to_scale_pct(bmi)

            # BMI Result card
            st.markdown(f"""
            <div class="bmi-result-card">
                <div class="bmi-number">{bmi}</div>
                <div class="bmi-category"><span class="bmi-emoji">{emoji}</span> {category}</div>
            </div>
            """, unsafe_allow_html=True)

            # Scale bar
            st.markdown(f"""
            <div class="bmi-scale" style="margin-top:18px;">
                <div class="bmi-scale-bar">
                    <div class="bmi-scale-marker" style="left:{pct}%;"></div>
                </div>
                <div class="bmi-scale-labels">
                    <span>Underweight<br>&lt;18.5</span>
                    <span style="text-align:center">Normal<br>18.5–24.9</span>
                    <span style="text-align:center">Overweight<br>25–29.9</span>
                    <span style="text-align:right">Obese<br>≥30</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.info(f"💡 {advice}")

            # Healthy weight range
            healthy_min = round(18.5 * (height ** 2), 1)
            healthy_max = round(24.9 * (height ** 2), 1)

            st.markdown(f"""
            <div class="range-card">
                <div class="range-item">
                    <span>Healthy min</span><span class="range-value">{healthy_min} kg</span>
                </div>
                <div class="range-item">
                    <span>Healthy max</span><span class="range-value">{healthy_max} kg</span>
                </div>
                <div class="range-item">
                    <span>Your weight</span><span class="range-highlight">{weight} kg</span>
                </div>
                <div class="range-item" style="border:none">
                    <span>Diff to healthy range</span>
                    <span class="range-value">{
                        "✅ In range" if healthy_min <= weight <= healthy_max
                        else f"{'↓' if weight < healthy_min else '↑'} {abs(round(weight - (healthy_min if weight < healthy_min else healthy_max), 1))} kg"
                    }</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if save_btn:
                if username and username not in ("➕ Create New User", ""):
                    add_bmi_record(username, weight, height, bmi, category)
                    st.success(f"✅ Record saved for **{username}**!")
                else:
                    st.error("Please enter a valid username before saving.")
        else:
            st.info("Enter your details on the left to see your BMI result.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – HISTORY
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("BMI History")

    users = get_all_users()
    if users:
        sel_user = st.selectbox("Select User", users, key="history_user")
        records  = get_user_records(sel_user)

        if records:
            st.subheader(f"{sel_user}'s Records")
            df = pd.DataFrame(records)
            df.columns = [c.title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)
            st.subheader("Latest Snapshot")

            latest = records[-1]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📅 Date",        latest["date"].split()[0])
            c2.metric("⚖️ Weight (kg)", latest["weight"])
            c3.metric("📏 Height (m)",  latest["height"])
            c4.metric("🔢 BMI",         latest["bmi"])
        else:
            st.info("No records yet. Head to the Calculator tab to add one!")
    else:
        st.info("No users found. Create a user in the Calculator tab first.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 – STATISTICS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("Statistics & Trends")

    users = get_all_users()
    if users:
        sel_user = st.selectbox("Select User", users, key="stats_user")
        records  = get_user_records(sel_user)

        if len(records) >= 2:
            bmis    = [r["bmi"]    for r in records]
            weights = [r["weight"] for r in records]
            dates   = [r["date"].split()[0] for r in records]

            # ── Summary metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📊 Avg BMI",       f"{sum(bmis)/len(bmis):.2f}")
            c2.metric("📉 Min BMI",        f"{min(bmis):.2f}")
            c3.metric("📈 Max BMI",        f"{max(bmis):.2f}")
            c4.metric("🗂️ Total Records",  len(records))

            trend = bmis[-1] - bmis[0]
            trend_msg = (
                f"📈 BMI increased by **{abs(trend):.2f}** since first record." if trend > 0
                else f"📉 BMI decreased by **{abs(trend):.2f}** since first record — great progress!" if trend < 0
                else "→ BMI unchanged since first record."
            )
            st.info(trend_msg)

            st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

            # ── BMI Trend chart
            st.subheader("BMI Trend Over Time")
            fig1, ax1 = plt.subplots(figsize=(11, 4))
            styled_chart(fig1, [ax1])

            x = np.arange(len(dates))
            ax1.fill_between(x, bmis, alpha=0.08, color='#2ecc71')
            ax1.plot(x, bmis, marker='o', lw=2.5, ms=8, color='#2ecc71', zorder=3, label='BMI')
            ax1.axhspan(18.5, 24.9, alpha=0.06, color='#2ecc71', label='Healthy range')
            ax1.axhline(18.5, color='#3498db',  ls='--', lw=1, alpha=0.5)
            ax1.axhline(25,   color='#f39c12',  ls='--', lw=1, alpha=0.5)
            ax1.axhline(30,   color='#e74c3c',  ls='--', lw=1, alpha=0.5)
            ax1.set_xticks(x); ax1.set_xticklabels(dates, rotation=40, ha='right', fontsize=8)
            ax1.set_ylabel('BMI', fontsize=10); ax1.set_xlabel('')
            ax1.set_title('BMI Progression', fontsize=13, fontweight='bold', pad=12)
            patches = [mpatches.Patch(color=c, label=l) for c,l in [('#3498db','Underweight'),('#2ecc71','Normal'),('#f39c12','Overweight'),('#e74c3c','Obese')]]
            ax1.legend(handles=patches, loc='upper right', facecolor='#111a14', edgecolor='#1e3328', labelcolor='#8ab89a', fontsize=8)
            plt.tight_layout()
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)

            # ── Weight Trend chart
            st.subheader("Weight Trend Over Time")
            fig2, ax2 = plt.subplots(figsize=(11, 4))
            styled_chart(fig2, [ax2])

            ax2.fill_between(x, weights, alpha=0.1, color='#52e890')
            ax2.plot(x, weights, marker='s', lw=2.5, ms=7, color='#52e890', zorder=3, label='Weight')
            ax2.set_xticks(x); ax2.set_xticklabels(dates, rotation=40, ha='right', fontsize=8)
            ax2.set_ylabel('Weight (kg)', fontsize=10); ax2.set_xlabel('')
            ax2.set_title('Weight Progression', fontsize=13, fontweight='bold', pad=12)
            ax2.legend(facecolor='#111a14', edgecolor='#1e3328', labelcolor='#8ab89a', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

        elif len(records) == 1:
            st.info("Add at least 2 records to unlock trend charts!")
        else:
            st.info("No records found for this user.")
    else:
        st.info("No users found. Create a user in the Calculator tab first.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 – HEALTH TIPS
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("Health Tips & Recommendations")

    bmi_input = st.number_input(
        "Enter your BMI", min_value=10.0, max_value=60.0, value=22.5, step=0.1, key="bmi_tips"
    )

    category, advice, emoji, color = get_bmi_category(bmi_input)
    tips = get_health_tips(bmi_input)

    cl, cr = st.columns([1, 1], gap="large")

    with cl:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{emoji} Your Category</div>
            <div style="font-size:2rem;font-weight:900;color:{color};margin-bottom:10px;">{category}</div>
            <div style="color:#7aaa8a;font-size:0.9rem;line-height:1.6;">{advice}</div>
        </div>
        """, unsafe_allow_html=True)

    with cr:
        tips_html = "".join([
            f'<div class="tip-item" style="animation-delay:{i*0.08}s"><span class="tip-icon">{icon}</span><span>{text}</span></div>'
            for i, (icon, text) in enumerate(tips)
        ])
        st.markdown(f"""
        <div class="card">
            <div class="card-title">💡 Personalised Tips</div>
            <div class="tips-grid">{tips_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="green-divider"></div>', unsafe_allow_html=True)

    # General guidelines
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-title">🏃 Exercise</div>
            <div class="guide-item"><span class="guide-dot">●</span>150 min moderate cardio per week</div>
            <div class="guide-item"><span class="guide-dot">●</span>Strength training 2× per week</div>
            <div class="guide-item"><span class="guide-dot">●</span>Break up sitting every hour</div>
            <div class="guide-item"><span class="guide-dot">●</span>Walk 8,000–10,000 steps daily</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-title">🥗 Nutrition</div>
            <div class="guide-item"><span class="guide-dot">●</span>Half your plate — vegetables & fruit</div>
            <div class="guide-item"><span class="guide-dot">●</span>Choose whole grains over refined</div>
            <div class="guide-item"><span class="guide-dot">●</span>Lean protein in every meal</div>
            <div class="guide-item"><span class="guide-dot">●</span>Limit ultra-processed foods & sugar</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-title">🌙 Lifestyle</div>
            <div class="guide-item"><span class="guide-dot">●</span>7–9 hours quality sleep nightly</div>
            <div class="guide-item"><span class="guide-dot">●</span>Manage stress — meditate or journal</div>
            <div class="guide-item"><span class="guide-dot">●</span>Stay socially connected</div>
            <div class="guide-item"><span class="guide-dot">●</span>Annual health check-ups</div>
        </div>
        """, unsafe_allow_html=True)