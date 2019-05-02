import socket
from threading import Thread

host = ''
port = 5000

all_address = {}
all_connections = {}

s = socket.socket()
s.bind((host,port))

def accept_request():
    while True:
        conn,address = s.accept()
        conn.send(bytes("Enter your name: ","utf-8"))
        print("Connected to: " + address[0])
        all_address[conn] = address
        Thread(target=handle_request,args=(conn,)).start()

def handle_request(conn):
    name = conn.recv(1024).decode("utf-8")
    conn.send(bytes("%s  \n"%name, "utf-8"))
    conn.send(bytes("Hey there! Welcome to >--HYPER-SPACE--< developed by 7enTropy7", "utf-8"))
    msg = "%s has joined this chat."%name
    send_to_clients(bytes(msg,"utf-8"))
    all_connections[conn] = name
    while True:
        msg = conn.recv(1024)
        if msg != bytes("{quit}","utf-8"):
            send_to_clients(msg, name + ": ")
        else:
            conn.send(bytes("{quit}","utf-8"))
            conn.close()
            del all_connections[conn]
            send_to_clients(bytes("%s has left this chat."%name,"utf-8"))
            break

def send_to_clients(msg,prefix=""):
    for c in all_connections:
        c.send(bytes(prefix,"utf-8")+msg)

if __name__ == "__main__":
    s.listen(4)
    print("Waiting for connections...")
    accept_thread = Thread(target=accept_request)
    accept_thread.start()
    accept_thread.join()
    s.close()