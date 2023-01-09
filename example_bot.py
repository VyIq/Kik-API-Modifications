#!/usr/bin/env python3
import logging
import sys

import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.datatypes.xmpp.xiphias import UsersResponse, UsersByAliasResponse
from kik_unofficial.datatypes.xmpp.roster import GroupSearchResponse
import random

listfr = ['a', 'b', 'c', 'd', 'e', 'f']
listfn = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

x = ''.join(random.choice(listfn + listfr) for _ in range(32))
y = ''.join(random.choice(listfn + listfr) for _ in range(16))
device_id = x
android_id = y

username = sys.argv[1] if len(sys.argv) > 1 else input('Username: ')
password = sys.argv[2] if len(sys.argv) > 2 else input('Password: ')


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = EchoBot()

class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password, android_id_override=android_id, device_id_override=device_id)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))

        if chat_message.body.lower() == "friend":
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "You can now add me to groups! <3")

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        if str(chat_message.raw_element).count("</alias-sender>") > 1 and "</alias-sender>" not in str(chat_message.body):
            return

        print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid, chat_message.body))

        if chat_message.body.lower() == "ping":
            self.client.send_chat_message(chat_message.group_jid, "Pong")

        # Keep in mind the bot won't pass Kik jail, there's probably a fix but I'm not sure the problem
        elif chat_message.body == "/gif":
            self.client.send_sponsored_gif_image(chat_message.group_jid,
            "Kitty", "URL", "TITLE", "ACTION")

        # Keep in mind the bot won't pass Kik jail, there's probably a fix but I'm not sure the problem
        elif chat_message.body == "/sticker":
            file_path = "sticker.png"
            self.client.send_sticker(chat_message.group_jid, file_path)

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        print("[+] Friend attribution request from " + response.referrer_jid)

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("[+] Peer info: " + str(response.users))

    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        pass

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        pass

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()
