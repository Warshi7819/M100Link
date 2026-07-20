![M100Link Logo](https://github.com/Warshi7819/M100Link/blob/main/images/logo_arrows_small.png) ![M100Link](https://github.com/Warshi7819/M100Link/blob/main/images/M100Link.png)

## Overview
This program enables you to transfer text files (and Basic programs) to and from your TRS-80 model 100 (presumably also the 102) over serial.

Needed equipment:
* A TRS-80 Model 100(/102) would be nice
* A modern PC or Laptop with USB 
* A USB to Serial Adapter
* A Null modem cable (DB9) because you gotta twist those wires. Buy one or create your own: http://www.cncsnw.com/NullMdm.htm
* A DB9 to DB25 adapter - unless you by some magic ended up with a null modem cable that has DB9 on one end and DB25 on the other.

When everything is hooked up it should look something like this:
![Cables](https://github.com/Warshi7819/M100Link/blob/main/images/cables.png)

## Before we start
On your modern computer - Ensure that you have Python3 installed (including the extra module pyserial) and that you have downloaded the following files from this project and placed them in a folder of your choice:
* M100Link.py
* ProgressBar.py
* Send.py
* Receive.py

> [!NOTE]
> As part of the release (right hand side) I have also included frozen binaries for Windows: Receive.exe and Send.exe that will enable you to use this without installing python. The binaries are created by using PyInstaller. 

## Transfering Text files (.DO) To Your TRS-80 Model 100
Hook up your TRS-80 Model 100 to your computer using the USB to serial adapter, Null modem cable and a DB9 to DB25 adapter. 

### On your TRS-80 Model 100
You will have to prepare the TRS-80 Model 100 to be able to receive a file. 

* Start the TELCOM program
* Type the folowing followed by hitting the ENTER key: STAT 58N1E
* Hit the F4 key to start listening
* Hit F2 to prepare for download, enter a name for the file (without ending, max 6 chars). Hit ENTER

### On your modern computer
The program you will use to send a file to your TRS-80 Model 100 is: Send.py

The program will by default use the "connection string" 58N1E and the first available COM port it finds. Thus if you only have one COM port available it should be as easy as:
**python Send.py --file FileNameHere**

The program will now send the file to your TRS-80 Model 100 and exit when done.

To see all arguments supported type **python Send.py -h**
```
python .\Send.py -h
usage: Send.py [-h] --file FILE [--port PORT] [--stat STAT]

Utility to send a file to your TRS-80 Model 100/102.

options:
  -h, --help   show this help message and exit
  --file FILE  Path to the file to be sent.
  --port PORT  Serial port to use for sending data (e.g., COM3 or /dev/ttyUSB0). If parameter not specified default port will
               be the first one found on the system.
  --stat STAT  Serial connection string e.g. 58N1E. If parameter not specified default 58N1E will be used.

Example: python Send.py --file test.txt
```
### Back On your TRS-80 Model 100
If everything worked you will have seen text fly by on your TRS-80 Model 100 as everything is echoed to the screen itself even though it also ends up in the specified file. 

To Exit to the main menu:
* Hit F8
* Answer Y to the “Disconnect?” question and hit ENTER
* Press F8 again and you’ll be back at the main menu.

You should see the newly transferred file in the file list here with the file ending .DO.

## Transfering Text files (.DO) To Your Modern Computer
Hook up your TRS-80 Model 100 to your computer using the USB to serial adapter, Null modem cable and a DB9 to DB25 adapter. 

### On your modern computer
The program you will use to receive a file from your TRS-80 Model 100 is: Receive.py

The program will by default use the "connection string" 58N1E and the first available COM port it finds. Thus if you only have one COM port available receiving a file should be as easy as:
**python Receive.py --file FileNameHere**

The program will now await transfer of a file from your TRS-80 Model 100 and exit when file is recevied.

To see all arguments supported type **python Receive.py -h**
```
python .\Receive.py -h
usage: Receive.py [-h] --file FILE [--port PORT] [--stat STAT]

Utility to receive a file from your TRS-80 Model 100/102.

options:
  -h, --help   show this help message and exit
  --file FILE  Filename to save in current directory.
  --port PORT  Serial port to use for receiving data (e.g., COM3 or /dev/ttyUSB0). If parameter not specified default port
               will be the first one found on the system.
  --stat STAT  Serial connection string e.g. 58N1E. If parameter not specified default 58N1E will be used.

Example: python Receive.py --file test.txt
```

### On your TRS-80 Model 100
Once you have started Receive.py as explained above you must now initiate the file transfer from this side. 

* Start the TELCOM program
* Type the folowing followed by hitting the ENTER key: STAT 58N1E
* Hit the F4 key to start listening
* Hit F3 to prepare for upload, enter the name of the file to upload (without ending, max 6 chars). Hit ENTER
* When asked for “Width:” type nothing, just hit ENTER

When the Receive.py program exits the file has been received on your modern computer. 

To get back to the main menu on your TRS-80 Model 100:
*	Hit F8
*	Answer Y to the “Disconnect?” question and hit ENTER
*	HIT F8

## Transfering Basic files (.BA) To Your TRS-80 Model 100
This is the same as for transfering text files. All files you receive on your TRS-80 model 100 will have the file ending .DO. This means that if you are actually sending a BASIC program you will have to go into BASIC to "rename" it from *.DO to a *.BA file to be able to execute it from the main menu. Let's assume you downloaded a file and named it **XYZ**. This means that you now have a file called **XYZ.DO** in the file list on the main menu. 

To "copy" it to a .BA file go into BASIC and type the following:

```
LOAD"XYZ.DO
SAVE"XYZ.BA
```

> [!NOTE]
> The process of first loading the .DO file and then saving it to .BA is actually converting the ASCII file to a binary format. When you use LOAD, the BASIC interpreter “tokenizes” the program to make it runnable and take less space.

Then exit basic (F8). Back at the main menu you should now see both a XYZ.DO file and a **XYZ.BA** file. Navigate to the XYZ.BA file and execute it by pressing the ENTER key. 

If you just want to load the XYZ.DO file in basic and run the program from there you don't need to rename it first. Just enter BASIC and:

```
LOAD"XYZ.DO
RUN
```

> [!NOTE]
> To delete a file e.g. the XYZ.DO file go into BASIC and type: KILL "XYZ.DO

> [!NOTE]
> If you want to transfer at BA file from your TRS-80 Model 100 to your modern computer you have to save it to .DO first. If not you will get a **No File. Upload Aborted.** error. If you have both a XYZ.DO and a XYZ.BA file on your machine it will choose to upload the **XYZ.DO** file.

> [!NOTE]
> You may also load a program in binary format .BA or ascii .DO directly from the BASIC interpreter over serial and execute it when done by issuing the command: **LOAD "COM:58N1E",R**
> 
> Once a program is loaded you can also of course save it as a RAM file using the **SAVE "filename"** command. If you want to save the program as pure ASCII you can use the **SAVE "filename",A** command. Where the trailing ,A specified exactly that.  

## Screenshot
![Action Photo](https://github.com/Warshi7819/M100Link/blob/main/images/example_usage.png)


## Demystifying The Connection String
88N1E you say?

As you saw above the TRS-80 uses the STAT command and a five character long string to specify the connection settings. But what does it all mean?
These five individual characters are used to define:
* Char 1: The baud rate (1 = 75, 2 = 110, 3 = 300, 4 = 600, 5 = 1200, 6 = 2400, 7 = 4800, 8 = 9600, 9 = 19200)
* Char 2: The size of the word (byte) in bits (7 or 8 bit)
* Char 3: The parity bit used for error checking (E for even, O for odd, N for none, I for ignore)
* Char 4: The number of stop bits (1 or 2)
* Char 5: Whether XON/XOFF is enabled (E) or disabled (D).

The default connection string in our program is **58N1E**. This then means:
* A Baud rate of 1200
* The word (byte) size is set to 8 bits
* None parity bit
* 1 stop bit
* XON/XOFF Enabled 

> [!NOTE]
> The connection string must be the same on both your modern computer and your TRS-80 Model 100 or there will be trouble. I set the baud rate to 1200 after getting into trouble with higher speeds. If you still have issues try to set it to e.g. 600. 

## BUT BUT.. What about REAL programs? .CO Files?
My program does not handle .CO files as they are a bit tricky. The easiest way to transfer programs written in machine language I have found is to use a tiny program called TEENY on your TRS-80 model 100 and a PTDD Emulator on your modern computer (PTDD = Portable Tandy Disk Drive). But there's a slight bootstrapping problem as TEENY is a .CO program as well! To install TEENY you need to follow these super simple steps:
* Download the [Teeny](https://github.com/bkw777/dl2/blob/master/clients/teeny/TEENY.100) bootstrap BASIC script. Once downloaded, send it over to your TRS-80 Model 100 just like it was a .DO file, load it in basic and run it. Select the default (just hit Enter) when asked difficult question.
* Once downloaded you will have to re-configure where HIGH MEMORY starts. First we need to figure out the correct number.
* Enter **?HIMEM:CALL9643**. This will output a bunch of numbers but we are only concerned about the number labeled Top: xxxxx number. For me this was **62213** but yours might differ.
* To set the new High Memory start location you enter **CLEAR0,TopNumber**. In my case this was: **CLEAR0,62213**
* You may now start the TEENY.CO program you have installed from the main menu.

At this point you are ready on the TRS-80 Model 100 side of things but there's nothing running on your modern computer yet that TEENY can talk to over serial. You will now have to install a PTDD emulator on you modern computer. Since I like python, and I found a PTDD emulator written in Python, the only one I have actually testet is [MCOMM](https://club100.org/memfiles/index.php?&direction=&order=&directory=Kurt%20McCullum/mComm%20Python). Unpack the .deb package (using 7zip) and find the files you need namely mcomm.py and tpdd.py. It has some flaws on windows but starts up nicely as long as you supply the path it should serve out files from. 

The following command will start it up and serve the files in the current directory: **python .\mcomm.py --path .** Once started you can head over to your TRS-80 model 100 and start using TEENY to download files served out by your modern computer. And yes, this also includes support for downloading .CO files.

> [!NOTE]
> Using TEENY is as simple as it gets.
> * To QUIT the program Enter: Q
> * To Download a file called FILE.DO Enter: L FILE.DO
> * To Upload a file called FILE.DO Enter: S FILE.DO
> * To Kill/Destroy/Terminate a file called FILE.DO Enter: K FILE.DO

Other TPDD Emulators that get's talked about more than this one (but I haven't tested yet) can be found [here](http://tandy.wiki/TPDD_server)

## OTHER HIGHLY RELEVANT INFO
I just like to tinker and it turns out that there are a lot of people like me. 99% of them seems to be active and part of the M100 mailing list: [Mailing List And Archive](http://lists.bitchin100.com/listinfo.cgi/m100-bitchin100.com). There's also a huge archive there that you can search through as soon as you have joined (free of charge). 

A wealth of knowledge can also be found on the Club100 [webpage](http://www.club100.org/) although it can be bit retro and hard to navigate at times.
