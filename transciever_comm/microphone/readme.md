# Getting microphone input and transmitting it across TCP Socket
In order to transmit audio samples over a TCP socket with hope to as little interference as possible all audio samples were kept as numpy arrays and transmitted as such.
## Transmitting 10 second audio recorded data using the py_arr_rec.py file and encoding it
```
data = rec.record(10)
print("data recorded")
data_str = pickle.dumps(data)
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        conn.send(data_str)
        conn.close()
```
<p align="center">
    <img src = "https://user-images.githubusercontent.com/60630614/111500007-e7ee0500-8719-11eb-8511-145a457213d1.png" width = "500" height = "500">
</p>

## Decoding the numpy array transmitted across the TCP socket and plotting it
```
data = b""
while True:
    packet = s.recv(4096)
    if not packet: break
    data += packet
data_arr = pickle.loads(data)
print(data_arr)
s.close()

    rec.plot(data_arr)
```
<p align="center">
    <img src = "https://user-images.githubusercontent.com/60630614/111499858-c3922880-8719-11eb-9150-20ab3b2a4107.png" width = "500" height = "500">
</p>

Both audio plots match, showing no noise is added to the audio sample during encoding and decoding of the transmission across TCP socket.
