#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib,xbmcplugin,xbmcgui,xbmc,xbmcaddon
from lib import util

addon_id = 'plugin.video.funvideos'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'

def MAIN(index=None):
	if not index: index = 0
	else: index = int(index) + 1
	unique_stuff = util.getpages(index)
	total = len(unique_stuff)
	for link in unique_stuff:
		try: title = link['title'].decode("utf-8")
		except: 
			title = link['title'].encode('ascii', 'ignore')
			pass
		informacao = { "Title": title}	
		addDir(title+' [COLOR yellow]['+link['prettyname']+'][/COLOR]',link['url'],1,link['thumbnail'],False,total,link['duration'],informacao,index)
	addDir('Seguinte >>','next',2,'',True,1,'','',index)		

def play(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass

def addDir(name,url,mode,iconimage,pasta,total,duration,informacao,index):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&index="+str(index)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+'/fanart.jpg')
	if informacao <> '': liz.setInfo( type="Video", infoLabels=informacao )	
	if duration <> '':
		liz.addStreamInfo('Video', {"duration":duration})	
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
        return ok
		
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
      
params=get_params()
url=None
name=None
mode=None
iconimage=None
index=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)

if mode==None or url==None or len(url)<1: MAIN()
elif mode==1: play(url)
elif mode==2: MAIN(index)
xbmcplugin.endOfDirectory(int(sys.argv[1]))