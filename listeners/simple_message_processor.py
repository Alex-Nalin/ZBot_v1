import xml.etree.ElementTree as ET
import os
import codecs
import json
import requests
import logging
import sym_api_client_python.clients.message_client as mess
from command.command import GetGiphyImage as Giphy

_configPath = os.path.abspath('../command/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)

class MessageProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def process(self, msg):
        msg_xml = msg['message']
        # This give the full message div
        #print("msg_xml: " + msg_xml)
        msg_root = ET.fromstring(msg_xml)
        msg_txt = msg_root[0].text
        #print("msg_txt: " + msg_txt)

        #if msg_txt == "/Test":
        if "/Test" in msg_txt:

            messagetosend = "Hey Whats up"
            msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')

            stream_id = msg['stream']['streamId']
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)

        #elif msg_txt == "/gif":
        elif "/gif" in msg_txt:
            Giphy(msg)

            # try:
            #     giphyAPIKey = _config['giphy']['apikey']
            #
            #     #giphyText = str(msg)
            #
            #     msg_xml = msg['message']
            #     # This give the full message div
            #     #print("msg_xml: " + msg_xml)
            #     msg_root = ET.fromstring(msg_xml)
            #     msg_txt = msg_root[0].text
            #     #print("msg_txt: " + msg_txt)
            #     giphyText = msg_txt[4:]
            #     #print("giphyText: " + giphyText)
            #
            #     #paramList = giphyText.split()
            #     paramList = giphyText.split()
            #
            #     isRandom = len(paramList) == 0 or paramList[0] == 'random'
            #
            #     if isRandom:
            #         ep = "http://api.giphy.com/v1/gifs/random"
            #         payload = {"apikey": giphyAPIKey}
            #     else:
            #         ep = "http://api.giphy.com/v1/gifs/translate"
            #         payload = {"apikey": giphyAPIKey, "s": giphyText}
            #
            #     response = requests.get(ep, params=payload).json()
            #
            #     if isRandom:
            #         print("Random")
            #         gifimagelink = (response['data']['image_original_url'])
            #         msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
            #
            #
            #     else:
            #         print("Specific")
            #         gifimagelink = (response['data']['images']['original']['url'])
            #         header = ' '.join(paramList)
            #
            #         msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
            #         #print("msgtoui: " + msgtoui)
            #
            #     messagetosend = msgtoui
            #     msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            #     #msg_to_send = '<messageML>' + messagetosend + '</messageML>'
            #     #print("msg_to_send: " + str(msg_to_send))
            #     stream_id = msg['stream']['streamId']
            #     #mess.MessageClient.send_msg(stream_id, msg_to_send)
            #     self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)
            #
            # except Exception as ex:
            #     errorStr = "Symphony REST Exception (system): {}".format(ex)
            #     logging.debug('error', errorStr)
            #     msgtoui = "Sorry, I could not return a GIF right now."
            #     messagetosend = msgtoui
            #     msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            #     stream_id = msg['stream']['streamId']
            #     self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)

        else:
            stream_id = msg['stream']['streamId']
            messagetosend = "What are you doing?"
            msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)


# def GetGiphyImage(msg):
#
#     #try:
#         giphyAPIKey = _config['giphy']['apikey']
#
#         #giphyText = str(msg)
#
#         msg_xml = msg['message']
#         # This give the full message div
#         print("msg_xml: " + msg_xml)
#         msg_root = ET.fromstring(msg_xml)
#         msg_txt = msg_root[0].text
#         print("msg_txt: " + msg_txt)
#         giphyText = msg_txt
#         print("giphyText: " + giphyText)
#
#         #paramList = giphyText.split()
#         paramList = giphyText.split()
#
#         isRandom = len(paramList) == 0 or paramList[0] == 'random'
#
#         if isRandom:
#             ep = "http://api.giphy.com/v1/gifs/random"
#             payload = {"apikey": giphyAPIKey}
#         else:
#             ep = "http://api.giphy.com/v1/gifs/translate"
#             payload = {"apikey": giphyAPIKey, "s": giphyText}
#
#         response = requests.get(ep, params=payload).json()
#
#         if isRandom:
#             gifimagelink = (response['data']['image_original_url'])
#             msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
#
#
#         else:
#             gifimagelink = (response['data']['images']['original']['url'])
#             header = ' '.join(paramList)
#
#             msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
#             print("msgtoui: " + msgtoui)
#
#         messagetosend = msgtoui
#         msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
#         #msg_to_send = '<messageML>' + messagetosend + '</messageML>'
#         print("msg_to_send: " + str(msg_to_send))
#         stream_id = msg['stream']['streamId']
#         #MessageProcessor.get_message_client().send_msg(stream_id, msg_to_send)
#         mess.MessageClient.send_msg(stream_id, msg_to_send)
#
#     # except Exception as ex:
#     #     errorStr = "Symphony REST Exception (system): {}".format(ex)
#     #     logging.debug('error', errorStr)
#     #     msgtoui = "Sorry, I could not return a GIF right now."
#     #     messagetosend = msgtoui
#     #     msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
#     #     #MessageProcessor.process(None, msg_to_send)
#     #     stream_id = msg['stream']['streamId']
#     #
#         # return msgtoui