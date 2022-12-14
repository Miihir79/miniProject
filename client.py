import socket
import os
import threading
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox


class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialazing socket with TCP and IPv4
        remote_ip = '127.0.0.1'  # IP address
        remote_port = 12129  # TCP port
        self.client_socket.connect((remote_ip, remote_port))  # connect to the remote server

    def initialize_gui(self):  # GUI initializer
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()
        self.matrix_button()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server,
                                  args=(self.client_socket,))  # Create a thread for the send and receive in same time
        thread.start()

    # function to recieve msg
    def receive_message_from_server(self, so):
        while True:
            try:
                buffer = so.recv(256)
                if not buffer:
                    break
                message = buffer.decode('utf-8')

                if "joined" in message:
                    user = message.split(":")[1]
                    message = user + " has joined"
                    self.chat_transcript_area.insert('end', message + '\n')
                    self.chat_transcript_area.yview(END)
                else:
                    self.chat_transcript_area.insert('end', message + '\n')
                    self.chat_transcript_area.yview(END)

            except:
                print("An error occurred!")
                self.client_socket.close()
                break

        so.close()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=120, height=30, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=120, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = data.encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

    def matrix_button(self):
        frame = Frame()
        Button(frame, text="Matrix Chat", width=10, command=matrixRun).pack(side='left')
        frame.pack()


# Method to call the matrix-client window
def matrixRun():
    os.system("python matrix-client.py")


# the main function
if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
