﻿# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,urllib2,xbmcaddon,xbmc
__name__	= xbmcaddon.Addon().getAddonInfo("id")
debug 		= xbmcaddon.Addon().getSetting('debug_mode')

def getKey(item):
	return item[0]
	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-").replace('"',"").replace("’","'")
	title = title.strip()
	return title

def open_url(url, encoding='utf-8'):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
		req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
		return link
	except BaseException as e: log(u"open_url ERROR: %s - %s" % (str(url),str(e)))
	
def listsites(sitesfile):
	list = []
	ins = open(sitesfile, "r" )	
	for line in ins: 
		parameters = json.loads(line)
		url=parameters['site']
		enabled=parameters['enabled']		
		list.append(json.loads('{"url":"'+url+'","enabled":"'+enabled+'"}'))						
	return list

def readoneline(file):
	f = open(file,"r")
	line = f.read()
	f.close()
	return line

def readalllines(file):
	f = open(file,"r")
	lines = f.readlines()
	f.close()
	return lines

def readfiletoJSON(file):
	f = open(file,"r")
	line = f.read().strip('\n')
	f.close()	
	return line
	
def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()

def removecache(cachePath):
	try:
		for root,dir,files in os.walk(cachePath):
			for f in files:
				if not '_cache' in f: os.unlink(os.path.join(root, f))
		return language(30022).encode('utf-8')
	except BaseException as e: log(u"removecache ERROR: %s" % (str(e)))

def get_api_language():
	lang = xbmcaddon.Addon().getSetting('pref_language')	
	if lang == "system": lang = xbmc.getLanguage(xbmc.ISO_639_1)
	else: lang = xbmcaddon.Addon().getSetting('pref_language')
	return lang

def settings_open(id):
	import xbmc
	xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)
	
def _log(module, msg):
	s = u"#[%s] - %s" % (module, msg)
	xbmc.log(s.encode('utf-8'), level=xbmc.LOGDEBUG)

def log(msg):
	if debug == 'true': _log(__name__, msg)