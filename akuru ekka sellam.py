import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="centered")

st.markdown('<h1 style="color: #166534; text-align: center;">🎈 අකුරු බෝල - සිංහල සෙල්ලම</h1>', unsafe_allow_html=True)

# අදියර 20 සඳහා දත්ත
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
    {"target": "වෙරළ", "pool": ["වෙර","ළ","ක","ම","ස","න","ප","ල","ග","ව"]},
    {"target": "ලංකාව", "pool": ["ලං","කා","ව","ක","ම","ස","න","ප","ල","ග"]}
]

levels_json = json.dumps(levels, ensure_ascii=False)

# HTML සහ JavaScript කොටස ඉතාම සරලව
game_html = f"""
<div id="game-wrapper" style="text-align: center; font-family: sans-serif;">
    <div style="background: white; padding: 10px; border: 2px solid green; border-radius: 10px;">
        <h4 id="lvl-txt">අදියර: 1</h4>
        <p>සාදන්න: <b id="hint" style="color: orange;"></b></p>
        <div id="display" style="font-size: 40px; min-height: 60px; background: #eee; border-radius: 10px; margin: 10px 0;"></div>
    </div>
    <canvas id="c" width="500" height="350" style="border: 3px solid green; border-radius: 10px; background: white;"></canvas>
</div>
<script>
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    const allLvl = {levels_json};
    let curIdx = 0, target = "", input = "", balls = [];

    function init(idx) {{
        curIdx = idx; target = allLvl[idx].target; input = "";
        document.getElementById('lvl-txt').innerText = "අදියර: " + (idx + 1);
        document.getElementById('hint').innerText = target;
        document.getElementById('display').innerText = "";
        document.getElementById('display').style.color = "black";
        balls = allLvl[idx].pool.map(c => ({{
            x: Math.random()*400+50, y: Math.random()*250+50,
            dx: Math.random()*2-1, dy: Math.random()*2-1,
            char: c, r: 30
        }}));
    }}
    function draw() {{
        ctx.clearRect(0,0,500,350);
        balls.forEach(b => {{
            ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fillStyle = "green"; ctx.fill();
            ctx.fillStyle = "white"; ctx.font = "20px Arial"; ctx.textAlign="center";
            ctx.fillText(b.char, b.x, b.y+7);
            if(b.x+b.r > 500 || b.x-b.r < 0) b.dx *= -1;
            if(b.y+b.r > 350 || b.y-b.r < 0) b.dy *= -1;
            b.x += b.dx; b.y += b.dy;
        }});
        requestAnimationFrame(draw);
    }}
    canvas.onclick = (e) => {{
        const r = canvas.getBoundingClientRect();
        const mx = e.clientX - r.left, my = e.clientY - r.top;
        balls.forEach(b => {{
            if(Math.sqrt((mx-b.x)**2 + (my-b.y)**2) < b.r) {{
                let next = input + b.char;
                if(target.startsWith(next)) {{
                    input = next; document.getElementById('display').innerText = input;
                    if(input === target) {{
                        setTimeout(() => {{ if(curIdx < 19) init(curIdx+1); else alert("ජය!"); }}, 500);
                    }}
                }} else {{
                    document.getElementById('display').innerText = next;
                    document.getElementById('display').style.color = "red";
                    setTimeout(() => {{ document.getElementById('display').innerText = input; document.getElementById('display').style.color = "black"; }}, 400);
                }}
            }}
        }});
    }};
    init(0); draw();
</script>
"""

components.html(game_html, height=600)
