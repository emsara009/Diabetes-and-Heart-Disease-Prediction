import streamlit as st
import numpy as np
import tensorflow as tf
import joblib
import json
import random
import hashlib

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuraHealth AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session State Defaults ──────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"
if "diabetes_result" not in st.session_state:
    st.session_state.diabetes_result = None
if "heart_result" not in st.session_state:
    st.session_state.heart_result = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "demo@neurahealth.ai": {
            "name": "Sara Khalid",
            "password": hashlib.sha256("demo123".encode()).hexdigest(),
            "age": 20,
            "blood_type": "A+",
            "physician": "Dr. Ayesha Khan",
        }
    }
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "login"

dark = st.session_state.dark_mode

# ─── Theme Variables (Midnight Aurora — Dark Purple · Violet · Emerald) ─────────
if dark:
    BG          = "#080612"
    BG2         = "#100d1f"
    CARD        = "rgba(18,12,36,0.92)"
    CARD_BORDER = "rgba(139,92,246,0.20)"
    TEXT        = "#e8e0ff"
    MUTED       = "#7a6fa0"
    ROSE        = "#a855f7"        # primary violet-purple
    ROSE2       = "#7c3aed"        # deep violet
    MAUVE       = "#6366f1"        # indigo
    RED         = "#c084fc"        # light violet (used for alerts)
    GREEN       = "#10b981"        # emerald green
    GOLD        = "#34d399"        # mint green accent
    SIDEBAR_BG  = "#050410"
    BLUR        = "blur(20px)"
    SHADOW      = "0 8px 40px rgba(168,85,247,0.14), 0 2px 12px rgba(0,0,0,0.6)"
    GLOW        = "0 0 28px rgba(168,85,247,0.28)"
    ACCENT      = ROSE
    ACCENT2     = ROSE2
else:
    BG          = "#f0ebff"
    BG2         = "#e0d4ff"
    CARD        = "rgba(255,255,255,0.84)"
    CARD_BORDER = "rgba(124,58,237,0.18)"
    TEXT        = "#1a0a2e"
    MUTED       = "#6b5a85"
    ROSE        = "#7c3aed"        # deep violet
    ROSE2       = "#5b21b6"        # darker violet
    MAUVE       = "#4f46e5"        # indigo
    RED         = "#8b5cf6"        # medium violet
    GREEN       = "#059669"        # emerald
    GOLD        = "#047857"        # dark emerald
    SIDEBAR_BG  = "#ddd0f8"
    BLUR        = "blur(14px)"
    SHADOW      = "0 4px 24px rgba(124,58,237,0.12), 0 1px 6px rgba(0,0,0,0.06)"
    GLOW        = "0 0 18px rgba(124,58,237,0.18)"
    ACCENT      = ROSE
    ACCENT2     = ROSE2

CYAN  = ACCENT
CYAN2 = ACCENT2

# ─── Mega CSS ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Lato:wght@300;400;700&display=swap');

/* ══ RESET ══════════════════════════════════════ */
html, body, [class*="css"] {{
    font-family: 'Lato', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
.stApp {{ background: {BG} !important; }}
.block-container {{ padding: 1.5rem 2rem 2rem !important; max-width: 100% !important; }}

/* ══ SCROLLBAR ══════════════════════════════════ */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background: {BG2}; }}
::-webkit-scrollbar-thumb {{ background: {ROSE}55; border-radius:3px; }}

/* ══ SIDEBAR ════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {ROSE}22 !important;
    padding: 0 !important;
}}
[data-testid="stSidebar"] > div {{ padding: 0 !important; }}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    border: none !important;
    text-align: left !important;
    width: 100% !important;
    padding: 0.75rem 1.4rem !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.88rem !important;
    color: {MUTED} !important;
    border-radius: 10px !important;
    margin: 0.1rem 0 !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {ROSE}15 !important;
    color: {ROSE} !important;
    transform: none !important;
}}

/* ══ GLOBAL BUTTONS ═════════════════════════════ */
.stButton > button {{
    background: linear-gradient(135deg, {ROSE}cc, {ROSE2}cc) !important;
    color: #fff !important;
    border: 1px solid {ROSE}55 !important;
    border-radius: 50px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.8rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.25s !important;
    backdrop-filter: {BLUR} !important;
}}
.stButton > button:hover {{
    box-shadow: 0 0 22px {ROSE}55 !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, {ROSE}, {ROSE2}) !important;
}}

/* ══ INPUTS ══════════════════════════════════════ */
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextInput > div > div > input {{
    background: {BG2} !important;
    border: 1px solid {ROSE}30 !important;
    color: {TEXT} !important;
    border-radius: 12px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 0.88rem !important;
}}
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {{
    border-color: {ROSE}80 !important;
    box-shadow: 0 0 12px {ROSE}25 !important;
}}
label, .stNumberInput label, .stSelectbox label {{
    color: {MUTED} !important;
    font-size: 0.82rem !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
}}
.stSlider > div > div > div > div {{ background: {ROSE} !important; }}

/* ══ GLASS CARD ══════════════════════════════════ */
.glass {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 24px;
    backdrop-filter: {BLUR};
    -webkit-backdrop-filter: {BLUR};
    box-shadow: {SHADOW};
    padding: 1.6rem;
    position: relative;
    overflow: hidden;
}}
.glass::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {ROSE}55, transparent);
}}
.glass-sm {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 16px;
    backdrop-filter: {BLUR};
    box-shadow: {SHADOW};
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}}

/* ══ METRIC CARDS ════════════════════════════════ */
.metric-card {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
    backdrop-filter: {BLUR};
    box-shadow: {SHADOW};
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}}
.metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: {GLOW}, {SHADOW};
}}
.metric-card .glow-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 0.4rem;
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 currentColor; }}
    50% {{ opacity: 0.7; box-shadow: 0 0 0 5px transparent; }}
}}

/* ══ BADGES ══════════════════════════════════════ */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.28rem 0.85rem;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
.badge-rose  {{ background:{ROSE}18;  border:1px solid {ROSE}55;  color:{ROSE}; }}
.badge-red   {{ background:{RED}18;   border:1px solid {RED}55;   color:{RED}; }}
.badge-green {{ background:{GREEN}18; border:1px solid {GREEN}55; color:{GREEN};}}
.badge-gold  {{ background:{GOLD}18;  border:1px solid {GOLD}55;  color:{GOLD}; }}
.badge-mauve {{ background:{MAUVE}18; border:1px solid {MAUVE}55; color:{MAUVE};}}

/* ══ PROGRESS BAR ════════════════════════════════ */
.prog-wrap {{
    background: {BG2};
    border-radius: 100px;
    height: 7px;
    overflow: hidden;
    margin: 0.5rem 0;
}}
.prog-fill {{
    height: 100%;
    border-radius: 100px;
    transition: width 1s ease;
}}

/* ══ CIRCULAR PROGRESS ═══════════════════════════ */
.ring-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}}
.ring-label {{
    font-size: 0.75rem;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* ══ TYPOGRAPHY ══════════════════════════════════ */
.display-title {{
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    color: {TEXT};
    line-height: 1.15;
    letter-spacing: -0.3px;
}}
.display-title span {{ color: {ROSE}; }}
.section-header {{
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: {TEXT};
    letter-spacing: 0.1px;
    margin: 0 0 0.2rem;
}}
.mono {{
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: {ROSE};
}}
.label-xs {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {MUTED};
}}
.big-num {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 800;
    color: {TEXT};
    line-height: 1;
}}
.text-rose  {{ color: {ROSE}  !important; }}
.text-red   {{ color: {RED}   !important; }}
.text-green {{ color: {GREEN} !important; }}
.text-muted {{ color: {MUTED} !important; }}
.text-gold  {{ color: {GOLD}  !important; }}
.text-mauve {{ color: {MAUVE} !important; }}

/* ══ ECG ANIMATION ═══════════════════════════════ */
@keyframes ecgMove {{
    0%   {{ stroke-dashoffset: 1000; }}
    100% {{ stroke-dashoffset: 0; }}
}}
.ecg-line {{
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    animation: ecgMove 3s ease-in-out infinite alternate;
}}

/* ══ GLOW BORDER ═════════════════════════════════ */
.glow-card {{
    box-shadow: 0 0 0 1px {ROSE}40, 0 0 30px {ROSE}18, {SHADOW} !important;
}}
.glow-red-card {{
    box-shadow: 0 0 0 1px {RED}40, 0 0 30px {RED}12, {SHADOW} !important;
}}

/* ══ SIDEBAR LOGO ════════════════════════════════ */
.sb-logo {{
    padding: 1.6rem 1.4rem 1.2rem;
    border-bottom: 1px solid {ROSE}18;
    margin-bottom: 0.5rem;
}}
.sb-logo h2 {{
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: {ROSE} !important;
    margin: 0;
    letter-spacing: -0.2px;
}}
.sb-logo p {{
    font-size: 0.7rem;
    color: {MUTED} !important;
    margin: 0.2rem 0 0;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
.sb-nav-section {{
    font-size: 0.65rem;
    color: {MUTED} !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 0.8rem 1.4rem 0.3rem;
    font-weight: 700;
}}
.sb-footer {{
    position: absolute;
    bottom: 1.5rem;
    left: 0; right: 0;
    padding: 0 1.4rem;
    font-size: 0.72rem;
    color: {MUTED} !important;
    border-top: 1px solid {ROSE}18;
    padding-top: 1rem;
}}

/* ══ NAVBAR ══════════════════════════════════════ */
.top-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.8rem;
    gap: 1rem;
}}
.nav-search {{
    background: {CARD};
    border: 1px solid {ROSE}22;
    border-radius: 50px;
    padding: 0.5rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    max-width: 320px;
    font-size: 0.84rem;
    color: {MUTED};
    backdrop-filter: {BLUR};
}}
.nav-right {{
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
.nav-icon {{
    width: 36px; height: 36px;
    background: {CARD};
    border: 1px solid {ROSE}22;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    cursor: pointer;
    backdrop-filter: {BLUR};
    transition: border-color 0.2s;
}}
.avatar {{
    width: 36px; height: 36px;
    background: linear-gradient(135deg, {ROSE}90, {ROSE2}90);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #fff;
    border: 2px solid {ROSE}55;
}}

/* ══ RESULT PANEL ════════════════════════════════ */
.result-positive {{
    background: linear-gradient(135deg, {RED}15, {RED}08);
    border: 1px solid {RED}50;
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
}}
.result-negative {{
    background: linear-gradient(135deg, {GREEN}15, {GREEN}08);
    border: 1px solid {GREEN}50;
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
}}
.result-pending {{
    background: {BG2};
    border: 2px dashed {ROSE}30;
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
}}

/* ══ LOGIN PAGE ══════════════════════════════════ */
.login-container {{
    max-width: 460px;
    margin: 2rem auto;
}}
.login-card {{
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-radius: 28px;
    backdrop-filter: {BLUR};
    box-shadow: {SHADOW}, 0 0 60px {ROSE}10;
    padding: 2.5rem 2.2rem;
    position: relative;
    overflow: hidden;
}}
.login-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {ROSE}, {ROSE2}, transparent);
}}
.login-card::after {{
    content: '✦';
    position: absolute;
    top: -20px; right: -10px;
    font-size: 120px;
    opacity: 0.03;
    pointer-events: none;
}}
.auth-tab-btn {{
    flex: 1;
    padding: 0.55rem 1rem;
    border-radius: 50px;
    font-family: 'Lato', sans-serif;
    font-size: 0.84rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    letter-spacing: 0.3px;
}}
.auth-tab-active {{
    background: linear-gradient(135deg, {ROSE}, {ROSE2});
    color: #fff;
    box-shadow: 0 2px 12px {ROSE}40;
}}
.auth-tab-inactive {{
    background: transparent;
    color: {MUTED};
}}

/* ══ HIDE STREAMLIT CHROME ═══════════════════════ */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
[data-testid="stToolbar"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)


# ─── Model Loaders ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        d_model  = tf.keras.models.load_model('diabetes_ann_model.h5')
        d_scaler = joblib.load('scaler.pkl')
        h_model  = tf.keras.models.load_model('heart_disease_ann_model.h5')
        h_scaler = joblib.load('heart_scaler.pkl')
        return d_model, d_scaler, h_model, h_scaler, True
    except:
        return None, None, None, None, False


d_model, d_scaler, h_model, h_scaler, models_loaded = load_models()


# ─── Helper Components ─────────────────────────────────────────────────────────────
def glass_metric(icon, label, value, unit="", color=None, delta=None):
    c = color or ROSE
    delta_html = ""
    if delta:
        d_color = GREEN if delta > 0 else RED
        d_arrow = "↑" if delta > 0 else "↓"
        delta_html = f"<span style='font-size:0.75rem;color:{d_color};margin-left:0.4rem;'>{d_arrow} {abs(delta)}</span>"
    return f"""
    <div class="metric-card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.7rem;">
            <span class="label-xs">{label}</span>
            <span style="font-size:1.3rem;">{icon}</span>
        </div>
        <div style="display:flex;align-items:baseline;gap:0.3rem;">
            <span class="big-num" style="color:{c};">{value}</span>
            <span style="font-size:0.78rem;color:{MUTED};">{unit}</span>
            {delta_html}
        </div>
        <div style="position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,{c}00,{c}80,{c}00);"></div>
    </div>"""


def progress_bar(pct, color, label="", show_pct=True):
    pct_display = f"{pct:.0f}%" if show_pct else ""
    return f"""
    <div style="margin-bottom:0.5rem;">
        {"<div style='display:flex;justify-content:space-between;margin-bottom:0.3rem;'><span style='font-size:0.78rem;color:{MUTED};'>{label}</span><span class='mono'>{pct_display}</span></div>" if label else ""}
        <div class="prog-wrap">
            <div class="prog-fill" style="width:{pct}%;background:linear-gradient(90deg,{color}99,{color});"></div>
        </div>
    </div>"""


def svg_ring(pct, color, size=90, stroke=8):
    r = (size - stroke * 2) // 2
    circ = 2 * 3.14159 * r
    offset = circ * (1 - pct / 100)
    return f"""
    <svg width="{size}" height="{size}" style="transform:rotate(-90deg)">
        <circle cx="{size//2}" cy="{size//2}" r="{r}" stroke="{MUTED}33" stroke-width="{stroke}" fill="none"/>
        <circle cx="{size//2}" cy="{size//2}" r="{r}" stroke="{color}" stroke-width="{stroke}"
                fill="none" stroke-dasharray="{circ}" stroke-dashoffset="{offset}"
                stroke-linecap="round"/>
    </svg>"""


def ecg_svg(width=320, height=60, color=None):
    c = color or ROSE
    path = "M0,30 L20,30 L25,5 L30,55 L35,15 L40,30 L80,30 L85,5 L90,55 L95,15 L100,30 L140,30 L145,5 L150,55 L155,15 L160,30 L200,30 L205,5 L210,55 L215,15 L220,30 L260,30 L265,5 L270,55 L275,15 L280,30 L320,30"
    return f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">
        <defs>
            <linearGradient id="ecgGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:{c};stop-opacity:0"/>
                <stop offset="40%" style="stop-color:{c};stop-opacity:1"/>
                <stop offset="100%" style="stop-color:{c};stop-opacity:0.3"/>
            </linearGradient>
        </defs>
        <path d="{path}" fill="none" stroke="url(#ecgGrad)" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round"
              class="ecg-line" style="filter:drop-shadow(0 0 4px {c}80)"/>
    </svg>"""


def blood_sugar_svg(width=300, height=80, color=None):
    c = color or ROSE2
    pts = [20, 45, 35, 30, 55, 25, 40, 50, 28, 42, 32, 48, 22, 38, 52]
    xs = [i * (width // (len(pts) - 1)) for i in range(len(pts))]
    ys = [height - (p / 60) * (height - 10) for p in pts]
    path_pts = " ".join(f"{'M' if i==0 else 'L'}{xs[i]},{ys[i]}" for i in range(len(pts)))
    fill_pts = path_pts + f" L{xs[-1]},{height} L{xs[0]},{height} Z"
    return f"""
    <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible">
        <defs>
            <linearGradient id="bsGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:{c};stop-opacity:0.4"/>
                <stop offset="100%" style="stop-color:{c};stop-opacity:0"/>
            </linearGradient>
        </defs>
        <path d="{fill_pts}" fill="url(#bsGrad)"/>
        <path d="{path_pts}" fill="none" stroke="{c}" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"
              style="filter:drop-shadow(0 0 4px {c}80)"/>
    </svg>"""


# ══════════════════════════════════════════════════════════════════════════════════
# LOGIN / REGISTER PAGE
# ══════════════════════════════════════════════════════════════════════════════════
def show_login_page():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {BG} 0%, {BG2} 50%, {BG} 100%) !important;
    }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
    <div style="text-align:center;padding:2.5rem 1rem 0.5rem;">
        <div style="font-size:3rem;margin-bottom:0.3rem;
                    animation:float 3s ease-in-out infinite;">🌌</div>
        <div style="font-family:'Playfair Display',serif;font-weight:800;
                    font-size:2.2rem;color:{ROSE};letter-spacing:-0.5px;">
            NeuraHealth <span style="color:{TEXT};">AI</span>
        </div>
        <div style="font-size:0.78rem;color:{MUTED};letter-spacing:3px;
                    text-transform:uppercase;margin-top:0.2rem;">
            Deep Learning Health Platform
        </div>
    </div>
    <style>
    @keyframes float {{
        0%,100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.6, 1])
    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("🔑  Sign In", use_container_width=True, key="tab_login"):
                st.session_state.auth_tab = "login"
                st.rerun()
        with tab_col2:
            if st.button("✨  Register", use_container_width=True, key="tab_register"):
                st.session_state.auth_tab = "register"
                st.rerun()

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

        if st.session_state.auth_tab == "login":
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:1.5rem;">
                <div style="font-family:'Playfair Display',serif;font-weight:700;
                            font-size:1.4rem;color:{TEXT};">Welcome Back 🌌</div>
                <div style="font-size:0.82rem;color:{MUTED};margin-top:0.3rem;">
                    Sign in to access your health dashboard
                </div>
            </div>
            """, unsafe_allow_html=True)

            login_email = st.text_input("📧  Email Address", placeholder="your@email.com", key="login_email")
            login_pass  = st.text_input("🔒  Password", type="password", placeholder="Enter your password", key="login_pass")

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            if st.button("🌌  Sign In to NeuraHealth", use_container_width=True, key="do_login"):
                if login_email and login_pass:
                    users = st.session_state.users_db
                    hashed = hashlib.sha256(login_pass.encode()).hexdigest()
                    if login_email in users and users[login_email]["password"] == hashed:
                        st.session_state.logged_in = True
                        st.session_state.current_user = users[login_email]
                        st.session_state.current_user["email"] = login_email
                        st.success(f"Welcome back, {users[login_email]['name']}! 🌌")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter your email and password.")

            st.markdown(f"""
            <div style="text-align:center;margin-top:1rem;font-size:0.8rem;color:{MUTED};">
                Demo: <span style="color:{ROSE};font-family:'DM Mono',monospace;">
                demo@neurahealth.ai</span> / 
                <span style="color:{ROSE};font-family:'DM Mono',monospace;">demo123</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:1.5rem;">
                <div style="font-family:'Playfair Display',serif;font-weight:700;
                            font-size:1.4rem;color:{TEXT};">Create Account ✦</div>
                <div style="font-size:0.82rem;color:{MUTED};margin-top:0.3rem;">
                    Join NeuraHealth AI today
                </div>
            </div>
            """, unsafe_allow_html=True)

            r_name   = st.text_input("👤  Full Name", placeholder="e.g. Sara Ahmed", key="r_name")
            r_email  = st.text_input("📧  Email Address", placeholder="your@email.com", key="r_email")
            r_age    = st.number_input("🎂  Age", 10, 120, 25, key="r_age")
            r_blood  = st.selectbox("🩸  Blood Type", ["A+","A-","B+","B-","AB+","AB-","O+","O-"], key="r_blood")
            r_doc    = st.text_input("🏥  Physician Name (optional)", placeholder="Dr. Name", key="r_doc")
            r_pass   = st.text_input("🔒  Password", type="password", placeholder="Create a password", key="r_pass")
            r_pass2  = st.text_input("🔒  Confirm Password", type="password", placeholder="Repeat password", key="r_pass2")

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

            if st.button("🌌  Create My Account", use_container_width=True, key="do_register"):
                if not all([r_name, r_email, r_pass, r_pass2]):
                    st.warning("⚠️ Please fill in all required fields.")
                elif r_pass != r_pass2:
                    st.error("❌ Passwords do not match.")
                elif len(r_pass) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                elif r_email in st.session_state.users_db:
                    st.error("❌ An account with this email already exists.")
                else:
                    st.session_state.users_db[r_email] = {
                        "name": r_name,
                        "password": hashlib.sha256(r_pass.encode()).hexdigest(),
                        "age": r_age,
                        "blood_type": r_blood,
                        "physician": r_doc or "Not assigned",
                    }
                    st.success(f"Account created! Welcome, {r_name} 🌌 Please sign in.")
                    st.session_state.auth_tab = "login"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin-top:2rem;font-size:0.73rem;color:{MUTED};">
        🌌 NeuraHealth AI v2.0 &nbsp;·&nbsp; Deep Learning Powered &nbsp;·&nbsp; Final Year Project 2025
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# GUARD
# ══════════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login_page()
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════════
user = st.session_state.current_user
user_initials = "".join([w[0].upper() for w in user["name"].split()[:2]])

with st.sidebar:
    st.markdown(f"""
    <div class="sb-logo">
        <h2>🌌 NeuraHealth</h2>
        <p>AI Prediction System v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:0.6rem 1.4rem;margin-bottom:0.3rem;">
        <div style="display:flex;align-items:center;gap:0.7rem;
                    background:{BG2};border-radius:12px;padding:0.7rem 0.9rem;
                    border:1px solid {ROSE}20;">
            <div style="width:34px;height:34px;border-radius:50%;
                        background:linear-gradient(135deg,{ROSE}80,{ROSE2}80);
                        display:flex;align-items:center;justify-content:center;
                        font-size:0.8rem;font-weight:700;color:#fff;
                        border:2px solid {ROSE}55;flex-shrink:0;">{user_initials}</div>
            <div>
                <div style="font-size:0.84rem;font-weight:700;color:{TEXT};">{user["name"]}</div>
                <div style="font-size:0.7rem;color:{MUTED};">{user.get("email","")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    status = "🟢 Models Loaded" if models_loaded else "🟡 Demo Mode"
    st.markdown(f"""
    <div style="padding:0.3rem 1.4rem 0.2rem;">
        <span class="badge {'badge-rose' if models_loaded else 'badge-gold'}">{status}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='sb-nav-section'>Main Menu</div>", unsafe_allow_html=True)

    pages = {
        "Dashboard":    "🌌",
        "Predictions":  "🔬",
        "Analytics":    "📊",
        "Patient Info": "👤",
        "Settings":     "⚙️",
    }

    for page_name, icon in pages.items():
        if st.button(f"{icon}  {page_name}", key=f"nav_{page_name}"):
            st.session_state.active_page = page_name
            st.rerun()

    st.markdown("<hr style='border-color:" + ROSE + "18;margin:1rem 0'>", unsafe_allow_html=True)
    toggle_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(toggle_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    if st.button("🚪  Sign Out", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.diabetes_result = None
        st.session_state.heart_result = None
        st.rerun()

    st.markdown(f"""
    <div class="sb-footer">
        <div style="margin-bottom:0.3rem;font-family:'DM Mono',monospace;font-size:0.68rem;color:{ROSE}99;">
            DEEP LEARNING POWERED
        </div>
        ANN · TensorFlow · Streamlit<br>
        <span style="color:{ROSE}60;">Final Year Project 2025</span>
    </div>
    """, unsafe_allow_html=True)


page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════════════════════
# TOP NAVBAR
# ══════════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="top-nav">
    <div>
        <div class="label-xs" style="margin-bottom:0.1rem;">NEURAHEALTH AI</div>
        <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.15rem;color:{TEXT};">{page}</div>
    </div>
    <div class="nav-search">
        🔍&nbsp; <span style="color:{MUTED};font-size:0.83rem;">Search patients, tests...</span>
    </div>
    <div class="nav-right">
        <div class="nav-icon">🔔</div>
        <div class="nav-icon">📋</div>
        <div class="avatar">{user_initials}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":

    col_hero, col_ecg = st.columns([3, 2], gap="large")

    with col_hero:
        st.markdown(f"""
        <div class="glass" style="min-height:180px;
             background:linear-gradient(135deg, {BG2} 0%, {CARD} 100%);">
            <span class="badge badge-rose" style="margin-bottom:0.8rem;">
                🌌 DEEP LEARNING ACTIVE
            </span>
            <div class="display-title" style="margin:0.6rem 0 0.8rem;">
                AI Health<br><span>Prediction</span> System
            </div>
            <div style="font-size:0.9rem;color:{MUTED};max-width:420px;line-height:1.7;">
                Neural network–powered screening for <b style="color:{TEXT};">Diabetes</b> and
                <b style="color:{TEXT};">Heart Disease</b>. Enter clinical parameters for
                instant deep-learning risk analysis.
            </div>
            <div style="display:flex;gap:0.8rem;margin-top:1.2rem;flex-wrap:wrap;">
                <span class="badge badge-rose">ANN Architecture</span>
                <span class="badge badge-green">Binary Classification</span>
                <span class="badge badge-gold">StandardScaler</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ecg:
        st.markdown(f"""
        <div class="glass glow-card" style="min-height:180px;display:flex;flex-direction:column;justify-content:space-between;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="label-xs">Live ECG Monitor</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.1rem;color:{TEXT};margin-top:0.2rem;">Cardiac Signal</div>
                </div>
                <span class="badge badge-green">
                    <span class="glow-dot" style="background:{GREEN};color:{GREEN};">●</span> NORMAL
                </span>
            </div>
            <div style="margin:0.8rem 0;">{ecg_svg(320, 60)}</div>
            <div style="display:flex;justify-content:space-between;">
                <div><div class="label-xs">BPM</div><span style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.4rem;color:{ROSE};">72</span></div>
                <div><div class="label-xs">SPO2</div><span style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.4rem;color:{GREEN};">98%</span></div>
                <div><div class="label-xs">Rhythm</div><span style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.4rem;color:{TEXT};">Sinus</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        st.markdown(glass_metric("🩸", "Glucose Level", "108", "mg/dL", ROSE, -3), unsafe_allow_html=True)
    with c2:
        st.markdown(glass_metric("💜", "Blood Pressure", "120/80", "mm Hg", RED), unsafe_allow_html=True)
    with c3:
        st.markdown(glass_metric("⚖️", "BMI Score", "24.3", "kg/m²", GREEN, 0.2), unsafe_allow_html=True)
    with c4:
        st.markdown(glass_metric("🧪", "Cholesterol", "185", "mg/dL", MAUVE, -5), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col_models, col_blood, col_risk = st.columns([2, 2, 1.5], gap="large")

    with col_models:
        st.markdown(f"""
        <div class="glass">
            <div class="section-header">🔬 Prediction Models</div>
            <div class="label-xs" style="margin-bottom:1rem;">Neural Network Status</div>
        """, unsafe_allow_html=True)

        for model_name, acc, color, icon in [
            ("Diabetes ANN", 78, ROSE, "🩸"),
            ("Heart Disease ANN", 83, GREEN, "💚"),
        ]:
            st.markdown(f"""
            <div style="background:{BG2};border:1px solid {color}22;border-radius:14px;padding:1rem;margin-bottom:0.7rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <span style="font-size:0.9rem;font-weight:600;">{icon} {model_name}</span>
                    <span class="mono" style="color:{color};">{acc}% acc</span>
                </div>
                <div style="display:flex;gap:0.5rem;margin-bottom:0.5rem;flex-wrap:wrap;">
                    <span class="badge" style="background:{color}15;border:1px solid {color}40;color:{color};font-size:0.65rem;">ANN</span>
                    <span class="badge" style="background:{color}15;border:1px solid {color}40;color:{color};font-size:0.65rem;">Binary</span>
                    <span class="badge" style="background:{color}15;border:1px solid {color}40;color:{color};font-size:0.65rem;">Sigmoid</span>
                </div>
                {progress_bar(acc, color)}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_blood:
        st.markdown(f"""
        <div class="glass">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <div class="section-header">📈 Blood Sugar Trend</div>
                <span class="badge badge-rose">7 Days</span>
            </div>
            <div class="label-xs" style="margin-bottom:1rem;">Glucose mg/dL over time</div>
            {blood_sugar_svg(300, 80)}
            <div style="display:flex;justify-content:space-between;margin-top:0.8rem;">
                <div style="text-align:center;">
                    <div class="label-xs">MIN</div>
                    <span style="font-family:'Playfair Display',serif;font-weight:700;color:{GREEN};">88</span>
                </div>
                <div style="text-align:center;">
                    <div class="label-xs">AVG</div>
                    <span style="font-family:'Playfair Display',serif;font-weight:700;color:{ROSE};">108</span>
                </div>
                <div style="text-align:center;">
                    <div class="label-xs">MAX</div>
                    <span style="font-family:'Playfair Display',serif;font-weight:700;color:{MAUVE};">142</span>
                </div>
                <div style="text-align:center;">
                    <div class="label-xs">STATUS</div>
                    <span style="font-family:'Playfair Display',serif;font-weight:700;color:{GREEN};font-size:0.85rem;">Normal</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_risk:
        st.markdown(f"""
        <div class="glass" style="height:100%;">
            <div class="section-header" style="margin-bottom:0.2rem;">🎯 Risk Overview</div>
            <div class="label-xs" style="margin-bottom:1.2rem;">AI Confidence Scores</div>
        """, unsafe_allow_html=True)

        for label, pct, color in [("Diabetes Risk", 24, ROSE), ("Heart Risk", 18, RED), ("Overall Health", 82, GREEN)]:
            st.markdown(f"""
            <div class="ring-wrap" style="margin-bottom:1.2rem;">
                <div style="position:relative;display:inline-block;">
                    {svg_ring(pct if label != 'Overall Health' else 82, color, 80, 7)}
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                                text-align:center;line-height:1;">
                        <span style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:800;color:{color};">{pct}%</span>
                    </div>
                </div>
                <span class="ring-label">{label}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTIONS
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "Predictions":

    tabs = st.tabs(["🩸  Diabetes Prediction", "💜  Heart Disease Prediction"])

    with tabs[0]:
        col_form, col_out = st.columns([3, 2], gap="large")

        with col_form:
            st.markdown(f"""
            <div class="glass" style="margin-bottom:1rem;">
                <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;">
                    <span style="font-size:1.6rem;">🩸</span>
                    <div>
                        <div class="section-header">Diabetes Risk Assessment</div>
                        <div class="label-xs">Enter clinical parameters — ANN model (16→8→1)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                preg    = st.number_input("Pregnancies", 0, 20, 3)
                bp      = st.number_input("Blood Pressure (mm Hg)", 0.0, 150.0, 72.0, 0.1)
                insulin = st.number_input("Insulin (µU/mL)", 0.0, 900.0, 79.0, 0.1)
                dpf     = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5, 0.001, format="%.3f")
            with c2:
                glucose  = st.number_input("Glucose (mg/dL)", 0.0, 300.0, 120.0, 0.1)
                skin     = st.number_input("Skin Thickness (mm)", 0.0, 100.0, 20.0, 0.1)
                bmi      = st.number_input("BMI (kg/m²)", 0.0, 70.0, 25.0, 0.1)
                age      = st.number_input("Age (years)", 1, 120, 33)

            st.markdown("</div>", unsafe_allow_html=True)
            predict_d = st.button("🌌  Run Diabetes Analysis", use_container_width=True)

        with col_out:
            st.markdown(f"""
            <div class="glass" style="margin-bottom:1rem;">
                <div class="section-header" style="margin-bottom:0.2rem;">AI Analysis Result</div>
                <div class="label-xs" style="margin-bottom:1rem;">Deep learning prediction output</div>
            """, unsafe_allow_html=True)

            if predict_d:
                if models_loaded:
                    data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
                    data_s = d_scaler.transform(data)
                    prob = float(d_model.predict(data_s, verbose=0)[0][0])
                else:
                    prob = random.uniform(0.15, 0.85)

                is_d = prob > 0.5
                st.session_state.diabetes_result = {"prob": prob, "positive": is_d}
                risk_pct = int(prob * 100)
                color = RED if is_d else GREEN
                label = "DIABETIC" if is_d else "NON-DIABETIC"
                icon  = "⚠️" if is_d else "✅"
                msg   = "High risk detected. Please consult a specialist." if is_d else "Low risk. Maintain healthy lifestyle."

                st.markdown(f"""
                <div class="{'result-positive' if is_d else 'result-negative'}">
                    <div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.5rem;color:{color};">{label}</div>
                    <div style="margin:0.8rem 0;">{svg_ring(risk_pct, color, 100, 9)}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:1.8rem;font-weight:500;color:{color};">{risk_pct}%</div>
                    <div class="label-xs" style="margin:0.3rem 0 0.8rem;">Risk Probability</div>
                    <div style="font-size:0.82rem;color:{MUTED};">{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-pending">
                    <div style="font-size:2.5rem;margin-bottom:0.6rem;">🩸</div>
                    <div style="font-size:0.9rem;color:{MUTED};">Enter parameters & run analysis</div>
                    <div class="label-xs" style="margin-top:0.5rem;">ANN model ready</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="glass-sm">
                <div class="section-header" style="font-size:0.9rem;margin-bottom:0.7rem;">📌 Normal Ranges</div>
                {progress_bar(45, ROSE, "Glucose: 70–99 mg/dL")}
                {progress_bar(60, GREEN, "BMI: 18.5–24.9 kg/m²")}
                {progress_bar(55, MAUVE, "Insulin: 16–166 µU/mL")}
                {progress_bar(50, RED, "BP: < 80 mm Hg")}
            </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        col_form2, col_out2 = st.columns([3, 2], gap="large")

        with col_form2:
            st.markdown(f"""
            <div class="glass" style="margin-bottom:1rem;">
                <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;">
                    <span style="font-size:1.6rem;">💜</span>
                    <div>
                        <div class="section-header">Heart Disease Risk Assessment</div>
                        <div class="label-xs">13-feature deep ANN model (32→16→8→1)</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                h_age  = st.number_input("Age", 1, 120, 52, key="h_age")
                h_sex  = st.selectbox("Sex", [(1,"Male"),(0,"Female")], format_func=lambda x:x[1])
                h_cp   = st.selectbox("Chest Pain Type", [(0,"Typical Angina"),(1,"Atypical Angina"),(2,"Non-anginal"),(3,"Asymptomatic")], format_func=lambda x:x[1])
                h_tbp  = st.number_input("Resting BP (mm Hg)", 80.0, 220.0, 125.0, 0.1)
                h_chol = st.number_input("Cholesterol (mg/dL)", 100.0, 600.0, 212.0, 0.1)
                h_fbs  = st.selectbox("Fasting BS > 120 mg/dL", [(0,"No"),(1,"Yes")], format_func=lambda x:x[1])
                h_ecg  = st.selectbox("Resting ECG", [(0,"Normal"),(1,"ST-T Abnormal"),(2,"LV Hypertrophy")], format_func=lambda x:x[1])
            with c2:
                h_thal = st.number_input("Max Heart Rate", 60.0, 220.0, 168.0, 0.1)
                h_exa  = st.selectbox("Exercise Angina", [(0,"No"),(1,"Yes")], format_func=lambda x:x[1])
                h_opk  = st.number_input("ST Depression", 0.0, 10.0, 1.0, 0.1)
                h_slp  = st.selectbox("Slope of ST", [(0,"Upsloping"),(1,"Flat"),(2,"Downsloping")], format_func=lambda x:x[1])
                h_ca   = st.number_input("Major Vessels (0–3)", 0, 3, 2)
                h_tha  = st.selectbox("Thalassemia", [(1,"Normal"),(2,"Fixed Defect"),(3,"Reversible")], format_func=lambda x:x[1])

            st.markdown("</div>", unsafe_allow_html=True)
            predict_h = st.button("💜  Run Cardiac Analysis", use_container_width=True)

        with col_out2:
            st.markdown(f"""
            <div class="glass" style="margin-bottom:1rem;">
                <div class="section-header" style="margin-bottom:0.2rem;">AI Cardiac Analysis</div>
                <div class="label-xs" style="margin-bottom:1rem;">Deep learning cardiac risk output</div>
            """, unsafe_allow_html=True)

            if predict_h:
                if models_loaded:
                    data = np.array([[h_age, h_sex[0], h_cp[0], h_tbp, h_chol, h_fbs[0],
                                      h_ecg[0], h_thal, h_exa[0], h_opk, h_slp[0], h_ca, h_tha[0]]])
                    data_s = h_scaler.transform(data)
                    prob = float(h_model.predict(data_s, verbose=0)[0][0])
                else:
                    prob = random.uniform(0.15, 0.85)

                is_h = prob > 0.5
                st.session_state.heart_result = {"prob": prob, "positive": is_h}
                risk_pct = int(prob * 100)
                color = RED if is_h else GREEN
                label = "DISEASE DETECTED" if is_h else "NO HEART DISEASE"
                icon  = "🚨" if is_h else "💚"
                msg   = "Cardiac risk detected. Seek cardiology consultation." if is_h else "Cardiac profile appears normal. Continue monitoring."

                st.markdown(f"""
                <div class="{'result-positive' if is_h else 'result-negative'}">
                    <div style="font-size:2.5rem;margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.4rem;color:{color};">{label}</div>
                    <div style="margin:0.8rem 0;">{svg_ring(risk_pct, color, 100, 9)}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:1.8rem;font-weight:500;color:{color};">{risk_pct}%</div>
                    <div class="label-xs" style="margin:0.3rem 0 0.8rem;">Risk Probability</div>
                    <div style="font-size:0.82rem;color:{MUTED};">{msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-pending">
                    <div style="font-size:2.5rem;margin-bottom:0.6rem;">💜</div>
                    <div style="font-size:0.9rem;color:{MUTED};">Enter parameters & run analysis</div>
                    <div class="label-xs" style="margin-top:0.5rem;">Cardiac ANN ready</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="glass-sm">
                <div class="section-header" style="font-size:0.9rem;margin-bottom:0.7rem;">📌 Cardiac Reference</div>
                {progress_bar(55, RED, "Cholesterol: < 200 mg/dL")}
                {progress_bar(50, ROSE, "Resting BP: < 120 mm Hg")}
                {progress_bar(70, GREEN, "Max HR: ~220 − age")}
                {progress_bar(0, MAUVE, "ST Depression: 0.0 (normal)")}
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "Analytics":

    c1, c2, c3 = st.columns([1.5, 2, 1.5], gap="large")

    with c1:
        st.markdown(f"""
        <div class="glass">
            <div class="section-header">🎯 Model Accuracy</div>
            <div class="label-xs" style="margin-bottom:1.2rem;">ANN Performance Metrics</div>
        """, unsafe_allow_html=True)
        for name, acc, prec, rec, color in [
            ("Diabetes", 78, 74, 72, ROSE),
            ("Heart Disease", 83, 81, 79, GREEN),
        ]:
            st.markdown(f"""
            <div style="background:{BG2};border-radius:14px;padding:1rem;margin-bottom:0.8rem;border:1px solid {color}22;">
                <div style="font-weight:600;font-size:0.88rem;color:{color};margin-bottom:0.6rem;">{name} Model</div>
                {progress_bar(acc, color, f"Accuracy: {acc}%")}
                {progress_bar(prec, color, f"Precision: {prec}%")}
                {progress_bar(rec, color, f"Recall: {rec}%")}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="glass">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <div class="section-header">💓 Cardiac Monitor</div>
                <span class="badge badge-green">● LIVE</span>
            </div>
            <div class="label-xs" style="margin-bottom:1rem;">Simulated cardiac signal</div>
            {ecg_svg(380, 70, ROSE)}
            <div style="height:0.5rem;"></div>
            {ecg_svg(380, 50, GREEN)}
            <div style="display:flex;justify-content:space-between;margin-top:1rem;">
                {"".join([f'<div style="text-align:center;"><div class="label-xs">{l}</div><span style="font-family:\'Playfair Display\',serif;font-weight:700;font-size:1.1rem;color:{c};">{v}</span></div>' for l,v,c in [("BPM","72",ROSE),("RR Int","820ms",TEXT),("QTc","420ms",MAUVE),("PR Int","160ms",GREEN)]])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="glass">
            <div class="section-header" style="margin-bottom:0.2rem;">🏥 Health Rings</div>
            <div class="label-xs" style="margin-bottom:1.2rem;">Patient vitals overview</div>
        """, unsafe_allow_html=True)
        for label, pct, color in [
            ("Cardiac Score", 82, GREEN),
            ("Glucose Control", 76, ROSE),
            ("BMI Index", 68, MAUVE),
            ("BP Control", 88, RED),
        ]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.8rem;
                        background:{BG2};border-radius:12px;padding:0.6rem 0.8rem;">
                <div style="position:relative;flex-shrink:0;">
                    {svg_ring(pct, color, 50, 5)}
                    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                                font-family:'Playfair Display',serif;font-size:0.65rem;font-weight:800;color:{color};">{pct}</div>
                </div>
                <div>
                    <div style="font-size:0.82rem;font-weight:600;color:{TEXT};">{label}</div>
                    <div class="label-xs">{pct}% score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    col_ai, col_bs = st.columns(2, gap="large")

    with col_ai:
        st.markdown(f"""
        <div class="glass">
            <div class="section-header" style="margin-bottom:0.2rem;">🤖 AI Confidence Distribution</div>
            <div class="label-xs" style="margin-bottom:1.2rem;">Feature importance & model certainty</div>
        """, unsafe_allow_html=True)
        features_d = [
            ("Glucose",     88, ROSE),
            ("BMI",         74, ROSE2),
            ("Age",         68, GREEN),
            ("Insulin",     61, MAUVE),
            ("Pregnancies", 45, MUTED),
            ("Blood Pres.", 42, RED),
        ]
        for feat, imp, color in features_d:
            st.markdown(progress_bar(imp, color, feat), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bs:
        st.markdown(f"""
        <div class="glass">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">
                <div class="section-header">📊 Glucose Trend Analytics</div>
                <span class="badge badge-rose">30 Days</span>
            </div>
            <div class="label-xs" style="margin-bottom:0.8rem;">Blood sugar pattern analysis</div>
            {blood_sugar_svg(400, 100, ROSE)}
            <div style="display:flex;gap:0.6rem;margin-top:1rem;flex-wrap:wrap;">
                <div class="glass-sm" style="flex:1;text-align:center;padding:0.7rem;">
                    <div class="label-xs">PRE-MEAL</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.2rem;color:{ROSE};">88</div>
                </div>
                <div class="glass-sm" style="flex:1;text-align:center;padding:0.7rem;">
                    <div class="label-xs">POST-MEAL</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.2rem;color:{MAUVE};">142</div>
                </div>
                <div class="glass-sm" style="flex:1;text-align:center;padding:0.7rem;">
                    <div class="label-xs">HbA1c EST.</div>
                    <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.2rem;color:{GREEN};">5.8%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PAGE: PATIENT INFO
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "Patient Info":

    col_profile, col_stats = st.columns([1.5, 2.5], gap="large")

    with col_profile:
        u = st.session_state.current_user
        st.markdown(f"""
        <div class="glass" style="text-align:center;padding:2rem 1.5rem;">
            <div style="width:80px;height:80px;border-radius:50%;
                        background:linear-gradient(135deg,{ROSE}80,{ROSE2}80);
                        display:flex;align-items:center;justify-content:center;
                        font-size:2rem;margin:0 auto 1rem;
                        border:3px solid {ROSE}55;box-shadow:{GLOW};">👤</div>
            <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.2rem;color:{TEXT};">
                {u["name"]}</div>
            <div class="label-xs" style="margin:0.3rem 0 0.8rem;">{u.get("email","")}</div>
            <span class="badge badge-rose">Active Patient</span>
            <hr style="border-color:{ROSE}18;margin:1.2rem 0;">
            <div style="text-align:left;">
                {"".join([f'<div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;font-size:0.85rem;"><span style="color:{MUTED};">{k}</span><span style="color:{TEXT};font-weight:500;">{v}</span></div>' for k,v in [("Age",f'{u.get("age","—")} years'),("Blood Type",u.get("blood_type","—")),("Physician",u.get("physician","—"))]])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        d_res = st.session_state.diabetes_result
        h_res = st.session_state.heart_result
        d_pct = int(d_res["prob"] * 100) if d_res else "—"
        h_pct = int(h_res["prob"] * 100) if h_res else "—"
        d_color = (RED if d_res and d_res["positive"] else GREEN) if d_res else MUTED
        h_color = (RED if h_res and h_res["positive"] else GREEN) if h_res else MUTED

        st.markdown(f"""
        <div class="glass-sm" style="margin-top:1rem;">
            <div class="section-header" style="font-size:0.9rem;margin-bottom:0.8rem;">🤖 Latest AI Predictions</div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;
                        background:{BG2};border-radius:10px;padding:0.6rem 0.8rem;">
                <div style="font-size:0.82rem;">🩸 Diabetes Risk</div>
                <span style="font-family:'Playfair Display',serif;font-weight:700;color:{d_color};">{d_pct}{'%' if d_res else ''}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                        background:{BG2};border-radius:10px;padding:0.6rem 0.8rem;">
                <div style="font-size:0.82rem;">💜 Heart Risk</div>
                <span style="font-family:'Playfair Display',serif;font-weight:700;color:{h_color};">{h_pct}{'%' if h_res else ''}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_stats:
        st.markdown(f"""
        <div class="glass" style="margin-bottom:1rem;">
            <div class="section-header" style="margin-bottom:0.2rem;">📋 Clinical Parameters</div>
            <div class="label-xs" style="margin-bottom:1.2rem;">Most recent lab results</div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(glass_metric("🩸", "Fasting Glucose", "108", "mg/dL", ROSE), unsafe_allow_html=True)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            st.markdown(glass_metric("⚖️", "BMI", "24.3", "kg/m²", GREEN), unsafe_allow_html=True)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            st.markdown(glass_metric("🧬", "Insulin Level", "79", "µU/mL", ROSE2), unsafe_allow_html=True)
        with c2:
            st.markdown(glass_metric("💜", "Blood Pressure", "125/82", "mm Hg", RED), unsafe_allow_html=True)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            st.markdown(glass_metric("🧪", "Cholesterol", "212", "mg/dL", MAUVE), unsafe_allow_html=True)
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            st.markdown(glass_metric("🫀", "Heart Rate", "72", "bpm", GREEN, 2), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass">
            <div class="section-header" style="margin-bottom:0.2rem;">📊 Health Summary</div>
            <div class="label-xs" style="margin-bottom:1rem;">AI-generated health score breakdown</div>
            {progress_bar(82, GREEN, "Overall Health Score")}
            {progress_bar(76, ROSE, "Metabolic Health")}
            {progress_bar(88, GREEN, "Cardiovascular Health")}
            {progress_bar(71, MAUVE, "Insulin Sensitivity")}
            {progress_bar(90, ROSE2, "Blood Pressure Control")}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════════
elif page == "Settings":

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
        <div class="glass" style="margin-bottom:1rem;">
            <div class="section-header" style="margin-bottom:1rem;">🎨 Appearance</div>
        """, unsafe_allow_html=True)
        mode_label = "Dark Mode" if dark else "Light Mode"
        st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        background:{BG2};border-radius:14px;padding:1rem;margin-bottom:0.8rem;">
                <div>
                    <div style="font-weight:600;font-size:0.9rem;">Theme Mode</div>
                    <div class="label-xs">Currently: {mode_label}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌙 Toggle Dark/Light Mode", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

        st.markdown(f"""
        <div class="glass" style="margin-top:1rem;">
            <div class="section-header" style="margin-bottom:1rem;">⚙️ Model Configuration</div>
            <div style="background:{BG2};border-radius:14px;padding:1rem;margin-bottom:0.8rem;">
                <div style="font-weight:600;font-size:0.9rem;margin-bottom:0.3rem;">Diabetes Model</div>
                <div class="mono">diabetes_ann_model.h5</div>
                <div class="label-xs" style="margin-top:0.3rem;">{'✅ Loaded' if models_loaded else '⚠️ Not found – demo mode'}</div>
            </div>
            <div style="background:{BG2};border-radius:14px;padding:1rem;">
                <div style="font-weight:600;font-size:0.9rem;margin-bottom:0.3rem;">Heart Disease Model</div>
                <div class="mono">heart_disease_ann_model.h5</div>
                <div class="label-xs" style="margin-top:0.3rem;">{'✅ Loaded' if models_loaded else '⚠️ Not found – demo mode'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass" style="margin-top:1rem;">
            <div class="section-header" style="margin-bottom:1rem;">👤 My Account</div>
            <div style="background:{BG2};border-radius:14px;padding:1rem;">
                {"".join([f'<div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;font-size:0.85rem;"><span style="color:{MUTED};">{k}</span><span style="color:{TEXT};font-weight:500;">{v}</span></div>' for k,v in [("Name", user["name"]),("Email", user.get("email","—")),("Blood Type", user.get("blood_type","—")),("Physician", user.get("physician","—"))]])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass" style="margin-bottom:1rem;">
            <div class="section-header" style="margin-bottom:1rem;">ℹ️ System Information</div>
            {"".join([f'<div style="display:flex;justify-content:space-between;padding:0.6rem 0;border-bottom:1px solid {ROSE}12;font-size:0.85rem;"><span style="color:{MUTED};">{k}</span><span class="mono">{v}</span></div>' for k,v in [("App Name","NeuraHealth AI v2.0"),("Framework","Streamlit"),("DL Library","TensorFlow/Keras"),("Preprocessing","Scikit-learn"),("Architecture","ANN (Sequential)"),("Activation","Sigmoid (output)"),("Loss Function","Binary Crossentropy"),("Optimiser","Adam")]])}
        </div>
        <div class="glass">
            <div class="section-header" style="margin-bottom:0.8rem;">⚠️ Medical Disclaimer</div>
            <div style="background:{RED}10;border:1px solid {RED}30;border-radius:14px;padding:1rem;font-size:0.83rem;color:{MUTED};line-height:1.75;">
                This application is for <b style="color:{TEXT};">educational and research purposes only</b>.
                Predictions are not a substitute for professional medical diagnosis.
                Always consult a qualified healthcare provider for clinical decisions.
            </div>
        </div>
        """, unsafe_allow_html=True)