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
dummy_client_called = 0
client_alive = True


def identify_client():
    print(socket.gethostbyname(socket.gethostname()))

def client_input(client_socket):
    print("Input: ")
    a = input()
    print(a)

def dummy_client(): 
    global dummy_client_called
    dummy = socket.socket()
    index = dummy_client_called % len(popular_sites)
    dummy.connect((popular_sites[index],80))
    for i in range(randrange(15)):
        dummy_packet = construct_dummy_packet(b'')
        dummy.send(dummy_packet)
    dummy.settimeout(100)
    while 1:
        dummy.recv(1024)  # receive response
    dummy.close()  # close the connection
    

def asyn_contact():
    global dummy_client_called, client_alive
    start = time.time()
    while client_alive:
        elapsed_time = time.time() - start
        if(elapsed_time > 60):
            start_time = time.time()
            packet = construct_packet(list(client_socket.getpeername()), "CLIENT-COMMUNICATING")
            client_socket.send(packet)
            dummy_client_called = dummy_client_called + 1

def client():
    global client_socket, port, hostname,dummy_client_called,client_alive # contains hostname and port number
    asyn_communication = threading.Thread(target = asyn_contact, args = ())
    asyn_communication.start()
    try:
        client_socket = socket.socket()  # instantiate
        #client_socket.settimeout()
        client_socket.connect((hostname, port))  # connect to the server
        identify_client()
        while 1:
            packet = client_socket.recv(1024)  # receive response
            data = deconstruct_packet(packet)
            if not data:
                continue  # if data is not received break
            print('Received from server: ' + data)  # show in terminal
    except:
        client_socket.close()  # close the connection
        client_alive = False
        asyn_communication.join()

def client_program():
    global dummy_client_called, client_alive
    threading.Thread(target = client, args = ()).start()
    while client_alive:
        i = input()
        threading.Thread(target = dummy_client, args = ()).start()
        packet = construct_packet(list(client_socket.getpeername()), i)
        if(packet != None):
            client_socket.send(packet)
            dummy_client_called = dummy_client_called + 1
    print("CLIENT DISCONNENTED")
    exit()

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
