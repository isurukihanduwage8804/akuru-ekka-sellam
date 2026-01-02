import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="අකුරු බෝල", layout="wide")

# 1. සිංහල අකුරු දත්ත
data = [
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
data_json = json.dumps(data, ensure_ascii=False)

# 2. UI එක සැකසීම
st.markdown('<h1 style="text-align:center;color:green;">🎈 අකුරු බෝල - සිංහල සෙල්ලම</h1>', unsafe_allow_html=True)

# 3. HTML කේතය කොටස් වලට වෙන් කර ඇත (Error වැළැක්වීමට)
h = '<div style="display:flex;flex-direction:column;align-items:center;font-family:sans-serif;touch-action:none;">'
h += '<div id="start" style="position:absolute;width:100%;height:100%;background:white;z-index:100;display:flex;justify-content:center;align-items:center;">'
h += '<button onclick="startGame()" style="padding:20px;font-size:20px;background:green;color:white;border:none;border-radius:10px;">ආරම්භ කරන්න</button></div>'
h += '<div style="display:flex;gap:20px;margin-bottom:10px;">'
h += '<div style="padding:10px;border:3px solid green;border-radius:15px;text-align:center;min-width:150px;">'
h += '<h3 id="lv">අදියර: 1</h3><div id="tm" style="font-size:30px;color:red;font-weight:bold;">30s</div></div>'
h += '<div style="flex:1;min-width:300px;"><div id="ds" style="font-size:40px;min-height:70px;border:3px dashed green;border-radius:15px;display:flex;align-items:center;justify-content:center;font-weight:bold;"></div>'
h += '<p style="text-align:center;">සාදන්න: <b id="ht" style="color:orange;font-size:25px;"></b></p></div></div>'
h += '<canvas id="c" width="800" height="450" style="border:4px solid green;border-radius:20px;background:#f0fff0;width:100%;"></canvas></div>'

h += '<script>'
h += 'const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");'
h += 'const all=' + data_json + ',lvT=document.getElementById("lv"),tmT=document.getElementById("tm"),dsT=document.getElementById("ds"),htT=document.getElementById("ht");'
h += 'let cur=0,tar="",inp="",balls=[],started=false,time=30,timer;'
h += 'let sndC=new Audio("
