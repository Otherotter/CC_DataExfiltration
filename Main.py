from Server import *
import socket, os, sys, signal, time, argparse


cc_flag = 0
helpMenuDescription = "Run a server that is able connect and communicate with clients"
port_help = "Enter a port number of your choosing"
hostname_help = "Enter a hostname of your choosing"

port = 2000
hostname = "localhost"

def echo(data):
    return data

def command_center():
    menu = "\t> View Clients\t> Send Operation:\t>Help"
    print("CommandCenter C&C:")
    print(menu)
    command = input()
    if command == 0:
        pass
    elif command == 1:
        pass
    else:
        pass


def server():
    global port, hostname
    print("server")
    ThreadedServer(hostname,port).listen()
    # server_socket = socket.socket()  # get instance
    # server_socket.bind((hostname, port))  # bind host address and port together
    # server_socket.listen(1)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))
    # while True:
    #     # receive data stream. it won't accept data packet greater than 1024 bytes
    #     data = conn.recv(1024).decode()
    #     if not data:
    #         if data is not received:
    #             break

    #     print("from connected user: " + str(data))
    #     data = echo(data)
  
    #     conn.send(data.encode())  # send data to the client

    # conn.close()  # close the connection
        
def init():
    parser = argparse.ArgumentParser(prog="CommandCenter", description=helpMenuDescription)
    parser.add_argument('-p', help=port_help, type=int, required=True)
    parser.add_argument('-n', help=hostname_help, type=str)
    return parser

def main(parser):
    global port, hostname
    if len(sys.argv) <= 1:
        parser.print_help()
        exit()
    else:
        parser = vars(parser.parse_args())
        print(parser)

    for options, args in parser.items():
        if parser[options] != None:
            if(options == 'p'):
                port = args
            elif(options == 'n'):
                hostname = args
    server()
    

if __name__ == "__main__":
    parser = init()
    main(parser)
    







# import socket
# import threading

# class ThreadedServer(object):
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.sock.bind((self.host, self.port))

#     def listen(self):
#         self.sock.listen(5)
#         while True:
#             client, address = self.sock.accept()
#             client.settimeout(60)
#             threading.Thread(target = self.listenToClient,args = (client,address)).start()

#     def listenToClient(self, client, address):
#         size = 1024
#         while True:
#             try:
#                 data = client.recv(size)
#                 if data:
#                     # Set the response to echo back the recieved data 
#                     response = data
#                     client.send(response)
#                 else:
#                     raise error('Client disconnected')
#             except:
#                 client.close()
#                 return False

# if __name__ == "__main__":
#     while True:
#         port_num = input("Port? ")
#         try:
#             port_num = int(port_num)
#             break
#         except ValueError:
#             pass