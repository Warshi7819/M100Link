#############################################################################
# Application : M100Link                                                    #
#  * Send and receive data over serial from your beloved                    # 
#    TRS-80 Model 100/102                                                   #
#                                                                           #
# File: Send.py                                                             #
# Author      : Retro And Gaming (2026)                                     #
# Date        : 10:29 01.04.26                                              #
#############################################################################
#                                                                           #
# https://github.com/Warshi7819/M100Link                                    #
#                                                                           #
#############################################################################

# Python modules
import argparse

# Own modules
from M100Link import M100Link

# 3rd Party modules

############################################################################

class Send:
    def __init__(self):
        """
        Constructor
        """
        pass

    def getArgumentParser(self):
        """
        Create and return the argument parser
        Arguments:
            None
        Returns:
            ArgumentParser object
        """
        parser = argparse.ArgumentParser(
            description="Utility to send a file to your TRS-80 Model 100/102.",
            epilog="Example: python Send.py --file test.txt"
        )

        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to the file to be sent."
        )

        parser.add_argument(
            "--port",
            type=str,
            required=False,
            help="Serial port to use for sending data (e.g., COM3 or /dev/ttyUSB0). If parameter not specified default port will be the first one found on the system."
        )

        parser.add_argument(
            "--stat",
            type=str,
            required=False,
            help="Serial connection string e.g. 58N1E. If parameter not specified default 58N1E will be used."
        )
        return parser

"""
Main program entry point
"""
if __name__ == "__main__":
    sender = Send()
    parser = sender.getArgumentParser()

    # Parse the arguments
    args = parser.parse_args()

    fileToSend = args.file
    port = ""

    print(f"File to send: {fileToSend}")
    if args.port:
        port = args.port        
        print(f"Using port: {port}")

    link = M100Link()
    if port == "":
        availablePorts = link.getAvailableComPorts()
        if len(availablePorts) == 0:
            print("No COM ports found, exiting.")
            exit(1)
        else:
            print("Available COM ports:")
            for port in availablePorts:
                print(f" - {port.device}: {port.description}")
            
            port = availablePorts[0].device
            print(f"\n\nNo port specified, using first available port: {port}") 

    # If supplied, override default connection string
    if args.stat:
        link.setConnectionString(args.stat)

    link.sendFile(fileToSend, port)