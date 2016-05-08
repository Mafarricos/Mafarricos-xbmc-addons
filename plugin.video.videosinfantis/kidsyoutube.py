#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,sys,xbmcaddon,math,os,base64
import socket
from urllib2 import urlopen, URLError, HTTPError
socket.setdefaulttimeout( 23 )  # timeout in seconds

addon_id = 'plugin.video.videosinfantis'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
key = base64.urlsafe_b64decode('QUl6YVN5Q2FfYVgySmxQZEEtSWtsQ1ZQOGRVek1fSE14cjNKajVr')
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
nextItemFile 		= os.path.join(dataPath,'next.txt')
playlistFile 		= os.path.join(dataPath,'playlist.txt')

if not os.path.exists(dataPath): os.makedirs(dataPath)
###################################################MENUS

def CATEGORIESyou():
		content = abrir_url("https://raw.githubusercontent.com/Mafarricos/Mafarricos-xbmc-addons/master/files/canaisinfantis.txt")	
		channels = re.findall(':Canal:.+?:(.+?):End:',content,re.DOTALL)
		maxresults=50
		startindex=''
		addDir('[COLOR green]KIDS YOUTUBE[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False,1,'',maxresults,startindex,'')		
		addDir('[COLOR yellow]Inicio[/COLOR]','','','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')
		numero_de_canais = len(channels)	
		for channel in channels:
			try:
				content = abrir_url('https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id='+channel+'&key='+key)
				match = re.compile('"title": "(.+?)",').findall(content)
				picture = re.compile('high": {\s+"url": "(.+?)"').findall(content)			
				try: totalresults = re.compile('"videoCount": "(\d+)"').findall(content)
				except: totalresults = re.compile('"totalResults": "(\d+)"').findall(content)
				addDir(match[0]+' [COLOR blue]('+totalresults[0]+' Videos)[/COLOR]',channel,16,picture[0],True,numero_de_canais,'',maxresults,startindex,'')
			except: pass
def MenuCreate(name,url,maxresults,startindex):
		open(nextItemFile, 'w').close()
		listchannel(name,url,maxresults,startindex)
		#addDir('[COLOR green]'+name+'[/COLOR]',url,'',addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')			
		#addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
		#addDir('[COLOR yellow]Todos[/COLOR]',url,14,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')			
		#addDir('[COLOR yellow]Playlists[/COLOR]',url,17,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')					

def playlistListing(name,url,maxresults,startindex):
		content = abrir_url('https://gdata.youtube.com/feeds/api/users/'+url+'/playlists?max-results=50&start-index=1&v=2&orderby=published')
		match = re.compile('<name>(.+?)</name>').findall(content)				
		addDir('[COLOR green]'+match[0]+'[/COLOR]',url,'',addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')			
		addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
		entry = re.compile('<entry(.+?)</entry>').findall(content)
		numeroentries = len(entry)			
		if numeroentries == 0: addDir('[COLOR red]SEM PLAYLISTS[/COLOR]',url,'','http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',False,1,'',maxresults,startindex,'')			
		for entries in entry:
			countHit = re.findall('<yt:countHint>(\d+)</yt:countHint>',entries,re.DOTALL)
			name = re.findall('<title>(.+?)</title>',entries,re.DOTALL)
			url = re.findall('<link rel=\'alternate\' type=\'text/html\' href=\'(.+?)\'/>',entries,re.DOTALL)
			img = re.findall('name=\'mqdefault\'/><media:thumbnail url=\'(.+?)\'',entries,re.DOTALL)				
			if countHit[0]<>0: addDir(name[0]+' ('+countHit[0]+' Videos)',url[0],14,img[0],True,numeroentries,'',maxresults,startindex,'')						
			
def listchannel(name,url,maxresults,startindex):
	nextItem = readoneline(nextItemFile)
	open(playlistFile, 'w').close()
	addDir('[COLOR yellow]Inicio[/COLOR]',url,13,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True,1,'',maxresults,startindex,'')	
	addDir('[COLOR yellow]Criar Playlist[/COLOR]',url,15,addonfolder+artfolder+'iconKyou.png',False,1,'',maxresults,startindex,'')
	if 'playlist' in url:
		url3 = url.replace("https://www.youtube.com/playlist?list=","")
		content = abrir_url('https://gdata.youtube.com/feeds/api/playlists/'+url3+'?max-results='+str(maxresults)+'&start-index='+str(startindex)+'&v=2.1')	
	else: 
		idvideo = ''
		if nextItem == '': content1 = abrir_url('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='+url+'&maxResults='+str(maxresults)+'&key='+key)
		else: content1 = abrir_url('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='+url+'&maxResults='+str(maxresults)+'&key=AIzaSyCa_aX2JlPdA-IklCVP8dUzM_HMxr3Jj5k&pageToken='+nextItem)
		id_videos = re.findall('"videoId": "(.+?)"',content1,re.DOTALL)
		for id_video in id_videos: idvideo = idvideo + id_video+','
		idvideo = idvideo[:-1]
		content = abrir_url('https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id='+idvideo+'&key='+key)
	content = replacecontent(content)	
	entry = re.compile('"kind": "youtube#video",(.+?)"projection":').findall(content)	
	totalresults = re.compile('"totalResults": (\d+),').findall(content1)
	nextPageToken = re.compile('"nextPageToken": "(.+?)",').findall(content1)
	numero_de_videos = len(entry)
	totalpages = int(math.ceil(float(totalresults[0])/float(maxresults)))
	for entries in entry:
		titulo = re.findall('"title": "(.+?)",',entries,re.DOTALL)	
		id_video = re.findall('"id": "(.+?)"',entries,re.DOTALL)
		img = 'https://i.ytimg.com/vi/'+id_video[0]+'/hqdefault.jpg'		
		plot = re.findall('"description": "(.+?)",',entries,re.DOTALL)		
		url2='plugin://plugin.video.youtube/?action=play_video&videoid='+id_video[0]
		if not plot: plotresume = ''
		else: plotresume = plot[0].decode("utf-8")
		informacao = { "Title": titulo[0] , "plot": plotresume}
		duration = returnduration(entries)
		writefile(playlistFile,"a",'::'+titulo[0]+'::::'+id_video[0]+'::::'+str(duration)+'::\n') 
		addDir(titulo[0],url2,2,img,False,numero_de_videos,duration,'','',informacao)
	try: 
		writefile(nextItemFile,"w",nextPageToken[0])
		addDir('[COLOR yellow] Próxima >>[/COLOR]',url,14,addonfolder+artfolder+'iconKyou.png',True,1,'',maxresults,startindex,'')
	except: pass

def returnduration(entries):
	try:
		duration = 0
		time = re.findall('"duration": "PT(\d+)M(\d+)S"', entries, re.DOTALL)
		if time:
			for min,sec in time: duration = int(min)*60+int(sec)
		else:
			time = re.findall('"duration": "PT(\d+)M"', entries, re.DOTALL)
			if time: duration = int(time[0])*60
			else:
				time = re.findall('"duration": "PT(\d+)S"', entries, re.DOTALL)
				if time: duration = time[0]
	except: 
		duration = 60
		pass
	return duration
	
def replacecontent(content):
	content = content.replace("\n","")
	content = content.replace("\t","")	
	content = content.replace("\r","")	
	return content

def playlistchannel(name,url,maxresults,startindex):
	playlist = xbmc.PlayList(1)
	playlist.clear()	
	progress = xbmcgui.DialogProgress()
	progress.create('Videos Infantis', 'A Criar Playlist!')
	content = readalllines(playlistFile)
	for cont in content:
		items = re.findall('::(.+?)::::(.+?)::::(\d+)::',cont,re.DOTALL)
		titulo = items[0][0]
		url2='plugin://plugin.video.youtube/?action=play_video&videoid='+items[0][1]		
		listitem = xbmcgui.ListItem('[B][COLOR orange]' + titulo.decode("utf-8") + '[/COLOR][/B]', iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png") 
		listitem.setProperty('IsPlayable', 'true')			
		playlist.add(url2, listitem)	
	try:
		progress.close()
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except:
		pass
		self.message("Couldn't play item.")

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

def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()
	
def pesquisa(siteurl):
      keyb = xbmc.Keyboard('', 'Videos Infantis')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            urlfinal=siteurl+'?s=' + encode + '&x=0&y=0'
            listar_videos(urlfinal,siteurl)
			
######################################################FUNCOES JÁ FEITAS
		
def abrir_url(url,post=None):
	if post == None: req = urllib2.Request(url)
	else: req = urllib2.Request(url,post)
	req.add_header('User-Agent', user_agent)
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
	
def log(msg):
	_log(__name__, msg)

def _log(module, msg):
	s = u"#[%s] - %s" % (module, msg)
	xbmc.log(s.encode('utf-8'), level=xbmc.LOGDEBUG)
	
def addDir(name,url,mode,iconimage,pasta,total,duration,maxresults,startindex,informacao):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&maxresults="+str(maxresults)+"&startindex="+str(startindex)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+artfolder+'kidsyoutube.jpg')	
	if duration <> '':
		liz.addStreamInfo('Video', {"duration":duration})
	if informacao <> '':
		liz.setInfo( type="Video", infoLabels=informacao )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
        return ok

###############################GET PARAMS

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
maxresults=None
startindex=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: maxresults=int(params["maxresults"])
except: pass
try: startindex=int(params["startindex"])
except: pass