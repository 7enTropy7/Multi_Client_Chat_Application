from tkinter import *
from threading import Thread
import socket

host = input('Enter host: ')
port = 5000

csoc = socket.socket()
csoc.connect((host,port))

def receive():
    while True:
        try:
            msg = csoc.recv(1024).decode("utf-8")
            chat.insert(END, msg)
        except OSError:
            break

def send(event=None):
    msg = message.get()
    message.set("")
    csoc.send(bytes(msg,"utf-8"))
    if msg == "{quit}":
        csoc.close()
        root.quit()

def close_win(event=None):
    message.set("{quit}")
    send()

root = Tk()
root.title("Hyper-Space")
root.configure(background='black')
frame = Frame(root)
message = StringVar()
scrollbar = Scrollbar(frame,bg='dark red')
chat = Listbox(frame,height=20,width=60,bg='black',fg='teal',yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT,fill=Y)
chat.pack(side=LEFT,fill=BOTH)
chat.pack()
frame.pack()
entry = Entry(root,textvariable=message)
entry.bind("<Return>",send)
entry.pack()
send_button = Button(root,text="Send",bg='green',fg='black',command=send)
send_button.pack()
root.protocol("WM_DELETE_WINDOW",close_win)

receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()