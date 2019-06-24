from .im_listener import IMListener
from .message_processor import MessageProcessor
import logging
import command.command as cmd


# A sample implementation of Abstract imListener class
# The listener can respond to incoming events if the respective event
# handler has been implemented


class IMListenerTestImp(IMListener):
    """Example implementation of IMListener

        sym_bot_client: contains clients which respond to incoming events

    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        
    def on_im_message(self, im_message):
        logging.debug('message received in IM', im_message)
        msg_processor = MessageProcessor(self.bot_client)
        messageItem = msg_processor.process(im_message)

        if messageItem.command == "help":
            help_client = cmd.Help(self.bot_client)
            message2ui = help_client.help()
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "giphy":
            giphy_client = cmd.GetGiphyImage(self.bot_client)
            message2ui = giphy_client.GetGiphy(messageItem.msg_text)
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "jokes":
            jokes_client = cmd.Jokes(self.bot_client)
            message2ui = jokes_client.getJokes()
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "funQuote":
            funQuote_client = cmd.FunQuote(self.bot_client)
            message2ui = funQuote_client.funQuote()
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "wiki":
            wiki_client = cmd.WikiSearch(self.bot_client)
            message2ui = wiki_client.wiki(messageItem.msg_text)
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "quoteoftheday":
            quoteoftheday_client = cmd.QuoteOftheDay(self.bot_client)
            message2ui = quoteoftheday_client.QoD()
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

        if messageItem.command == "weather":
            weather_client = cmd.Weather(self.bot_client)
            message2ui = weather_client.weather(messageItem.msg_text)
            print("message2ui: " + str(message2ui))
            self.bot_client.get_message_client().send_msg(messageItem.streamID, message2ui)

    def on_im_created(self, im_created):
        logging.debug('IM created!', im_created)
