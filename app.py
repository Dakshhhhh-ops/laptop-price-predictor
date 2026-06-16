import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="LaptopLens · Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0B0F1A !important;
    color: #C8D0E7 !important;
}
.block-container { padding: 2.5rem 3rem 4rem 3rem !important; max-width: 1280px !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.wordmark { font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; letter-spacing:-0.02em; color:#F0F4FF !important; }
.wordmark span { color:#3E8BFF; }
.nav-bar { display:flex; align-items:center; justify-content:space-between; padding:0 0 2.5rem 0; border-bottom:1px solid #1E2740; margin-bottom:3rem; }
.nav-links { display:flex; gap:2rem; }
.nav-links a { font-size:0.82rem; font-weight:500; letter-spacing:0.06em; text-transform:uppercase; color:#5A6A8A !important; text-decoration:none; }
.nav-links a:hover { color:#F0F4FF !important; }

.hero-eyebrow { font-family:'Space Grotesk',sans-serif; font-size:0.72rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:#3E8BFF; margin-bottom:0.9rem; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2.2rem,4vw,3.4rem); font-weight:700; line-height:1.1; letter-spacing:-0.03em; color:#F0F4FF; margin:0 0 1.1rem 0; }
.hero-title em { font-style:normal; color:#3E8BFF; }
.hero-sub { font-size:0.97rem; line-height:1.7; color:#5A6A8A; max-width:520px; margin-bottom:2.5rem; }
.hero-badges { display:flex; gap:0.6rem; flex-wrap:wrap; margin-bottom:3rem; }
.badge { background:#141928; border:1px solid #1E2740; border-radius:99px; padding:0.3rem 0.85rem; font-size:0.75rem; font-weight:500; color:#7A8BAA; letter-spacing:0.02em; }
.badge-blue { background:rgba(62,139,255,0.08); border-color:rgba(62,139,255,0.25); color:#3E8BFF; }

.metric-strip { display:flex; gap:1rem; margin-bottom:3rem; flex-wrap:wrap; }
.metric-tile { flex:1; min-width:120px; background:#111622; border:1px solid #1A2338; border-radius:12px; padding:1.1rem 1.3rem; }
.metric-num { font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:700; color:#F0F4FF; letter-spacing:-0.04em; line-height:1; margin-bottom:0.25rem; }
.metric-desc { font-size:0.72rem; color:#5A6A8A; font-weight:500; }

.section-label { font-family:'Space Grotesk',sans-serif; font-size:0.68rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:#3E8BFF; margin-bottom:0.6rem; padding-bottom:0.55rem; border-bottom:1px solid #1E2740; }
.section-gap { margin-top:1.6rem; }

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background-color:#0D1220 !important; border-color:#1E2A42 !important; border-radius:10px !important; color:#C8D0E7 !important; font-size:0.9rem !important; }
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover { border-color:#3E8BFF !important; }
div[data-baseweb="select"] svg { fill:#5A6A8A !important; }
.stNumberInput input { background-color:#0D1220 !important; color:#C8D0E7 !important; border-radius:10px !important; border:1px solid #1E2A42 !important; font-size:0.9rem !important; }
label[data-testid="stWidgetLabel"] p, .stSelectbox label p, .stNumberInput label p { font-family:'Space Grotesk',sans-serif !important; font-size:0.78rem !important; font-weight:600 !important; letter-spacing:0.05em !important; text-transform:uppercase !important; color:#5A6A8A !important; margin-bottom:0.3rem !important; }
[data-baseweb="popover"] { background:#111622 !important; border:1px solid #1E2A42 !important; border-radius:10px !important; }
[data-baseweb="menu"] li { background:#111622 !important; color:#C8D0E7 !important; font-size:0.88rem !important; }
[data-baseweb="menu"] li:hover { background:#1A2740 !important; color:#F0F4FF !important; }

.stButton > button { background:linear-gradient(135deg,#3E8BFF 0%,#1A5FCC 100%) !important; color:#fff !important; border:none !important; border-radius:12px !important; padding:0.85rem 2.5rem !important; font-family:'Space Grotesk',sans-serif !important; font-size:0.95rem !important; font-weight:600 !important; letter-spacing:0.04em !important; width:100% !important; box-shadow:0 4px 24px rgba(62,139,255,0.25) !important; transition:opacity 0.2s ease !important; }
.stButton > button:hover { opacity:0.88 !important; box-shadow:0 6px 32px rgba(62,139,255,0.4) !important; }

.result-wrap { background:linear-gradient(135deg,rgba(62,139,255,0.08),rgba(26,95,204,0.04)); border:1px solid rgba(62,139,255,0.3); border-radius:16px; padding:2rem; margin-top:1.2rem; text-align:center; }
.result-label { font-family:'Space Grotesk',sans-serif; font-size:0.72rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:#3E8BFF; margin-bottom:0.5rem; }
.result-price { font-family:'Space Grotesk',sans-serif; font-size:3rem; font-weight:700; letter-spacing:-0.04em; color:#F0F4FF; line-height:1.1; }
.result-note { font-size:0.8rem; color:#5A6A8A; margin-top:0.5rem; }

.spec-card { background:#111622; border:1px solid #1A2338; border-radius:16px; padding:2rem; position:sticky; top:2rem; }
.spec-header { font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:600; color:#F0F4FF; margin-bottom:0.25rem; }
.spec-sub { font-size:0.8rem; color:#5A6A8A; margin-bottom:1.5rem; }
.spec-row { display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid #141928; font-size:0.85rem; }
.spec-row:last-child { border-bottom:none; }
.spec-key { color:#5A6A8A; font-weight:500; }
.spec-val { color:#C8D0E7; font-weight:600; font-family:'Space Grotesk',sans-serif; font-size:0.82rem; }
.spec-divider { border:none; border-top:1px solid #1E2740; margin:1.2rem 0; }
.spec-section-lbl { font-family:'Space Grotesk',sans-serif; font-size:0.65rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:#3E8BFF; margin:0 0 0.6rem 0; padding-bottom:0.4rem; border-bottom:1px solid #1E2740; }

.footer { margin-top:5rem; padding-top:2rem; border-top:1px solid #1A2338; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }
.footer-copy { font-size:0.78rem; color:#3A4A65; }
.footer-links { display:flex; gap:1.5rem; }
.footer-links a { font-size:0.78rem; color:#3A4A65 !important; text-decoration:none; }
.footer-links a:hover { color:#5A6A8A !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        with open("pipe.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

pipe = load_model()

st.markdown("""
<div class="nav-bar">
    <div class="wordmark">Laptop<span>Lens</span></div>
    <div class="nav-links">
        <a href="https://github.com/Dakshhhhh-ops/laptop-price-predictor" target="_blank">GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p class="hero-eyebrow">Machine Learning &middot; Price Intelligence</p>
<h1 class="hero-title">Estimate any laptop's<br><em>fair market price</em></h1>
<p class="hero-sub">Configure your laptop's specifications and get an instant ML-powered price estimate. Built on a gradient-boosted pipeline trained on 1,300+ real-world listings.</p>
<div class="hero-badges">
    <span class="badge badge-blue">Random Forest &middot; Pipeline</span>
    <span class="badge">Scikit-learn</span>
    <span class="badge">13 Features</span>
    <span class="badge">&#8377; INR Output</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-strip">
    <div class="metric-tile"><div class="metric-num">1,302</div><div class="metric-desc">Training samples</div></div>
    <div class="metric-tile"><div class="metric-num">13</div><div class="metric-desc">Input features</div></div>
    <div class="metric-tile"><div class="metric-num">~89%</div><div class="metric-desc">R&sup2; score</div></div>
    <div class="metric-tile"><div class="metric-num">12</div><div class="metric-desc">Brands covered</div></div>
</div>
""", unsafe_allow_html=True)

col_form, col_preview = st.columns([3, 2], gap="large")

with col_form:

    st.markdown('<p class="section-label">Brand &amp; Category</p>', unsafe_allow_html=True)
    r1a, r1b = st.columns(2)
    with r1a:
        company = st.selectbox("Company", ["Dell","HP","Lenovo","Asus","Acer","Apple","MSI","Toshiba","Samsung","LG","Huawei","Razer"])
    with r1b:
        typename = st.selectbox("Type", ["Notebook","Ultrabook","Gaming","2 in 1 Convertible","Workstation","Netbook"])

    st.markdown('<p class="section-label section-gap">Memory &amp; Build</p>', unsafe_allow_html=True)
    r2a, r2b, r2c = st.columns(3)
    with r2a:
        ram = st.selectbox("RAM (GB)", [2,4,6,8,12,16,24,32,64], index=3)
    with r2b:
        hdd = st.selectbox("HDD (GB)", [0,128,256,500,512,1000,2000])
    with r2c:
        ssd = st.selectbox("SSD (GB)", [0,8,128,256,512,1024,2048], index=2)
    weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

    st.markdown('<p class="section-label section-gap">Display</p>', unsafe_allow_html=True)
    r3a, r3b = st.columns(2)
    with r3a:
        screen_size = st.number_input("Screen Size (inches)", min_value=10.0, max_value=20.0, value=15.6, step=0.1)
    with r3b:
        resolution = st.selectbox("Resolution", ["1366x768","1600x900","1920x1080","2560x1440","2560x1600","3840x2160"], index=2)
    r4a, r4b = st.columns(2)
    with r4a:
        touchscreen = st.selectbox("Touchscreen", ["No","Yes"])
    with r4b:
        ips = st.selectbox("IPS Display", ["No","Yes"])

    st.markdown('<p class="section-label section-gap">Processor &amp; Graphics</p>', unsafe_allow_html=True)
    r5a, r5b = st.columns(2)
    with r5a:
        cpu_brand = st.selectbox("CPU", ["Intel Core i3","Intel Core i5","Intel Core i7","AMD Processor","Other Intel Processor"], index=2)
    with r5b:
        gpu_brand = st.selectbox("GPU Brand", ["Intel","Nvidia","AMD"], index=1)
    cpu_speed = st.number_input("CPU Speed (GHz)", min_value=0.5, max_value=6.0, value=2.5, step=0.1)

    st.markdown('<p class="section-label section-gap">Operating System</p>', unsafe_allow_html=True)
    os_choice = st.selectbox("OS", ["Windows","Mac","Linux","No OS","Other"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button("⚡ Estimate Price")

    if predict_clicked:
        X_res = int(resolution.split("x")[0])
        Y_res = int(resolution.split("x")[1])
        ppi = ((X_res**2 + Y_res**2)**0.5) / screen_size
        query = pd.DataFrame(
            [[company, typename, ram, weight, int(touchscreen=="Yes"), int(ips=="Yes"),
              ppi, cpu_brand, cpu_speed, hdd, ssd, gpu_brand, os_choice]],
            columns=["Company","TypeName","Ram","Weight","Touchscreen","IPS","PPI",
                     "Cpu Brand","Cpu Speed","HDD","SSD","Gpu_brand","os"],
        )
        if pipe:
            prediction = np.exp(pipe.predict(query)[0])
            st.markdown(
                f'<div class="result-wrap">'
                f'<div class="result-label">Estimated Market Price</div>'
                f'<div class="result-price">&#8377; {prediction:,.0f}</div>'
                f'<div class="result-note">Based on ML pipeline &middot; Results are indicative</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="result-wrap">'
                '<div class="result-label">Model Not Found</div>'
                '<div class="result-price" style="font-size:1.5rem;color:#5A6A8A;">pipe.pkl missing</div>'
                '<div class="result-note">Place your trained pipe.pkl in the same directory</div>'
                '</div>',
                unsafe_allow_html=True,
            )

with col_preview:
    X_res_p = int(resolution.split("x")[0])
    Y_res_p = int(resolution.split("x")[1])
    ppi_p   = ((X_res_p**2 + Y_res_p**2)**0.5) / screen_size
    ppi_tier = "Retina" if ppi_p > 220 else ("QHD+" if ppi_p > 160 else ("FHD" if ppi_p > 100 else "HD"))
    ts_icon  = "&#10003;" if touchscreen == "Yes" else "&#10007;"
    ips_icon = "&#10003;" if ips == "Yes" else "&#10007;"

    spec_html = (
        '<div class="spec-card">'
        '<div class="spec-header">Live Configuration</div>'
        '<div class="spec-sub">Updates as you fill the form</div>'
        '<p class="spec-section-lbl">System</p>'
        '<div class="spec-row"><span class="spec-key">Brand</span><span class="spec-val">' + company + '</span></div>'
        '<div class="spec-row"><span class="spec-key">Type</span><span class="spec-val">' + typename + '</span></div>'
        '<div class="spec-row"><span class="spec-key">OS</span><span class="spec-val">' + os_choice + '</span></div>'
        '<div class="spec-row"><span class="spec-key">Weight</span><span class="spec-val">' + f"{weight:.1f} kg" + '</span></div>'
        '<hr class="spec-divider">'
        '<p class="spec-section-lbl">Processor</p>'
        '<div class="spec-row"><span class="spec-key">CPU</span><span class="spec-val">' + cpu_brand + '</span></div>'
        '<div class="spec-row"><span class="spec-key">Speed</span><span class="spec-val">' + f"{cpu_speed:.1f} GHz" + '</span></div>'
        '<div class="spec-row"><span class="spec-key">GPU</span><span class="spec-val">' + gpu_brand + '</span></div>'
        '<hr class="spec-divider">'
        '<p class="spec-section-lbl">Memory</p>'
        '<div class="spec-row"><span class="spec-key">RAM</span><span class="spec-val">' + f"{ram} GB" + '</span></div>'
        '<div class="spec-row"><span class="spec-key">SSD</span><span class="spec-val">' + f"{ssd} GB" + '</span></div>'
        '<div class="spec-row"><span class="spec-key">HDD</span><span class="spec-val">' + f"{hdd} GB" + '</span></div>'
        '<hr class="spec-divider">'
        '<p class="spec-section-lbl">Display</p>'
        '<div class="spec-row"><span class="spec-key">Size</span><span class="spec-val">' + f'{screen_size}" {ppi_tier}' + '</span></div>'
        '<div class="spec-row"><span class="spec-key">Resolution</span><span class="spec-val">' + resolution + '</span></div>'
        '<div class="spec-row"><span class="spec-key">PPI</span><span class="spec-val">' + f"{ppi_p:.0f} ppi" + '</span></div>'
        '<div class="spec-row"><span class="spec-key">Touchscreen</span><span class="spec-val">' + ts_icon + '</span></div>'
        '<div class="spec-row"><span class="spec-key">IPS Panel</span><span class="spec-val">' + ips_icon + '</span></div>'
        '</div>'
    )
    st.markdown(spec_html, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div class="footer-copy">&#169; 2026 LaptopLens &middot; Built with Streamlit &amp; Scikit-learn</div>
    <div class="footer-links">
        <a href="https://github.com/Dakshhhhh-ops/laptop-price-predictor" target="_blank">GitHub</a>
        <a href="#">Dataset</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)