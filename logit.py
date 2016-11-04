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

cmds = {}
currentLogName = tryGettingFile()

# 	helpText():
#
#	Prints out the text of  commands
def helpText():
	for k, v in cmds.items():
		print( "\t" + k + " " + v.desc)


def isALog( log ):
	return log in pickle.load( open(file + infoFile, "rb" ))['logs']


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
	if isALog( name ):
		errorWarning( name + " is already a log!" )
		return 0
	
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
def logTo( instring, log = currentLogName ):
	# load log
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


# 	printOutLog( log ):
#
# 	Prints out all the saved strings that are in a log
def printOutLog( log = currentLogName ):
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
def putDateInLog( log = currentLogName):
	now = datetime.datetime.now()
	workingLog = pickle.load( open(filePath + log, "rb" ))
	workingLog['logs'].append(now.strftime("[%a %Y-%m-%d]"))
	workingLog['lastEdit'] = now.strftime("%Y-%m-%d %H:%M")
	pickle.dump(workingLog, open(filePath + log, "w"))

#	outInfo( log ):
#
#	Prints out the info of the of the log
def outInfo( log = currentLogName ):
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
def saveLogToFile( file, log = currentLogName ):
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
def starting( log = currentLogName ):
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
def editLog( log = currentLogName ):
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
def breakLine( log = currentLogName ):
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
def deleteLog( log = currentLogName ):
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
def longestLog( log = currentLogName ):
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
	def __init__(self, name, desc, func, argN = 0, argP = 0):
		self.name = name
		self.desc = desc
		self.func = func
		self.argN = argN
		self.argP = argP
	
	def doFunction(self, args):
		self.func(*args)

# The command strings
cmds = {
	'-new'		: Command("new", "\'name\' : creates a new log", newLog, 1, 1),
	'-n'		: Command("name",  ": prints out the name of the current log", outCurrent, 0, 1),
	'-ls'		: Command("list",  ": lists out all the logs", listOutLogs),
	'-o'		: Command("open",  ": opens the another log", setCurrentLog, 1, 1),
	'-s'		: Command("save",  "\'name\' : saves the log to text file", saveLogToFile, 1, 2),
	'-d'		: Command("date",  ": adds todays date to the log", putDateInLog, 0, 1),
	'-out'		: Command("out",  ": prints out the logs", printOutLog, 0, 1),
	'-to'		: Command("to",  "\'name\' \'msg\' : logs the given name", logTo, 2, 2),
	'-i'		: Command("info",  ": prints out the info", outInfo, 0, 1),
	'-start'	: Command("start",  ": starts a log console", starting, 0, 1),
	'-edit'		: Command("edit",  ": you can remove logs", editLog, 0, 1),
	'-break'	: Command("break",  ": adds a break line in log", breakLine, 0, 1),
	'-in'		: Command("from",  "\'name\' \'file\' : imports from a saved text file", inputLogFromFile, 2, 2),
	'-del'		: Command("delete",  ": deletes the current log", deleteLog, 0, 1),
	'--setup'	: Command("setup",  ": sets up the Logit saves", setup),
	'--help'	: Command("help", ": Shows the help message", helpText)
	}

#	main()
#
#	This is a the main funciton of the progam
def main():
	currentLogName = tryGettingFile()
	if (len(sys.argv) == 1):
		print(currentLogName)

	i = 1
	while i < len(sys.argv):
		command = sys.argv[i]
		if command in cmds:
			c = cmds[command]
			#set up the options
			options = []
			
			if (c.argN == c.argP):
				for j in range(0, c.argN):
					options.append( sys.argv[i + 1 + j] )
				i = i + c.argN
		
			c.doFunction(options)
		elif (command[0] != '-'):
			cmds['-to'].doFunction([command, currentLogName])

		else:
			errorWarning(command + " is not a valid command")
		i = i + 1



# this is where it all starts
main()
