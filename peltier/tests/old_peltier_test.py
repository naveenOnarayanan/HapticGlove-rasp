import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 22
Motor1B = 21
Motor1E = 18
LED1 = 8

GPIO.setup(LED1,GPIO.OUT)

 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

print "LED"
GPIO.output(LED1,GPIO.LOW)
 
print "Turning motor on"
GPIO.output(Motor1A,GPIO.HIGH)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)
 
sleep(15)
GPIO.output(Motor1E,GPIO.LOW)
sleep(2)

print "Turning motor on opposite"
GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.HIGH)
GPIO.output(Motor1E,GPIO.HIGH)

sleep(10)
 
print "Stopping motor"
GPIO.output(Motor1E,GPIO.LOW)
sleep(2)


