import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f0fdf4; }
    .main-title { color: #166534; text-align: center; font-size: 35px; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎈 අකුරු බෝල - සිංහල සෙල්ලම</div>', unsafe_allow_html=True)

# අදියර දත්ත
levels_list = [
    {"target": "අම්මා", "pool": ["අ","ම්","මා","ක","ල","ප","ද","ග","ඉ","ස"]},
    {"target": "පාසල", "pool": ["පා","ස","ල","ග","න","ද","අ","ක","ම","ය"]},
    {"target": "පොත", "pool": ["පො","ත","ල","ය","ක","ම","ද","න","ස","ර"]},
    {"target": "මල්", "pool": ["ම","ල්","ග","ප","පො","ත","ද","ක","අ","න"]},
    {"target": "ගස", "pool": ["ග","ස","ම","ල","ක","අ","ඉ","ප","න","ද"]},
    {"target": "වැව", "pool": ["වැ","ව","ල","ක","ස","න","ම","අ","ප","ද"]},
    {"target": "හිරු", "pool": ["හි","රු","ස","ල","ක","අ","ම","න","ප","ද"]},
    {"target": "අලියා", "pool": ["අ","ලි","යා","ක","ම","ල","ස","න","ප","ද"]},
    {"target": "කමල", "pool": ["ක","ම","ල","අ","ඉ","උ","එ","ඔ","ක","ග"]},
    {"target": "රට", "pool": ["ර","ට","ම","ල","ක","අ","ස","න","ප","ද"]}
]

levels_json = json.dumps(levels_list, ensure_ascii=False)

game_template = """
<div id="main-container" style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif; touch-action: none;">
    <div id="start-screen" style="position: absolute; width: 100%; height: 100%; background: rgba(255,255,255,0.9); z-index: 100; display: flex; justify-content: center; align-items: center; border-radius: 20px;">
        <button onclick="startGame()" style="padding: 20px 40px; font-size: 22px; background: #22c55e; color: white; border: none; border-radius: 10px; cursor: pointer;">ආරම්භ කරන්න</button>
    </div>

    <div style="display: flex; width: 98vw; justify-content: center; flex-wrap: wrap; gap: 10px;">
        <div style="width: 250px; background: white; padding: 15px; border-radius: 15px; border: 3px solid #16a34a; text-align: center;">
            <h3 id="lvl-txt" style="color: #166534; margin: 0;">අදියර: 1</h3>
            <div style="margin: 10px 0; padding: 10px; background: #fee2e2; border-radius: 10px; border: 2px solid #ef4444;">
                <span style="font-size: 14px; color: #991b1b;">ඉතිරි කාලය</span><br>
                <span id="timer" style="font-size: 30px; font-weight: bold; color: #b91c1c;">30s</span>
            </div>
            <p style="margin: 5px 0; font-size: 14px;">සාදන්න:</p>
            <h2 id="hint" style="color: #c2410c; background: #ffedd5; padding: 5px; border-radius: 8px;">-</h2>
        </div>

        <div style="flex: 1; min-width: 350px; position: relative;">
            <div id="display" style="font-size: 40px; min-height: 70px; background: white; border: 3px dashed #16a34a; border-radius: 15px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #166534;"></div>
            <canvas id="c" width="800" height="500" style="border: 4px solid #16a34a; border-radius: 20px; background: radial-gradient(#fff, #dcfce7); width: 100%; height: auto; touch-action: none;"></canvas>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById('c'), ctx = canvas.getContext('2d');
    const allLvl = DATA_JSON;
    const tmrTxt = document.getElementById('timer'), disp = document.getElementById('display'), hintTxt = document.getElementById('hint');
    
    let clickSnd = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    let winSnd = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    let curIdx = 0, target = "", input = "", balls = [], gameStarted = false, timeLeft = 30, timer;

    function startGame() { document.getElementById('start-screen').style.display='none'; gameStarted=true; init(0); draw(); }

    function startTimer() {
        clearInterval(
