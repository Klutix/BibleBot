
from flask import Flask, request, Response
from kik import KikApi, Configuration
import pymysql
from kik.messages import messages_from_json, TextMessage, ReceiptMessage, ReadReceiptMessage, SuggestedResponseKeyboard, TextResponse,StartChattingMessage
import collections


class Features(object):
    manuallySendReadReceipts = False
    receiveReadReceipts      = False
    receiveDeliveryReceipts  = False
    receiveIsTyping          = False
    
class configuration(object):
    webhook = ""
    staticKeyboard = None
    features = Features()
    
class KikBot():
    config = configuration()
    kik = None
    afeatures ={}

    def __SetDefaultFeatures(self):
        global afeatures
        afeatures = {"manuallySendReadReceipts" : self.config.features.manuallySendReadReceipts,
                     "receiveReadReceipts"      : self.config.features.receiveReadReceipts,
                     "receiveDeliveryReceipts"  : self.config.features.receiveDeliveryReceipts,
                     "receiveIsTyping"          : self.config.features.receiveIsTyping}
        return afeatures
        
    def __init__(self,BOT_USER_NAME,API_KEY):
        global kik
        kik = KikApi(BOT_USER_NAME,API_KEY)
        
    def ApplyConfig(self):
        global kik
        self.__SetDefaultFeatures()
        kik.set_configuration(Configuration(webhook = self.config.webhook, features = self.afeatures, static_keyboard = self.config.staticKeyboard))
    
    def GetMessages(self):
            return messages_from_json(request.json['messages'])
            
    #!!!!!!!!!!!!!!!!!!!!!!!!OVEWRITE US!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def OverridableTextMessagedRecieved(self,messageObject,testData=''):
               
        kik.send_messages([
                        TextMessage(
                            to=messageObject.from_user,
                            chat_id=messageObject.chat_id,
                            body="Hello World"+testData
                            #keyboards =  SetKeyboard(messageObject.from_user)              
                        )
                    ])
        
        return Response(status=200)
    
    def OverridableRecieptMessagedRecieved():
        pass
        
    def ReturnResponse(self,statusNo=''):
        if statusNo == '':
            statusNo = 200
        return Response(status=statusNo)
    
    def SendMesssage(self,messageObject=None,fromUser='',ChatId ='',Body = '',Keyboard=None):        
        kik.send_messages([
                        TextMessage(
                            to=messageObject.from_user if fromUser =='' else fromUser,
                            chat_id=messageObject.chat_id if ChatId=='' else ChatId,
                            body="Reset Canceled" if Body=='' else Body,
                            keyboards = Keyboard if Keyboard is not None else None
                        )
                    ])
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def VerifySignature(self):
        if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
            return Response(status=403)
            
    def isTextMessage(self,message):
            if isinstance(message, TextMessage):                                
                return True
                
    def isRecieptMessage(self,message):
            if isinstance(message, ReadReceiptMessage):         
                return True
                


