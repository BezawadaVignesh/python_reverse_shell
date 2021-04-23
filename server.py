import socket
import sys
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = int(input("Enter PORT: "))
ADDR = (SERVER, PORT)
server = socket.socket()

def create_socket():
    try:
        print("Trying to create socket..")
        global server

        server = socket.socket()
        server.bind(ADDR)

        print("[SUCCESSFUL]Socket created successfully.")

    except socket.error as err:
        print(f"Socket creation failed with {err}")


def bind_server():
    global server;
    server.listen()
    print(f"[LISTENING] Server has started listening on {SERVER}")
    conn, addr = server.accept()

    print(f"Connection has been established | IP {addr[0]} | Port {addr[1]}")
    send_commands(conn)

    conn.close()
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            server.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024*5), "utf-8")

            print(client_response, end="")


def main():
    create_socket()
    bind_server()


main()