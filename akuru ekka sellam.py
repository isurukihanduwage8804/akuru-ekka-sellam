import streamlit as st
import streamlit.components.v1 as components
import json

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f0fdf4; }
    .title-text { color: #166534; text-align: center; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">🎈 අකුරු බෝල - සිංහල සෙල්ලම</h1>', unsafe_allow_html=True)

# 2. අදියර 20 සඳහා දත්ත
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
    {"target": "රට", "pool": ["ර","ට","ම","ල","ක","අ","ස","න","ප","ද"]},
    {"target": "නිවස", "pool": ["නි","ව","ස","ග","ල","ප","ද","අ","ඉ","උ"]},
    {"target": "සීනුව", "pool": ["සී","නු","ව","ල","ක","ය","ර","ප","ම","ද"]},
    {"target": "පන්සල", "pool": ["ප","න්","ස","ල","ග","න","ම","අ","ය","ර"]},
    {"target": "අහස", "pool": ["අ","හ","ස","ල","ක","ම","න","ග","ව","ද"]},
    {"target": "ළමයා", "pool": ["ළ","ම","යා","ක","ස","න","ප","ල","ග","ව"]},
    {"target": "දොඩම්", "pool": ["දො","ඩ","ම්","ක","ම","ල","ස","න","ප","ද"]},
    {"target": "කෙසෙල්", "pool": ["කෙ","සෙ","ල්","ල","ම","න","ප","ග","ව","අ"]},
    {"target": "පෑන", "pool": ["පෑ","න","ල","ක","ම","ස","ය","ර","ව","ද"]},
    {"target": "වෙරළ", "pool": ["වෙ","ර","ළ","ක","ම","ස","න","ප","ල","ග"]},
    {"target": "ලංකාව", "pool": ["ලං","කා","ව","ක","ම","ස","න","ප","ල","ග"]}
]

levels_json = json.dumps(levels_list, ensure_ascii=False)

# 3. Game Engine (JavaScript & HTML)
# Error එක මඟහරවා ගැනීමට html කේතය කොටස් වශයෙන් ලියමි
game_html = """
<div id="game-wrapper" style="text-align: center; font-family: 'Arial', sans-serif;">
    <div style="background: white; padding: 15px; border-radius: 15px; border: 2px solid #2e7d32; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 5px;">
            <h3 id="level-indicator" style="color: #2e7d32; margin: 0;">අදියර: 1 / 20</h3>
            <div style="color: #15803d; font-weight: bold; font-size: 18px;">
                සාදන්න: <span id="target-hint" style="color: #c2410c; background: #ffedd5; padding: 2px 8px; border-radius: 5px;"></span>
            </div>
        </div>
        <div id="word-display" style="font-size: 45px; min-height: 70px; color: #1b5e20; background: #f9fafb; border: 3px dashed #2e7d32; border-radius: 15px; margin: 5px auto; width: 400px; display: flex; align-items: center; justify-content: center; font-weight: bold;"></div>
    </div>
    <canvas id="gameCanvas" width="550" height="380" style="background: radial-gradient(#fff, #e8f5e9); border-radius: 20px; border: 5px solid #2e7d32; cursor: pointer;"></canvas>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const display = document.getElementById('word-display');
    const levelText = document.getElementById('level-indicator');
    const hintText = document.getElementById('target-hint');
    
    const clickSound = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    const winSound = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    let allLevels = """ + levels_json + """;
    let currentLvlIdx = 0;
    let target = "";
    let currentInput = "";
    let balls = [];

    function initLevel(idx) {
        currentLvlIdx = idx;
        target = allLevels[idx].target;
        let pool = allLevels[idx].pool;
