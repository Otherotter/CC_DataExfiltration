import socket, os, sys, signal, time, argparse
import threading
import selectors
from Conversions import *
from scapy.sendrecv import send

cc_flag = 0
helpMenuDescription = "Run the client"
port_help = "Enter a port number of your choosing"
hostname_help = "Enter a hostname of your choosing"
port = 2000
hostname = "localhost"
client_socket = None

def identify_client():
    print(socket.gethostbyname(socket.gethostname()))

def client_input(client_socket):
    print("Input: ")
    a = input()
    print(a)

def client():
    global client_socket, port, hostname # contains hostname and port number
    client_socket = socket.socket()  # instantiate
    #client_socket.settimeout()
    client_socket.connect((hostname, port))  # connect to the server
    identify_client()
    while 1:
        data = client_socket.recv(1024).decode()  # receive response
        if not data:
            continue  # if data is not received break
        print('Received from server: ' + data)  # show in terminal


    client_socket.close()  # close the connection

def client_program():
    threading.Thread(target = client, args = ()).start()
    while 1:
        i = input()
        packet = construct_packet(list(client_socket.getpeername()), i)
        client_socket.send(packet)
        #print(i)

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
    client_program()

if __name__ == "__main__":
    parser = init()
    main(parser)
    















#     import socket, os, sys, signal, time, argparse
# import threading
# import selectors
# cc_flag = 0
# helpMenuDescription = "Run the client"
# port_help = "Enter a port number of your choosing"
# hostname_help = "Enter a hostname of your choosing"

# port = 2000
# hostname = "localhost"
# client_socket = None
# def identify_client():
#     print(socket.gethostbyname(socket.gethostname()))

# def client_input():
#     print("Input: ")
#     a = input()
#     print(a)



# def client_read():
#     global client_socket
#     #client_socket.send(message.encode())  # send message
#     #client_socket.send("asdf".encode())
#     data = client_socket.recv(1024).decode()  # receive response
#     print('Received from server: ' + data)  # show in terminal

# def client_program():
#     global client_socket, port, hostname # contains hostname and port number
#     # host = socket.gethostname()  # as both code is running on same pc. Run server before connecting 
#     # port = 2000  # socket server port number
#     client_socket = socket.socket()  # instantiate
#     #socket.settimeout(1000)
#     client_socket.connect((hostname, port))  # connect to the server
#     # print(client_socket.getaddrinfo(hostname, port)) # connect to the server
#     sel = selectors.DefaultSelector()
#     sel.register(sys.stdin, selectors.EVENT_WRITE, client_input)
#     sel.register(client_socket, selectors.EVENT_READ, client_read)
#     identify_client()
#     while 1:
#         events = sel.select(5)
#         print(events)
#         for key, mask in events:
#             callback = key.data
#             callback()
#         #client_socket.send(message.encode())  # send message

#         # client_socket.send("asdf".encode())
#         # data = client_socket.recv(1024).decode()  # receive response
#         # if not data:
#         #     continue  # if data is not received break
#         # print('Received from server: ' + data)  # show in terminal


#     client_socket.close()  # close the connection


# def init():
#     parser = argparse.ArgumentParser(prog="CommandCenter", description=helpMenuDescription)
#     parser.add_argument('-p', help=port_help, type=int, required=True)
#     parser.add_argument('-n', help=hostname_help, type=str)
#     return parser

# def main(parser):
#     global port, hostname
#     if len(sys.argv) <= 1:
#         parser.print_help()
#         exit()
#     else:
#         parser = vars(parser.parse_args())
#         print(parser)

#     for options, args in parser.items():
#         if parser[options] != None:
#             if(options == 'p'):
#                 port = args
#             elif(options == 'n'):
#                 hostname = args
#     client_program()

# if __name__ == "__main__":
#     parser = init()
#     main(parser)
    