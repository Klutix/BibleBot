from flask import Flask, request, Response
from kik import KikApi, Configuration
from BibleDB import BibleDB
import os
from kik.messages import messages_from_json, TextMessage, ReceiptMessage, ReadReceiptMessage, SuggestedResponseKeyboard, TextResponse,StartChattingMessage
from kiktasty import KikBot
app = Flask(__name__)
kikbot = KikBot('bvseek','2890196b-0c31-4f2c-8a6d-497d40c8d5d6')
kikbot.config.webhook = 'https://b0254af7.ngrok.io'
kikbot.ApplyConfig()
Bible = BibleDB()
data = Bible.ResolveRequest("1 Peter 1:1-3")
@app.route('/', methods=['POST'])
def incomming():
    kikbot.VerifySignature()
    messages = kikbot.GetMessages()
    for message in messages:
        if kikbot.isTextMessage(message):
            data = Bible.ResolveRequest(message.body)
            if data == '':
                data = 'Please Us Book C:V-V format'
            kikbot.SendMesssage(message,Body=data)
            return kikbot.ReturnResponse()
        if kikbot.isRecieptMessage(message):
            pass

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)


