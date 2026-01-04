#############################################################################
# Application : M100Link                                                    #
#  * Send and receive data over serial from your beloved                    # 
#    TRS-80 Model 100/102                                                   #
#                                                                           #
# File: M100Link.py                                                         #
# Author      : Retro And Gaming (2026)                                     #
# Date        : 11:02 01.03.26                                              #
#############################################################################
#                                                                           #
# https://github.com/Warshi7819/M100Link                                    #
#                                                                           #
#############################################################################

# Python modules
import serial
import serial.tools.list_ports
import time
import os
import os.path

# Own modules

# 3rd Party modules

############################################################################

class M100Link:
	def __init__(self):
		"""
		Constructor - set some default parameters. These are tuned for my TRS-80 Model 100, 
		your mileage may vary. If you loose data in transfer, try reducing chunkSize and/or
		increasing pauseBetweenChunk
		"""
		# Chunk size for sending and receiving data
		self.chunkSize = 20
		# Pause between sending and receiving chunks in seconds	
		self.pauseBetweenChunk = 0.1
		# Set Default value for connection string
		self.connectionString = "58N1E"
		# Set Default value for xon/xoff
		self.xonXoffEnabled = True

	def getAvailableComPorts(self):
		""" 
		Get a list of available COM	ports, empty list returned if none found
	
		Arguments:
			None
		Returns:
			list of available COM ports
		"""
		ports = serial.tools.list_ports.comports()
		return ports

	def setConnectionString(self, connStr):
		"""
		Set the connection string to be used for serial communication
		Arguments:
			connStr - connection string e.g. 88N1E
		Returns:
			None
		"""
		# validation by parsing it
		self.parseConnectionString(connStr)
		# Seems ok, set new value
		self.connectionString = connStr

	def parseConnectionString(self, connStr):
		"""
		Parse a connection string into its components and verify correctness
		Arguments:
			connStr - connection string e.g. 88N1E
		Returns:
			dictionary with connection parameters
		"""
		if len(connStr) != 5:
			raise ValueError("Connection string must be exactly 5 characters long")

		# Baud rate lookup table
		baudLookup = {
			'1': 75,
			'2': 110,
			'3': 300,
			'4': 600,
			'5': 1200,
			'6': 2400,
			'7': 4800,
			'8': 9600,
			'9': 19200
		}

		baudChar, wordChar, parityChar, stopChar, xonxoffChar = connStr
		# Decode each field
		baudRate = baudLookup.get(baudChar)
		if baudRate is None:
			raise ValueError(f"Invalid baud rate code: {baudChar}")
		if wordChar not in ('7', '8'):
			raise ValueError(f"Invalid word size: {wordChar}")
		wordSize = int(wordChar)
		if parityChar not in ('E', 'O', 'N', 'I'):
			raise ValueError(f"Invalid parity: {parityChar}")
		parity = parityChar
		if stopChar not in ('1', '2'):
			raise ValueError(f"Invalid stop bits: {stopChar}")
		stopBits = int(stopChar)
		if xonxoffChar not in ('E', 'D'):
			raise ValueError(f"Invalid XON/XOFF flag: {xonxoffChar}")
		xonxoffEnabled = (xonxoffChar == 'E')
		return {
			"baudRate": baudRate,
			"wordSize": wordSize,
			"parity": parity,
			"stopBits": stopBits,
			"xonXoffEnabled": xonxoffEnabled
		}
	
	def getStringChunks(self, content, chunkSize):
		"""
		Split a string into chunks of specified size
		
		Arguments:
			string - input string
			chunkSize - size of each chunk
		Returns:
			list of string chunks
		"""
		chunks = []
		while len(content) > chunkSize: 
			chunks.append(content[:chunkSize])
			content = content[chunkSize:]

		if len(content) > 0:
			chunks.append(content)

		return chunks
	
	def openSerialPort(self, port):
		"""
		Open the specified serial port
	
		Arguments:
			port - string specifying the port to open (e.g. on Windows 'COM3' or Unix '/dev/ttyUSB0')
		Returns:
			serial port object
		"""
		print("Using connection string: " + self.connectionString)
		connParams = self.parseConnectionString(self.connectionString)

		self.xonXoffEnabled = connParams["xonXoffEnabled"]

		print("Opening port: " + port + "...")
		s = serial.Serial()
		s.port=port
		s.baudrate=connParams["baudRate"]
		if connParams["wordSize"] == 7:
			s.bytesize = serial.SEVENBITS
		else:
			s.bytesize = serial.EIGHTBITS
		if connParams["stopBits"] == 1:
			s.stopbits = serial.STOPBITS_ONE
		else:
			s.stopbits = serial.STOPBITS_TWO
		if connParams["parity"] == 'E':
			s.parity = serial.PARITY_EVEN
		elif connParams["parity"] == 'O':
			s.parity = serial.PARITY_ODD
		elif connParams["parity"] == 'N':
			s.parity = serial.PARITY_NONE
		else:
			# I for Ignore is left but not supportet by lib. setting to None
			# and hoping for the best
			s.parity = serial.PARITY_NONE

		if self.xonXoffEnabled:
			s.xonxoff = 1
		else:
			s.xonxoff = 0
		
		s.timeout=0
		s.open()	

		return s

	def sendFile(self, filePath, comPort):
		"""
		Send a file over the specified serial port

		Arguments:
			filePath - path to the file to send
			serialPort - serial port object
		Returns:
			None
		"""
		print("Opening serial port...")
		serialPort = self.openSerialPort(comPort)

		print("Preparing file for transmission...")
		# Read the entire file into memory, usually not a problem for small trs-80 files
		fp = open(filePath, 'r')
		content = fp.read()
		fp.close()

		# replace all newlines by linefeeds
		content = content.replace("\n", "\r")
		if self.xonXoffEnabled:
			# Signal EOF by adding \x1A - The Ascii control char "SUB" or "Ctrl+Z"
			content = content + "\x1A"

		# Relax sending, a few chars at a time with some delay
		chunks = self.getStringChunks(content, self.chunkSize)
		print("Sending...")
		for chunk in chunks:
			print(f"Sending chunk: " + chunk)
			out = chunk.encode('ascii')
			serialPort.write(out)
			time.sleep(self.pauseBetweenChunk)
		

		serialPort.flush()
		print("Finalizing. Waiting 2 seconds...")
		time.sleep(2)
		serialPort.close()
		print("Done")

	def receiveFile(self, filePath, comPort):
		"""
		Receive a file over the specified serial port
	
		Arguments:
			filePath - path to save the received file
			serialPort - serial port object
		Returns:
			None
		"""
		print("Opening serial port...")
		serialPort = self.openSerialPort(comPort)
		# Bussy waiting to see if data becomes available over serial
		print("Waiting for transmission...")
		data = serialPort.read(self.chunkSize)
		while (len(data) == 0):
			data = serialPort.read(self.chunkSize)
		
		print("Receiving...")
		content = ""

		while (len(data) != 0):
			# Replace all line feeds to new lines
			received = data.decode("ascii").replace("\r", "\n")
			if self.xonXoffEnabled:
				# Remove the EOF char \x1A if present in current chunk
				received = received.replace("\x1A", "")
			content += received
			time.sleep(self.pauseBetweenChunk)
			data = serialPort.read(self.chunkSize)
	
		# Write it to disk
		fp = open(filePath, 'w')
		fp.write(content)
		fp.flush()
		fp.close()