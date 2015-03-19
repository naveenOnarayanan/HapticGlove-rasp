import serial
import time
import ipdb

# can be easily replaced with a file name for testing without servos
ser = serial.Serial('/dev/ttyACM0', 9600)
#ser = open("servo_output.txt", "w")

# tested and functional
def add_zeros_to_int(int_val):
	if(len(str(int_val)) == 1):
		return "00" + str(int_val)
	elif(len(str(int_val)) == 2):
		return "0" + str(int_val)
	else:
		return str(int_val)

def send(motor_hash, ser):
	item_count = 0
	for motor, pos in last_sent.iteritems():
		if motor in motor_hash:
			ser.write("%s:%s" 
				%(
					servo_table[motor],
					add_zeros_to_int(motor_hash[motor])
				)
			)
		else:
			ser.write("%s:%s" 
				%(
					servo_table[motor],
					add_zeros_to_int(pos)
				)
			)

		if(item_count < 2):
			ser.write(",")
		item_count += 1
	ser.write("\n")

# todo:
# make sure you're throwing the proper error
# figure out how to keep the `last_sent` in your class

happy_test_vals = [{"finger":20}, {"finger":3, "thumb":4}, {"finger":180, "under":0}, {"finger":0, "under":180, "thumb":90}, {"finger":900, "under":900, "thumb":900}]
error_test_vals = [{"finger":180, "under":180}, {"finger":180, "under":180, "thumb":90}, {"finger":0, "under":180, "thumb":90, "dicks":20}]

last_sent = {"finger":0, "thumb":0, "under":180}
servo_table = {"finger":0, "thumb":1, "under":2}

for test_val in happy_test_vals:
	time.sleep(3)
	send(test_val, ser)