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
    return "ok"


if __name__ == '__main__':
app.run(debug=True)
