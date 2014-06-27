#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
import socket
from urllib2 import urlopen, URLError, HTTPError
socket.setdefaulttimeout( 23 )  # timeout in seconds
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.tipolol'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
siteurl = 'http://tipolol.org'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'

#Expressões Regulares
catExpression = '<li id="menu-item-\d+" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-\d+"><a href="(.+?)">(.+?)</a></li>'
postExpression = '<h1 class="post-title">.+?<h3>Partilha nas redes sociais:</h3>'
postCatExpression = '<div class="span8 entry-video" style="margin-bottom:30px;">.+?<div class="divider-post span8"></div>'
postTitleExpression = '<h1 class="post-title"><a href=".+?" title=".+?" rel="bookmark">(.+?)</a>'
postPlotExpression = '<div class="entry-content">\s+<p>(.+?)</p><div class='
postUrlExpression = '<iframe.+?height="400".+?src="(.+?)"'
nextpageExpression = '<link rel="next" href="(.+?)" />'
pagesExpression = '<span class="pages">Page (\d+) of (\d+):</span>'
lastpageExpression = 'title="Last Page">(\d+)</a>'

################################################## 
#MENUS
def CATEGORIES():
	try :
		req = urllib2.Request(siteurl)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)	
	except HTTPError, e:
		addDir(str(e.code),siteurl,'',addonfolder+'/icon.png',False,1,'','')
		print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
	except URLError, e:
		addDir(str(e.reason),siteurl,'',addonfolder+'/icon.png',False,1,'','')
		print 'We failed to reach a server. Reason:', str(e.reason)
	else :
		addDir('[COLOR blue]Tipo LOL[/COLOR]',siteurl,'',addonfolder+'/icon.png',False,1,'','')
		addDir('',siteurl,'','',False,1,'','')		
		addDir('Últimos',siteurl,1,addonfolder+'/icon.png',True,1,'','')		
		addDir('Categorias',siteurl,2,addonfolder+'/icon.png',True,1,'','')	
		
##################################################
#FUNCOES
def listar_categorias(url):
	conteudo = abrir_url(url);
	link = re.findall(catExpression,conteudo,re.DOTALL)
	tamanho = len(link)
	for url,name in link:
		addDir(name,url,4,addonfolder+'/icon.png',True,tamanho,'','')		

def listar_videos(url):
	conteudo = abrir_url(url)	
	entry = re.findall(postExpression,conteudo,re.DOTALL)
	tamanho = len(entry)
	for entries in entry:	
		titulo = re.compile(postTitleExpression).findall(entries)
		plot = re.compile(postPlotExpression).findall(entries)
		url = re.compile(postUrlExpression).findall(entries)
		if url:
			size = ''
			if 'youtube' in url[0]:
				id_video = re.compile('//www.youtube.com/embed/(.+?)\?.+?').findall(url[0])
				if id_video: videoid = id_video[0]
				else: videoid=url[0].replace('//www.youtube.com/embed/','');				
				img = 'https://i1.ytimg.com/vi/'+videoid+'/hqdefault.jpg'
				urlfinal='plugin://plugin.video.youtube/?action=play_video&videoid='+videoid
				try:
					youtubeAPI = abrir_url('https://gdata.youtube.com/feeds/api/videos/'+videoid+'?v=2')	
					duration = re.compile('<yt:duration seconds=\'(\d+)\'/>').findall(youtubeAPI)
					if duration: size = duration[0]
				except: 
					urlfinal = ''
					pass
			elif 'dailymotion' in url[0]:
				match2 = re.compile('http://www.dailymotion.com/embed/video/(.+?)\?.+?').findall(url[0])
				if match2:
					urlfinal = url_solver('http://www.dailymotion.com/video/'+match2[0])
					img = 'http://www.dailymotion.com/thumbnail/video/'+match2[0]
					try:
						dailyAPI = abrir_url('https://api.dailymotion.com/video/'+match2[0]+'?fields=duration')	
						duration = re.compile('{"duration":(\d+)}').findall(dailyAPI)
						if duration: size = duration[0]				
					except: 
						urlfinal = ''					
						pass
			if img == '': img = addonfolder+'/icon.png'
			if not plot: plotresume = ''
			else: plotresume = plot[0].decode("utf-8")
			informacao = { "Title": titulo[0].decode("utf-8"), "plot": plotresume}	
			title = convert_title(titulo[0])
			if urlfinal <> '': addDir('[COLOR green]'+title+'[/COLOR]',urlfinal,3,img,False,tamanho,size,informacao)
	try:
		pages = re.compile(pagesExpression).findall(conteudo)
		for currentpage,lastpage in pages: numpages=currentpage+'/'+lastpage
	except: 
		numpages = ''
		pass
	link = re.compile(nextpageExpression).findall(conteudo)
	if link: addDir("[COLOR yellow](Página "+numpages+") Próxima >>[/COLOR]",link[0],1,'',True,1,'','')		

def listar_videos_cat(url):
	conteudo = abrir_url(url)	
	entry = re.findall(postCatExpression,conteudo,re.DOTALL)
	tamanho = len(entry)
	for entries in entry:	
		titulo = re.compile(postTitleExpression).findall(entries)
		plot = re.compile(postPlotExpression).findall(entries)
		url = re.compile(postUrlExpression).findall(entries)
		if url:
			size = ''
			if 'youtube' in url[0]:
				id_video = re.compile('//www.youtube.com/embed/(.+?)\?.+?').findall(url[0])
				if id_video: videoid = id_video[0]
				else: videoid=url[0].replace('//www.youtube.com/embed/','');				
				img = 'https://i1.ytimg.com/vi/'+videoid+'/hqdefault.jpg'
				urlfinal='plugin://plugin.video.youtube/?action=play_video&videoid='+videoid
				try:
					youtubeAPI = abrir_url('https://gdata.youtube.com/feeds/api/videos/'+videoid+'?v=2')	
					duration = re.compile('<yt:duration seconds=\'(\d+)\'/>').findall(youtubeAPI)
					if duration: size = duration[0]
				except: 
					urlfinal = ''
					pass
			elif 'dailymotion' in url[0]:
				match2 = re.compile('http://www.dailymotion.com/embed/video/(.+?)\?.+?').findall(url[0])
				if match2:
					urlfinal = url_solver('http://www.dailymotion.com/video/'+match2[0])
					img = 'http://www.dailymotion.com/thumbnail/video/'+match2[0]
					try:
						dailyAPI = abrir_url('https://api.dailymotion.com/video/'+match2[0]+'?fields=duration')	
						duration = re.compile('{"duration":(\d+)}').findall(dailyAPI)
						if duration: size = duration[0]				
					except: 
						urlfinal = ''					
						pass
			if img == '': img = addonfolder+'/icon.png'
			if not plot: plotresume = ''
			else: plotresume = plot[0].decode("utf-8")
			informacao = { "Title": titulo[0].decode("utf-8"), "plot": plotresume}	
			title = convert_title(titulo[0])
			if urlfinal <> '': addDir('[COLOR green]'+title+'[/COLOR]',urlfinal,3,img,False,tamanho,size,informacao)
	try:
		pages = re.compile(pagesExpression).findall(conteudo)
		for currentpage,lastpage in pages: numpages=currentpage+'/'+lastpage
	except: 
		numpages = ''
		pass
	link = re.compile(nextpageExpression).findall(conteudo)
	if link: addDir("[COLOR yellow](Página "+numpages+") Próxima >>[/COLOR]",link[0],1,'',True,1,'','')		

def convert_title(titulo):
	titulo = titulo.replace("&quot;","\"")
	return titulo
	
def url_solver(urlfinal):
	import urlresolver
	sources=[]
	hosted_media = urlresolver.HostedMediaFile(url=urlfinal)
	sources.append(hosted_media)
	source = urlresolver.choose_source(sources)
	if source: stream_url = source.resolve()
	else: stream_url = '-'
	return stream_url
	
def play(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass
			
######################################################FUNCOES JÁ FEITAS
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,pasta,total,duration=None,informacao=None):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+'/fanart.jpg')
	if informacao <> '': liz.setInfo( type="Video", infoLabels=informacao )	
	if duration <> '':
		liz.addStreamInfo('Video', {"duration":duration})	
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

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

#################################
#MODOS

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: listar_videos(url)
elif mode==2: listar_categorias(url)
elif mode==3: play(url)
elif mode==4: listar_videos_cat(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))