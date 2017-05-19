from flask import Flask, request, Response
from kik import KikApi, Configuration
from BibleDB import BibleDB
import os
from kik.messages import messages_from_json, TextMessage, ReceiptMessage, ReadReceiptMessage, SuggestedResponseKeyboard, TextResponse,StartChattingMessage
from kiktasty import KikBot
app = Flask(__name__)
kikbot = KikBot('BOT_NAME','BOT_ID')
kikbot.config.webhook = 'WEBHOOK'
kikbot.ApplyConfig()
Bible = BibleDB()
@app.route('/', methods=['POST'])
def incomming():
    kikbot.VerifySignature()
    messages = kikbot.GetMessages()
    for message in messages:
        if kikbot.isTextMessage(message):
            data = Bible.ResolveRequest(message.body)
            if data == '':
                data = 'Please Use (B C:V-V) format'
            kikbot.SendMesssage(message,Body=data)
            return kikbot.ReturnResponse()
        if kikbot.isRecieptMessage(message):
            pass

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)


