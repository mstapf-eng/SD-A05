# Creating a Connection between transciever and computer
## Know the port settings
kenwood ts-2000: COM1 - 9600 bps - cts, rts enabled

## Use pyserial library
<https://pyserial.readthedocs.io/en/latest/pyserial.html#overview>
```
>>> ser = serial.Serial()
>>> ser.baudrate = 19200
>>> ser.port = 'COM1'
>>> ser
Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
>>> ser.open()
>>> ser.is_open
True
>>> ser.close()
>>> ser.is_open
False
```

## Initialize the serial port
```
import serial

def initSerialPort(COMPORT):
    # Let's now define the specific settings for the port (and the radio).
    ser = serial.Serial()

    ser.port = COMPORT
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.xonxoff = False
    ser.rtscts = True #rts and cts are enabled
    ser.dsrdtr = False
    ser.timeout = 0.25
    ser.setDTR(0)
    ser.setRTS(1)
 ```
 
 ## Check for a port connection and retrieve frequency
 ### Using the IF command
 ```
data = send_command(ser, 'IF;', 38)
# Now the response from the radio is parsed...
tmp  = data.decode('ascii')
freq = float(tmp[2:13])/1000. # This is the frequency in kHz.
tmp  = int(tmp[28])           # This is current state TX/RX.
Status = ['RX', 'TX']
txstatus = Status[tmp]
 ```
 
 ## Check mode variable of the transciever
 ```
data = send_command(ser, 'MD;', 4)
# Now the response from the radio is parsed...
tmp = data.decode('ascii')
radioMode = ["none", "LSB", "USB", "CW", "FM", "AM", "FSK", "CW-R", "none.", "FSK-R"]
mode = int(tmp[2:3])
```

## Close port and print variable data
```
ser.close()	# Serial port is closed.

print(NAME + " v" + VERSION + ", by " + AUTHOR)
print("QRG [kHz]:\t" + str(freq))
print("Mode:     \t" + radioMode[mode])
print("Status:   \t" + txstatus)
```
![port_con](https://user-images.githubusercontent.com/60630614/109561847-b33c4580-7aab-11eb-9d60-6fc7204ad090.PNG)
