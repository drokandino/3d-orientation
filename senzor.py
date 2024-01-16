import smbus
import time
import redis
import math

# Init of SMBBus object
bus = smbus.SMBus(1)

# Set measurement mode to +/- 2g
bus.write_byte_data(0x1D, 0x16, 0x05)

# Wait half second to ensure that data is written to sensor
time.sleep(0.5)

# Init of Redis object
r = redis.Redis()

while True:
	# Read 6 bytes of acceleration data back from 0x00 (register address)
	# X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB
	data=bus.read_i2c_block_data(0x1D, 0x00, 6)
	
	xAcc = (data[0] | data[1] << 8)
	if xAcc > 511 :
		xAcc -= 1024
	xAcc -= 14
	xAcc = float(xAcc)
	xAcc = xAcc / 64


	yAcc = (data[2] | data[3] << 8)
	if yAcc > 511 :
		yAcc -= 1024
	
	yAcc += 19
	yAcc = float(yAcc)
	yAcc = yAcc / 64
	

	zAcc = (data[4] | data[5] << 8)
	if zAcc > 511 :
		zAcc -= 1024
	
	zAcc -= 16
	zAcc = float(zAcc)
	zAcc = zAcc / 64
	 
	
	if xAcc == 0:
		xAcc = 0.1
	if yAcc == 0:
		yAcc = 0.1
	if zAcc == 0:
		zAcc = 0.1	
	
	# Calculate roll and pitch 
    roll = math.atan(yAcc / math.sqrt(pow(xAcc, 2) + pow(zAcc, 2))) * 180 / 3.14
	pitch = math.atan(-1 * xAcc / math.sqrt(pow(yAcc, 2) + pow(zAcc, 2))) * 180 / 3.14
	
	# Write data to redis server
	r.set("x", xAcc)
	r.set("y", yAcc)
	r.set("z", zAcc)
	r.set("roll", roll)
	r.set("pitch", pitch)
		
	time.sleep(0.1)