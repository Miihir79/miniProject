import sys
import re
import subprocess
from  tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox
import matrix_commander

# Method to check for errors in execution in matrix methods
def workCheck() -> None:
    try: 
        ret = matrix_commander.main()

        if ret == 0:
            print("matrix_commander finished successfully.")
        else:
            print(
                f"matrix_commander failed with {ret} error{'' if ret == 1 else 's'}."
            )
    except Exception as e:
        print(f"Exception happened: {e}")
        ret = 99

def sendMsg(msg):
    sys.argv[0] = "matrix-commander"
    sys.argv.extend(["--message", msg])

    workCheck()

def receiveMsg():
    cmd = ["matrix-commander", "--tail", "--listen-self"]
    result = subprocess.run(cmd, capture_output = True)

    finalMsg = result.stdout
    # Converting byte to str
    finalMsg = finalMsg.decode()

    recMsg = formatMsg(finalMsg)

    workCheck()

    return recMsg

# Method to format the incoming string of recieved msgs
def formatMsg(string):
    msgList = re.split("\n", string)

    dispTxt = []
    for msg in msgList:
        if msg != '':
            splitMsg = re.split("\|", msg)
            print(splitMsg)
            finalTxt = splitMsg[1] + ':' + splitMsg[3]
            dispTxt.append(finalTxt)

    dispTxtStr = "\n".join(dispTxt)
    return dispTxtStr

class GUI:
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_gui()

    def initialize_gui(self):  # GUI initializer
        self.root.title("Socket Chat")
        self.root.resizable(0, 0)
        self.display_chat_box()
        self.display_chat_entry_box()
        self.recieve_chat()

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='Chat Box:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
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
        message = data
        self.chat_transcript_area.insert('end', message + '\n')
        self.chat_transcript_area.yview(END)
        sendMsg(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def startRec(self):
        showThis = receiveMsg()
        # print(showThis,type(showThis))
        self.chat_transcript_area.insert('end', showThis + '\n')
        self.chat_transcript_area.yview(END)

    def recieve_chat(self):
        frame = Frame()
        Button(frame, text = "Refresh", width = 10, command = self.startRec).pack(side = 'left')
        frame.pack()



if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW")
    root.mainloop()