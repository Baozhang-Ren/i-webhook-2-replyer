from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
#Baozhang Ren baozhangren
PAGE_ACCESS_TOKEN_page1_app1 = 'EAApVD5mMAYQBAHOjjrc5B6ZCct4ghNpUyMMAYRuTVcN3tOujYTqUw3YEET4EMnZCu72QIpWQ9YhkKEWpKZBDU7IEaAJneRfdiZAAtfP96RzAusgv6iEfnFIKGIEqPz33Yfk8us23BU1D3hlfSCQKn763ZAHZANjfoDBqxU3JAgiQZDZD'
SEND_API_URL_page1_app1 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page1_app1

PAGE_ACCESS_TOKEN_page1_app2 = 'EAALC8ZAZCw0TcBAAkSklwegZBfHLs8MXPYj137ghUZBucr5nrjYcn2N5i4ZBKpCW3bXtUiNXlZCXCyPKBJXZBZAHimczLKMjY0haTbubAl9aN0eQPlmfhMY5PGJaxbazSBUXNRoB0qttZAS6bqw8WssLGGiuyEeea4ZCUAPUAbXRMrMQZDZD'
SEND_API_URL_page1_app2 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page1_app2

PAGE_ACCESS_TOKEN_page2_app1 = 'EAApVD5mMAYQBAK2ykO1MC0Gsf2ZChITTbREgQxFPunoIs0PQRrZCxXrMrLg4j8i5rDUKT5WIZCmZB8OrPCHdSML8ETpMtFMEUxIhKQYc0pYKvZBo4p0aPDCYd5q75kHGCMmTPjaovvZCxdm93XnJ4APlSwzng3qH14nDcEP0KcIEY0QaeSht9ZB'
SEND_API_URL_page2_app1 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page2_app1

PAGE_ACCESS_TOKEN_page2_app2 = 'EAALC8ZAZCw0TcBADHCr7v3Vmqa4yaXFjqRfDhHCE5pM6ClrpSRWQFMUpwv0yjZC4tsMqNQG1btr5ne89Ywqga4kLctVCZBlV2cG2bfCdb3XbgOltgHj4E2CG2RJg1sxLIk2ZBWZAQZBjZBwiTLolDh6cGnarnZCtPEnKVlatGxePpOpvQ5cKc0RVI'
SEND_API_URL_page2_app2 = 'https://graph.facebook.com/v8.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN_page2_app2

HEADERS = {'content-type': 'application/json'}
IG_ACC_TO_REPLY = '17841434643766488'
APP_ID = '2908275256066436'
APP_NAME = 'baozhangren'
HOP_EVENTS = set(['request_thread_control','pass_thread_control','take_thread_control','pass_metadata'])
      
      
def send_message(body):
  print('body',body)
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

