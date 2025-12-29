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
    <div style="text-align: center; font-family: Arial, sans-serif; margin-top: 50px;">
        <h1 style="color: #2ecc71;">Eat Token Decoder API is Running!</h1>
        <p><b>Credit:</b> Nivashini</p>
        <p><b>Powered By:</b> @ft_rosie._ & @krix_i43 </p>
        <hr style="width: 50%; border: 1px solid #eee;">
        <h2 style="color: #7f8c8d;">Use <code>/Eat?eat_token={Your Eat Token}</code> endpoint to get data.</h2>
    </div>
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


