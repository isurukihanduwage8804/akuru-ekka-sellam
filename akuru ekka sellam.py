import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල", layout="wide")

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
<div style="text-align: center; font-family: sans-serif; touch-action: none;">
    <div id="start-screen" style="position: absolute; width: 100%; height: 100%; background: white; z-index: 10; display: flex; justify-content: center; align-items: center;">
        <button onclick="startGame()" style="padding: 20px; font-size: 20px; cursor: pointer;">සෙල්ලම අරඹන්න</button>
    </div>
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 10px;">
        <div style="padding: 10px; border: 2px solid green; border-radius: 10px; min-width: 150px;">
            <h3 id="lvl">අදියර: 1</h3>
            <div id="tmr" style="font-size: 25px; color: red; font-weight: bold;">30s</div>
        </div>
        <div id="disp" style="font-size: 40px; border: 3px dashed green; width: 300px; min-height: 60px; border-radius: 10px;"></div>
    </div>
    <p>සාදන්න: <b id="hint" style="color: orange; font-size: 24px;"></b></p>
    <canvas id="c" width="800" height="450" style="border: 4px solid green; border-radius: 20px; background: white; width: 100%;"></canvas>
</div>

<script>
    const canvas = document.getElementById('c'), ctx = canvas.getContext('2d');
    const allLvl = {levels_json}, lvlTxt = document.getElementById('lvl');
    const tmrTxt = document.getElementById('tmr'), disp = document.getElementById('disp'), hint = document.getElementById('hint');
    
    let curIdx = 0, target = "", input = "", balls = [], gameStarted = false, timeLeft = 30, timer;
    let clickSnd = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    let winSnd = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    function startGame() {{ document.getElementById('start-screen').style.display='none'; gameStarted=true; init(0); draw(); }}

    function init(idx) {{
        curIdx = idx; target = allLvl[idx].target; input = "";
        lvlTxt.innerText = "අදියර: " + (idx + 1); hint.innerText = target; disp.innerText = "";
        clearInterval(timer); timeLeft = 30; tmrTxt.innerText = "30s";
        timer = setInterval(() => {{
            timeLeft--; tmrTxt.innerText = timeLeft + "s";
            if(timeLeft <= 0) {{ clearInterval(timer); alert("කාලය අවසන්!"); init(curIdx); }}
        }}, 1000);
        balls = allLvl[idx].pool.map(c => ({{ x: Math.random()*700+50, y: Math.random()*350+50, dx: (Math.random()-0.5)*4, dy: (Math.random()-0.5)*4, char: c, r: 40 }}));
    }}

    function draw() {{
        ctx.clearRect(0,0,800,450);
        balls.forEach(b => {{
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fillStyle = "green"; ctx.fill(); ctx.fillStyle = "white";
            ctx.font = "bold 25px Arial"; ctx.textAlign="center"; ctx.fillText(b.char, b.x, b.y+10);
            if(b.x+b.r > 800 || b.x-b.r < 0) b.dx *= -1; if(b.y+b.r > 450 || b.y-b.r < 0) b.dy *= -1;
            b.x += b.dx; b.y += b.dy;
        }});
        requestAnimationFrame(draw);
    }}

    function handle(e) {{
        if(!gameStarted) return; e.preventDefault();
        const r = canvas.getBoundingClientRect(), scaleX = 800/r.width, scaleY = 450/r.height;
        const cx = e.touches ? e.touches[0].clientX : e.clientX, cy = e.touches ? e.touches[0].clientY : e.clientY;
        const mx = (cx - r.left)*scaleX, my = (cy - r.top)*scaleY;
        balls.forEach(b => {{
            if(Math.sqrt((mx-b.x)**2 + (my-b.y)**2) < b.r) {{
                clickSnd.currentTime = 0; clickSnd.play();
                let next = input + b.char;
                if(target.startsWith(next)) {{
                    input = next; disp.innerText = input; timeLeft = 30;
                    if(input === target) {{ winSnd.play(); setTimeout(() => init(curIdx+1), 800); }}
                }} else {{ disp.innerText = next; setTimeout(() => disp.innerText = input, 400); }}
            }}
        }});
    }}
    canvas.addEventListener('mousedown', handle); canvas.addEventListener('touchstart', handle, {{passive: false}});
</script>
"""

components.html(game_html, height=700)
