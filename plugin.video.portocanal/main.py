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

addon_id = 'plugin.video.portocanal'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
siteurl = 'http://www.portocanal.sapo.pt'
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
		addDir(str(e.code),siteurl,'',addonfolder+'/icon.png',False,1)
		print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
	except URLError, e:
		addDir(str(e.reason),siteurl,'',addonfolder+'/icon.png',False,1)
		print 'We failed to reach a server. Reason:', str(e.reason)
	else :
		addDir('[COLOR blue]PORTO[/COLOR] CANAL',siteurl,'',addonfolder+'/icon.png',False,1)
		addDir('',siteurl,'','',False,1)		
		addDir('Noticias',siteurl+'/ultimas/',1,addonfolder+'/icon.png',True,1)		
		addDir('Programas',siteurl+'/programas/',2,addonfolder+'/icon.png',True,1)	
		
##################################################
#FUNCOES
def listar_categorias_noticias(url):
	conteudo = abrir_url(url);
	entry = re.findall('<div class="menu_seccoes_noticias menu_seccoes_noticias_desktop">.+?</div>',conteudo,re.DOTALL)
	for entries in entry:
		link = re.compile('<li><a data-link="expandir" href="(.+?)">(.+?)</a></li>').findall(entries)
		tamanho = len(link)
		addDir("[COLOR blue]FC PORTO[/COLOR]",siteurl+'/videos/noticias/7',3,'http://www.fcporto.pt/_layouts/STYLES/FCPorto.Internet.UI/images/header/logo.png',True,tamanho)	
		addDir("ÚLTIMAS",siteurl+'/videos/noticias/',3,'http://www.fcporto.pt/_layouts/STYLES/FCPorto.Internet.UI/images/header/logo.png',True,tamanho)			
		for url,name in link:
			if not 'pesquisa' in url:
				addDir(h.unescape(name).encode("utf-8"),siteurl+'/videos'+url,3,addonfolder+'/icon.png',True,tamanho)		

def listar_categorias_programas(url):
	conteudo = abrir_url(url);
	entry = re.findall('<nav class="programasSelect">.+?</nav>',conteudo,re.DOTALL)
	for entries in entry:
		link = re.compile('<option value="(\d+)"><p>(.+?)</p></option>').findall(entries)
		tamanho = len(link)
		for url,name in link:
			addDir(h.unescape(name).encode("utf-8"),siteurl+'/videos/programas/'+url,3,'http://portocanal.sapo.pt/uploads/cursos/curso_0000'+url+'_00002.jpg',True,tamanho)		
			
def listar_videos(url):
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True,1)			
	conteudo = abrir_url(url)	
	entry = re.findall('<div class="videosBarraNegra" id="v">.+?<footer class="footer">',conteudo,re.DOTALL)
	print str(len(entry))
	for entries in entry:	
		link = re.compile('<div class="videoJanelaUmItem">\s+<a href="(.+?)" title="(.+?)"><figure data-idVideo=".+?" class="videosVODLink"><img src="(.+?)" alt="" /></figure></a>\s+<div class="videoJanelaUmItemTitulo"><a href=".+?"></a></div>\s+<div class="videoJanelaUmItemResumo">.+?</div>\s+<div class="videoJanelaUmItemData">(.+?)</div>').findall(entries)
		if not link:
			link = re.compile('<div class="videoJanelaUmItem">\s+<a href="(.+?)" title="(.+?)"><figure data-idVideo=".+?" class="videosVODLink"><img src="(.+?)" alt=".+?" /></figure></a>\s+<div class="videoJanelaUmItemTitulo"><a href=".+?">.+?</a></div>\s+<div class="videoJanelaUmItemResumo">.+?</div>\s+<div class="videoJanelaUmItemData">(.+?)</div>').findall(entries)
		tamanho = len(link)
		for url,name,img,data in link:
			addDir('[COLOR orange]'+data+'[COLOR] - [COLOR green]'+h.unescape(name).encode("utf-8")+'[/COLOR]',siteurl+url,4,img,False,tamanho)
		link = re.compile('<span class="reyterPaginadorSeguinte"><a data-link="expandir" href="(.+?)">></a></span>').findall(entries)
		if link:
			addDir("[COLOR yellow]Próxima >>[/COLOR]",siteurl+link[0],3,'',True,1)		
			
def resolver_fonte(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('file=(.+?)/mov/.+?"').findall(codigo_fonte)
	if match:
		return match[0]+'/mov'
		
def play(url):
  url=resolver_fonte(url)
  listitem = xbmcgui.ListItem()  
  listitem.setPath(url)
  listitem.setProperty('IsPlayable', 'true')
  try:
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(url)
  except:
   pass
   #self.message("Couldn't play item.")
			
######################################################FUNCOES JÁ FEITAS
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,pasta,total):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+'/fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
        return ok
		
###############################GET PARAMS
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
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
elif mode==1: listar_categorias_noticias(url)
elif mode==2: listar_categorias_programas(url)
elif mode==3: listar_videos(url)
elif mode==4: play(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))