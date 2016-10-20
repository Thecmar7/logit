#!/usr/bin/env python

# logit
'''
	Okay so I wanna make this logger application
	It's functions: 
		logit -new "name"		// creates a new log
		logit -o "name"		// opens
		logit -s "name"		// outputs the log to a txt file
		logit -d 			// date it
		logit -ls 			// list out the saved logs 
		logit -out 			// out current log 
		logit -out "name"
		logit "This is a thing to log"
		logit -to "name" "this is a thing to log"
		logit -i 			// get info about current log
		logit -edit 		// edit the log		

	9/2/2016
''' 
import sys
import pickle 

import time
import datetime 
from datetime import date, timedelta

import os

class cmds:
	newing 	= "new"
	listing = "ls"
	opening = "o" 
	saving	= "s"
	dating 	= "d"
	outing 	= "out"
	toing 	= "to"
	infoing = "i"
	starting= "start" 
	editing = "edit"
	setting = "setup"
	helping = "help"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


complete = "/usr/local/my_scripts"
filePath = complete + "/logit_saves/"
infoFile = "logit_current.p"

#	This is if  you need to reset the current.p file
# current = { "current": "", "logs": [], count: 0, }
# pickle.dump( current, open(filePath + infoFile, "w") )

# 	helpText():
#
#	Prints out the text of  commands
def helpText():
	print(	"\tlogit -" + cmds.newing + " \"name\"		// creates a new log\n" +
			"\tlogit -" + cmds.opening + " \"name\"			// opens\n" +
			"\tlogit -" + cmds.saving + " \"name\"			// outputs the log to a txt file\n" +
			"\tlogit -" + cmds.dating + " 			// date it\n" +
			"\tlogit -" + cmds.listing + " 			// list out the saved logs\n" +
			"\tlogit -" + cmds.outing + " 			// out current log\n" +
			"\tlogit -" + cmds.outing + " \"name\"		// prints out given log\n" +
			"\tlogit \"This is a thing to log\"\n" +
			"\tlogit -" + cmds.toing + " \"name\" \"this is a thing to log\"\n" +
			"\tlogit -" + cmds.infoing + " 			// info about log\n" +
			"\tlogit -" + cmds.starting + " 			// Starts a log console\n" +
			"\tlogit -" + cmds.editing + "			// Allows you to edit the log")

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
		if (log[0] != '['):
			print("    " + log)
		else:
			print(log)

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

# TODO: EditLog ( log ):
#
# Will open the log and allow the user to edit the log
def editLog( log ):
	workingLog = pickle.load( open( filePath + log, "rb" ) )
	for i in range(0, len(workingLog["logs"])):
		print("[" + str(i) + "] " + workingLog["logs"][i] )

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



#	main()
#
#	This is a the main funciton of the progam
def main():

	if (len(sys.argv) == 1):
		# no given arguments
		currentLogName = tryGettingFile()
		
		print( currentLogName )

	# given 1 argument
	elif (len(sys.argv) == 2):
		# one given argument
		if (sys.argv[1] == "-setup"):
			current = {  
						"current": "",
						"logs": [], 
						"count": 0,
					  }
			pickle.dump( current, open(filePath + infoFile, "w") )
			currentLogName = pickle.load( open( filePath + infoFile, "rb" ) )['current']
		else:
			currentLogName = tryGettingFile()

			if (sys.argv[1] == "-" + cmds.dating):
				putDateInLog( currentLogName )
			elif (sys.argv[1] == "-" + cmds.listing):
				listOutLogs()
			elif (sys.argv[1] == "-" + cmds.outing):
				printOutLog( currentLogName )
			elif (sys.argv[1] == "--help"):
				helpText()
			elif (sys.argv[1] == "-" + cmds.infoing):
				outInfo( currentLogName )
			elif (sys.argv[1] == "-" + cmds.starting):
				starting( currentLogName )
			else:
				logTo(currentLogName, sys.argv[1])

	# 2 given arguments 
	elif (len(sys.argv) == 3):
		currentLogName = tryGettingFile()

		if (sys.argv[1] == "-" + cmds.newing):
			newLog(sys.argv[2])
		elif (sys.argv[1] == "-" + cmds.editing):
			editLog()
		elif (sys.argv[1] == "-" + cmds.opening):
			setCurrentLog(sys.argv[2])
		elif (sys.argv[1] == "-" + cmds.saving):
			saveLogToFile( currentLogName, sys.argv[2] )
			print( "save the log to the file: " + sys.argv[2] ) 
		elif(sys.argv[1] == "-" + cmds.outing):
			printOutLog(sys.argv[2])

	# 3 given arguments 
	elif (len(sys.argv) == 4):
		currentLogName = tryGettingFile()

		if(sys.argv[1] == "-" + cmds.toing):
			logTo(sys.argv[2], sys.argv[3])
		elif(sys.argv[1] == "out"):
			printOutLog(sys.argv[2])

# this is where it all starts
main()