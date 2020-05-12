from scapy.layers.http import HTTP, HTTPRequest
from scapy.layers.inet import IP
from scapy.sendrecv import send
from scapy.all import *
#load_layer('http')

zero = '\u200c'  # 0
one = '\u200d'  # 1

send = "0000"
disconnect = "0001"
clients = "0010"
echo = "0011"
drop = "0100"
access = "0101"
all = "0110"


''' CONTIANS CODE USED BY BOTH SERVER AND CLIENT'''
def binary_converter(message):
    res = ''
    message2 = message
    msg_list = message2.split()
    if msg_list[0] == 'ALL':
        res = all
        if msg_list[1] == 'SEND':
            res = res + send
            command_len = 9 # len('ALL SEND') + 1
            message = message[command_len:]
            res = res + ''.join(format(ord(i), '08b') for i in message)
        elif msg_list[1] == 'ECHO':
            res = res + echo
        elif msg_list[1] == 'DISCONNECT':
            res = res + disconnect
    elif msg_list[0] == 'DROP':
        res = drop
    elif msg_list[0] == 'CLIENTS':
        res = clients
    elif msg_list[0] == 'ACCESS':
        res = access + msg_list[1]
    else:
        res = ''.join(format(ord(i), '08b') for i in msg_list[0])
        if msg_list[1] == 'SEND':
            res = res + send
            command_len = len(msg_list) + 18
            message = message[command_len:]
            res = res + ''.join(format(ord(i), '08b') for i in message)
        elif msg_list[1] == 'ECHO':
            res = res + echo
        elif msg_list[1] == 'DISCONNECT':
            res = res + disconnect
    return res
    # binary_to_unicode(res)


def binary_to_unicode(message):
    final_res = ''
    # print("LEN: " + str(len(message)))
    for i in message:
        if i == '0':
            final_res += zero
        if i == '1':
            final_res += one
    return final_res

def unicode_to_binary(message):
    index1 = 0
    index2 = 3
    final_final_res = ''

    while index1 < len(message):
        if message[index1:index2] == b'\xe2\x80\x8c':
            final_final_res += "0"
        elif message[index1:index2] == b'\xe2\x80\x8d':
            final_final_res += "1"
        index1 += 3
        index2 += 3

    return final_final_res


def binary_deconverter(message):
    index1 = 4
    index2 = 12
    command = ''
    new_message = ''

    if message[0:4] == "0110":
        command = "ALL"
        if message[4:8] == "0000":
            command += " "
            command += "SEND"
            index1 = 8
            index2 = 16
            while index1 < len(message):
                character = chr(int(message[index1:index2], 2))
                new_message += character
                index1 += 8
                index2 += 8
            return command + ' ' + new_message
        if message[4:8] == "0001":
            command += " "
            command += "DISCONNECT"
            return command
        if message[4:8] == "0011":
            command += " "
            command += "ECHO"
            return command
    # if message[0:4] == "0000":
    #     command = "SEND"
    elif message[0:4] == "0010":
        command = "CLIENTS"
        return command
    elif message[0:4] == "0100":
        command = "DROP"
        return command
    elif message[0:4] == "0101":
        command = "ACCESS"
        return command
    else:
        index1 = 0
        index2 = 8
        while index1 < 120:
            character = chr(int(message[index1:index2], 2))
            command += character
            index1 += 8
            index2 += 8
        if message[120:124] == "0000":
            command += " "
            command += "SEND"
            index1 = 124
            index2 = 132
            while index1 < len(message):
                character = chr(int(message[index1:index2], 2))
                new_message += character
                index1 += 8
                index2 += 8
            return command + ' ' + new_message
        if message[120:128] == "0001":
            command += " "
            command += "DISCONNECT"
            return command
        if message[120:128] == "0011":
            command += " "
            command += "ECHO"
            return command


def construct_packet(addr, input):
    if input == None:
        return
    r_input = binary_converter(input)
    if r_input == None:
        return
    print(r_input)
    r_input = binary_to_unicode(r_input)
    if r_input == None:
        return
    print(r_input)

    packet = IP(dst=addr[0], port=addr[1])/HTTP()/HTTPRequest(
                Referer=r_input
            )
    return bytes(packet)

def deconstruct_packet(self, packet):
    message = packet[HTTPRequest].Referer
    message = unicode_to_binary(message.encode())
    message = binary_deconverter(message)
    return message
