import streamlit as st
import streamlit.components.v1 as components
import json

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="wide")

# CSS මගින් පිටුවේ පෙනුම සකස් කිරීම
st.markdown("""
<style>
    .stApp { background-color: #f0fdf4; }
    .main-title { color: #166534; text-align: center; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎈 අකුරු බෝල - සිංහල සෙල්ලම</div>', unsafe_allow_html=True)

# 2. අදියර 20 සඳහා දත්ත
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

levels_json = json.dumps(levels, ensure_ascii=False)

# 3. Game Engine (JavaScript & HTML)
game_html = f"""
<div id="main-container" style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif;">
    
    <div id="start-screen" style="position: absolute; width: 100%; height: 100%; background: rgba(255,255,255,0.9); z-index: 100; display: flex; justify-content: center; align-items: center; border-radius: 20px;">
        <button onclick="startGame()" style="padding: 20px 40px; font-size: 24px; background: #22c55e; color: white; border: none; border-radius: 10px; cursor: pointer;">සෙල්ලම ආරම්භ කරන්න (Start Game)</button>
    </div>

    <div style="display: flex; width: 95vw; justify-content: space-between; align-items: flex-start; gap: 20px;">
        
        <div style="flex: 1; background: white; padding: 20px; border-radius: 20px; border: 4px solid #16a34a; text-align: center; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
            <h2 id="lvl-txt" style="color: #166534; margin: 0;">අදියර: 1</h2>
            <hr>
            <p style="font-size: 18px; color: #666;">සාදන්න අවශ්‍ය වචනය:</p>
            <h1 id="hint" style="color: #c2410c; background: #ffedd5; padding: 10px; border-radius: 10px; font-size: 35px;">-</h1>
        </div>

        <div style="flex: 2.5; position: relative;">
            <div id="display" style="font-size: 50px; min-height: 80px; background: white; border: 4px dashed #16a34a; border-radius: 20px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #166534;"></div>
            <canvas id="c" width="800" height="500" style="border: 5px solid #16a34a; border-radius: 20px; background: radial-gradient(#fff, #dcfce7); cursor: pointer; width: 100%;"></canvas>
        </div>

        <div style="flex: 1; background: white; padding: 20px; border-radius: 20px; border: 4px solid #16a34a; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
            <h3 style="color: #166534; margin-top: 0;">උපදෙස්</h3>
            <ul style="color: #444; font-size: 16px; text-align: left; line-height: 1.6;">
                <li>පාවෙන බෝල මත ක්ලික් කර වචනය හදන්න.</li>
                <li>වැරදුනහොත් වචනය රතු පැහැ වේ.</li>
                <li>නිවැරදි වූ විට ශබ්දයක් ඇසෙනු ඇත.</li>
            </ul>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const allLvl = {levels_json};
    
    let clickSound = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    let winSound = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    let curIdx = 0, target = "", input = "", balls = [], gameStarted = false;

    function startGame() {{
        document.getElementById('start-screen').style.display = 'none';
        gameStarted = true;
        init(0);
        draw();
    }}

    function init(idx) {{
        curIdx = idx; target = allLvl[idx].target; input = "";
        document.getElementById('lvl-txt').innerText = "අදියර: " + (idx + 1);
        document.getElementById('hint').innerText = target;
        document.getElementById('display').innerText = "";
        document.getElementById('display').style.color = "#166534";
        
        balls = [];
        allLvl[idx].pool.forEach(char => {{
            balls.push({{
                x: Math.random()*700+50, y: Math.random()*400+50,
                dx: (Math.random()-0.5)*4, dy: (Math.random()-0.5)*4,
                char: char, r: 40
            }});
        }});
    }}

    function draw() {{
        ctx.clearRect(0,0,800,500);
        balls.forEach(b => {{
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fillStyle = "#22c55e"; ctx.fill();
            ctx.strokeStyle = "#14532d"; ctx.lineWidth = 3; ctx.stroke();
            ctx.fillStyle = "white"; ctx.font = "bold 28px Arial"; ctx.textAlign="center";
            ctx.fillText(b.char, b.x, b.y+10);
            
            if(b.x+b.r > 800 || b.x-b.r < 0) b.dx *= -1;
            if(b.y+b.r > 500 || b.y-b.r < 0) b.dy *= -1;
            b.x += b.dx; b.y += b.dy;
        }});
        requestAnimationFrame(draw);
    }}

    canvas.onclick = (e) => {{
        if(!gameStarted) return;
        const r = canvas.getBoundingClientRect();
        const scaleX = 800 / r.width;
        const scaleY = 500 / r.height;
        const mx = (e.clientX - r.left) * scaleX;
        const my = (e.clientY - r.top) * scaleY;

        balls.forEach(b => {{
            if(Math.sqrt((mx-b.x)**2 + (my-b.y)**2) < b.r) {{
                clickSound.currentTime = 0; clickSound.play();
                let next = input + b.char;
                if(target.startsWith(next)) {{
                    input = next; document.getElementById('display').innerText = input;
                    if(input === target) {{
                        winSound.play();
                        setTimeout(() => {{ 
                            if(curIdx < 19) init(curIdx+1); 
                            else alert("විශිෂ්ටයි! ඔබ සියලුම අදියර ජයග්‍රහණය කළා!"); 
                        }}, 800);
                    }}
                }} else {{
                    document.getElementById('display').innerText = next;
                    document.getElementById('display').style.color = "red";
                    setTimeout(() => {{ 
                        document.getElementById('display').innerText = input; 
                        document.getElementById('display').style.color = "#166534"; 
                    }}, 400);
                }}
            }}
        }});
    }};
</script>
"""

components.html(game_html, height=750)
