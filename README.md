![M100Link Logo](https://github.com/Warshi7819/M100Link/blob/main/images/logo_arrows_small.png) ![M100Link](https://github.com/Warshi7819/M100Link/blob/main/images/M100Link.png)

## Overview
This program enables you to transfer text files (and Basic programs) to and from your TRS-80 model 100 over serial.

Needed equipment:
* A TRS-80 Model 100/102 would be nice
* A modern PC or Laptop with USB 
* A USB to Serial Adapter
* A Null modem cable (DB9) because you gotta twist those wires. Buy one or create your own: http://www.cncsnw.com/NullMdm.htm
* A DB9 to DB25 adapter - unless you by some magic ended up with a null modem cable that has DB9 on one end and DB25 on the other. 

## Before we start
On your modern computer - Ensure that you have Python3 installed and that you have downloaded the following files from this project and placed them in a folder of your choice:
* M100Link.py
* Send.py
* Receive.py

## Transfering Text files (.DO) To Your TRS-80 Model 100
Hook up your TRS-80 Model 100 to your computer using the USB to serial adapter, Null modem cable and a DB9 to DB25 adapter. 

### On your TRS-80 Model 100
You will have to prepare the TRS-80 Model 100 to be able to receive a file. 

* Start the TELECOM program
* Type the folowing followed by hitting the ENTER key: STAT 58N1E
* Hit the F4 key to start listening
* Hit F2 to prepare for download, enter a name for the file (without ending, max 6 chars). Hit ENTER

### On your modern computer
The program you will use to send a file to your TRS-80 Model 100 is: Send.py

The program will by default use the "connection string" 58N1E and the first available COM port it finds. Thus if you only have one COM port available it should be as easy as:
**python Send.py --file FileNameHere**

To see all arguments supported type python **Send.py -h**
```
python .\Send.py -h
usage: Send.py [-h] --file FILE [--port PORT] [--stat STAT]

Utility to send a file to your TRS-80 Model 100/102.

options:
  -h, --help   show this help message and exit
  --file FILE  Path to the file to be sent.
  --port PORT  Serial port to use for sending data (e.g., COM3 or /dev/ttyUSB0). If parameter not specified default port will be the first one
               found on the system.
  --stat STAT  Serial connection string e.g. 58N1E. If parameter not specified default 58N1E will be used.

Example: python Send.py --file test.txt
```

## Transfering Text files (.DO) To Your Modern Computer
Hook up your TRS-80 Model 100 to your computer using the USB to serial adapter, Null modem cable and a DB9 to DB25 adapter. 


## Transfering Basic files (.BA)
Same as for text files. Whatever you do you end up with a file with the .DO ending. So after you have transfered that BASIC program as a text file you'll have to go into BASIC to "rename" it from *.DO to a *.BA (basic) file. Let's assume you downloaded a file and named it XYZ. This means that you now have a file called XYZ.DO in the file list on the main menu. 

To copy it to a .BA file go into BASIC and type the following:

```
LOAD"XYZ.DO
SAVE"XYZ.BA
```

Then exit basic (F8). Back at the main menu you should now see both a XYZ.DO file and a XYZ.BA file. Select the XYZ.BA file and execute it by pressing the ENTER key. 

> [!NOTE]
> To delete a file e.g. the XYZ.DO file go into BASIC and type: KILL "XYZ.DO

> [!NOTE]
> If you want to transfer at BA file from your TRS-80 Model 100 to your modern computer you probably have to rename it to .DO first.


