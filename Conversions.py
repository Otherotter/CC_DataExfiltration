zero = '\u200c'  # 0
one = '\u200d'  # 1

send = "0000"
disconnect = "0001"
clients = "0010"
echo = "0011"
drop = "0100"

res = ''
final_res = ''
final_final_res = ''


def binary_converter(message):
    global res

    message2 = message
    msg_list = message2.split()

    if msg_list[0] == 'SEND':
        res = send
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'DISCONNECT':
        res = disconnect
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'CLIENTS':
        res = clients
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'ECHO':
        res = echo
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    elif msg_list[0] == 'DROP':
        res = drop
        command_len = len(msg_list[0]) + 1
        message = message[command_len:]
    res += ''.join(format(ord(i), 'b') for i in message)

    return res
    # binary_to_unicode(res)


def binary_to_unicode(message):
    global final_res
    print("LEN: " + str(len(message)))
    for i in message:
        if i == '0':
            final_res += zero
        if i == '1':
            final_res += one
    return final_res

def unicode_to_binary(message):
    index1 = 0
    index2 = 3
    global final_final_res

    while index1 < len(message):
        if message[index1:index2] == b'\xe2\x80\x8c':
            final_final_res += "0"
        elif message[index1:index2] == b'\xe2\x80\x8d':
            final_final_res += "1"
        index1 += 3
        index2 += 3