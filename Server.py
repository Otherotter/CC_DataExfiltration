import socket
import threading
import socketserver

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
        menu = "CC-DATA\n[CLIENTS : print clients]   [COMMAND <IP> <OPTION> <(optional)>: command client]\n\t<IP> : Type in client's IP to send to specific client. ALL to send to all clients\n\t<OPTION>: [echo] [send] [disconnect]"
        return menu

    def clients(self, device):
        '''Prints all clients connected with the server'''
        if self.client_list == []:
            device.send("NO CLIENTS")
        else:
            for i in self.client_list:
                device.send(i.ip)

    # def echo(self, device):
    #     '''The client should echo back with there IP'''
    #     device.send("echo")

    # def disconnect(self, device):
    #     pass

    # def send(self, device, command):
    #     device.send(command)
    
    def excute_command(self, device, command):
        if command != "send":
            device.send(command)
        elif command != "disconnect":
            device.close()
        else:
            device.send("echo")

    def command(self, addr, command):
        if command != "echo" or command != "send" or command != "disconnect":
            menu()
            return
        if addr == "ALL":
            for i in self.client_list:
                excute_command(i,command)
        else:
            client = locateBy_(addr)
            if(client != None):
                excute_command(client, command)


    def insert(self, client):
        self.client_list.append(client)
    
    def locateBy_(self, search, option):
        if option == 0:
            for i in self.client_list:
                if i.ip == search:
                    return i


class ClientInfo():
    def __init__(self, client, address, cc):
        self.elevated = False
        self.client = client
        self.address = address
        self.ip = 0
        self.center = cc


    def elevatation(self, password : str):
        print(password)
        if(password == "AAAAA"):
            self.elevated = True 
            self.send("ACCESS GRANTED, WELCOME!", self.client)
            self.send(self.center.menu(), self.client)
        else:
            self.elevated = False

            

    def send(self, message, client):
        message = bytes(message,"utf-8")
        client.send(message)
        if type(message) is not bytes:
            message = bytes(message,"utf-8")
            client.send(message)
        else:
            client.send(message)


    def handle(self):
        print("HERE")
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)


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
        print("parse")
        message = message[:20].split()
        print(message[0] == "access" )
        command = message[0]
        if command == "ACCESS":
            if(len(message) == 2):
                client_instance.elevatation(message[1])
        elif client_instance.elevatation:
            if command == "CLIENTS":
                if len(message) == 1:
                    self.cc.clients(client_instance)
            elif command == "COMMAND": 
                if len(message) == 3 or len(message) == 4:
                    self.cc.command(client_instance)
            elif command == "DROP":
                if len(message) == 1:
                    client_instance.elevatation()


    def listenToClient(self, client, address):
        size = 1024
        client_instance = ClientInfo(client, address, self.cc)
        self.cc.insert(client_instance)
        while True:
            data = client.recv(size)
            data = data.decode()
            if data:
                print(str(data))
                # Set the response to echo back the recieved data 
                
                self.parser(str(data), client_instance)
                #response = data
                #client.send(response)
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