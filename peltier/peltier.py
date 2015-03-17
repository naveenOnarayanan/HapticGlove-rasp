import RPi.GPIO as GPIO

class Peltier:
	@staticmethod
	def init():
		GPIO.setmode(GPIO.BOARD)
		# warm
		GPIO.setup(22,GPIO.OUT)
		# cool
		GPIO.setup(24,GPIO.OUT)
		#enable 
		GPIO.setup(18,GPIO.OUT)

	@staticmethod
	def hot():
		print("hot")
		GPIO.output(22,GPIO.HIGH)
		GPIO.output(24,GPIO.HIGH)
		GPIO.output(18,GPIO.LOW)

	@staticmethod
	def cold():
		print("cold")
		GPIO.output(22,GPIO.LOW)
		GPIO.output(24,GPIO.HIGH)
		GPIO.output(18,GPIO.HIGH)

	@staticmethod
	def stop():
		print("stop")
		GPIO.output(22,GPIO.LOW)
		GPIO.output(24,GPIO.LOW)
		GPIO.output(18,GPIO.LOW)
		
                
