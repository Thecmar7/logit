#!/usr/bin/env python

# logit
'''
	Okay so I wanna make this logger application
	
	9/2/2016
	10/31/2016
''' 
import sys
import pickle 

import time
import datetime 
from datetime import date, timedelta

import os
import readline


# so I can change the output colors
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
    WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

#complete = "/usr/local/my_scripts"
# these need to become variables in the info file.
complete = "/Users/TheCmar7/Developer/python/Logit"
directory = "/logit_saves/"
infoFile = "logit_current.p"
filePath = complete + directory

#	This is if  you need to reset the current.p file
# current = { "current": "", "logs": [], count: 0, }
# pickle.dump( current, open(filePath + infoFile, "w") )

# 	helpText():
#
#	Prints out the text of  commands
def helpText( cmds ):
	for k, v in cmds.items():
		print("\t" v.cmd + " " + v.desc)
	
	
	'''
	print(	"\tlogit " + cmds.newing + " \"name\"		// creates a new log\n" +
			"\tlogit " + cmds.opening + " \"name\"			// opens\n" +
			"\tlogit " + cmds.saving + " \"name\"			// outputs the log to a txt file\n" +
			"\tlogit " + cmds.dating + " 			// date it\n" +
			"\tlogit " + cmds.listing + " 			// list out the saved logs\n" +
			"\tlogit " + cmds.outing + " 			// out current log\n" +
			"\tlogit " + cmds.outing + " \"name\"		// prints out given log\n" +
			"\tlogit \"This is a thing to log\"\n" +
			"\tlogit " + cmds.toing + " \"name\" \"this is a thing to log\"\n" +
			"\tlogit " + cmds.infoing + " 			// info about log\n" +
			"\tlogit " + cmds.starting + " 			// Starts a log console\n" +
			"\tlogit " + cmds.breaking + " 			// puts a break line \n" +
			"\tlogit " + cmds.editing + "			// Allows you to edit the log \n"+
			"\tlogit " + cmds.fromFile + "			// Allows the input from a text file")
	'''


# 	setCurrentLog ( name ):
#
# 	This sets the current log to a name 
def setCurrentLog( name ):
	workingLog = pickle.load( open(filePath + infoFile, "rb" ))
	workingLog['current'] = name
	pickle.dump( workingLog, open(filePath + infoFile, "w"))


#	newLog ( name ):
#
#	creates a new log with the name that is given 
def newLog( name ):
	workingLog = pickle.load( open(filePath + infoFile, "rb" ))
	workingLog['logs'].append(name)
	workingLog['count'] = workingLog['count'] + 1;
	pickle.dump (workingLog, open(filePath + infoFile, "wb"))

	print("created a new log: " + sys.argv[2])
	now = datetime.datetime.now()
	newLog = {
				"name": name,
				"dateCreated": now.strftime("%Y-%m-%d %H:%M"),
				"lastEdit": now.strftime("%Y-%m-%d %H:%M"), 
				"count": 0,
			 	"logs":	[]
			 }

	pickle.dump( newLog, open(filePath + name, "wb") )
	setCurrentLog(name)


#	logTo ( log, instr):
#
#	logs the given message to the log 
def logTo( log, instr ):
	# load log
	workingLog = pickle.load( open(filePath + log, "rb" ))

	# TODO: get the date thingy to working
	# if last edit is one day ago
	now = datetime.datetime.now()
	
	t = time.strptime(workingLog['lastEdit'], "%Y-%m-%d %H:%M")
	nextDate = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday) + timedelta(1)

	if ( nextDate < now ):
		putDateInLog( log ) 

	mes = str(now.strftime("%H:%M - ")) + instr

	workingLog['logs'].append(mes)
	workingLog['lastEdit'] = now.strftime("%Y-%m-%d %H:%M")
	workingLog['count'] = workingLog['count'] + 1
	pickle.dump (workingLog, open(filePath + log, "w"))


# 	printOutLog( log ):
#
# 	Prints out all the saved strings that are in a log
def printOutLog( log ):
	workingLog = pickle.load( open(filePath + log, "rb" ))['logs']
	for log in workingLog:
		if (log[0] == '['):
			print(log)
		elif (log[0] == "|"):
			print("      " + log)
		else:
			print("    " + log)

#	putDateInLog( log ):
#
#	This adds a log that is the current date 
def putDateInLog( log ):
	now = datetime.datetime.now()
	workingLog = pickle.load( open(filePath + log, "rb" ))
	workingLog['logs'].append(now.strftime("[%a %Y-%m-%d]"))
	workingLog['lastEdit'] = now.strftime("%Y-%m-%d %H:%M")
	pickle.dump(workingLog, open(filePath + log, "w"))

#	outInfo( log ):
#
#	Prints out the info of the of the log
def outInfo( log ):
	workingLog = pickle.load( open(filePath + log, "rb" ))
	print("name:		" + workingLog['name'])
	print("Created: 	" + workingLog['dateCreated'])
	print("Last Editted:	" + workingLog['lastEdit'])
	print("# of logs:   	" + str(workingLog['count']))

# 	listOutLogs():
#
#	This prints out the all of the current notes 
def listOutLogs():
	savedLogs = pickle.load( open(filePath + infoFile, "rb" ))['logs']
	for log in savedLogs:
		print("\t" + log)

#	saveLogToFile():
#
#	This saves the log to a text file 
def saveLogToFile( log, file ):
	workingLog = pickle.load( open( filePath + log, "rb" ) )
	f = open( file, 'w' )
	f.write( "name:     \t" + workingLog["name"] + "\n" )
	f.write( "Created:  \t" + workingLog["dateCreated"] + "\n" )
	f.write( "Edited:   \t" + workingLog["lastEdit"] + "\n" )
	f.write( "Log Count:\t" + str( workingLog["count"] ) + "\n" )
	f.write( "-- Log -- \n" )
	logs = workingLog['logs']
	for l in logs:
		f.write(l + "\n")



# 	starting ( log ):
# 
#	Allows the user to input consecutive logs
def starting( log ):
	os.system('clear')
	inputs = ""
	print("\"-quit\" to stop logging\n\"-d\" to date")

	# Keeps taking input until the user specifies quit.
	while (inputs != "-quit"):
		inputs = raw_input(log + bcolors.OKBLUE + " >> " + bcolors.ENDC)
		if (inputs != "-quit"):
			if (inputs == "-d"):
				putDateInLog(log)
			else:	
				logTo(log, inputs)



#	tryGettingFile
#
#	This will try to connect to the file and then return the file name or kill the
#	program
def tryGettingFile():
	try:
		currentLogName = pickle.load( open(filePath + infoFile, "rb") )['current']
	except IOError:
		print("Try running the \"logit -setup\" command")
		exit(1)

	# if it succeeds 
	return currentLogName;

#   EditLog ( log ):
#
# 	Will open the log and allow the user to edit the log
def editLog( log ):
	workingLog = pickle.load( open( filePath + log, "rb" ) )
	for i in range(0, len(workingLog["logs"])):
		print("[" + str(i + 1) + "] " + workingLog["logs"][i] )

	theI = raw_input("# to delete (q to quit): ")

	# Q to quit 
	if (theI == 'q'):
		return 0

	# Checking the edit input
	if (int(theI) - 1 >= len(workingLog['logs']) or int(theI) <= 0):
		print("not in index")
		return 0

	ans = raw_input("Delete \'" + workingLog['logs'][int(theI) - 1] + "\'? Y/n ")
	if (ans.upper()[0] == 'Y'): 
		workingLog['logs'].pop(int(theI) - 1)
		print("Deleted")
		workingLog['count'] = workingLog['count'] - 1

	pickle.dump(workingLog, open(filePath + log, "w"))

#	Breaking
#
#	Adds a line to the timeline making the log look a little nicer.
def breakLine( log ):
	print("Break Line Added")
	workingLog = pickle.load( open( filePath + log, "rb" ) )
	workingLog['logs'].append("|")
	pickle.dump( workingLog, open( filePath + log, "w" ) )

#	inputLogFromFile
#
#	This will allow the user to save from a file that was outputted from his
#	program
def inputLogFromFile( file ):
	
	# Try to open the file
	try:
		# open the file and look at the line
		with open( file ) as f:
			
			name = f.readline().split(':')[1].strip()
			createdDate = f.readline().split(':')[1].strip()
			editedDate = f.readline().split(':')[1].strip()
			logCount = f.readline().split(':')[1].strip()
			
			f.readline() # don't need
			
			# Create a new log with the given name
			newLog(name)
		
			# get the newly created pickle
			workingLog = pickle.load( open( filePath + name, "rb" ) )

			for line in f:
				# is it a date
				if ( line[0] == '[' ):
					workingLog['logs'].append(line.rstrip())
				# is it a line break
				elif ( line[0] == '|' ):
					workingLog['logs'].append(line.rstrip())
				# its an actual input and we need a log
				else:
					workingLog['logs'].append(line.rstrip())
					workingLog['count'] = workingLog['count'] + 1

		# save the new log
		pickle.dump( workingLog, open( filePath + name, "w" ) )

	# file not a thing
	except IOError:
		print( file + ": Is not a file.")

#	setup
#
#	This function is used to initially set up the info file of the current
#	log and what not
def setup():
	current = {
		"current": "",
		"logs": [],
		"count": 0
	}
			
	try:
		#
		pickle.dump( current, open(filePath + infoFile, "w") )
		currentLogName = pickle.load( open( filePath + infoFile, "rb" ) )['current']
	except IOError:
		# no current logs directory.. so make one
		newpath = os.path.dirname(os.path.realpath(__file__))
		newpath = newpath + "/logit_saves/"
		current['path'] = newpath
		if not os.path.exists(newpath):
			os.makedirs(newpath)
			pickle.dump( current, open(filePath + infoFile, "w") )
			currentLogName = pickle.load( open( filePath + infoFile, "rb" ) )['current']

#	deleteLog( log )
#
#	Will allow the user to delete an entire log
def deleteLog( log ):
	workingInfo = pickle.load( open( filePath + infoFile, "rb" ))
	if ( log in workingInfo['logs'] ):
		ans = raw_input("Are you sure you want to delete \'" + log + "\'? Y/n ")
		if (ans.upper()[0] == 'Y'):
			workingInfo['logs'].remove(log)
			pickle.dump( workingInfo, open(filePath + infoFile, "w") )
			os.remove(filePath + log)
			#TODO change current
	else:
		print("not a log")



# TODO:	longestLog( log )
#
#	getting the longest log from a given log
def longestLog( log ):
	workingLog = pickle.load( open( filePath + log, rb ) )
	len = 0
	ind = 0
	for log in workingLog['logs']:
		if ( len > len(log) ):
			len = len(log)

	return len

# TODO:	shortenString( input, len )
#
#	Shorten the string an returns an array of the given length
def shortenString( input, len ):
	chunks = len(input)
	chunk_size = len
	return [ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

# TODO: insert date
#
# ###

#	errorWarning( errorString )
#
#
def errorWarning( errorString ):
	print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + errorString)

#	outCurrent()
#
#	Prints out the current working log
def outCurrent():
	print(tryGettingFile())


#	Class Command
#
#	name
#	cmd
#	desc
#	func
#	TODO: options
class Command:
	def __init__(self, name, cmd, desc, func):
		self.name = name
		self.cmd  = cmd
		self.desc = desc
		self.func = func
	
	def doFunction(args):
		self.func(*args)

# The command strings
cmds = {
	'new'	: Command("new", "-new", "\'name\' : creates a new log", newLog),
	'n'		: Command("name", "-n", ": prints out the name of the current log", outCurrent),
	'ls'	: Command("list", "-ls", ": lists out all the logs", listOutLogs),
	'o'		: Command("open", "-o", ": opens the another log", setCurrent),
	's'		: Command("save", "-s", "\'name'\ : saves the log to text file", saveLogToFile),
	'd'		: Command("date", "-d", ": adds todays date to the log", putDateInLog),
	'out'	: Command("out", "-out", ": prints out the logs", printOutLog),
	'to'	: Command("to", "-to", "\'name\' : logs the given name", logTo),
	'i'		: Command("info", "-i", ": prints out the info", outInfo),
	'start'	: Command("start", "-start", ": starts a log console", starting),
	'edit'	: Command("edit", "-edit", ": you can remove logs", editLog),
	'break'	: Command("break", "-break", ": adds a break line in log", breakLine),
	'in'	: Command("from", "-in", "\'name\' : imports from a saved text file", fromFile),
	'del'	: Command("delete", "-del", ": deletes the current log", deleteLog),
	'setup'	: Command("setup", "--setup", ": sets up the Logit saves", setup),
	'help'	: Command("help", "--help", ": Shows the help message", helpText)
	}
	'''
		new		= "-new"
		name	= "-n"
		listing = "-ls"
		opening = "-o"
		saving	= "-s"
		dating 	= "-d"
		outing 	= "-out"
		toing 	= "-to"
		infoing = "-i"
		starting= "-start"
		editing = "-e"
		breaking= "-b"
		fromFile= "-in"
		deleting= "-del"
		markdown= "-md"
		setting = "--setup"
		helping = "--help"
		'''




#	main()
#
#	This is a the main funciton of the progam
def main():

	#
	for arg in range( 0, len(sys.argv) ):
		currentLogName = tryGettingFile()
		if (arg[0] == '-' and arg[1] == '-'):
			# help
			if (arg[2] == 'h'):
				helpText()
			# setup
			elif (arg[2] == 's'):
				setup()
			else:
				errorWarning( arg + " is not a command. ")
		elif (arg[0] == '-'):

	

	if (len(sys.argv) == 1):
		# no given arguments
		currentLogName = tryGettingFile()
		
		print( currentLogName )

	# given 1 argument
	elif (len(sys.argv) == 2):
		# one given argument
		if (sys.argv[1] ==   cmds.setting):
			setup()

		else:
			currentLogName = tryGettingFile()

			if (sys.argv[1] ==   cmds.dating):
				putDateInLog( currentLogName )
			elif (sys.argv[1] ==   cmds.listing):
				listOutLogs()
			elif (sys.argv[1] ==   cmds.outing):
				printOutLog( currentLogName )
			elif (sys.argv[1] == cmds.helping):
				helpText()
			elif (sys.argv[1] ==   cmds.infoing):
				outInfo( currentLogName )
			elif (sys.argv[1] ==   cmds.starting):
				starting( currentLogName )
			elif (sys.argv[1] ==   cmds.editing):
				editLog( currentLogName )
			elif (sys.argv[1] ==   cmds.breaking):
				breakLine( currentLogName )
			else:
				if ( sys.argv[1][0] != '-' ):
					logTo( currentLogName, sys.argv[1] )
				else:
					errorWarning(sys.argv[1] + " is not a valid command")
					helpText()

	# 2 given arguments 
	elif (len(sys.argv) == 3):
		currentLogName = tryGettingFile()

		if (sys.argv[1] == cmds.newing):
			newLog(sys.argv[2])
		elif (sys.argv[1] == cmds.editing):
			editLog()
		elif (sys.argv[1] == cmds.opening):
			setCurrentLog(sys.argv[2])
		elif (sys.argv[1] == cmds.saving):
			saveLogToFile( currentLogName, sys.argv[2] )
			print( "save the log to the file: " + sys.argv[2] )
		elif (sys.argv[1] == cmds.fromFile):
			#TODO
			inputLogFromFile( sys.argv[2] )
		elif (sys.argv[1] == cmds.deleting):
			print("in Developement")
			deleteLog(sys.argv[2])
		elif(sys.argv[1] == cmds.outing):
			printOutLog(sys.argv[2])
		else:
			errorWarning(sys.argv[1] + " is not a valid command")
			helpText()

	# 3 given arguments
	elif (len(sys.argv) == 4):
		currentLogName = tryGettingFile()
		if(sys.argv[1] == cmds.toing):
			logTo(sys.argv[2], sys.argv[3])
		elif(sys.argv[1] == cmds.outing):
			printOutLog(sys.argv[2])
		else:
			errorWarning(sys.argv[1] + " is not a valid command")
			helpText()

	# 4 giveb arguments
	elif (len(sys.argv) == 5):
		currentLogName = tryGetting()
		if (sys.argv[1] ==   cmds.outing):
			if (sys.argv[3] == ):
				print("out but in mark down")
			else:
				print("out in latex")



# this is where it all starts
main()
