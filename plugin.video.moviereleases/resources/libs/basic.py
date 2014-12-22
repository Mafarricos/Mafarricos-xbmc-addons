# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,urllib2,xbmcaddon,xbmc,xbmcgui
__name__	= xbmcaddon.Addon().getAddonInfo("id")
addonName	= xbmcaddon.Addon().getAddonInfo("name")
debug 		= xbmcaddon.Addon().getSetting('debug_mode')
addonPath   = xbmcaddon.Addon().getAddonInfo("path")
language	= xbmcaddon.Addon().getLocalizedString
getSetting	= xbmcaddon.Addon().getSetting

def getKey(item):
	return item[0]
	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-").replace('"',"").replace("’","'")
	title = title.strip()
	return title
	
def open_url(url,post=None):
	if post == None: req = urllib2.Request(url)
	else: req = urllib2.Request(url,post)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	try: 
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link		
	except BaseException as e: log(u"open_url ERROR: %s - %s" % (str(url),str(e).decode('ascii','ignore')))		
	except urllib2.HTTPError, e: log(u"open_url HTTPERROR: %s - %s" % (str(url),str(e.code)))
	except urllib2.URLError, e: log(u"open_url URLERROR: %s - %s" % (str(url),str(e.reason)))
	except httplib.HTTPException, e: log(u"open_url HTTPException: %s" % (str(url)))
		
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

def library_movie_add(originalname, url, imdb_id, year):
	return ''
#        try:
#            if getSetting("check_library") == 'true': filter = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
#            filter = unicode(filter, 'utf-8', errors='ignore')
#            filter = json.loads(filter)['result']['movies']
#            filter = [i for i in filter if imdb in i['imdbnumber']][0]
#        except:
#            filter = []
#
#        try:
#            if not filter == []: return
#            if not xbmcvfs.exists(movieLibrary): xbmcvfs.mkdir(movieLibrary)
#
#            sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)
#            content = '%s?mode=2&originalname=%s&year=%s&imdb_id=%s&url=%s' % (sys.argv[0], originalname, year, imdb_id, url)
#
#            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
#            folder = os.path.join(movieLibrary, enc_name)
#            if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)

#            stream = os.path.join(folder, enc_name + '.strm')
#            file = xbmcvfs.File(stream, 'w')
#            file.write(str(content))
#            file.close()
#        except:
#            return


#	index().infoDialog(language(30309).encode("utf-8"), name)
#	if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
#		xbmc.executebuiltin('UpdateLibrary(video)')
		
def progressbar(progress,f,totalpass,message,message2=None,message3=None,normal=False):
	if normal: percent = int( ( f / float(totalpass) ) * 100)
	else: percent = int( ( int(totalpass)-f / float(totalpass) ) * 100)
	print '##eei',f,totalpass
	progress.update( percent, message, message2, message3 )
	if progress.iscanceled():
		progress.close()
		xbmcgui.Dialog().ok('ERROR','Cancelled.')
		return ''

def infoDialog(str, header=addonName):
	try: xbmcgui.Dialog().notification(header, str, addonPath+'icon.png', 3000, sound=False)
	except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonPath+'icon.png'))

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