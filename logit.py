#!/usr/bin/env python

# logit
'''
	Okay, so I wanna make this logger application
	
	09 / 02 / 2016	- it works
	10 / 31 / 2016	- it works real well
	11 / 08 / 2016	- it does not work
					- Commands need a better way of being processed.
					- I don't know how to do that
					- I am thinking of a tree type thing RECURSION!
				
	11 / 09 / 2016	- I learned about argparse. I might need to make this python3
					- Nah not using argparse anymore.
	
	03 / 29 / 2017	- made parsing functions for general command handling.
					- This is a huge and very simple improvement.

	02 / 25 / 2019	- Lets see what I remember 
					- Holy cow it's longer than I remember.

					- why did I not use argparse? 
					-	Cause it's confusing.
	
'''
import sys				# for system things like File I/O
import pickle			# for saving objects, pickling is so easy.

import time				# so I can get the time
import datetime			# so I can get the date

# this is why you label things at the time of adding it to the top of the code and not as a aftersight 5 monthes later
from datetime import date, timedelta	

import os				# For os stuff
import readline			# For readline



# ******************************************************************************
#	tryGettingFile
#
#	This will try to connect to the file and then return the file name or kill
#	the program
# ******************************************************************************
def tryGettingFile():
	try:
		currentLogName = pickle.load(open(filePath + infoFile, "rb"))['current']
	except IOError:
		print("Try running the \"logit -setup\" command")
		exit(1)

	return currentLogName;

# ******************************************************************************
# so I can change the output colors
# ******************************************************************************
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# ******************************************************************************
# --> GLOBALS <--

# TODO make these less specific for more users

# complete = "/usr/local/my_scripts"
# these need to become variables in the info file.
complete = "/Users/TheCmar7/Developer/python/Logit"
directory = "/logit_saves/"
infoFile = "logit_current.p"
filePath = complete + directory

cmds = {}
currentLogName = tryGettingFile()
# ******************************************************************************

# ******************************************************************************
#	setup
#
#	This function is used to initially set up the info file of the current
#	log and what not
# ******************************************************************************
def setup():
	current = {
		"current": "",
		"logs": [],
		"count": 0
	}
	
	try:
		# try and open the pickle and load the current name
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

# ******************************************************************************
#	longestLog( log = currentLog )
#
#	getting the longest log from a given log
# ******************************************************************************
def longestLog( log = currentLogName ):
	if (isALog(log)):
		workingLog = pickle.load( open( filePath + log, rb ) )
		len = 0
		ind = 0
		for log in workingLog['logs']:
			if ( len > len(log) ):
				len = len(log)
		return len
	else:
		return -1

# ******************************************************************************
#	shortenString( input, len )
#
#	Shorten the string an returns an array of the given length
# ******************************************************************************
def shortenString( input, len ):
	chunks = len(input)
	chunk_size = len
	return [ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

# ******************************************************************************
#	errorWarning( errorString )
#
#
# ******************************************************************************
def errorWarning( errorString ):
	print(bcolors.WARNING + "ERROR: " + bcolors.ENDC + errorString)


# ******************************************************************************
#	outCurrent()
#
#	Prints out the current working log
# ******************************************************************************
def outCurrent():
	print(tryGettingFile())

# ******************************************************************************
# 	helpText():
#
#	Prints out the text of commands
# ******************************************************************************
def helpText():
	for k, v in cmds.items():
		print("\t" + v.helpDescription())

# ******************************************************************************
#	isALog ( log )
#
#	Returns true if the log is one of the saved logs.
# ******************************************************************************
def isALog( log ):
	return log in pickle.load(open(filePath + infoFile, "rb"))['logs']

# ******************************************************************************
# 	setCurrentLog ( name ):
#
# 	This sets the current log to a name
# ******************************************************************************
def setCurrentLog( name ):
	if isALog(name):
		workingLog = pickle.load(open(filePath + infoFile, "rb"))
		workingLog['current'] = name
		pickle.dump(workingLog, open(filePath + infoFile, "w"))
		return True
	else:
		errorWarning(name + " is not a log")
		return False

# ******************************************************************************
#	newLog ( name ):
#
#	creates a new log with the name that is given
# ******************************************************************************
def newLog( name ):
	if not isALog( name ):
		workingLog = pickle.load(open(filePath + infoFile, "rb"))
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

		pickle.dump(newLog, open(filePath + name, "wb"))
		setCurrentLog(name)
		return True
	else:
		errorWarning( name + " is already a log" )
		return False



# ******************************************************************************
#	logTo ( instring, log = currentLog ):
#
#	logs the given message to the log
# ******************************************************************************
def logTo( instring, log = currentLogName ):
	if isALog(log):
		
		workingLog = pickle.load( open(filePath + log, "rb" ))

		# TODO: get the date thingy to working
		# if last edit is one day ago
		now = datetime.datetime.now()
		
		t = time.strptime(workingLog['lastEdit'], "%Y-%m-%d %H:%M")
		nextDate = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday) + timedelta(1)

		if ( nextDate < now ):
			putDateInLog( log ) 

		mes = str(now.strftime("%H:%M - ")) + instring

		workingLog['logs'].append(mes)
		workingLog['lastEdit'] = now.strftime("%Y-%m-%d %H:%M")
		workingLog['count'] = workingLog['count'] + 1
		pickle.dump (workingLog, open(filePath + log, "w"))
		return True
	else:
		errorWarning(log + "is not a log")
		return False


# ******************************************************************************
# 	printOutLog( log = currentLog ):
#
# 	Prints out all the saved strings that are in a log
# ******************************************************************************
def printOutLog( log = currentLogName ):
	if isALog(log):
		print(log)
		workingLog = pickle.load( open(filePath + log, "rb" ))['logs']
		for log in workingLog:
			if (log[0] == '['):
				print(log)
			elif (log[0] == "|"):
				print("      " + log)
			else:
				print("    " + log)
		return True
	else:
		errorWarning(log + " is not a log")
		return False

# ******************************************************************************
#	putDateInLog( log = currentLog ):
#
#	This adds a log that is the current date 
# ******************************************************************************
def putDateInLog( log = currentLogName):
	now = datetime.datetime.now()
	workingLog = pickle.load( open(filePath + log, "rb" ))
	workingLog['logs'].append(now.strftime("[%a %Y-%m-%d]"))
	workingLog['lastEdit'] = now.strftime("%Y-%m-%d %H:%M")
	pickle.dump(workingLog, open(filePath + log, "w"))

# ******************************************************************************
#	outInfo( log = currentLog ):
#
#	Prints out the info of the of the log
# ******************************************************************************
def outInfo( log = currentLogName ):
	if isALog(log):
		workingLog = pickle.load( open(filePath + log, "rb" ))
		print("name:		" + workingLog['name'])
		print("Created: 	" + workingLog['dateCreated'])
		print("Last Editted:	" + workingLog['lastEdit'])
		print("# of logs:   	" + str(workingLog['count']))
		return True
	else:
		errorWarning(log + " is not a log")
		return False

# ******************************************************************************
# 	listOutLogs():
#
#	This prints out the all of the current notes 
# ******************************************************************************
def listOutLogs():
	
	savedLogs = pickle.load( open(filePath + infoFile, "rb" ))['logs']
	for log in savedLogs:
		print("\t" + log)

# ******************************************************************************
#	saveLogToFile():
#
#	This saves the log to a text file 
# ******************************************************************************
def saveLogToFile( file, log = currentLogName ):
	if isALog(log):
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
		return True
	else:
		errorWarning(log + " is not a log")
		return False



# ******************************************************************************
# 	starting ( log = currentLog ):
# 
#	Allows the user to input consecutive logs
# ******************************************************************************
def starting( log = currentLogName ):
	if isALog(log):
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
		return True
	else:
		errorWarning(log + " is not a log")
		return False


# ******************************************************************************
#	tryGettingFile
#
#	This will try to connect to the file and then return the file name or kill the
#	program
# ******************************************************************************
def tryGettingFile():
	try:
		currentLogName = pickle.load( open(filePath + infoFile, "rb") )['current']
	except IOError:
		print("Try running the \"logit -setup\" command")
		exit(1)

	# if it succeeds 
	return currentLogName;

# ******************************************************************************
#   EditLog ( log = currentLog ):
#
# 	Will open the log and allow the user to edit the log
# ******************************************************************************
def editLog( log = currentLogName ):
	if (isALog(log)):
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
		return True
	else:
		errorWarning(log + "is not a log")
		return False

# ******************************************************************************
#	Breaking ( log = currentLog )
#
#	Adds a line to the timeline making the log look a little nicer.
# ******************************************************************************
def breakLine( log = currentLogName ):
	if (isALog(log)):
		print("Break Line Added")
		workingLog = pickle.load( open( filePath + log, "rb" ) )
		workingLog['logs'].append("|")
		pickle.dump( workingLog, open( filePath + log, "w" ) )
		return True
	else:
		errorWarning(log + " is not a log")
		return False

# ******************************************************************************
#	inputLogFromFile
#
#	This will allow the user to save from a file that was outputted from his
#	program
# ******************************************************************************
def inputLogFromFile( file, ):
	
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

		return True



	# file not a thing
	except IOError:
		errorWarning( file + ": Is not a file.")
		return False

# ******************************************************************************
#	deleteLog( log = currentLog )
#
#	Will allow the user to delete an entire log
# ******************************************************************************
def deleteLog( log = currentLogName ):
	if (isALog(log)):
		workingInfo = pickle.load( open( filePath + infoFile, "rb" ))
		ans = raw_input("Are you sure you want to delete \'" + log + "\'? Y/n ")
		if (ans.upper()[0] == 'Y'):
			workingInfo['logs'].remove(log)
			pickle.dump( workingInfo, open(filePath + infoFile, "w") )
			os.remove(filePath + log)
		#TODO change current
		return True
	else:
		# Print Warning, Return False
		print("not a log")
		return False

'''
	Class CommandList

'''


# ******************************************************************************
#	Class Command
#
#	command
#	name
#	cmd
#	desc
#	func
# ******************************************************************************
class Command:
	def __init__(self, arg, name, desc, func, possibleOptions = {}):
		self.arg = arg		# the inputted argument to fire function
		self.name = name	# the name that helps user know what the function does
		self.desc = desc	# a description of the functions
		self.func = func	# the function that is fired
		# an object that is the types of the possible function options
		self.possibleOptions = possibleOptions
	
	def helpDescription(self):
		return self.arg + "\t: " + self.name + "\t- " + self.desc
	
	def doFunction(self, options):
		for i in range(0, len(options)):
			break;
		
		self.func(*options)

# ******************************************************************************
#	Class CommandDictionary
#
# ******************************************************************************
class CommandDictionary:
	def __init__(self):
		self.commandDict = {}
	
	def addCommand(self, command):
		self.commandDict[command.arg] = command
	
	def getCommandByName(self, name):
		return "TODO: IMPLEMENT"
		
	def getCommandByArg(self, arg):
		return self.commandDict[arg]
		
	def runCommandByArg(self, arg, options = []):
		return 0
	


# ******************************************************************************
# *******************PARSING****************************************************
# ******************************************************************************

# ******************************************************************************
#	ParseNewLog
#
# ******************************************************************************
def parseNewLog(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given for filename")
	else:
		newLog(options[0])

# ******************************************************************************
#	ParseNewLog
#
# ******************************************************************************
def parseOutCurrent(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		outCurrent()

# ******************************************************************************
#	parseListOutLogs
#
# ******************************************************************************
def parseListOutLogs(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		listOutLogs()

# ******************************************************************************
#	parseSetCurrentLog
#
# ******************************************************************************
def parseSetCurrentLog(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 0):
		errorWarning(name + ": no arguments given")
	else:
		setCurrentLog(options[0])


# ******************************************************************************
#	parseSaveLogToFile
#
# ******************************************************************************
def parseSaveLogToFile(name, options):
	if (len(options) > 2):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 1):
		saveLogToFile(option[0])
	elif (len(options) == 2):
		if (isALog(options[0])):
			saveLogToFile(option[1], options[0])
		elif (isALog(options[1])):
			saveLogToFile(option[1], options[0])
		else:
			errorWarning("need a valid Log name")
	else:
		errorWarning("Not enough arguments")



# ******************************************************************************
#	parsePutDateInLog
#
# ******************************************************************************
def parsePutDateInLog(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 1):
		if (isALog(options[0])):
			putDateInLog(options[0])
		else:
			errorWarning(options[0]  + "is not a valid Log name")
	else:
		putDateInLog()



# ******************************************************************************
#	parsePrintOutLog
#
# ******************************************************************************
def parsePrintOutLog(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		printOutLog()

# ******************************************************************************
#	parseOutInfo
#
# ******************************************************************************
def parseOutInfo(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 1):
		if (isALog(options[0])):
			outInfo(options[0])
		else:
			errorWarning(options[0] + " is not a valid Log name")
	else:
		outInfo()

# ******************************************************************************
#	parseStarting
#
# ******************************************************************************
def parseStarting(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		starting()

# ******************************************************************************
#	parseEditLog
#
# ******************************************************************************
def parseEditLog(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 1):
		if (isALog(options[0])):
			editLog(options[0])
		else:
			errorWarning(options[0] + " is not a valid Log name")
	else:
		editLog()

# ******************************************************************************
#	parseBreakLine
#
# ******************************************************************************
def parseBreakLine(name, options):
	if (len(options) > 1):
		errorWarning(name + ": too many arguments given")
	elif (len(options) == 1):
		if (isALog(options[1])):
			breakLine(options[0])
		else:
			errorWarning(options[0] + " is not a valid Log name")
	else:
		breakLine()

# ******************************************************************************
#	parseInputLogFromFile
#
# ******************************************************************************
def parseInputLogFromFile(name, options):
	if (len(options) < 0):
		errorWarning(name + ": not enough arguments given")
	else:
		inputLogFromFile(options[0])


# ******************************************************************************
#	parseInputLogFromFile
#
# ******************************************************************************
def parseDeleteLog(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		deleteLog()

# ******************************************************************************
#	parseSetup
#
# ******************************************************************************
def parseSetup(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		setup()


# ******************************************************************************
#	parseHelpText
#
# ******************************************************************************
def parseHelpText(name, options):
	if (len(options) > 0):
		errorWarning(name + ": too many arguments given")
	else:
		helpText()


# ******************************************************************************
#	The command strings
#	key		=> Value
#	caller	=> Command Object
# ******************************************************************************
cmds = {
	'-new'		: Command("-new",
						"new",
						"[\'name\'] creates a new log",
						parseNewLog),
				
	'-n'		: Command('-n',
						"name",
						"prints out the name of the current log",
						parseOutCurrent),
						  
	'-ls'		: Command(	'-ls',
							"list",
						  	"lists out all the saved logs",
						 	parseListOutLogs),
						  
	'-o'		: Command("-o",
						  "open",
						  "[\'name\'] opens another log",
						  parseSetCurrentLog),
						  
	'-s'		: Command('-s',
							"save",
						  "[\'name\'] saves the log to text file",
						  parseSaveLogToFile),

	'-d'		: Command('-d',
						"date",
						  "adds todays date to the log",
						  parsePutDateInLog),

	'-out'		: Command('-out',
						"out",
						  "prints out the messages",
						  parsePrintOutLog),

	'-i'		: Command('-i',
							"info",
						  "prints out the info",
						  parseOutInfo),

	'-start'	: Command("-start",
							"start",
						  "starts a log console",
						  parseStarting),

	'-edit'		: Command('-edit',	
							"edit",
						  "you can remove logs",
						  parseEditLog),

	'-break'	: Command('-break',
						"break",
						  "adds a break line in log",
						  parseBreakLine),

	'-in'		: Command('-in',
							"from file",
						  "[\'name\'] [\'file\'] imports from a saved text file",
						  parseInputLogFromFile),
	'-del'		: Command('-del',
						"delete",
						  "deletes the current log",
						  parseDeleteLog),
	# I should make a make file that does this so that people that download
	# the git can easily set it up and start using it.
	'--setup'	: Command('--setup',
						"setup",
						  "sets up the Logit saves",
						  parseSetup),
	'--help'	: Command('--help',
						"help",
						  "Shows the help message",
						  parseHelpText)
	}

# ******************************************************************************
#	main()
#
#	This is a the main funciton of the progam
# ******************************************************************************
def main():
	#  SUGG: Should I make it so people can use just the first letter of the command?
	#		 I would need to change some of the ambiguous commands
	#  TODO: check the options that there are no top options that are the same name as
	#		 options
	
	# arguments
	arguments = sys.argv[1:]
	#print(arguments)
	
	# If there are no arguments
	currentLogName = tryGettingFile()
	if (len(arguments) == 0):
		print(currentLogName)
	
	# so now every function doesn't need to be a seperate entity,
	# the function can be used by parsing up the function options and
	# then using the functions where they are needed.
	
	# split into smaller arrays at every top level option
	splits = []
	usedComm = []
	leftOver = []
	commands = cmds.keys()
	for i in range(0, len(arguments)):
		if arguments[i] in commands:
			splits.append(i)
			usedComm.append(arguments[i])
		else:	
			leftOver.append(arguments[i])
		
	if len(arguments) not in splits:
		splits.append(len(arguments))

	# log the text given
	if (len(leftOver) == 1 and len(arguments) == 1):
		logTo(leftOver[0])

	# do commands
	for j in range(0, len(usedComm)):
		thisSplit = splits[j + 1]
		theseArgs = arguments[splits[j] + 1:thisSplit]
		command = cmds.get(usedComm[j])
		#print( str(j) + " thissplit: " + str(thisSplit))
		#print(str(j) + " theseArgs: " + str(theseArgs))
		#print(str(j) + " command: " + str(command))
		command.func(usedComm[j], theseArgs)
	

	
	# print(splits)
	# print(usedComm)
	# print(leftOver)






	


# ******************************************************************************
#
# this is where it all starts
#
# ******************************************************************************
if __name__ == "__main__":
	main()
