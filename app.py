# Python libraries that we need to import for our bot
import datetime
import random
from flask import Flask, request, render_template
from decimal import Decimal
import requests
import psycopg2
from pymessenger.bot import Bot
from flask_sqlalchemy import SQLAlchemy

import os 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rnuuqpbopgncua:3d91d3bc5c3f611a48c76b63231c4e11f0d385329c98c8c6fae96cd0a848d8b4@ec2-54-227-241-179.compute-1.amazonaws.com:5432/deaeql5ahe7n7c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ACCESS_TOKEN = 'EAADVw0N2kHEBAGsaysJSKBGrS0SXAK91JaU1yDrShLaOywRoJshD3ZBYkDY2Jb9lPxCG2TRX5ZBwd4m2wwPb8DOKW7uU7dz1NT410b1QP1UK5exVVKP26Ldyo4izFp7lcXT4bcsPK18yDYLf5AkxxY1J2AF8uWHbpQ7Yvb0AZDZD'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'VERIFY_TOKEN'   # VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] not need
bot = Bot(ACCESS_TOKEN)
    

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    text_send = db.Column(db.Text)
    text_receive = db.Column(db.Text)
    date = db.Column(db.String(100), default=datetime.datetime.utcnow)
    session = db.Column(db.Text)


# We will receive messages that Facebook sends our bot at this endpoint


@app.route("/bot", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    exist_user = Message.query.filter_by(user_id=recipient_id).first()
                    if message['message'].get('text'):
                        r_msg = message['message']['text']
                        # declearing variable
                        response_sent_text = ''
                        t_hi = ['hi','Hi','HI','hI']
                        t_hello = ['hello','Hello','HELLO','hlw','Hlw','HLW']
                        t_fine = ['fine', 'Fine', 'Nice', 'nice', 'Great', 'great', ':)']
                        t_how_r_u = ['how are you?', 'How are you?']
                        t_hmm = ['hmm', 'Hmm', 'oh', 'ooh', 'ok', 'okay', 'Ok', 'OK', 'Okay']
                        t_who_r_u = ['who are you?', 'Who are you?']
                        t_temp = ['temperature in dhaka', 'what is temperature in dhaka?', 'dhaka temperature', 'dhaka temp', 'temp']
                        t_tnx = ['tnx', 'thanks', 'thank you', 'Thanks', 'Tnx', 'Thank you']

                        # matching text for reply
                        if r_msg in t_hi:
                            if exist_user:
                                response_sent_text = 'Hello, welcome back :)'
                            else:
                                response_sent_text = 'Hello, how can I help you?'                         
                        elif r_msg in t_hello:
                            if exist_user:
                                response_sent_text = 'Hi, welcome back :)'
                            else:
                                response_sent_text = 'Hi, how can I help you?'
                        elif r_msg in t_fine:
                            response_sent_text = ':)'
                        elif r_msg in t_how_r_u:
                            response_sent_text = 'I am fine. You?'
                        elif r_msg in t_hmm:
                            response_sent_text = 'Hmm'
                        elif r_msg in t_tnx:
                            response_sent_text = 'You are welcome :)'
                        elif r_msg in t_who_r_u:
                            response_sent_text = 'I am Bot. Made by SSL Developer Team.'
                        elif r_msg in t_temp:
                            w_api_address = 'https://api.darksky.net/forecast/66f19b250a5e0730c037c857603339f4/23.8103,90.4125'
                            data = requests.get(w_api_address).json()
                            weather = {
                                'temperature': data['currently']['temperature'],
                                'icon': data['currently']['icon'],
                                'summary': data['currently']['summary']
                            }
                            f_temp = int(weather['temperature'])
                            c_temp = (f_temp - 32) * 5 / 9
                            r_c_temp = round(c_temp)
                            weather_vaule = {
                                'title': str(r_c_temp) + '°C',
                                'image_url': weather['icon'],
                                'subtitle': weather['summary']
                            }
                            # sending template msg
                            send_temp_message(recipient_id, weather_vaule, r_msg)
                        else:
                            response_sent_text = "Unknown text! You can type 'temp' to know temperature. :)"
                        
                        # sending text msg
                        if response_sent_text != '':
                            send_message(recipient_id, response_sent_text, r_msg)
                        
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        r_msg = get_file_message()
                        send_file_message(recipient_id, r_msg)
    return "Message Processed"


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('fbchat.html')


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid token!'


# chooses a random message to send to the user
def get_text_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


def get_file_message():
    sample_responses = "This is file type."
    # return selected item to the user
    return sample_responses
    

# uses PyMessenger to send response to user
def send_message(recipient_id, response, r_msg):
    # sends user the text message provided via input response parameter
    now = datetime.datetime.now()
    time_format = now.strftime("%d/%m/%y %H:%M")
    session_query = Message(user_id=recipient_id, text_send=response, text_receive=r_msg,
                             date=time_format, session=response)
    if session_query:
        db.session.add(session_query)
        db.session.commit()
        bot.send_text_message(recipient_id, response)
    else:
        response = 'Sorry something went wrong! at ' + time_format
        bot.send_text_message(recipient_id, response)

    return "success"


def send_temp_message(recipient_id, weather_vaule, r_msg):
    # sends user the text message provided via input response parameter
    now = datetime.datetime.now()
    time_format = now.strftime("%d/%m/%y %H:%M")
    txt_snd = weather_vaule['title']
    session_query = Message(user_id=recipient_id, text_send=txt_snd, text_receive=r_msg,
                             date=time_format, session=txt_snd)
    if session_query:
        db.session.add(session_query)
        db.session.commit()
        bot.send_generic_message(recipient_id, weather_vaule)
    else:
        response = 'Sorry something went wrong! at ' + time_format
        bot.send_generic_message(recipient_id, response)

    return "success"


def send_file_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
