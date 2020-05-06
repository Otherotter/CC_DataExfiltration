import socket, os, sys, signal, time

cc_flag = 0

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
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024
    time.sleep(1)
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            if data is not received break
             break
        print("from connected user: " + str(data))
        data = echo(data)
  
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection
        


if __name__ == '__main__':
    server_program()
