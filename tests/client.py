import socket
import sys
import datetime
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('172.31.206.241', 3000)
server_address_2 = ('172.31.206.241', 3001)

try:
    print datetime.datetime.now().time()
    message = '{"timestamp": 1404330711, "angle": 180}'
    print>>sys.stderr, 'sending %s' % message
    sock.sendto(message, server_address)
    sleep(2)
    message = '{"timestamp": 1404330711, "angle": 0}'
    print>>sys.stderr, 'sending %s' % message
    sock.sendto(message, server_address)
    sleep(2)
    message = '{"timestamp": 1404330711, "temperature": 10}'
    print>>sys.stderr, 'sending %s' % message
    sock.sendto(message, server_address_2)
    sleep(2)
    message = '{"timestamp": 1404330711, "temperature": -10}'
    print>>sys.stderr, 'sending %s' % message
    sock.sendto(message, server_address_2)
    sleep(2)
    message = '{"timestamp": 1404330711, "temperature": 0}'
    print>>sys.stderr, 'sending %s' % message
    sock.sendto(message, server_address_2)

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

