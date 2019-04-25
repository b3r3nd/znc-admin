#!/usr/bin/python

# @project 	Daffy
# @name 	pythonzncadmin.py
# @description	Pyhon ZNC Admin
# @authors 	b3r3nd
# @version 	1.1
# @date 	-

import znc

def SendChan(self, chan, msg):
	self.PutIRC("PRIVMSG " + chan + " :" + msg)

def SendNotice(self, nick, msg):
	self.PutIRC("NOTICE " + nick + " :" + msg)

class pythonzncadmin(znc.Module):
	description = "Daffy - Python ZNC Admin"

	# Only ZNC Admins can load this module
	def OnLoad(self, args, message):
		user = self.GetUser().GetUserName()
		ZNC = znc.CZNC().Get().FindUser(user)
		if ZNC is None:
			return False
		if ZNC.IsAdmin() == True:
			return True
		return False

	def OnChanMsg(self, nick, channel, message):
		if (message.s).index("$") == 0:
			args = (message.s).split(' ')
			cmd = args[0][1:].lower()
			chan = channel.GetName()
			nickname = nick.GetNick()

		# Version
		if cmd == "version":
			version = znc.CZNC.GetTag()
			SendNotice(self, nickname, version)
			SendNotice(self, nickname, "By berend & Brainscrewer")

		# Uptime
		if cmd == "uptime":
			ZNC = znc.CZNC.Get()
			uptime = ZNC.GetUptime()
			SendNotice(self, nickname, "Uptime: " + uptime)

		# Global ZNC Information
		# Displayed in CTable
		if cmd == "zncinfo":
			ZNC = znc.CZNC.Get()
			paths = ["Home Path_" + ZNC.GetHomePath(), "Cur Path_" + ZNC.GetCurPath(), 
				"User Path_" + ZNC.GetUserPath(), "Config Path_" + ZNC.GetConfPath()]

			info = ["Status Prefix_" + ZNC.GetStatusPrefix(), "ZNC Skin_" + ZNC.GetSkinName(), 
				"Max Buffer_" + str(ZNC.GetMaxBufferSize()), "Server Throttle_" + str(ZNC.GetServerThrottle()),
				"Connect Delay_" + str(ZNC.GetConnectDelay()), "Anon IP Limit_" + str(ZNC.GetAnonIPLimit())]

			table = znc.CTable()
			table.AddColumn("Setting")
			table.AddColumn("Value")

			for item in paths:
				item = item.split("_")
				table.AddRow()
				table.SetCell("Setting", item[0])
				table.SetCell("Value", item[1])

			for item2 in info:
				item2 = item2.split("_")
				table.AddRow()
				table.SetCell("Setting", item2[0])
				table.SetCell("Value", item2[1])

			id = 0
			line = znc.String()
			while table.GetLine(id, line):
				id += 1
				SendNotice(self, nickname, line.s)

		# Specific User Information
		# Displayed in CTable
		if cmd == "info":
			if len(args) == 2:
				user = args[1]
				ZNC = znc.CZNC.Get().FindUser(user)
				if ZNC is None:
					SendNotice(self, nickname, "No such User: " + args[1])
				else:
					info = ["Username_" + ZNC.GetUserName(), "Nick_" + ZNC.GetNick(), "AltNick_" + ZNC.GetAltNick(),
						"Ident_" + ZNC.GetIdent(), "RealName_" + ZNC.GetRealName(), "IsAdmin_" + str(ZNC.IsAdmin()), 
						"Connected_" + str(ZNC.IsUserAttached())]

					table = znc.CTable()
					table.AddColumn("Setting")
					table.AddColumn("Value")

					for item in info:
						item = item.split("_")
						table.AddRow()
						table.SetCell("Setting", item[0])
						table.SetCell("Value", item[1])

					id = 0
					line = znc.String()
					while table.GetLine(id, line):
						id += 1
						SendNotice(self, nickname, line.s)

			else:
				SendNotice(self, nickname, "Invalid Parameters: info <zncname>")

		if cmd == "adduser":
			if len(args) == 4:
				zncUser = znc.String()
				zncUser = args[1]
				sendUser = args[2]
				pWord = args[3]
				ZNC = znc.CZNC.Get().FindUser(zncUser)
				if ZNC is None:
					SendChan(self, chan, "none")
					sError = znc.String()
					SendChan(self, chan, "string")

					User = znc.CUser(zncUser)
					SendChan(self, chan, zncUser)
					Salt = znc.String()
					Salt = znc.CUtils.GetSalt()
					SendChan(self, chan, "GetSalt")

					#SaltPass = znc.CUser.SaltedHash(pWord, Salt)
					#SendChan(self, chan, SaltPass)
					SendChan(self, chan, Salt)

					#User.SetPass(znc.CUser.SaltedHash(pWord, Salt), znc.CUser.HASH_DEFAULT, Salt)
					User.SetNick(zncUser)
					SendChan(self, chan, "setpass")

					znc.CZNC.Get().AddUser(User, sError)
					SendChan(self, chan, "Added!")
					SendChan(self, chan, sError.s)

					rError = znc.String()
					znc.CZNC.Get().WriteConfig()
					SendChan(self, chan, "Write Conf")
					SendChan(self, chan, rError)

				else:
					SendChan(self, chan, "exist")

			SendChan(self, chan, "done")


		return znc.CONTINUE

