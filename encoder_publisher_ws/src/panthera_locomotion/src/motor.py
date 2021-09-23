import serial
import time
import keyboard
import math
import serial.tools.list_ports

class RoboteqMotor():
	# 12rpm = 133 units
	def __init__(self, serialnumber, name):
		self.sn = serialnumber
		self.name = name
		self.dir = {'lb': 1, 'rb': 2, 'lf': 3, 'rf': 4}
		p = list(serial.tools.list_ports.grep(self.sn))
		self.port = '/dev/' + p[0].name
		self.ser = serial.Serial(self.port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

		self.wheel_diamter = 0.36
		self.ratio = 1000
		self.initialize()
		self.once = 0

	def initialize(self):
		self.ser.write("# c\r\n")                      # Clear buffer
		self.ser.write("?CB\r\n")                      # select CB for hall sensor or C for encoder
		#self.ser.write("# 10\r\n")                     # read data every 10ms
		#self.ser.write("!CB 1 0_!CB 2 0\r\n")
		#self.ser.write("^BPOL 1 3\r\n")
		self.ser.write("^VAR 1 {}\r\n".format(self.dir[self.name]))
		#self.ser.write("!EES\r\n")
		#self.ser.write("!EELD\r\n")


	def writeSpeed(self, rpm):
		# 16 units = 1 rpm
		'''
		if self.once == 0:
			self.ser.write("?VAR 1\r\n")
			ln = self.ser.read(32).split('\r')
			for i in ln:
				if "VAR=" in i:
					print(i)
					self.once += 1
					break
		'''
		speed = rpm * 15.8
		self.ser.write("!G {}\r\n".format(str(speed)))
		ln = self.ser.read(16).split('\r')
		#print(ln)

	def speed_to_rps(self, speed):
		return speed/self.wheel_diamter

	def readCurrent(self):
		self.ser.write("?AC 1\r")
		rpm = self.ser.read(1000)
		print(rpm)

	def writeAcc(self, acc):
		# increase motor spped by 0.1* rpm per s
		# acc is in motor units
		self.ser.write("!AC 1 {}\r".format(str(acc)))

	def e_stop(self):
		self.ser.write("!EX\r")

	def set_mode(self, mode):
		if mode == 0:
			print("open loop mode")
		elif mode == 1:
			print("closed-loop speed mode")
		elif mode == 5:
			print("closed-loop torque mode")
		self.ser.write("^MMOD {}\r".format(str(mode)))
		self.ser.write("?TRQ\r")
		t = str(self.ser.readline())
		for i in t:
			print(I)
		print(t)

	def set_torque(self, data):
		self.ser.write("!GIQ 1 {}\r".format(str(data*10)))

	def torque_const(self, data):
		self.ser.write("^TNM 1 1523\r") 

	def read(self):
		self.ser.read(1000)

	def custom_write(self, msg):
		self.ser.write(msg + "\r")