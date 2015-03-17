from time import sleep
import servo.servo as servo

#servo.Servo.tilt(180,"finger")
#sleep(2)
#servo.Servo.stop("finger")
#sleep(2)
servo.Servo.tilt(0,"finger")
sleep(2)
servo.Servo.stop("finger")
