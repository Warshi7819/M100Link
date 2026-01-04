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
	
	"""
	Constructor - set some default parameters. These are tuned for my TRS-80 Model 100, 
	your mileage may vary. If you loose data in transfer, try reducing chunkSize and/or
    increasing pauseBetweenChunk
	"""
	def __init__(self):
		# Chunk size for sending and receiving data
		self.chunkSize = 10
		# Pause between sending and receiving chunks in seconds	
		self.pauseBetweenChunk = 0.1

	""" 
	Get a list of available COM	ports, empty list returned if none found
	
	Arguments:
		None
	Returns:
		list of available COM ports
	"""
	def getAvailableComPorts(self):
		ports = serial.tools.list_ports.comports()
		return ports

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
	
	"""
	Open the specified serial port
	
	Arguments:
		port - string specifying the port to open (e.g. on Windows 'COM3' or Unix '/dev/ttyUSB0')
	Returns:
		serial port object
	"""
	def openSerialPort(self, port):
		print("Opening port: " + port + "...")

		s = serial.Serial()
		s.port=port
		s.baudrate=9600
		s.bytesize = serial.EIGHTBITS
		s.timeout=0
		s.open()	

		return s


	"""
	Send a file over the specified serial port

	Arguments:
		filePath - path to the file to send
		serialPort - serial port object
	Returns:
		None
	"""
	def sendFile(self, filePath, comPort):

		print("Opening serial port...")
		serialPort = self.openSerialPort(comPort)

		print("Preparing file for transmission...")
		# Read the entire file into memory, usually not a problem for small trs-80 files
		fp = open(filePath, 'r')
		content = fp.read()
		fp.close()

		# replace all newlines by linefeeds
		content = content.replace("\n", "\r")
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

	"""
	Receive a file over the specified serial port
	
	Arguments:
		filePath - path to save the received file
		serialPort - serial port object
	Returns:
		None
	"""
	def receiveFile(self, filePath, serialPort):
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


if __name__ == "__main__":
	# TEST SENDING FILE
	link = M100Link()
	fileToSend = os.path.join(os.getcwd(), "test.txt")
	availablePorts = link.getAvailableComPorts()
	
	if(len(availablePorts) == 0):
		print("No COM ports available")
	else:
		print("Available COM ports:")
		for port in availablePorts:
			print(f" - {port.device}: {port.description}")
	
		# Just open the first available port - how many com ports do people have these days?
		print(f"Opening first available port: {availablePorts[0].device}")
		
		# Try sending a file
		link.sendFile(fileToSend, availablePorts[0].device)


