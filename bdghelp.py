#!/usr/bin/python
# @Author b3r3nd
# @version 1.0
# @project BdG Help

import socket
import sys
from random import randint
import re
import MySQLdb
 
#----------------------------------- Settings --------------------------------------#
network = 'irc.onlinegamesnet.net'
port = 6667
homechan = 'xxxxxx'
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'PASS xxx\r\n')
irc.send ( 'NICK BdGHelp\r\n' )
irc.send ( 'USER BdGHelp BdGHelp BdGHelp :BdGHelp\r\n' )

#----------------------------------------------------------------------------------#


#---------------------------------- Functions -------------------------------------#
def GetChan(data):
	chan = data.split('#')[1]
        chan = chan.split(' ')[0]
	chan = '#' + chan
	return chan

def GetHost(host):							# Return Host
	host = host.split('@')[1]
	host = host.split(' ')[0]
	return host


def GetNick(data):							# Return Nickname
	nick = data.split('!')[0]
	nick = nick.replace(':', ' ')
	nick = nick.replace(' ', '')
	nick = nick.strip(' \t\n\r')
	return nick

def Notice(nick, msg):
	irc.send('NOTICE ' + nick + ' :' + msg + '\r\n')

def Send(msg):
	irc.send('PRIVMSG ' + homechan + ' :' + msg +  '\r\n')

def SendP(chan, msg):
	irc.send('PRIVMSG ' + chan + ' :' + msg + '\r\n')

def Join(chan):
	irc.send ( 'JOIN ' + chan + '\r\n' )

def Part(chan):
	irc.send ( 'PART ' + chan + '\r\n' )

#------------------------------------------------------------------------------#


while True:
	action = 'none'
	data = irc.recv ( 4096 ) 
	print data

	if data.find ( 'INVITE' ) != -1:
			Join(homechan)

	if data.find ( 'PING' ) != -1:
			irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )


	#--------------------------- Action check --------------------------------#
	if data.find('#') != -1:
		action = data.split('#')[0]
		action = action.split(' ')[1]

	if data.find('NICK') != -1:
		if data.find('#') == -1:
			action = 'NICK'

	#----------------------------- Actions -----------------------------------#
	if action != 'none':

		if action == 'JOIN':
			chan = GetChan(data)
			nick2 = GetNick(data) 
			if data.find('#BdG-Support') != -1:
				Send(nick2 + " Joined #BdG-Support")
	
                if action == 'PART':
                        chan = GetChan(data)
                        nick2 = GetNick(data)
                        if data.find('#BdG-Support') != -1:
                                Send(nick2 + " has left #BdG-Support")

		if action == 'PRIVMSG':
			if data.find('$') != -1:
				x = data.split('#')[1]
				x = x.split('$')[1]
				info = x.split(' ')
				info[0] = info[0].strip(' \t\n\r')
				
				#
				# Check CMD From database
				#
				
                                db = MySQLdb.connect(host="localhost", user="xxxxx", passwd="xxxxxx", db="bdghelp")
                                cur = db.cursor()
                                cur.execute("SELECT * FROM help_cmds")
                              	chan = GetChan(data)
				nick = GetNick(data)
				for row in cur.fetchall():
					id = row[0]
                                        cmd = row[1]
                                        action = row[2]
					type = row[3]
                                        
					if info[0] == cmd:
						if type == 'public':
							SendP(chan, nick + " -> " + action)
						if type == 'private':
							Notice(nick, action)
						if type == 'staff':
							Send(nick + " -> " + action)
				cur.close()
		
				#
				# Cmd list from database
				#

				if info[0] == 'cmds':
					db = MySQLdb.connect(host="localhost", user="xxxxx", passwd="xxxxxxx", db="xxxxxxx")
                                	cur = db.cursor()
                                	cur.execute("SELECT * FROM help_cmds")

					Notice(nick, "Commands Received from database")
					Notice(nick, "Type     | Command | Action ")
					for row in cur.fetchall():
                                        	id = row[0]
                                        	cmd = row[1]
                                        	action = row[2]
                                        	type = row[3]
						if type != 'staff':
							message = type + "  |  " + cmd + "  |  " + action
							Notice(nick, message)

					Notice(nick, "End of Commands")
                                cur.close()

				#
				# Staff Cmds From database
				#
			
                                if info[0] == 'scmds':
                                        db = MySQLdb.connect(host="localhost", user="xxxx", passwd="xxxxx", db="bdghelp")
                                        cur = db.cursor()
                                        cur.execute("SELECT * FROM help_cmds")

                                        Notice(nick, "Commands Received from database")
                                        Notice(nick, "Type     | Command | Action ")
                                        for row in cur.fetchall():
                                                id = row[0]
                                                cmd = row[1]
                                                action = row[2]
                                                type = row[3]
                                                if type == 'staff':
                                                        message = type + "  |  " + cmd + "  |  " + action
                                                        Notice(nick, message)

                                        Notice(nick, "End of Commands")
                                cur.close()


				#
				# Add cmd to mysql database
				# 

				if info[0] == 'addcmd':
					args = data.split('addcmd ')[1]
					arg = args.split('_')
					try:					
						arg[2] = arg[2].strip(' \n\r')
						query = "INSERT INTO help_cmds (id, cmd, action, type) VALUES (1, '" + arg[0] + "', '" + arg[1] + "', '" + arg[2] + "')"
						SendP(chan, "Done")
						cur = db.cursor()
						cur.execute(query)
						db.commit()
   						cur.close()
					except MySQLdb, e:
						print "Error %d: %s" % (e.args[0],e.args[1])
	 				except:
                                                Send("Invalid Parameters")

				#
				# Del cmd from database
				#

				if info[0] == 'delcmd':
					try:
						args = data.split('delcmd')[1]
						args = args.strip(" \t\n\r")
						query = "delete from help_cmds WHERE cmd='" + args + "'"
						SendP(chan, "Done")
						cur = db.cursor()
						cur.execute(query)
						db.commit()
						cur.close()
					except MySQLdb, e:
                                                print "Error %d: %s" % (e.args[0],e.args[1])
                                        except:
                                                Send("Invalid Parameters")
				



