# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib,urllib2,xbmcplugin,xbmcgui,xbmc,re

def MAIN():
	html = open_url('http://jell.yfish.us/')
	data = re.findall('<td class="file"><a href="(.+?)">(.+?)</a></td>\s+<td>(.+?)</td>\s+<td>(\d+) <span class="faded">Mbps</span></td>\s+<td><b>(\d+)</b> <span class="faded">Mbps</span></td>\s+<td>(\d+) <span class="faded">Mbps</span></td>\s+<td>:(\d+)</td>\s+<td>(\d+) <span class="faded">MB</span></td>', html, re.DOTALL)
	for url,name,profile,bitmin,bitavg,bitmax,seconds,size in data:
		informacao = { "Title": name}			
		addDir(name+' [Profile Level:'+profile+', Bitrate Min:'+bitmin+' Mbps, Bitrate Avg:'+bitavg+' Mbps, Bitrate Max.:'+bitmax+' Mbps, Size:'+size+' MB]','http://jell.yfish.us/'+url,1,'',False,seconds,informacao)	
	original = re.findall('<table id="original" cellpadding="0" cellspacing="0">(.+?)</table>', html, re.DOTALL)
	urlname = re.findall('<td class="file"><a href="(.+?)">(.+?)</a></td>', original[0], re.DOTALL)
	for url,name in urlname:
		urltext=url
		nametext=name
	profile = re.findall('<td class="profile">(.+?)</td>', original[0], re.DOTALL)
	bitmin = re.findall('<td class="bitrate">(\d+) <span class="faded">Mbps</span></td>', original[0], re.DOTALL)
	bitmavg = re.findall('<td class="bitrate"><b>(\d+)</b> <span class="faded">Mbps</span></td>', original[0], re.DOTALL)
	bitmax = re.findall('<td class="bitrate">(\d+) <span class="faded">Mbps</span></td>', original[0], re.DOTALL)	
	seconds = re.findall('<td class="runtime">:(\d+)</td>', original[0], re.DOTALL)	
	size = re.findall('<td class="size">(\d+) <span class="faded">MB</span></td>', original[0], re.DOTALL)	
	informacao = { "Title": name}			
	addDir(nametext+' [Profile Level:'+profile[0]+', Bitrate Min:'+bitmin[0]+' Mbps, Bitrate Avg:'+bitavg[0]+' Mbps, Bitrate Max.:'+bitmax[0]+' Mbps, Size:'+size[0]+' MB]','http://jell.yfish.us/'+urltext,1,'',False,seconds[0],informacao)	

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
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass

def addDir(name,url,mode,iconimage,pasta,duration,informacao):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if informacao <> '': liz.setInfo( type="Video", infoLabels=informacao )	
	if duration <> '':
		liz.addStreamInfo('Video', {"duration":duration})	
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
elif mode==1: play(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))