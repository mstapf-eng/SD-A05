#!/usr/bin/python3
import socket, pickle
import npy_arr_rec as rec

def create_port(audio_time = 3):
    s = socket.socket()
    host = socket.gethostname()
    port = 9999

    s.bind((host, port))

    print("Waiting for connection")
    s.listen(5)

    data = rec.record(audio_time) #record 3 second audio transmission
    print("data recorded")
    print(data)
    data_str = pickle.dumps(data)
    print("data encoded")
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        conn.send(data_str)
        conn.close()
        rec.plot(data)
create_port()
