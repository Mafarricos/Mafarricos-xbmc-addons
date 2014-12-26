# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,xbmcaddon,xbmcgui
addonName	= xbmcaddon.Addon().getAddonInfo("name")
addonPath   = xbmcaddon.Addon().getAddonInfo("path")

def open_url(url,post=None,headers=None):
	try:
		if not post:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
			req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		else:
			req = urllib2.Request(url,post,headers)
		response = urllib2.urlopen(req,timeout=15)
		link=response.read()
		response.close()
		return link
	except BaseException as e: print '##ERROR-addonsresolver:open_url: '+str(url)+' '+str(e)
	
def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()
	
def readoneline(file):
	f = open(file,"r")
	line = f.read()
	f.close()
	return line
	
def infoDialog(str, header=addonName):
	try: xbmcgui.Dialog().notification(header, str, addonPath+'icon.png', 3000, sound=False)
	except: xbmc.executebuiltin("Notification(%s,%s, 6000, %s)" % (header, str, addonPath+'icon.png'))