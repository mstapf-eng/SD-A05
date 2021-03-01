#/python3
COMPORT = 'COM1'  # Name of the serial port.
DEBUG = True  # Debug logging level (False is no output).
DELAY = 0.15  # [ms] Interval to wait for radio's responses.

VERSION = '0.1'
AUTHOR = 'A05'

import time
import serial


# Ultra-simple debugging function: it prints out
# messages to the standard output (console) if the
# global variable DEBUG is set to True
def log(s):
    if DEBUG:
        print(s)


# Utility function for sending a command to the radio.
# It requires specifying the serial port object (see PySerial)
# the actual ASCII string to be sent and the length (in # bytes)
# of the expected reaction/answer from the radio.
def send_command(ser, command, expected_answer_length):
    # the command string is first encoded..
    ser.write(command.encode())  # and the it is sent over serial port.
    time.sleep(DELAY)  # Wait for the radio to respond.
    while True:  # Let's start  an infinite loop.
        n = ser.in_waiting  # Check how many bytes of the response.
        data = ser.read(n)  # Read them all into a 'data' variable.
        if n == expected_answer_length:  # Stop the polling if the radio
            break  # answered as we expected it to do.
        log(command + " : radio not responding...")  # If not, let's wait.
        ser.reset_output_buffer()  # Clear output serial buffer.
        ser.reset_input_buffer()  # Clear output serial buffer.
        ser.write(command.encode())  # Let's repeat the command.
        time.sleep(DELAY)  # Wait for the radio to respond.
    return data  # Return what has been replied by the radio.


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

    # Let's check whether the port is already open.
    if ser.is_open:
        log('The serial port ' + ser.name + ' was already open!')
        ser.close()  # Let's simply close it.

    log('Opening the serial port...')
    try:
        ser.open()  # Let's now open the serial port.
    except:
        log("Failed: an exception occurred!")
        print("ERROR: Unable opening port: " + COMPORT)
        exit()

    ser.reset_output_buffer()  # Clear output serial buffer.
    ser.reset_input_buffer()  # Clear output serial buffer.

    # Otherwise, let's print that everything went fine...
    log('Success! Port ' + ser.name + ' has been open.')

    return ser  # The serial port 'object' is returned
