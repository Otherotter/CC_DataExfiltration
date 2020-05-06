import socket, os, sys, signal, time

cc_flag = 0


def sigusr1_handler(signum, frame):
    cc_flag = 1
    print('Signal handler called with signal', signum)

def sigalrm_handler(signum, frame):
    print('Signal handler called with signal', signum)

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


def server_program():
    # n = os.fork()
    # if n == 0:
    #     while(1):
    #         a = input()
    #         if(a == "C&C"):
    #             print("Here: " + a)

    # print("asdf")
    # signal.signal(signal.SIGUSR1, sigusr1_handler)
        #get the hostname
    # signal.signal(signal.SIGALRM, sigalrm_handler)
    # signal.alarm(1)
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    time.sleep(1)
    print("asdf")
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        #data = conn.recv(1024).decode()
        # if not data:
        #     # if data is not received break
        #     break
        #print("from connected user: " + str(data))
        #data = echo(data)
        data = input()
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection
        


if __name__ == '__main__':
    server_program()