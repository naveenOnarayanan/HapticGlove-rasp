class Servo:
	def __init__(self, ser):
		self.last_sent = {"finger":0, "thumb":0, "under":180}
		self.servo_table = {"finger":0, "thumb":1, "under":2}
		self.ser = ser

	def add_zeros_to_int(self, int_val):
		if(len(str(int_val)) == 1):
			return "00" + str(int_val)
		elif(len(str(int_val)) == 2):
			return "0" + str(int_val)
		else:
			return str(int_val)

	def send(self, motor_hash):
		item_count = 0
		for motor, pos in self.last_sent.iteritems():
			if motor in motor_hash:
				self.ser.write("%s:%s" 
					%(
						self.servo_table[motor],
						add_zeros_to_int(motor_hash[motor])
					)
				)
			else:
				self.ser.write("%s:%s" 
					%(
						self.servo_table[motor],
						add_zeros_to_int(pos)
					)
				)

			if(item_count < 2):
				self.ser.write(",")
			item_count += 1
		self.ser.write("\n")

	def tilt(self, degrees, motor = "finger"):
		if(degrees < 0 or degrees > 180):
			print("TOO FAR")
			return
		elif(motor == "bottom"):
			if(abs(self.last_value["finger"] - degrees) < 180):
				print("NO FIGHTING")
				return
		elif(motor == "finger"):
			if(abs(self.last_value["bottom"] - degrees) < 180):
				print("NO FIGHTING")
				return
		else:
			print(degrees)
			self.send({motor:degrees})

	def stop(self, motor = "finger"):
		self.send({motor:900})