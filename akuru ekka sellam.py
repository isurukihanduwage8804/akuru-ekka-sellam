import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල", layout="wide")

# 1. දත්ත (Data)
levels = [
    {"target": "අම්මා", "pool": ["අ","ම්","මා","ක","ල","ප","ද","ග","ඉ","ස"]},
    {"target": "පාසල", "pool": ["පා","ස","ල","ග","න","ද","අ","ක","ම","ය"]},
    {"target": "පොත", "pool": ["පො","ත","ල","ය","ක","ම","ද","න","ස","ර"]},
    {"target": "මල්", "pool": ["ම","ල්","ග","ප","පො","ත","ද","ක","අ","න"]},
    {"target": "ගස", "pool": ["ග","ස","ම","ල","ක","අ","ඉ","ප","න","ද"]}
]
data_json = json.dumps(levels, ensure_ascii=False)

# 2. Sound Links (Error වැළැක්වීමට කෙටි පේළි ලෙස)
s1 = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
s2 = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

# 3. HTML කේතය සෑදීම
h = '<div style="text-align:center;font-family:sans-serif;touch-action:none;">'
h += '<div id="start" style="position:absolute;width:100%;height:100%;background:white;z-index:9;display:flex;justify-content:center;align-items:center;">'
h += '<button onclick="startGame()" style="padding:20px;font-size:20px;background:green;color:white;border-radius:10px;">ආරම්භ කරන්න</button></div>'
h += '<div style="display:flex;justify-content:center;gap:20px;">'
h += '<div style="padding:10px;border:3px solid green;border-radius:15px;">'
h += '<h3 id="lv">අදියර: 1</h3><div id="tm" style="font-size:30px;color:red;font-weight:bold;">30s</div></div>'
h += '<div style="flex:1;max-width:400px;"><div id="ds" style="font-size:40px;min-height:70px;border:3px dashed green;border-radius:15px;display:flex;align-items:center;justify-content:center;"></div>'
h += '<p>සාදන්න: <b id="ht" style="color:orange;font-size:25px;"></b></p></div></div>'
h += '<canvas id="c" width="800" height="450" style="border:4px solid green;border-radius:20px;background:#f0fff0;width:100%;"></canvas></div>'

h += '<script>'
h += 'const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");'
h += 'const all=' + data_json + ',lvT=document.getElementById("lv"),tmT=document.getElementById("tm"),dsT=document.getElementById("ds"),htT=document.getElementById("ht");'
h += 'let cur=0,tar="",inp="",balls=[],started=false,time=30,timer;'
h += 'let sndC=new Audio("' + s1 + '");'
h += 'let sndW=new Audio("' + s2 + '");'

h += 'function startGame(){document.getElementById("start").style.display="none";started=true;init(0);draw();}'
h += 'function startT(){clearInterval(timer);time=30;tmT.innerText="30s";timer=setInterval(()=>{time--;tmT.innerText=time+"s";if(time<=0){clearInterval(timer);alert("කාලය අවසන්!");init(cur);}},1000);}'
h += 'function init(idx){if(idx>=all.length){alert("ඔබ සියලු අදියර ජයගත්තා!");return;}cur=idx;tar=all[idx].target;inp="";lvT.innerText="අදියර: "+(idx+1);htT.innerText=tar;dsT.innerText="";startT();'
h += 'balls=all[idx].pool.map(c=>({x:Math.random()*700+50,y:Math.random()*350+50,dx:(Math.random()-0.5)*4,dy:(Math.random()-0.5)*4,char:c,r:40}));}'

h += 'function draw(){ctx.clearRect(0,0,800,450);balls.forEach(b=>{ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fillStyle="green";ctx.fill();ctx.fillStyle="white";ctx.font="bold 25px Arial";ctx.textAlign="center";ctx.fillText(b.char,b.x,b.y+10);'
h += 'if(b.x+b.r>800||b.x-b.r<0)b.dx*=-1;if(b.y+b.r>450||b.y-b.r<0)b.dy*=-1;b.x+=b.dx;b.y+=b.dy;});requestAnimationFrame(draw);}'

h += 'function handle(e){if(!started)return;e.preventDefault();const r=canvas.getBoundingClientRect(),sx=800/r.width,sy=450/r.height;'
h += 'const cx=e.touches?e.touches[0].clientX:e.clientX,cy=e.touches?e.touches[0].clientY:e.clientY,mx=(cx-r.left)*sx,my=(cy-r.top)*sy;'
h += 'balls.forEach(b=>{if(Math.sqrt((mx-b.x)**2+(my-b.y)**2)<b.r){sndC.currentTime=0;sndC.play();let n=inp+b.char;'
h += 'if(tar.startsWith(n)){inp=n;dsT.innerText=inp;time=30;if(inp===tar){sndW.play();setTimeout(()=>{init(cur+1);},800);}}'
h += 'else{dsT.innerText=n;dsT.style.color="red";setTimeout(()=>{dsT.innerText=inp;dsT.style.color="black";},400);}}});}'
h += 'canvas.addEventListener("mousedown",handle);canvas.addEventListener("touchstart",handle,{passive:false});'
h += '</script>'

components.html(h, height=700)
