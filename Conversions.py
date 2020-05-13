from scapy.layers.http import HTTP, HTTPRequest
from scapy.layers.inet import IP
from scapy.sendrecv import send
from scapy.all import *
#load_layer('http')
from random import randrange
import socket

zero = '\u200c'  # 0
one = '\u200d'  # 1

send = "0000"
disconnect = "0001"
clients = "0010"
echo = "0011"
drop = "0100"
access = "0101"
all = "0110"

raw_packet_bytes = [b'\x32\x15\xca\x2d\xb1\x38\x2c\xf0\x0c\x1d\x84\xb3\x6a\xab\x86\x00',b'\xf9\x76\xe7\xab\x1d\xa6\xdb\x31\x9c\xe9\xd4\xec\x23\x0c\xa4\x76',b'\x7c\x04\xd0\xbb\x6a\x52\x08\xf1\xea\x5e\x4a\x00\x08\x00\x45\x00',b'\x05\x92\x00\x00\x40\x00\x3c\x06\x94\x29\x2d\x39\x5b\x01\xac\x18',b'\x70\xea\x01\xbb\xc9\xca\x47\xa8\x81\xe0\x49\x9e\xcf\x70\x80\x10',b'\x08\x01\x05\xe3\x00\x00\x01\x01\x08\x0a\xa8\x9a\xdb\xd4\x23\x8a',b'\x79\xc0\x1b\x77\xa4\xe4\x32\xc2\xd7\x75\x06\xd5\x7f\xf5\xc8\xb1',b'\xea\xbc\xda\xaa\x1b\x39\x6d\x55\x62\x20\xe5\xba\xfd\x10\x8d\x68',b'\x5b\x75\x7f\x20\xad\x58\x22\xa2\x19\x11\x91\xa4\x61\xb2\xa1\xf6',b'\x0b\x25\xcc\x47\x47\x9e\x09\x71\x44\xaf\xe9\xe3\xb5\x71\xcd\x10',b'\x48\xbe\x12\x47\xd2\x64\xc4\xb7\xe2\x6a\xfe\x47\x3b\xd1\x61\xda',b'\xf0\x9b\x14\x25\x21\xb7\xcb\x48\xaf\xb3\x15\xe3\xc3\x46\x3d\xec',b'\xf5\xc8\xb2\xef\xee\x71\xf4\x48\x0b\xb8\xc5\xf2\x33\xa3\x3f\xe3',b'\xd5\xd1\x55\x2c\x6f\xae\xf2\x22\xca\xce\x5e\xe7\x4e\xd3\x3e\x18',b'\xd0\x59\x41\x10\xcf\xfc\xac\xd8\x49\xbf\x8f\x62\x6a\x65\xb0\xcf',b'\x76\x49\x72\xfb\x48\xcf\xbe\xb7\xac\xb4\xc0\x49\x25\x18\x8f\xb1',b'\x52\x3b\x8e\xf9\x7b\x8a\x7a\x12\x29\xa7\x3e\xa0\x41\x7e\x5d\x55',b'\xeb\xf7\x33\xda\x24\xda\x55\xd0\x02\x63\x0f\xfe\xfa\x1c\xd6\x8a',b'\x4b\x90\x8f\xe6\x2d\x3b\x8f\xaf\xa8\x23\x2f\xef\x84\xd3\x40\x0b',b'\x8b\xdf\x83\x69\x74\xf4\xd6\x25\x8b\x2f\x2c\x78\x2d\x27\xe1\xdb',b'\xaf\xb9\x49\x21\x78\x5e\x39\x25\x2e\x4e\x30\xb3\x7d\x44\x74\x8a',b'\xf8\x7b\xe5\xea\x6f\x38\xa8\xe6\xca\xe8\x17\xf4\xfd\xb4\xec\xb8',b'\xae\xd0\x7f\x9b\x81\x6f\xcc\x60\xa7\x9d\xba\x5f\x37\x4d\x11\x9a',b'\xa3\x09\x07\x0e\x7d\x0a\x3a\xe3\xbb\xe8\x58\x71\x23\x16\x84\xcd',b'\xcf\x2e\x98\x51\xae\x45\x02\x5b\xb7\x13\x7f\x0f\x79\x13\x50\x58',b'\x57\xa7\x39\x01\xd0\xbe\xb9\x24\x2c\x16\xae\xa7\xc6\x4f\xa6\x66',b'\x06\x86\x80\x05\xd8\x1f\x22\x96\x9d\x69\xec\x46\x7d\x8b\x2e\x78',b'\xb7\xb6\x7b\x90\xb1\x16\xa9\xb5\x1f\xa0\x18\xeb\xf6\x4d\x44\x1f',b'\x5e\x11\xb4\x99\xd9\x35\x42\x36\x6d\x7b\x14\xb5\x0b\xc2\x80\xbc',b'\x6d\x71\xd7\x4b\x9a\x85\x5c\x1c\x78\x4d\xfc\x3d\xa9\x5c\x03\xa2',b'\xf4\xbc\x70\x60\xbd\xa6\x6d\xfe\xe7\xb9\xd2\x6c\xa7\x84\xf6\x5c',b'\xd4\x7e\x8d\x6b\x5d\xec\xec\xb0\xb3\xcb\x3e\xaf\xf9\xb2\x5b\x96',b'\x19\xfa\x87\x4f\x7c\x24\xd8\xc8\xe2\xc0\xbf\xe5\xbf\x95\x6f\x34',b'\x77\x60\xad\x46\x05\x37\xca\x9c\x63\x84\x23\xd1\x34\x3d\xdb\xb8',b'\x48\xe2\x58\x25\x88\x31\x41\x2e\x55\x05\x33\x6c\x2a\x4e\x75\x47',b'\x04\xe6\xbc\xbe\xed\x0e\xe8\xe6\xa9\x56\x77\x6c\x8b\x3c\xe2\xc0',b'\xe7\x6f\x20\xa7\x90\x2b\xd0\xde\x82\xe3\xcb\x6e\x4b\x9c\x5a\x72',b'\x33\xc2\xc2\xbe\x4e\xc0\x57\x20\x08\xe2\xc4\xd8\x53\x29\x47\x99',b'\x20\xa9\xce\x40\x36\xe7\xd6\x16\x64\xfc\x6c\x14\x73\x9f\x1f\xf6',b'\x54\x35\x1b\x77\xe7\x43\x55\x8c\x55\x40\x50\xd8\xb9\x85\x74\xe7',b'\x0f\x8f\x31\x28\xf6\xd6\xa4\x2e\xd9\xbc\x79\x57\x18\x01\x78\x35',b'\xbf\xd0\xca\x81\xc5\x36\x02\x6e\x8b\xc1\x3e\x51\x91\xed\x9c\x3a',b'\x36\xc0\xef\x3d\x4c\xc8\x2e\xbb\xf3\xfe\x4a\xd0\x34\xd9\xe9\x75',b'\x83\x00\x8f\xf6\x04\xba\xef\x91\x09\x8e\x7e\xc5\x22\x73\x26\xa1',b'\xd5\x9a\x5f\xf9\xc3\x8b\xb6\xa3\x06\xee\x1c\x10\xca\x3f\x98\xe4',b'\x31\x70\x31\xe2\x6e\x2f\x12\xd3\x02\xb1\x5a\x1c\x6e\x72\xfd\xc5',b'\xd5\xaa\xd4\x3c\x92\xd0\x21\x4e\x7f\xa5\x5b\x13\x0d\x21\xd8\x9d',b'\x41\x4c\x96\x50\xde\x72\x62\xaf\x67\x84\x48\x2c\xbd\x71\x33\x79',b'\x85\x3c\x14\x58\x7b\x02\xdb\xc7\xac\x56\x5f\x6f\xc6\xe4\x3e\x16',b'\x44\x2d\xaa\x09\x62\xba\x67\x99\x57\x2b\x92\xa4\x57\xe0\xf6\x14']
popular_sites = ["www.hulu.com", "www.netflix.com", "www.twitch.com", "www.youtube.com", "www.disneyplus.com", "www.pornhub.com", "www.hbo.com", "www.uniqlo.com", "www.wikipedia.com", "www.stonybrook.edu", "www.google.com", "www.tesla.com"]
packet_size = [20, 42, 77, 123, 222, 324, 425, 583, 632, 723]


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
        res = access + ''.join(format(ord(i), '08b') for i in message[7:])
    elif msg_list[0] == 'SEND':
        res = send
        command_len = 5  # len('SEND') + 1
        message = message[command_len:]
        res = res + ''.join(format(ord(i), '08b') for i in message)
    elif msg_list[0] == 'DISCONNECT':
        res = disconnect
    elif msg_list[0] == 'ECHO':
        res = echo
    else:
        if len(msg_list) >= 2:
            res = ''.join(format(ord(i), '08b') for i in msg_list[0])
            if msg_list[1] == 'SEND':
                res = res + send
                command_len = len(msg_list) + 18
                message = message[command_len:]
                res = res + ''.join(format(ord(i), '08b') for i in message)
        elif msg_list[0] == 'ECHO':
            res = res + echo
        elif msg_list[0] == 'DISCONNECT':
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

    if message == None:
        return
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
        password = ''
        index1 = 4
        index2 = 12
        while index1 < len(message):
            character = chr(int(message[index1:index2], 2))
            password += character
            index1 += 8
            index2 += 8
        return command + ' ' + password
    elif message[0:4] == "0000":
        command = "SEND"
        new_message = ''
        index1 = 4
        index2 = 12
        while index1 < len(message):
            character = chr(int(message[index1:index2], 2))
            new_message += character
            index1 += 8
            index2 += 8
        return command + ' ' + new_message
    elif message[0:4] == '0001':
        command = "DISCONNECT"
        return command
    elif message[0:4] == '0011':
        command = "ECHO"
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
    print("DEBUG1: " + r_input)
    if r_input == None:
        return
    r_input = binary_to_unicode(r_input)
    print("DEBUG2: " + r_input)
    if r_input == None:
        return
    packet = IP(dst=addr[0])/HTTP()/HTTPRequest(
                Referer=r_input
            )
    return bytes(packet)

def scapy_packet(addr, input):
    if input == None:
        return None
    r_input = binary_converter(input)
    if r_input == None:
        return None
    # print(r_input)
    r_input = binary_to_unicode(r_input)
    if r_input == None:
        return None
    # print(r_input)
    packet = IP(dst=addr[0])/HTTP()/HTTPRequest(
                Referer=r_input
            )
    return packet

def deconstruct_packet(packet):
    # print(packet)
    packet = HTTPRequest(packet)
    message = packet[HTTPRequest].Referer
    message = unicode_to_binary(message)
    print("DEBUG3: " + message)
    message = binary_deconverter(message)
    return message


def construct_dummy_packet(packet:bytes):
    global raw_packet_bytes, popular_sites, packet_size
    original_packet_size = len(packet)
    new_size = packet_size[randrange(10)]
    while 1:
        if len(packet) > new_size:
            break
        packet = packet + raw_packet_bytes[randrange(50)]
    return packet
