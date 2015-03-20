import socket
import sys
import struct
import array
import threading
import time
import json
import multiprocessing
import datetime
import serial
import servo.servo as servo

CLIENT_ADDR = ('10.22.214.188', 8000)
accel_gyro = ["", ""]
servo_data = ["","",""]
sock = 'nil'

# Initialize once for reading and writing
#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('COM4', 9600)

class poll(threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port

    def run(self):
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
                sock_d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock_d.sendto("{\"servo\": [" + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "]}", ("127.0.0.1", 3003))

class server (threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
        if (name == "servo"):
            servo.Servo(ser)
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = get_ip(sock)
        if (self.name is 'servo_read'):
            ip = "127.0.0.1"
        server_address = (ip, self.port)

        sock.bind(server_address)
        print '%s %s %s \n' % (ip, self.port, self.name)

        servo_exec = None

        while True:
            data, addr = sock.recvfrom(1024)
            print self.port

            # JSON Info
            print(data)
            info = json.loads(data)
            print datetime.datetime.now().time()
            if (self.name is 'servo'):
                #handle servo data in seperate thread
                # { 'timestamp': aabbccxxyyzz, 'angle': 300  }
        
                if (servo_exec is None or (servo_exec is not None and not servo_exec.is_alive())):
                    if (info["angle"] is not 0):
                        servo_exec = threading.Thread(target=servo.Servo.tilt, args=(info["angle"], info["motor"], ))
                    else:
                        servo_exec = threading.Thread(target=servo.Servo.stop, args=())
                    servo_exec.start()
            elif (self.name is 'servo_read'):
                servo_data[0] = info["servo"][0]
                servo_data[1] = info["servo"][1]
                servo_data[2] = info["servo"][2]
                # sock_d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # sock_d.sendto("{\"servo\": [" + str(servo_data[0]) + "," + str(servo_data[1]) + "," + str(servo_data[2]) + "]}", CLIENT_ADDR)
                print("{\"servo\": [" + str(servo_data[0]) + "," + str(servo_data[1]) + "," + str(servo_data[2]) + "]}")


def get_ip(sock):
    ip = "10.22.63.8"
    return ip

servo_server = server(1, "servo", 3000)
servo_read_server = server(4, "servo_read", 3003)
servo_poll = poll(2, "servo_poll", 3004)

servo_server.daemon = True
servo_read_server.daemon = True
servo_poll.daemon = True

# Running on seperate thread
servo_read_server.start()
servo_poll.start()
# Running on seperate thread
servo_server.run()
    

