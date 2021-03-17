#!/usr/bin/python3
from init_port import *
COMPORT = 'COM1'
ser = initSerialPort(COMPORT)
class commands:
    def __init__(self, type =None, freq =None, sound_vol = None, power = None):
        self.command_type = type
        self.frequency = freq
        self.af_gain = sound_vol
        self.pow_stat = power
    def type_command(self):
        if self.command_type == 'IF':
            return if_command()
        elif self.command_type == 'MD':
            return md_command()
        elif self.command_type == 'AG':
            return ag_command()
        elif self.command_type == 'AC':
            return ac_command()
        elif self.command_type == 'PS':
            return ps_command()
        elif self.command_type == 'PC':
            return pc_command()
        elif self.command_type == 'FA':
            return fa_command(self.frequency)

def if_command():
    data = send_command(ser, 'IF;', 38)
    tmp = data.decode('ascii')
    freq = float(tmp[2:13]) / 1000.  # This is the frequency in kHz.
    tmp = int(tmp[28])  # This is current state TX/RX.
    Status = ['RX', 'TX']
    txstatus = Status[tmp]
    print("Frequency(kHz):   \t" + str(freq))
    print("Status:   \t" + txstatus)
def md_command():
    data = send_command(ser, 'MD;', 4)
    tmp = data.decode('ascii')
    radioMode = ["none", "LSB", "USB", "CW", "FM", "AM", "FSK", "CW-R", "none.", "FSK-R"]
    mode = int(tmp[2:3])
    print("Mode:   \t" + mode)
def ag_command():
    data = send_command(ser, 'AG0;', 7)
    tmp = data.decode('ascii')
    af_gain = int(tmp[3:6])
    tmp = int(tmp[3])
    transciever = ['Main Transciever', 'Sub-reciever']
    txtran = transciever[tmp]
    print("AF Gain:   \t" + str(af_gain))
    print("Transciever:   \t" + txtran)
def ac_command():
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
    print("TX:   \t" + tx)
    print("RX:   \t" + rx)
    print("Tuning Status:   \t" + tune)
def ps_command():
    data = send_command(ser, 'PS;', 4)
    tmp = data.decode('ascii')
    tmp = int(tmp[2])
    pow_stat = ['On', 'Off']
    power = pow_stat[tmp]
    print("Power Status:   \t" + power)
def pc_command():
    data = send_command(ser, 'PC;', 6)
    tmp = data.decode('ascii')
    output_pow = int(tmp[2:5])
    print("Output Power:   \t" + output_pow)
def fa_command(frequency):
    data = send_command(ser, 'FA' + frequency + ';', 4)
    
    
def main():
    x = commands('IF')
    ser.close()  # Serial port is closed.
    
if __name__ == '__main__':
    main()
