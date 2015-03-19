import RPi.GPIO as GPIO

class Peltier:
	@staticmethod
	def init():
		GPIO.setmode(GPIO.BOARD)
		# warm
		GPIO.setup(19,GPIO.OUT)
		# cool
		GPIO.setup(24,GPIO.OUT)
		# enable 
		GPIO.setup(12,GPIO.OUT)
		# test
		#GPIO.setup(26,GPIO.OUT)

	@staticmethod
	def hot():
		print("hot")
		GPIO.output(19,GPIO.LOW)
		GPIO.output(24,GPIO.HIGH)
		GPIO.output(12,GPIO.HIGH)
		#GPIO.output(26,GPIO.LOW)

	@staticmethod
	def cold():
		print("cold")
		GPIO.output(19,GPIO.HIGH)
		GPIO.output(24,GPIO.LOW)
		GPIO.output(12,GPIO.HIGH)
                #GPIO.output(26,GPIO.HIGH)

	@staticmethod
	def stop():
		print("stop")
		GPIO.output(19,GPIO.LOW)
		GPIO.output(24,GPIO.LOW)
		#GPIO.output(26,GPIO.HIGH)
		
                
