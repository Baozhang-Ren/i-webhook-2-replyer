from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
#Baozhang Ren baozhangren
PAGE_ACCESS_TOKEN_page1_app1 = 'EAApVD5mMAYQBAKduKLOGAJtW1MVWuUJHPkMqq3aoMRxVqF4f5BLPmZCwwOzXveNxakENFjWePZAShe1tYqvpWmXTwd0QJNUQd3WnwpNenErFuU1ZAf0ZCU8n71w3KQhv0XVD3kXLZAwCHUFMJnwIQjFxr5cynZCM5q6jzJ3DShqfAd08HeqIZC5'
SEND_API_URL_page1_app1 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page1_app1

PAGE_ACCESS_TOKEN_page1_app2 = 'EAALC8ZAZCw0TcBAH8ySbpu9O3u1ZB6gmSHusXh3fpuGCgFqqP7bWqty7rDdTGRvTQbTforGBOZAtsQZCGjAsWKNrNQgmZAC8cWdtlFIwZAN7ffvicit1kgaw1cQhA1ofn41QjPWmO58ZCpomoLSH10fSyASpkBo683OlZA6YZBeZBSBfsz1EqG2dKEv'
SEND_API_URL_page1_app2 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page1_app2

PAGE_ACCESS_TOKEN_page2_app1 = 'EAApVD5mMAYQBAGOdqhUa3zVoSzuSsSDajQ3ZB01UOouy8Al1yYZCx9RIw67bFLtujFVY8iASfh7qHJOnjwcfqXBeRsTN9x94kVnpdmm7dQSDZBZA1ci3cBxwAkMIASXNXLMEt1os77h46ZANkhAeiMmdTZAaQr7K9EV7W5vZBM7WioFtEX8fzGC'
SEND_API_URL_page2_app1 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page2_app1

PAGE_ACCESS_TOKEN_page2_app2 = 'EAALC8ZAZCw0TcBAIbzHsTYUTduklZAUOWZAWqeUPgGZAXM3vP98GymSYH4IZAveMy2tZB7FEidNGPWWtCqrhK6HITMUIEZCY74Bx8sOS7dOXhUVZACRR3dZCBpEK1LhZARLnZCczSndslcICgqUqZB5aYLYAJBbJyTCkHO4mHIZB4rWR1FaZCnRdfolZAYt8'
SEND_API_URL_page2_app2 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page2_app2

HEADERS = {'content-type': 'application/json'}
IG_ACC_TO_REPLY = '90010208321901'
APP_ID = '2908275256066436'
APP_NAME = 'baozhangren'
HOP_EVENTS = set(['request_thread_control','pass_thread_control','take_thread_control','pass_thread_metadata'])
      
      
def send_message(body):
  try:
    for entry in body['entry']:
      page = 'page1'
      if(entry['id'] != IG_ACC_TO_REPLY):
        print(entry['id'],'return')
        page = 'page2'
      app = 'app1'
      if 'messaging' in entry:
        channel = 'messaging';
      else:
        channel = 'standby';
        app = 'app2'
      print('page',page,'app',app)
      if page=='page1':
        if app=='app1':
          url = SEND_API_URL_page1_app1
        else:
          url = SEND_API_URL_page1_app2
      else:
        if app=='app1':
          url = SEND_API_URL_page2_app1
        else:
          url = SEND_API_URL_page2_app2
      for message in entry[channel]:
        if 'echoing_back' in message:
          return
        sender = message['sender']['id']
        recipient_id =  message['recipient']['id']
        webhook_type = None
        if 'message' in message: 
          webhook_type='message'
        for event in HOP_EVENTS:
          if event in message:
            webhook_type = event
            break
        if webhook_type == None:
          return
        if 'text' in message[webhook_type]:
          msg_text = message[webhook_type]['text']
          if 'echoing_back' in msg_text:
            return
        body['echoing_back'] = 'true'
        body['app_id'] = APP_ID
        body['app_name'] = APP_NAME
        if 'is_echo' in message[webhook_type]:
          send_message_to_recipient(json.dumps(body), recipient_id, sender, url)
          print('sent message to recipient_id', recipient_id)
        else:
          if webhook_type in HOP_EVENTS:
            send_message_to_recipient(json.dumps(body), recipient_id, sender,url)
            print('sent message to HOP_EVENTS recipient', recipient_id)
            return
          send_message_to_recipient(json.dumps(body), sender, recipient_id,url)
          print('sent message to sender', sender)
  except Exception as e:
     print("swapnilc-Exception sending")
     print(e)
      
      
def send_message_to_recipient(message_text, recipient_id, page_id,url):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
  }
  r = requests.post(url, data=json.dumps(message), headers=HEADERS)
  if r.status_code != 200:
    print('== ERROR====')
    print(url)
    print(r.json())
    print('==============')

@app.route('/')
@app.route('/index')
def index():
  print("index")
  return 'Hello, World!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    
    mode = request.args['hub.mode']
    token = request.args['hub.verify_token']
    challenge = request.args['hub.challenge']
    if mode and token:
      if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return challenge
      else:
        return make_response('wrong token', 403)
    else:
      return make_response('invalid params', 400)
  else: # POST
    body = json.loads(request.data)
    print("swapnilc-Mydata")
    print(body)
    send_message(body)
    return ("", 205)

