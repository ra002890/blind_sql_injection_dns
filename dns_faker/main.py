import socket
from dns import message

print('Hello World!')

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 8053  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    print('Attaching to ports!')
    s.bind((HOST, PORT))
    while True:
        data, addr = s.recvfrom(1024)
        if not data:
            break
        qmessage = message.from_wire(data)
        listdict = list(qmessage.index)
        print(f'{addr} send: {listdict[0][1]}')    