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

addon_id = 'plugin.video.tabrutal'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
siteurl = 'http://www.tabrutal.pt'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'

################################################## 
#MENUS
def CATEGORIES():
	try :
		req = urllib2.Request(siteurl)
		req.add_header('User-Agent', user_agent)
		response = urllib2.urlopen(req)	
		#response = urlopen( siteurl )
	except HTTPError, e:
		addDir(str(e.code),siteurl,'',addonfolder+'/icon.png',False,1,'','')
		print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
	except URLError, e:
		addDir(str(e.reason),siteurl,'',addonfolder+'/icon.png',False,1,'','')
		print 'We failed to reach a server. Reason:', str(e.reason)
	else :
		addDir('[COLOR blue]TÁ BRUTAL[/COLOR]',siteurl,'',addonfolder+'/icon.png',False,1,'','')
		addDir('',siteurl,'','',False,1,'','')		
		addDir('Últimos',siteurl,1,addonfolder+'/icon.png',True,1,'','')		
		addDir('Categorias',siteurl,2,addonfolder+'/icon.png',True,1,'','')	
		
##################################################
#FUNCOES
def listar_categorias(url):
	conteudo = abrir_url(url);
	entry = re.findall('<div class="top-menu">.+?<a href="http://www.tabrutal.pt/politica',conteudo,re.DOTALL)
	for entries in entry:
		link = re.compile('<a href="(.+?)">(.+?)</a>').findall(entries)
		tamanho = len(link)
		for url,name in link:
			if not 'Imagens' in name: addDir(name,url,1,addonfolder+'/icon.png',True,tamanho,'','')		

def listar_videos(url):
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True,1,'','')	
	conteudo = abrir_url(url)	
	entry = re.findall('<div class="fblike_button" style="margin: 10px 0;".+?data-layout="button_count" data-share="true"',conteudo,re.DOTALL)
	tamanho = len(entry)
	for entries in entry:	
		titulo = re.compile("<span st_title='(.+?)'").findall(entries)
		plot = re.compile('</iframe></div>\s+<p>(.+?)</p>').findall(entries)
		url = re.compile('<p><iframe.+?src="(.+?)"').findall(entries)
		urlfinal = ''
		img = ''
		size = ''
		if url:
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
					else: size = '';
				except:
					urlfinal='KT'
					pass
			elif 'sapo' in url[0]:
				url2 = re.compile('file=http://(.+?)/(.+?)/mov/').findall(url[0])
				for dominio,ID in url2:
					urlfinal = 'http://'+dominio+'/'+ID+'/mov/1'
					try:
						sapoAPI = abrir_url('http://videos.sapo.pt/'+ID)	
						duration = re.compile('<span class="lks">Dura&ccedil;&atilde;o:</span> (\d+):(\d+):(\d+)&nbsp;').findall(sapoAPI)
						for horas,minutos,segundos in duration:
							size = (int(segundos))+(int(minutos)*60)+(int(horas)*3600)
						imagem = re.compile('<meta property="og:image" content="(.+?)"/>').findall(sapoAPI)
						if imagem: img = imagem[0]		
					except:
						urlfinal='KT'
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
						urlfinal='KT'
						pass
			if img == '': img = addonfolder+'/icon.png'
			if not plot: plotresume = ''
			else: plotresume = plot[0].decode("utf-8")
			informacao = { "Title": titulo[0].decode("utf-8"), "plot": plotresume}	
			title = convert_title(titulo[0])
			if 'liveleak' in url[0]:
				try:
					liveleakAPI=abrir_url(url[0])	
					print liveleakAPI
					url= re.compile('file: "(.+?)"').findall(liveleakAPI)		
					urlfinal = url[0]
					image= re.compile('image: "(.+?)"').findall(liveleakAPI)
					img = image[0]
				except:
					urlfinal='KT'
					pass	
			elif 'vimeo' in url[0]:
				try:
					urlfinal = url_solver(url[0].replace('//player.vimeo.com/video/','http://www.vimeo.com/'))
					vimeoAPI=abrir_url('http://vimeo.com/api/v2/video/'+url[0].replace('//player.vimeo.com/video/','')+'.xml')	
					image= re.compile('<thumbnail_large>(.+?)</thumbnail_large>').findall(vimeoAPI)
					img = image[0]		
					duration = re.compile('<duration>(\d+)</duration>').findall(vimeoAPI)
					size = duration[0]				
				except:
					urlfinal='KT'
					pass		
			elif 'videolog' in url[0]:
				try:
					ID = re.compile('id_video=(.+?)&amp').findall(url[0])
					videoID = ID[0]
					urlfinal,img = getStreamUrlVL(videoID)
				except:
					urlfinal='KT'
					pass						
			if urlfinal <> 'KT': addDir('[COLOR green]'+title+'[/COLOR]',urlfinal,3,img,False,tamanho,size,informacao)
	pages = re.compile('<span class="pages">Page (.+?)</span>').findall(conteudo)
	numpages=pages[0].replace(' of ','/');	
	link = re.compile('<span class="current">\d+</span><a href="(.+?)" class="page" title="\d+">\d+</a>').findall(conteudo)
	if link: addDir("[COLOR yellow](Página "+numpages+") Próxima >>[/COLOR]",link[0],1,'',True,1,size,'')		

def getStreamUrlVL(id):
	content = abrir_url("http://videolog.tv/"+id)
	match = re.compile('<meta property="og:image" content="http://videos.videolog.tv/(.+?)/(.+?)/g_'+id+'_\d+').findall(content)
	image = re.compile('<meta property="og:image" content="(.+?)">').findall(content)
	for first,last in match: return 'http://videos.videolog.tv/'+first+'/'+last+'/'+id+'.mp4',image[0]

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

def addDir(name,url,mode,iconimage,pasta,total,duration,informacao):
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

xbmcplugin.endOfDirectory(int(sys.argv[1]))