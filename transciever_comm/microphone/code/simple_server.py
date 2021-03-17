#!/usr/bin/python3

import socket, pickle
import npy_arr_rec as rec

def create_port():
    s = socket.socket()
    host = socket.gethostname()
    port = 9999

    s.bind((host, port))

    print("Waiting for connection")
    s.listen(5)

    data = rec.record(10)
    print("data recorded")
    data_str = pickle.dumps(data)
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        conn.send(data_str)
        conn.close()
        rec.plot(data)
create_port()
