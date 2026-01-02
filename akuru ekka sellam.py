import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="wide")

# CSS මගින් Graphics ලස්සන කිරීම
st.markdown("""
<style>
    .stApp { background-color: #f0fdf4; }
    .main-title { color: #166534; text-align: center; font-size: 35px; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎈 අකුරු බෝල - සිංහල සෙල්ලම</div>', unsafe_allow_html=True)

# අදියර දත්ත
levels = [
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

levels_json = json.dumps(levels, ensure_ascii=False)

game_html = f"""
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
    const allLvl = {levels_json}, tmrTxt = document.getElementById('timer');
    const disp = document.getElementById('display'), hintTxt = document.getElementById('hint');
    
    let clickSnd = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    let winSnd = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    let curIdx = 0, target = "", input = "", balls = [], gameStarted = false, timeLeft = 30, timer;

    function startGame() {{ document.getElementById('start-screen').style.display='none'; gameStarted=true; init(0); draw(); }}

    function startTimer() {{
        clearInterval(timer); timeLeft = 30; tmrTxt.innerText = "30s";
        timer = setInterval(() => {{
            timeLeft--; tmrTxt.innerText = timeLeft + "s";
            if(timeLeft <= 0) {{ clearInterval(timer); alert("කාලය අවසන්! නැවත උත්සාහ කරන්න."); init(curIdx); }}
        }}, 1000);
    }}

    function init(idx) {{
        curIdx = idx; target = allLvl[idx].target; input = "";
        document.getElementById('lvl-txt').innerText = "අදියර: " + (idx + 1);
        hintTxt.innerText = target; disp.innerText = "";
        startTimer();
        balls = allLvl[idx].pool.map(c => ({{
            x: Math.random()*700+50, y: Math.random()*400+50,
            dx: (Math.random()-0.5)*4, dy: (Math.random()-0.5)*4,
            char: c, r: 45
        }}));
    }}

    function draw() {{
        ctx.clearRect(0,0,800,500);
        balls.forEach(b => {{
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fillStyle = "#22c55e"; ctx.fill();
            ctx.strokeStyle = "#14532d"; ctx.lineWidth = 3; ctx.stroke();
            ctx.fillStyle = "white"; ctx.font = "bold 30px Arial"; ctx.textAlign="center";
            ctx.fillText(b.char, b.x, b.y+12);
            if(b.x+b.r > 800 || b.x-b.r < 0) b.dx *= -1; if(b.y+b.r > 500 || b.y-b.r < 0) b.dy *= -1;
            b.x += b.dx; b.y += b.dy;
        }});
        requestAnimationFrame(draw);
    }}

    function handle(e) {{
        if(!gameStarted) return; e.preventDefault();
        const r = canvas.getBoundingClientRect(), sx = 800/r.width, sy = 500/r.height
