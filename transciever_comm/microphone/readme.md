# Getting microphone input and transmitting it across TCP Socket
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
![Figure_1](https://user-images.githubusercontent.com/60630614/111500007-e7ee0500-8719-11eb-8511-145a457213d1.png)
## Decoding the numpy array and plotting it
![Figure_1](https://user-images.githubusercontent.com/60630614/111499858-c3922880-8719-11eb-9150-20ab3b2a4107.png)
