import serial
import time
import socket
def receiving(ser):
    global last_received

    buffer_string = ''
    while True:
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]
            data = last_received.split(',')
            for i in range(len(data)):
                angle_raw = data[i].split(':')
                data[i] = angle_raw[len(angle_raw) - 1]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto("{\"servo\": [" + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "]}", ("127.0.0.1", 3003))

ser = serial.Serial('/dev/ttyACM0', 9600)
receiving(ser)
