import socket, os, sys, signal, time

master_pid = -1
alarm_flag = 0

def sigalrm_handler(signum, frame):
    print('Signal handler called with signal', signum)
    alarm_flag = 1

def identify_client():
    print(socket.gethostbyname(socket.gethostname()))


def client_program():
    global master_pid, alarm_flag
    print(socket.gethostbyname("www.google.com"))
    a=socket.gethostbyaddr("18.218.176.168")
    master_pid = os.getpid()
    # print(a)
    # print(socket.socket().connect(("18.218.176.168",80)))

    n = os.fork()
    if n == 0:
        signal.alarm(1)
        while(1):
            if(alarm_flag ==1):
                print("ASdf")
                signal.alarm(1)
                alarm_flag = 0

   
    

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    identify_client()
    message = input(" -> ")  # take input
    start_time = time.time()
    while message.lower().strip() != 'bye':
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        if(elapsed_time > 60):
            start_time = time.time()
            print("Connectbacktoserver")
        #client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if not data:
            # if data is not received break
            continue

        print('Received from server: ' + data)  # show in terminal

        # message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()