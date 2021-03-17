import socket, pickle
import npy_arr_rec as rec

def read_port(host = '129.32.60.214'):
    s = socket.socket()
    host = host
    port = 9999

    s.connect((host,port))

    data = b""
    while True:
        packet = s.recv(4096)
        if not packet: break
        data += packet

    data_arr = pickle.loads(data)
    print(data_arr)
    s.close()

    print("Playback occuring")
    rec.playback(data_arr)
    print("Playback done")
    rec.plot(data_arr)

    #print ('Received', repr(data_arr))


read_port()
