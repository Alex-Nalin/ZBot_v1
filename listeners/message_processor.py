import xml.etree.ElementTree as ET
import os
import codecs
import json

from command.command import GetGiphyImage, Joke

## Adding the variable from config.json file
_configPath = os.path.abspath('../command/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)

"""This will process the message posted in Symphony UI"""
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

        if '/bot' in msg_txt and 'joke' in msg_txt:
            joke_client = Joke(self.bot_client)
            stream_id = msg['stream']['streamId']
            joke_client.send_joke(stream_id)


        #if msg_txt == "/Test":
        elif "/Test" in msg_txt:

            messagetosend = "Hey Whats up"
            msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')

            stream_id = msg['stream']['streamId']
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)


        #elif msg_txt == "/gif":
        elif "/gif" in msg_txt:
            #print(msg_txt)
            GetGiphy_client = GetGiphyImage(self.bot_client)
            stream_id = msg['stream']['streamId']
            GetGiphy_client.send_giphy(stream_id)

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

        return msg_txt