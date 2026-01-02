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

# 2. Sound Links
s1 = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
s2 = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

# 3. HTML කේතය (Canvas ප්‍රමාණය අඩු කර ඇත)
h = '<div style="text-align:center;font-family:sans-serif;touch-action:none;">'
h += '<div id="start" style="position:absolute;width:100%;height:100%;background:white;z-index:9;display:flex;justify-content:center;align-items:center;">'
h += '<button onclick="startGame()" style="padding:15px;font-size:18px;background:green;color:white;border-radius:10px;">ආරම්භ කරන්න</button></div>'
h += '<div style="display:flex;justify-content:center;gap:15px;margin-bottom:10px;">'
h += '<div style="padding:8px;border:3px solid green;border-radius:12px;min-width:120px;">'
h += '<h4 id="lv" style="margin:0;">අදියර: 1</h4><div id="tm" style="font-size:24px;color:red;font-weight:bold;">30s</div></div>'
h += '<div style="flex:1;max-width:350px;"><div id="ds" style="font-size:35px;min-height:60px;border:3px dashed green;border-radius:12px;display:flex;align-items:center;justify-content:center;"></div>'
h += '<p style="margin:5px 0;">සාදන්න: <b id="ht" style="color:orange;font-size:22px;"></b></p></div></div>'
# මෙහි width=600 සහ height=400 ලෙස අඩු කර ඇත
h += '<canvas id="c" width="600" height="400" style="border:4px solid green;border-radius:15px;background:#f0fff0;max-width:100%;height:auto;"></canvas></div>'

h += '<script>'
h += 'const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");'
h += 'const all=' + data_json + ',lvT=document.getElementById("lv"),tmT=document.getElementById("tm"),dsT=document.getElementById("ds"),htT=document.getElementById("ht");'
h += 'let cur=0,tar="",inp="",balls=[],started=false,time=30,timer;'
h += 'let sndC=new Audio("' + s1 + '");'
h += 'let sndW=new Audio("' + s2 + '");'

h += 'function startGame(){document.getElementById("start").style.display="none";started=true;init(0);draw();}'
h += 'function startT(){clearInterval(timer);time=30;tmT.innerText="30s";timer=setInterval(()=>{time--;tmT.innerText=time+"s";if(time<=0){clearInterval(timer);alert("කාලය අවසන්!");init(cur);}},1000);}'
h += 'function init(idx){if(idx>=all.length){alert("සියලු අදියර ජයගත්තා!");return;}cur=idx;tar=all[idx].target;inp="";lvT.innerText="අදියර: "+(idx+1);htT.innerText=tar;dsT.innerText="";startT();'
# බෝල වල වේගය සහ ප්‍රමාණයද ප්‍රමාණයට ගැලපෙන සේ සකස් කළා
h += 'balls=all[idx].pool.map(c=>({x:Math.random()*500+50,y:Math.random()*300+50,dx:(Math.random()-0.5)*3,dy:(Math.random()-0.5)*3,char:c,r:35}));}'

h += 'function draw(){ctx.clearRect(0,0,600,400);balls.forEach(b=>{ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fillStyle="green";ctx.fill();ctx.fillStyle="white";ctx.font="bold 22px Arial";ctx.textAlign="center";ctx.fillText(b.char,b.x,b.y+8);'
h += 'if(b.x+b.r>600||b.x-b.r<0)b.dx*=-1;if(b.y+b.r>400||b.y-b.r<0)b.dy*=-1;b.x+=b.dx;b.y+=b.dy;});requestAnimationFrame(draw);}'

h += 'function handle(e){if(!started)return;e.preventDefault();const r=canvas.getBoundingClientRect(),sx=600/r.width,sy=400/r.height;'
h += 'const cx=e.touches?e.touches[0].clientX:e.clientX,cy=e.touches?e.touches[0].clientY:e.clientY,mx=(cx-r.left)*sx,my=(cy-r.top)*sy;'
h += 'balls.forEach(b=>{if(Math.sqrt((mx-b.x)**2+(my-b.y)**2)<b.r){sndC.currentTime=0;sndC.play();let n=inp+b.char;'
h += 'if(tar.startsWith(n)){inp=n;dsT.innerText=inp;time=30;if(inp===tar){sndW.play();setTimeout(()=>{init(cur+1);},800);}}'
h += 'else{dsT.innerText=n;dsT.style.color="red";setTimeout(()=>{dsT.innerText=inp;dsT.style.color="black";},400);}}});}'
h += 'canvas.addEventListener("mousedown",handle);canvas.addEventListener("touchstart",handle,{passive:false});'
h += '</script>'

components.html(h, height=650)
