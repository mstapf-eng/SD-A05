#!/usr/bin/python3
from init_port import *

ser = initSerialPort(COMPORT)
##############################################################
##IF command
# to recieve frequency
data = send_command(ser, 'IF;', 38)
tmp  = data.decode('ascii')
freq = float(tmp[2:13])/1000. # This is the frequency in kHz.
tmp  = int(tmp[28])           # This is current state TX/RX.
Status = ['RX', 'TX']
txstatus = Status[tmp]
##############################################################
## MD command
# to recieve mode
data = send_command(ser, 'MD;', 4)
tmp = data.decode('ascii')
radioMode = ["none", "LSB", "USB", "CW", "FM", "AM", "FSK", "CW-R", "none.", "FSK-R"]
mode = int(tmp[2:3])
##############################################################
# KYO command
data = send_command(ser, 'KY0;', 0)
##############################################################
## MG command
# to recieve mic gain
data = send_command(ser, 'MG;', 6)
tmp = data.decode('ascii')
mic_gain = int(tmp[2:5])
##############################################################
## AG command
# to recieve AF gain
# from main transciever
data = send_command(ser, 'AG0;', 7)
tmp = data.decode('ascii')
af_gain = int(tmp[3:6])
tmp = int(tmp[3])
transciever = ['Main Transciever', 'Sub-reciever']
txtran = transciever[tmp]
# to set AF gain
# from main transciever
#command(AG)--0,1-val for gain---
data = send_command(ser, 'AG050;', 7)
ser.close()	# Serial port is closed.
##############################################################
## AC command
#read internal antenna tuner status
data = send_command(ser, 'AC;', 6)
tmp = data.decode('ascii')
temp = int(tmp[2])
rx_stat = ['RX-AT THRU', 'RX-AT IN']
rx = rx_stat[temp]
temp = int(tmp[3])
tx_stat = ['TX-AT THRU', 'TX-AT IN']
tx = tx_stat[temp]
temp = int(tmp[4])
tune_stat = ['Tuning is stopped', 'tuning is active', 'Tuning cannot be completed']
tune = tune_stat[temp]
# set internal tuner status
data = send_command(ser, 'AC111;', 6)
##############################################################
## PS command
# reads the power ON/OFF status
data = send_command(ser, 'PS;', 4)
tmp = data.decode('ascii')
tmp = int(tmp[2])
pow_stat = ['On', 'Off']
power = pow_stat[tmp]
# sets the power ON/OFF
data = send_command(ser, 'PS1;', 4) # power on
data = send_command(ser, 'PS0;', 4) # power off
##############################################################
## PC Command
# Sets or reads the output power
#reads output power
data = send_command(ser, 'PC;', 6)
tmp = data.decode('ascii')
output_pow = int(tmp[2:5])
# sets output power
data = send_command(ser, 'PC070;', 6)
##############################################################
## CG command
# to recieve carrier gain
# from main transciever
data = send_command(ser, 'CG;', 6)
tmp = data.decode('ascii')
car_gain = int(tmp[3:5])
# set carrier gain
data = send_command(ser, 'CG050;', 6)
##############################################################
## FA sets frequency
#set frequency
#data = send_command(ser, 'FA' + '00043092076' + ';', 4)
data = send_command(ser, 'FA' + '00014592076' + ';', 4)
