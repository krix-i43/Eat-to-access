from flask import Flask, jsonify, request
import requests
from urllib.parse import urlparse, parse_qs
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

app = Flask(__name__)
app.json.sort_keys = False 

def get_garena_data(eat_token):
    try:
        callback_url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        response = requests.get(callback_url, allow_redirects=False, timeout=10)

        if 300 <= response.status_code < 400 and "Location" in response.headers:
            redirect_url = response.headers["Location"]
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)

            token_value = query_params.get("access_token", [None])[0]
            account_id = query_params.get("account_id", [None])[0]
            account_nickname = query_params.get("nickname", [None])[0]
            region = query_params.get("region", [None])[0]

            if not token_value or not account_id:
                return {"error": "Failed to extract data from Garena"}
        else:
            return {"error": "Invalid access token or session expired"}

        openid_url = "https://shop2game.com/api/auth/player_id_login"
        openid_headers = { 
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ar-MA,ar;q=0.9,en-US;q=0.8,en;q=0.7,ar-AE;q=0.6,fr-FR;q=0.5,fr;q=0.4",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "source=mb; region=MA; mspid2=ca21e6ccc341648eea845c7f94b92a3c; language=ar; _ga=GA1.1.1955196983.1741710601; datadome=WY~zod4Q8I3~v~GnMd68u1t1ralV5xERfftUC78yUftDKZ3jIcyy1dtl6kdWx9QvK9PpeM~A_qxq3LV3zzKNs64F_TgsB5s7CgWuJ98sjdoCqAxZRPWpa8dkyfO~YBgr; session_key=v0tmwcmf1xqkp7697hhsno0di1smy3dm; _ga_0NY2JETSPJ=GS1.1.1741710601.1.1.1741710899.0.0.0",
            "Origin": "https://shop2game.com",
            "Referer": "https://shop2game.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"'
        }
        payload = {"app_id": 100067, "login_id": str(account_id)}

        openid_res = requests.post(openid_url, headers=openid_headers, json=payload, timeout=10)
        openid_data = openid_res.json()

        open_id = openid_data.get("open_id")
        

        return {
            "credit": "Nivashini",
            "Power By": "insta : @ft_rosie._ & @krix_i43",
            "status": "success",
            "account_id": account_id,
            "account_nickname": account_nickname,
            "open_id": open_id,
            "access_token": token_value,
            "region": region
        }


    except Exception as e:
        return {"error": "Server error", "details": str(e)}

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Eat Token Decoder</title>
<style>
:root{
    --bg:#020617;
    --card:#0f172a;
    --text:#fff;
    --accent:#22d3ee;
}
body.light{--bg:#f8fafc;--card:#fff;--text:#000;--accent:#2563eb;}
body.neon{--bg:#000;--card:#020617;--text:#fff;--accent:#00ffff;}

body{
    background:var(--bg);
    color:var(--text);
    font-family:Arial;
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.frame{
    aspect-ratio:9/16;
    width:min(100vw,420px);
    background:var(--card);
    border-radius:20px;
    padding:14px;
    display:flex;
    flex-direction:column;
    gap:8px;
    box-shadow:0 0 20px var(--accent);
}

h1{text-align:center;color:var(--accent);margin:4px 0;}
input,button{padding:10px;border-radius:8px;border:none;}
button{background:var(--accent);cursor:pointer;}
button:disabled{background:#475569;}

.card{background:var(--bg);padding:8px;border-radius:8px;font-size:13px;}
.hidden{display:none;}

#trollBox{
    font-size:13px;
    min-height:28px;
    white-space:pre-line;
    opacity:0.95;
}

#toast{
    position:fixed;
    bottom:20px;
    background:var(--accent);
    color:black;
    padding:10px 16px;
    border-radius:20px;
    display:none;
}
</style>
</head>

<body class="dark">

<div class="frame">
    <h1>🍪 Eat Token</h1>

    <div style="display:flex;gap:6px;">
        <button onclick="setMode('dark')">🌙</button>
        <button onclick="setMode('light')">☀️</button>
        <button onclick="setMode('neon')">✨</button>
    </div>

    <input id="token" placeholder="Paste Eat Token"
           onfocus="showMindVoice()">

    <div id="mindVoice" style="font-size:13px;opacity:0.85;display:none;"></div>

    <button onclick="alert('Button click aagudhu da 😄')">Decode</button>

    <div id="trollBox"></div>

    <div id="smart" class="hidden">
        <div class="card"><b>UID:</b> <span id="uid"></span></div>
        <div class="card"><b>Name:</b> <span id="name"></span></div>
        <div class="card"><b>Region:</b> <span id="region"></span></div>
        <div class="card">
            <b>Access Token:</b><br>
            <small id="accesstoken"></small><br>
            <button onclick="copyToken()">📋 Copy</button>
        </div>
        <div class="card">
            <b>Expiry:</b>
            <div id="countdown">--:--:--</div>
        </div>
    </div>

    <button onclick="toggleRaw()">Show Raw JSON</button>
    <pre id="raw" class="hidden"></pre>

    <button onclick="openInsta()">📸 Follow on Instagram</button>
</div>

<div id="toast"></div>

<script>
/* ---------- THEME ---------- */
function setMode(m){ document.body.className = m; }

/* ---------- TOAST ---------- */
function toast(msg){
    const t = document.getElementById("toast");
    t.innerText = msg;
    t.style.display="block";
    setTimeout(()=>t.style.display="none",2000);
}

/* ---------- MIND VOICE (RANDOM) ---------- */
let mindVoiceShown=false;
const mindVoices=[
 '🧠 Un mind voice: "Idhu work aaguma da?"',
 '🧠 Un mind voice: "Server down irukumo?"',
 '🧠 Un mind voice: "Scam ah irukaadhe 😅"',
 '🧠 Un mind voice: "Token safe ah?"',
 '🧠 Un mind voice: "Developer trust pannalama 🤔"'
];
const mindReplies=[
 '😎 Relax. Aagum.',
 '🔥 Chill da.',
 '💪 Trust the process.',
 '✨ Smooth-aa work aagum.'
];
function showMindVoice(){
    if(mindVoiceShown) return;
    mindVoiceShown=true;
    const mv=document.getElementById("mindVoice");
    mv.style.display="block";
    mv.innerText=mindVoices[Math.floor(Math.random()*mindVoices.length)];
    setTimeout(()=>mv.innerText=mindReplies[Math.floor(Math.random()*mindReplies.length)],1500);
}

/* ---------- GOD MODE TROLL ---------- */
const godSuccessMemes=[
 "🥳 Paathiya… sonnen la 😎",
 "🔥 Decode easy da boss",
 "😏 Tool mela nambikkai vechaa ipdi dhaan",
 "💪 Success! Coffee time ☕"
];
const godExpiryMemes=[
 "🪦 R.I.P Token\nBorn: Few minutes ago\nDied: Just now 😭\n👉 New token eduthutu va da",
 "⌛ Token expiry aagiruchu 😅\n🆕 Pudhu token kondu va",
 "📜 Archaeology report:\nIndha token romba pazhasu 😂",
 "😴 Token tired\n🔁 Fresh token try pannu"
];

function godModeStart(){
    const b=document.getElementById("trollBox");
    b.innerText="❌ SERVER ERROR\nConnection lost";
    setTimeout(()=>b.innerText="😂 Just kidding da…\n🤖 AI thinking…",800);
    setTimeout(()=>b.innerText="🤖 Thinking…\n🤖 Overthinking…\n🤖 Dei naan robot da 😅",1500);
    setTimeout(()=>b.innerText='🧠 Un mind voice:\n"Idhu thirumba troll ah?"\n😂 Aama da',2400);
}
function godModeSuccess(){
    document.getElementById("trollBox").innerText=
        godSuccessMemes[Math.floor(Math.random()*godSuccessMemes.length)];
}
function godModeExpiry(){
    document.getElementById("trollBox").innerText=
        godExpiryMemes[Math.floor(Math.random()*godExpiryMemes.length)];
}

/* ---------- COUNTDOWN ---------- */
let timer=null;
function startCountdown(sec){
    const el=document.getElementById("countdown");
    clearInterval(timer);
    timer=setInterval(()=>{
        if(sec<=0){ el.innerText="❌ Token Expired"; clearInterval(timer); return; }
        let h=Math.floor(sec/3600),
            m=Math.floor((sec%3600)/60),
            s=sec%60;
        el.innerText=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
        sec--;
    },1000);
}

/* ---------- MAIN DECODE ---------- */
let tokenValue=null;
async function decode(){
    const t=document.getElementById("token").value;
    if(!t){ toast("Enter token"); return; }

    godModeStart();

    const r=await fetch("/Eat?eat_token="+t);
    const d=await r.json();

    document.getElementById("raw").innerText=JSON.stringify(d,null,2);

    if(!d.access_token){
        godModeExpiry();
        return;
    }

    tokenValue=d.access_token;
    document.getElementById("uid").innerText=d.account_id;
    document.getElementById("name").innerText=d.account_nickname;
    document.getElementById("region").innerText=d.region;
    document.getElementById("accesstoken").innerText=tokenValue;

    document.getElementById("smart").classList.remove("hidden");
    startCountdown(7200); // example: 2 hours
    godModeSuccess();
}

/* ---------- UTILS ---------- */
function copyToken(){
    navigator.clipboard.writeText(tokenValue);
    toast("Access Token Copied");
}
function toggleRaw(){
    document.getElementById("raw").classList.toggle("hidden");
}
function openInsta(){
    window.open("https://instagram.com/ft_rosie._","_blank");
}
</script>

</body>
</html>
"""


@app.route("/Eat", methods=["GET"])
def get_token_info():
    eat_token = request.args.get("eat_token")

    if not eat_token:
        return jsonify({"error": "Missing access token parameter."}), 400

    result = get_garena_data(eat_token)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5030)




