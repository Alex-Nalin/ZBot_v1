import os
import codecs
import json
import requests
import logging
from time import sleep

_configPath = os.path.abspath('../command/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)


class GetGiphyImage:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def GetGiphy(self):

        try:
            giphyAPIKey = _config['giphy']['apikey']

            ep = "http://api.giphy.com/v1/gifs/random"
            payload = {"apikey": giphyAPIKey}

            # paramList = giphyText.split()
            # isRandom = len(paramList) == 0 or paramList[0] == 'random'
            #
            # if isRandom:
            #     ep = "http://api.giphy.com/v1/gifs/random"
            #     payload = {"apikey": giphyAPIKey}
            # else:
            #     ep = "http://api.giphy.com/v1/gifs/translate"
            #     payload = {"apikey": giphyAPIKey, "s": giphyText}

            response = requests.get(ep, params=payload).json()

            # if isRandom:
            #     #print("Random")
            #     gifimagelink = (response['data']['image_original_url'])
            #     msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
            #
            # else:
            #     #print("Specific")
            #     gifimagelink = (response['data']['images']['original']['url'])
            #     header = ' '.join(paramList)
            #     msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

            gifimagelink = (response['data']['image_original_url'])
            msgToUI = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

        except Exception as ex:
            errorStr = "Symphony REST Exception (system): {}".format(ex)
            logging.debug('error', errorStr)
            msgToUI = "Sorry, I could not return a GIF right now."

        return msgToUI


    def send_giphy(self, stream_id):

        messagetosend = self.GetGiphy()

        ## This send the card with a space in front, like an image is missing
        # msg_to_send = dict(
        #     message='<messageML><div class="wysiwyg">' +
        #             '<p>' +
        #             str(messagetosend) +
        #             '</p></div>'
        #             '</messageML>')

        msg_to_send = dict(message="<messageML>" + str(messagetosend) + "</messageML>")

        #print("msg_to_send: " + str(msg_to_send))
        self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)


class Joke:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def get_random_joke(self):
        logging.debug('Getting a random joke..')
        url = 'https://official-joke-api.appspot.com/jokes/random'

        try:
            response = requests.get(url)
            response_body = json.loads(response.text)
            question = response_body['setup']
            punchline = response_body['punchline']
            return question, punchline
        except requests.exception.HTTPError as e:
            return "", ""

    def send_joke(self, stream_id):
        question, punchline = self.get_random_joke()
        for line in question, punchline:
            msg_to_send = dict(
                message='<messageML><div class="wysiwyg">' +
                        '<p>' +
                        line +
                        '</p></div>'
                        '</messageML>')
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)
            sleep(3)
        self.bot_client.get_message_client().send_msg_with_attachment(
            stream_id,
            '<messageML>Attachment POC</messageML>',
            'nameoftheImage.png',
            '../data/image.png')