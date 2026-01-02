import streamlit as st
import streamlit.components.v1 as components

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="අකුරු බෝල - සිංහල සෙල්ලම", page_icon="🎈", layout="centered")

# --- CSS: පිටුවේ පෙනුම ---
st.markdown("""
<style>
    .stApp { background-color: #f0fdf4; }
    .title-text { color: #166534; text-align: center; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">🎈 අකුරු බෝල - සිංහල සෙල්ලම</h1>', unsafe_allow_html=True)

# 2. අදියර 20 සඳහා වචන (Levels Data)
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

# 3. Game Engine (JavaScript & HTML)
# මෙහිදී JavaScript මගින් සම්පූර්ණ Game එකම පාලනය වේ.
game_code = f"""
<div id="game-wrapper" style="text-align: center; font-family: 'Arial', sans-serif;">
    <div style="margin-bottom: 10px;">
        <h3 id="level-indicator" style="color: #2e7d32; margin: 0;">අදියර: 1 / 20</h3>
        <div id="word-display" style="font-size: 40px; min-height: 60px; color: #1b5e20; background: #ffffff; border: 4px solid #2e7d32; border-radius: 15px; margin: 10px auto; width: 350px; display: flex; align-items: center; justify-content: center; letter-spacing: 5px;"></div>
    </div>
    <canvas id="gameCanvas" width="550" height="380" style="background: radial-gradient(#fff, #e8f5e9); border-radius: 20px; border: 5px solid #2e7d32; cursor: crosshair;"></canvas>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const display = document.getElementById('word-display');
    const levelText = document.getElementById('level-indicator');
    
    const clickSound = new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3');
    const winSound = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');

    let levels = {levels};
    let currentLvl = 0;
    let target = levels[0].target;
    let pool = levels[0].pool;
    let currentInput = "";
    let balls = [];

    function initLevel(idx) {{
        currentLvl = idx;
        target = levels[idx].target;
        pool = levels[idx].pool;
        currentInput = "";
        display.innerText = "";
        levelText.innerText = "අදියර: " + (idx + 1) + " / 20";
        
        balls = [];
        pool.forEach(char => {{
            balls.push({{
                x: Math.random() * 450 + 50,
                y: Math.random() * 280 + 50,
                dx: (Math.random() - 0.5) * 4,
                dy: (Math.random() - 0.5) * 4,
                char: char,
                radius: 35,
                color: "#4caf50"
            }});
        }});
    }}

    function animate() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        balls.forEach(b => {{
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
            ctx.fillStyle = b.color;
            ctx.fill();
            ctx.strokeStyle = "#1b5e20";
            ctx.lineWidth = 3;
            ctx.stroke();
            
            ctx.fillStyle = "white";
            ctx.font = "bold 24px Arial";
            ctx.textAlign = "center";
            ctx.fillText(b.char, b.x, b.y + 10);
            
            if(b.x + b.radius > canvas.width || b.x - b.radius < 0) b.dx *= -1;
            if(b.y + b.radius > canvas.height || b.y - b.radius < 0) b.dy *= -1;
            b.x += b.dx;
            b.y += b.dy;
        }});
        requestAnimationFrame(animate);
    }}

    canvas.addEventListener('mousedown', (e) => {{
        const rect = canvas.getBoundingClientRect();
        const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
        const my = (e.clientY - rect.top) * (canvas.height / rect.height);
        
        balls.forEach(b => {{
            const dist = Math.sqrt((mx - b.x)**2 + (my - b.y)**2);
            if(dist < b.radius) {{
                clickSound.play();
                currentInput += b.char;
                display.innerText = currentInput;
                
                if(currentInput === target) {{
                    winSound.play();
                    setTimeout(() => {{
                        if(currentLvl < 19) {{
                            initLevel(currentLvl + 1);
                        }} else {{
                            alert("සුභ පැතුම්! ඔබ සියලුම අදියර ජයග්‍රහණය කළා!");
                            initLevel(0);
                        }}
                    }}, 600);
                }} else if (!target.startsWith(currentInput)) {{
                    currentInput = "";
                    display.innerText = "";
                }}
            }}
        }});
    }});

    initLevel(0);
    animate();
</script>
"""

components.html(game_code, height=600)

st.sidebar.title("📊 Game Info")
st.sidebar.info("අකුරු බෝල මත ක්ලික් කරන්න. නිවැරදි අනුපිළිවෙලට අකුරු තෝරා වචනය සම්පූර්ණ කරන්න.")
if st.sidebar.button("Restart Game"):
    st.rerun()
