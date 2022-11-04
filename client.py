import random
import socket
import threading
from colorama import Fore, init, Back

init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

clientColor = random.choice(colors)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12129))

idName = input("Choose a name: ")


def recieveMessage():
    while True:  # infinite loop
        try:
            message = client.recv(1024).decode('ascii')
            if message == "RequestIdName":
                client.send(idName.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def sendMessage():
    while True:
        userSays = input(":")
        message = f'{clientColor}{idName}: {userSays}{Fore.RESET}'
        client.send(message.encode('ascii'))

# This thread receives messages 
recieveThread = threading.Thread(target=recieveMessage)
# Making the thread daemon so that it ends whenever the main thread ends
recieveThread.daemon = True
recieveThread.start()

sendThread = threading.Thread(target=sendMessage)
sendThread.start()
