#!/usr/bin/python3
from init_port import *

NAME = 'read_freq.py'

ser = initSerialPort(COMPORT)

log("Sending FA command...")
#------------------------------------------------------------------------------
check = '00014591052'
data = send_command(ser, 'FA' + check + ';', 0)
time.sleep(0.5)
check = '00014594055'
data = send_command(ser, 'FA' + check + ';', 0)
time.sleep(0.5)
check = '00014595052'
data = send_command(ser, 'FA' + check + ';', 0)

#------------------------------------------------------------------------------
log("FA: success!")

#------------------------------------------------------------------------------
log("Sending IF command...")
#------------------------------------------------------------------------------
data = send_command(ser, 'IF;', 38)
# Now the response from the radio is parsed...
tmp  = data.decode('ascii')
freq = float(tmp[2:13])/1000. # This is the frequency in kHz.
tmp  = int(tmp[28])           # This is current state TX/RX.
Status = ['RX', 'TX']
txstatus = Status[tmp]
#------------------------------------------------------------------------------
log("IF: success!")
#------------------------------------------------------------------------------

#ser.reset_output_buffer()
#ser.reset_input_buffer()

#------------------------------------------------------------------------------
log("Sending MD command...")
#------------------------------------------------------------------------------
data = send_command(ser, 'MD;', 4)
# Now the response from the radio is parsed...
tmp = data.decode('ascii')
radioMode = ["none", "LSB", "USB", "CW", "FM", "AM", "FSK", "CW-R", "none.", "FSK-R"]
mode = int(tmp[2:3])
#------------------------------------------------------------------------------
log("MD: success!")
#------------------------------------------------------------------------------

ser.close()	# Serial port is closed.

print(NAME + " v" + VERSION + ", by " + AUTHOR)
print("QRG [kHz]:\t" + str(freq))
print("Mode:     \t" + radioMode[mode])
print("Status:   \t" + txstatus)
#outputString = str(freq) + ' kHz, ' + radioMode[mode] + ', ' + txstatus
