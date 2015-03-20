import socket
import sys
import struct
import fcntl
import array
import threading
import time
import json
import multiprocessing
import datetime

import servo.servo as servo
import peltier.peltier as peltier

servo = ["", ""]
accel_gyro = ["", ""]

class server (threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port
        peltier.Peltier.init()
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        ip = 0

        interfaces = get_interfaces(sock)
        for interface in interfaces:
            if interface[0] is 'eth0' or 'wlan0':
                ip = interface[1]

        server_address = (ip, self.port)

        sock.bind(server_address)
        print '%s %s %s \n' % (ip, self.port, self.name)

        servo_exec = None 
        peltier_exec = None

        while True:
            data, addr = sock.recvfrom(1024)
            print data
            print self.port

            # JSON Info
            info = json.loads(data)
            print datetime.datetime.now().time()
            if (self.name is 'servo'):
                #handle servo data in seperate thread
                # { 'timestamp': aabbccxxyyzz, 'angle': 300  }
    
                if (servo_exec is None or (servo_exec is not None and not servo_exec.is_alive())):
                    if (info["angle"] is not 0):
                        servo_exec = threading.Thread(target=servo.Servo.tilt, args=(info["angle"], "finger", ))
                    else:
                        servo_exec = threading.Thread(target=servo.Servo.stop, args=())
                    servo_exec.start()
            elif (self.name is 'peltier'):
                # { 'timestamp': aabbccxxyyzz, 'temperature': 5 }
                if (peltier_exec is None or (peltier_exec is not None and not peltier_exec.is_alive())):
                    if (info["temperature"] > 0):
                        peltier_exec = threading.Thread(target=peltier.Peltier.hot, args=())
                    elif (info["temperature"] == 0):
                        peltier_exec = threading.Thread(target=peltier.Peltier.stop, args=())
                    else:
                        peltier_exec = threading.Thread(target=peltier.Peltier.cold, args=())
                    peltier_exec.start()
            elif (self.name is 'servo_send'):



def format_ip(ip):
    return str(ord(ip[0])) + '.' \
            + str(ord(ip[1])) + '.' \
            + str(ord(ip[2])) + '.' \
            + str(ord(ip[3]))

def get_interfaces(sock):
    total_bytes = 256 * 32;
    interface_info = array.array('B', '\0' * total_bytes)
    output_bytes = struct.unpack('iL', fcntl.ioctl(
       sock.fileno(),
       0x8912,
       struct.pack('iL', total_bytes, interface_info.buffer_info()[0])
    ))[0]

    interfaces = []

    str_interface_info = interface_info.tostring()

    for i in range (0, output_bytes, 32):
        name = str_interface_info[i:i+32].split('\0', 1)[0]
        ip = str_interface_info[i+20:i+24] 
        interfaces.append((
            name,
            format_ip(ip)
        ))

    return interfaces


servo_server = server(1, "servo", 3000)
peltier_server = server(2, "peltier", 3001)
servo_send_server = server(3, "servo_send", 3002)
servo_server.daemon = True
peltier_server.daemon = True
servo_send_server.daemon = True

# Running on seperate thread
servo_server.start()
# Running on main thread
peltier_server.run()


