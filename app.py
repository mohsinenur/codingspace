from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAADVw0N2kHEBAGsaysJSKBGrS0SXAK91JaU1yDrShLaOywRoJshD3ZBYkDY2Jb9lPxCG2TRX5ZBwd4m2wwPb8DOKW7uU7dz1NT410b1QP1UK5exVVKP26Ldyo4izFp7lcXT4bcsPK18yDYLf5AkxxY1J2AF8uWHbpQ7Yvb0AZDZD"


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    unknown = "Unknown text! I will reply you later. :)"
    hlw = "Hello"
    sm_emo = ":)"
    if message == "hi":
        reply(sender, hlw)
    elif message == "how are you?":
        reply(sender, "fine. you?")
    elif message == "ok":
        reply(sender, sm_emo)
    elif message == sm_emo:
        reply(sender, sm_emo)
    else:
        reply(sender, unknown)

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
