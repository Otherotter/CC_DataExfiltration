import socket, os, sys, signal, time

def identify_client():
    print(socket.gethostbyname(socket.gethostname()))

def client_program():
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

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
