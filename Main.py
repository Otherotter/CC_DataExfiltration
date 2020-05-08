from Server import *
import socket, os, sys, signal, time, argparse

cc_flag = 0
helpMenuDescription = "Run a server that is able connect and communicate with clients"
port_help = "Enter a port number of your choosing"
hostname_help = "Enter a hostname of your choosing"

port = 2000
hostname = "localhost"


def server():
    global port, hostname
    print("server")
    ThreadedServer(hostname,port).listen()
        
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
    