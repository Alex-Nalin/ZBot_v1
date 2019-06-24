import xml.etree.ElementTree as ET
import os
import codecs
import json

from command.command import punchJoke

## Adding the variable from config.json file
_configPath = os.path.abspath('../command/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)

class MessageItem:

    def __init__(self):

        self.firstname = ""
        self.lastname = ""
        self.streamID = ""
        self.command = ""
        self.msg_text = ""

"""This will process the message posted in Symphony UI"""
class MessageProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def process(self, msg):

        messageItem = MessageItem()

        messageItem.firstname = msg['user']['firstName']
        messageItem.lastname = msg['user']['lastName']
        messageItem.userID = msg['user']['userId']
        messageItem.streamID = msg['stream']['streamId']
        messageItem.streamType = msg['stream']['streamType']

        print("--> User ID: " + str(messageItem.userID) + " & full name: " + str(messageItem.firstname) + " " + str(messageItem.lastname))
        print("--> Stream Type: " + str(messageItem.streamType) + " with stream ID: " + str(messageItem.streamID))

        msg_xml = msg['message']
        msg_root = ET.fromstring(msg_xml)
        messageItem.msg_text = msg_root[0].text

        msg_text = messageItem.msg_text

        print("msg_txt: " + msg_text)

        if "/help" in msg_text:
            messageItem.command = "help"

        elif '/bot' in msg_text and 'joke' in msg_text:
            joke_client = punchJoke(self.bot_client)
            stream_id = msg['stream']['streamId']
            joke_client.send_joke(stream_id)


        elif "/jokes" in msg_text:
            messageItem.command = "jokes"

        elif "/funQuote" in msg_text:
            messageItem.command = "funQuote"

        #if msg_txt == "/Test":
        elif "/Test" in msg_text:

            messagetosend = "Hey Whats up " + messageItem.firstname
            msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            stream_id = msg['stream']['streamId']
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)

            # messagetosend = "Hey Whats up " + messageItem.firstname + " dude"
            # msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            # stream_id = msg['stream']['streamId']
            # self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)
            # messageItem.command = "test"

        # elif "/quoteoftheday" in msg_text or "/qod" in msg_text:
        elif msg_text == "/quoteoftheday" or msg_text == "/qod":
            messageItem.command = "quoteoftheday"

        elif "/wiki" in msg_text:
            messageItem.command = "wiki"

        #elif msg_txt == "/gif":
        elif "/gif" in msg_text:
            messageItem.command = "giphy"

            #print(msg_txt)
            # GetGiphy_client = GetGiphyImage(self.bot_client)
            # stream_id = msg['stream']['streamId']
            # GetGiphy_client.send_giphy(stream_id)

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

        elif "/weather" in msg_text:
            messageItem.command = "weather"


        else:
            stream_id = msg['stream']['streamId']
            messagetosend = "What are you doing?"
            msg_to_send = dict(message='<messageML>' + messagetosend + '</messageML>')
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)

        return messageItem