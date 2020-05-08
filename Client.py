import socket, os, sys, signal, time

def identify_client():
    print(socket.gethostbyname(socket.gethostname()))

def client_program():
    host = socket.gethostname()  # as both code is running on same pc. Run server before connecting 
    port = 2000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    identify_client()
    while 1:
        #client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if not data:
            continue  # if data is not received break
        print('Received from server: ' + data)  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
