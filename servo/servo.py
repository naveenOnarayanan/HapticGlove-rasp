from RPIO import PWM

class Servo:
	@staticmethod
	def tilt(degrees, motor = "finger"):
		servo = PWM.Servo()
		motors = {"finger":17, "thumb":22}
		if(degrees < 0 or degrees > 180):
			print("TOO FAR")
			return
		else:
			# because the max PWM is 400 and the minimum is 2400
			# and the max granularity is 10 microseconds
			print(degrees)
			servo.set_servo(motors[motor], 
				( 400 + int(round(2000*degrees/180/10))*10 )  
			)

	@staticmethod
	def stop(motor = "finger"):
		servo = PWM.Servo()
		motors = {"finger":17, "thumb":22}
		print("stop")
		servo.stop_servo(motors[motor])

