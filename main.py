import threading
import socket

host = "127.0.0.1"  # local host
port = 12129
clientsList = []
IdentityName = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


def broadCastMessage(message):
    for client in clientsList:
        client.send(message)


def handleClient(client):
    while True:  # endless loop
        try:
            message = client.recv(1024)  # packet size
            broadCastMessage(message)

        except:
            index = clientsList.index(client)
            clientsList.remove(client)
            client.close()
            identity = IdentityName[index]
            broadCastMessage(f'{identity} left the chat'.encode('ascii'))
            IdentityName.remove(identity)
            break


def recieveMessage():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("RequestIdName".encode('ascii'))  # message for client to give a name
        identityName = client.recv(1024).decode('ascii')
        IdentityName.append(identityName)
        clientsList.append(client)

        print(f'Identity Name of client is {identityName}')
        broadCastMessage(f'{identityName} joined the channel!'.encode('ascii'))  # for all the clients
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()

        print(f"Active Connections: {threading.activeCount() - 1}")


print("The Server is listening.")
recieveMessage()
