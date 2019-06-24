import logging
from .room_listener import RoomListener
from .message_processor import MessageProcessor
import command.command as cmd
# A sample implementation of Abstract RoomListener class
# The listener can respond to incoming events if the respective event
# handler has been implemented


class RoomListenerTestImp(RoomListener):
    """Example implementation of RoomListener

        sym_bot_client: contains clients which respond to incoming events

    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client

    def on_room_msg(self, msg):
        logging.debug('room msg received', msg)
        msg_processor = MessageProcessor(self.bot_client)
        messageItem = msg_processor.process(msg)

        if messageItem.command == "giphy":
            giphy_client = cmd.GetGiphyImage(self.bot_client)
            message2ui = giphy_client.GetGiphy(messageItem.msg_text)
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


    def on_room_created(self, room_created):
        logging.debug('room created', room_created)

    def on_room_deactivated(self, room_deactivated):
        logging.debug('room Deactivated', room_deactivated)

    def on_room_member_demoted_from_owner(self,
                                          room_member_demoted_from_owner):
        logging.debug('room member demoted from owner',
                      room_member_demoted_from_owner)

    def on_room_member_promoted_to_owner(self, room_member_promoted_to_owner):
        logging.debug('room member promoted to owner',
                      room_member_promoted_to_owner)

    def on_room_reactivated(self, room_reactivated):
        logging.debug('room reactivated', room_reactivated)

    def on_room_updated(self, room_updated):
        logging.debug('room updated', room_updated)

    def on_user_joined_room(self, user_joined_room):
        logging.debug('USER JOINED ROOM', user_joined_room)

    def on_user_left_room(self, user_left_room):
        logging.debug('USER LEFT ROOM', user_left_room)
