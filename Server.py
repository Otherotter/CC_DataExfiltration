import socket
import threading
import socketserver
import time

from scapy.layers.http import HTTP, HTTPRequest
from scapy.sendrecv import send
from  scapy.all import * 

load_layer('http')
class ThreadedServerHandler (socketserver.BaseRequestHandler):
    def __init__(self, iterable):
        print("INIT") 

    def handle(self):
        print("HERE")
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class CommandCenter():
    def __init__(self):
        self.client_list = []

    def menu(self):
        menu = "CC-DATA\n[CLIENTS : print clients]   [COMMAND <IP> <OPTION> <(optional)>: command client]\n\t<IP> : Type in client's IP to send to specific client. ALL to send to all clients\n\t<OPTION>: [echo] [send] [disconnect]\n"
        return menu

    def clients(self, device):
        '''Prints all clients connected with the server'''
        if self.client_list == []:
            device.send_message("NO CLIENTS")
        else:
            print(len(self.client_list))
            device.send_message(str(len(self.client_list)))
            for i in self.client_list:
                device.send_message(i.ip)

    # def echo(self, device):
    #     '''The client should echo back with there IP'''
    #     device.send("echo")

    # def disconnect(self, device):
    #     pass

    # def send(self, device, command):
    #     device.send(command)
    
    def excute_command(self, device, command, optional=None):
        
        if command != "SEND" and command != "DISCONNECT" and command != "ECHO":
            device.send_message(self.menu())
            return

        if command == "SEND" and optional != None:
            packet = self.construct_packet(device.ip, command, optional)
            #device.send_cc_message(packet)
            device.send_message(optional)

        # if command == "SENDP" and optional != None:
        #     device.send_cc_message(optional)

        elif command == "DISCONNECT":
            packet = self.construct_packet(device.ip, command, optional)
            device.close()
        else:
            packet = self.construct_packet(device.ip, command, optional)
            device.send_message("ECHO")

    def command(self, addr, command, optional=None):
        print("command1")
        print(addr)
        print(command)
        print(optional)
        print(command != "ECHO")
        if command != "ECHO" and command != "SEND" and command != "DISCONNECT":
            self.menu()
            return
        print("command2")
        if addr == "ALL":
            for i in self.client_list:
                self.excute_command(i,command,optional)
        else:
            client = locateBy_(addr)
            if(client != None):
                self.excute_command(client, command,optional)


    def insert(self, client):
        self.client_list.append(client)
    
    def locateBy_(self, search, option):
        if option == 0:
            for i in self.client_list:
                if i.ip == search:
                    return i

    def construct_packet(self, ip, command, message=None):
        #MARCFUNCTON
        packet = IP(dst=ip)/HTTP()/HTTPRequest(
                    Referer=command
                )
        return bytes(packet)

class ClientInfo():
    def __init__(self, client, address):
        self.elevated = False
        self.client = client
        self.address = address
        self.ip = address[0] 
        self.cc = CommandCenter()


    def elevatation(self, passwoCrd=None):
        print(passwoCrd)
        if(passwoCrd == "PASSWORD"):
            self.elevated = True 
            self.send_message("ACCESS GRANTED, WELCOME!")
            self.send_message(self.center.menu())
        else:
            self.elevated = False


    def send_message(self, message):
        if type(message) is not bytes:
            message = message.encode()
            self.client.send(message)
        else:
            self.client.send(message)

    def close(self):
        self.client.close()


    def send_cc_message(self, message):
        send = "\u0030"
        disconnect = "\u0031"
        clients = "\u0032"
        echo = "\u0033"
        drop = "\u0034"
        space = "\u0020"
        message = send + '\u200c' + space + '\u200c' + "\u0079\u0065\u0065"
        # message = message.encode()
        if len(message) <= 1024:
            packet = HTTP() / HTTPRequest(
                Referer=message
            )
            self.send_message("RECEIVED")
            self.send_message(packet[HTTPRequest].Referer)
            # read_cc_message(packet)


    def read_cc_message(self, packet):
        message2 = "message sent"
        message = packet[HTTPRequest].Referer
        if type(message) is not bytes:
            message2 = message2.encode()
            self.client.send(message2)
            message = message.encode('utf-8', 'ignore')
            self.client.send(message)
        else:
            self.client.send(message2)
            self.client.send(message)


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.cc = CommandCenter()

    def listen(self):
        self.sock.listen(1)
        while True:
            client, address = self.sock.accept()
            #client.settimeout()
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

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


    def listenToClient(self, client, address):
        size = 1024
        client_instance = ClientInfo(client, address)
        self.cc.insert(client_instance)
        print("ADDED CLIENT: " + client_instance.ip)
        while True:
            #client_instance.send_message("Hello from Server")
            #packet = HTTP()/HTTPRequest(Referer="\u200d")
            #p = bytes(packet)
            #client.send(p)
            time.sleep(2)
            data = client.recv(size)
            data = data.decode()
            if data:
                #Set the response to echo back the recieved data 
                self.parser(str(data), client_instance)
            else:
                raise print('Client disconnected')
            # try:
            #     data = client.recv(size)
            #     data = data.decode()
            #     if data:
            #         print(str(data))
            #         # Set the response to echo back the recieved data 
                    
            #         self.parser(str(data), client_instance)
            #         #response = data
            #         #client.send(response)
            #     else:
            #         raise print('Client disconnected')
            # except:
            #     print("something happends")
            #     #client.close()
            #     #return False