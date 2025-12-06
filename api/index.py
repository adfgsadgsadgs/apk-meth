import requests
from flask import Flask, jsonify, request
import time
app = Flask(__name__)
title = "F557C"
secret = "6PKBC415W4HQD96CKEMRXW4BPQ87S9TOKDBAJEHSZMNMOYYTIC"   
def GetUserId(ticket):return ticket[:16].replace("'", "").replace("-", "").replace(".", "")
def Headers():return {"content-type": "application/json", "X-SecretKey": secret}
def OculusValidationMadeByQwizx(ocid, nonce):
    keys = ["OC|31195460226768852|cfeddbca5c068fca7299363512cee68e"]
    for token in keys:
        try:
            url = f"https://graph.oculus.com/{ocid}?access_token={token}"
            response = requests.get(url, headers={"Content-Type": "application/json"})
            data = response.json()
            if 'id' in data:return True
            if 'error' in data:
                message = data['error'].get('message')
                if "Invalid OAuth access token - Cannot parse access token" in message:continue
            url = "https://graph.oculus.com/user_nonce_validate"
            response = requests.post(url, json={"nonce": nonce, "access_token": token})
            data = response.json()
            if data.get("is_valid") == "true":return True
            if 'error' in data:
                message = data['error'].get('message')
                if "Invalid OAuth access token - Cannot parse access token" in message:
                    continue
        except Exception as e:
            print(e)
    print("invalid")
    return False
@app.route("/photon", methods=["GET", "POST"])
def PhotonMadeByQwizx():
    data = request.get_json(silent=True) or request.args
    data = {k.lower(): v for k, v in data.items()}
    ticket = data.get("ticket") or data.get("username")
    nonce = data.get("nonce")
    titleid = data.get("appid")
    token = data.get("token")
    pid = GetUserId(ticket)
    if titleid != title: return jsonify({"error":"no"}), 403
    print(f"{data}")
    if not ticket:return jsonify({"error":"NO"}), 403
    if not nonce:return jsonify({"error":"NO"}), 403
    return jsonify({"ResultCode": 1,"StatusCode": 200, "UserId": pid, "AppId": titleid, "Ticket": ticket, "Token": token,"Nonce": nonce})
@app.route("/api/PlayFabAuthentication", methods=["POST"])
def PlayFabAuthentcationMadeByQwizx():
    data = request.get_json()
    oculus_id = data.get("OculusId")
    nonce = data.get("Nonce")
    if not data.get("Platform") == "Quest":return jsonify({"Message": "scary hacker!!"}), 403
    if not oculus_id or not OculusValidationMadeByQwizx(oculus_id, nonce):
        print("no nonce or ocid")
        return jsonify({"error": "no way brotein shake"}), 403
    lr = requests.post(url=f"https://{title}.playfabapi.com/Server/LoginWithServerCustomId",json={"ServerCustomId": f"OCULUS{oculus_id}","CreateAccount": True},headers=Headers())
    if lr.status_code == 200:
        d = lr.json().get("data")
        requests.post(url=f"https://{title}.playfabapi.com/Client/LinkCustomID",json={"CustomId": f"OCULUS{oculus_id}", "ForceLink": True},headers={"content-type": "application/json","x-authorization": d.get("SessionTicket")})
        print({"PlayFabId": d.get("PlayFabId"), "SessionTicket": d.get("SessionTicket"), "EntityToken": d.get("EntityToken", {}).get("EntityToken"), "EntityId": d.get("EntityToken", {}).get("Entity", {}).get("Id"), "EntityType": d.get("EntityToken", {}).get("Entity", {}).get("Type")}) 
        return jsonify({"PlayFabId": d.get("PlayFabId"),"SessionTicket": d.get("SessionTicket"),"EntityToken": d.get("EntityToken", {}).get("EntityToken"), "EntityId": d.get("EntityToken", {}).get("Entity", {}).get("Id"),"EntityType": d.get("EntityToken", {}).get("Entity", {}).get("Type")}), 200
    if lr.status_code == 403:
        data = lr.json()
    if data.get("errorCode") == 1002:
        reason, times = next(iter(data.get("errorDetails", {}).items()), ("no reason ?", []))
        print(reason)
        return jsonify({"BanMessage": reason,"BanExpirationTime": times[0] if times else "no expo ?"}), 403
@app.route("/cbfn", methods=["POST"])
def CheckForBadNameMadeByQwizx():return jsonify({"result": 0})
@app.route("/t", methods=["POST", "GET"])
def TitleDataMadeByQwizx():
    res = requests.post(f"https://{title}.playfabapi.com/Server/GetTitleData", headers=Headers())
    data = res.json().get("data", {}).get("Data", {})
    def n(obj):
        if isinstance(obj, dict):return {k: n(v) for k, v in obj.items()}
        elif isinstance(obj, list):return [n(i) for i in obj]
        elif isinstance(obj, str):return obj.replace("\\n", "\n")
        else:return obj
    f = n(data)
    return jsonify(f)










import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

badNames = [
    "NIG", "NIIG", "KKK", "NIGA", "NAZI", "BIGNIG", "BLACKNIG", "NIGAH", "BANANANIG", "NIGIS", "GAYNIG",
    "FAG", "NIGGA", "NIGNIG", "NIGZILLA", "NIGG", "NIGABALLS", "NIGMON", "NIGNOG", "NIGSY", "NIGRE",
    "GORILLANIG", "NIGKEY", "GORNIGA", "DADDYNIGA", "NIGMON", "HITLER", "NIIG", "N1GGA", "N1GA", "NIGR",
    "N1GGA", "N1GA", "N199A", "KKKLORD", "KKKMEMBER", "KKKMAN", "KKKMASTER", "KKKLEADER", "STINKYJEW",
    "NIGAB", "NIGAMO", "NIBBA", "NIGLET", "NIGWERD", "NIGUH", "NIGK", "NIGWARD", "NIQQA", "NIGDIRT", "NI99",
    "MONKENIGA", "NIGAB", "NIGHA", "H1TLER", "HITL3R", "H1TL3R", "KKKOFFICIAL", "NIGBA11S", "SPIDERNIG",
    "NIGSLAVE", "NIGILA", "NIGBALL", "NIGILLA", "SPIDANIGA", "BLACKNIGA", "NIG2MONKE", "NIGMAN", "NIGATOES",
    "NIGMAN", "NIGWAD", "MYNIGA", "NIGTARD", "NIGTURD", "NIGWORD", "NIGLIT", "NIGMAN", "NIGLER", "NIGSBALL",
    "SANDNIG", "SNOWNIG", "NIGQA", "DIRTYNIG", "NIGAFUCK", "HITTLER", "NIGFART", "NIGBA", "N1GWARD", "NIGHKA",
    "LITTLENIG", "NIGAH", "NIGBOB", "MASTERNIG", "NIGBOT", "NIGVR", "WARNIG",
    "NIGGER", "NIGGGER", "NIGERZ", "FAGGOT", "NIGAR", "NIGUR", "NIGG3R", "N1GGER", "N1GG3R", "NIGER",
    "NIGKILL", "NIGASLAYER", "NIGERMON", "NI66ER", "GEORGEFL", "GEORGFL", "NIIGGE", "NIIGGR", "CHINK",
    "N1GUR", "N1GER", "NICKG", "NIKGU", "NIKGE", "N199GE", "GASJEW", "KILLJEW", "JEWSLAYER", "JEWSSUCK",
    "GASTHEJEW", "KIKE", "NIBBER", "NIGOR", "NIGCER", "FUCKBLACK", "NIQQER", "FUCKJEW", "NI99ER", "NATEHIG",
    "FUCKLGBT", "FVCKLGBT", "HATELGBT", "NIG5ER", "IHATEGAY", "IH8GAY", "IH8LGBT", "IH8JEW", "IH8BLACK",
    "NICGER", "NIGQER", "H8NIG", "NIG3ER", "NIG3R", "NIGHER", "IHATENIG", "MONKEYNIG", "NIGEATSKFC",
    "FUCKGAYS", "N199ER", "N1663R", "N1993R", "N166ER", "NIGHUR", "N1G3R", "N1GGGERR", "NIG4R", "NIGEER",
    "NIGYR", "NIGBIGGER", "NIGCKER", "NIGIR", "NIG33R", "KXK", "KKX", "XXK", "KXX", "JMAN", "K9", "GAY9", "SLAVE",
    "H1TLER", "PENIS", "VAGINA", "MAXO", "ELLIOT", "KILLNIGGERS", "PORNHUB", "CHILDPORN", "CP", "DICK", "ANAL",
    "MINI99", "GAYSEX", "RAPE", "PORNO", "LESBIAN", "CUMSLUT", "DEEPTHROAT", "JMANCURLY", "DAISY09", "J3VU", "BOT",
    "TTTPIG", "JMANCURLY", "STATUE", "JMANFAN", "TTT", "MOSA", "H4PKY", "WARNING", "HACKER", "GAYMANCURLY",
    "TTTPIGFAN", "ELLIOTFAN", "H4PKYFAN", "MOSAFAN", "TOP1GROUND", "TOP1FLICK", "PIG", "BRN", "BRNMOSA", "GTC",
    "BODA", "K9", "K9FAN", "MAXOFAN", "ELLIOTJR", "TTTPIGJR", "TTTJR", "PIGJR", "MAXOJR", "JMANJR", "JMANCURLYJR",
    "911", "TERRORIST", "TWINTOWERS", "SKIBIDI", "SKIBIDITOILET", "L1RSONISGAY", "SILLYISGAY", "TOP1", "VMT", "VMTFAN",
    "VMTJR", "TTPIG", "LEMMING", "CJVR", "NIGER", "NIGA", "ALECVR", "GAYPIG", "FUCKNIGGERS", "FUCKNIGGAS", "SAVAFAN", 
    "SAVA", "SAVAJR", "FUCKNIGAS", "NIGA", "NIGGERA", "NIGERA", "SUCKMYDICK", "SAVAFAN", "SAVA", "SAVAVR", "COSMO" # add more if needed lol
]

# result : 1 warns the user
# result : 2 kicks the user from the game
# result : 0 means the name is good

@app.route("/api/CheckForBadName", methods=["POST"])
def Check():
    room = request.get_json().get("FunctionArgument", {}).get("forRoom")
    name = request.get_json().get("FunctionArgument", {}).get("name")

    if name in badNames:
        return jsonify({
            "result": 1
        }), 200
    
    else:
        return jsonify({
            "result": 0
        })

