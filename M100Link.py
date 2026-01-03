import serial
import serial.tools.list_ports
import time
import os
import os.path

class M100Link:
	
	"""
	Constructor
	"""
	def __init__(self):
		pass

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
		# Read the entire file into memory
		fp = open(filePath, 'r')
		content = fp.read()
		fp.close()

		# replace all newlines by linefeeds
		content = content.replace("\n", "\r")
		# Add the TRS-80's EOF
		content = content + "\x1A"

		# Relax sending, 100 chars at a time with some delay
		chunks = self.getStringChunks(content, 10)
		print("Sending...")
		for chunk in chunks:
			print(f"Sending chunk: " + chunk)
			out = chunk.encode('ascii')
			serialPort.write(out)
			time.sleep(1)
		

		serialPort.flush()
		print("Finalizing. Waiting 5 seconds...")
		time.sleep(5)
		print("Done")
		serialPort.close()


	"""
	Receive a file over the specified serial port
	
	Arguments:
		filePath - path to save the received file
		serialPort - serial port object
	Returns:
		None
	"""
	def receiveFile(self, filePath, serialPort):
		# We poll the serial line to detect a transmission
		print("Waiting for transmission...")
		data = serialPort.read(1)
		while (len(data) == 0):
			data = serialPort.read(1)
		
		print("Receiving...")
		content = ""

		while (len(data) != 0):
			# Replace all line feeds to new lines
			received = data.decode("ascii").replace("\r", "\n")
			# Remove the TRS-80's EOF
			received = received.replace("\x1A", "")
			content += received
			time.sleep(0.1)
			data = serialPort.read(100)
	
		# Write it to disk
		fp = open(filePath, 'w')
		fp.write(content)
		fp.flush()
		fp.close()


if __name__ == "__main__":
	link = M100Link()
	fileToSend = os.path.join(os.getcwd(), "alien.ba")
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


