# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib,urllib2,xbmcplugin,xbmcgui,xbmc,re,xbmcaddon,os

addonId             = xbmcaddon.Addon().getAddonInfo("id")
getSetting          = xbmcaddon.Addon().getSetting
language            = xbmcaddon.Addon().getLocalizedString

def MAIN():
	html = open_url('http://canal180.pt/#tv-contents')
	#print html
	data = re.findall('<li class="shadow item curated-by  background-image" style="background-image:url\(\'(.+?)\'\);">\s+<a href="(.+?)"rel="portfolio" data-title-id=".+?">\s+<div class="overlay">\s+<h3>(.+?)</h3>', html, re.DOTALL)
	for thumb,url,title in data:
		addDir(title.strip(),url,1,thumb,True,0,'')

def playlist(url):
	html = open_url(url)
	data = re.findall('<a class="rsImg" href="(.+?)" data-rsVideo="(.+?)">(.+?)</a>', html, re.DOTALL)
	for thumb,url,title in data:
		addDir(title,url,2,thumb,False,0,'')

def open_url(url,type=None):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def play(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url.replace('https://vimeo.com/','plugin://plugin.video.vimeo/play/?video_id=').replace('http://vimeo.com/','plugin://plugin.video.vimeo/play/?video_id='),xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass

def addDir(name,url,mode,iconimage,pasta,duration,informacao):
	context = []
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if duration <> '': liz.addStreamInfo('Video', {"duration":duration})
	context.append((language(30016).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=2&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(context, replaceItems=False) 	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
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
elif mode==1: playlist(url)
elif mode==2: play(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))