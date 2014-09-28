#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
import socket
from urllib2 import urlopen, URLError, HTTPError
socket.setdefaulttimeout( 23 )  # timeout in seconds
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.sicnoticias'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
#siteurlID = selfAddon.getSetting('site-view')
listagemID = selfAddon.getSetting('list-view')
if listagemID == '0':listagemtext='Todos (Vídeos e Texto)'
if listagemID == '1':listagemtext='Apenas Vídeos'
if listagemID == '2':listagemtext='Apenas Texto'
siteurl = 'http://sicnoticias.sapo.pt'
	
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'


################################################## 
#MENUS

def CATEGORIES():
	addDir('Última Edição',siteurl+'/ultima-edicao',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)
	addDir('País',siteurl+'/pais',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)
	addDir('Mundo',siteurl+'/mundo',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)
	addDir('Economia',siteurl+'/economia',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)		
	addDir('Desporto',siteurl+'/desporto',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)	
	addDir('Cultura',siteurl+'/cultura',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)	
	addDir('Opinião',siteurl+'/opiniao',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)		
	addDir('Em Vídeo',siteurl+'/noticias/em-video',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)		
	addDir('Premium',siteurl+'/premium',1,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)	
	addDir('','','','',False)			
	addDir('Programas',siteurl+'/programas',3,'http://digitalsherpa.com/wp-content/uploads/2013/04/social-media-marketing-tool.png',True)			
	addDir('','','','',False)		
	addDir('(Fonte: '+siteurl+' Listagem: ['+listagemtext+'])','','','',False)
	#addDir('[COLOR blue]Definições[/COLOR]',siteurl,7,'',False)	
##################################################
#FUNCOES
def pesquisa():
      keyb = xbmc.Keyboard('', 'Sic Noticias')
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote(search)
            urlfinal=siteurl+'?s=' + encode + '&x=0&y=0'
            listar_videos(urlfinal)

def reconstruct_list_videos(match,level):
	url = re.findall('data-src="(.+?)"',match[0],re.DOTALL)
	img = re.findall('data-thumbnail="(.+?)"',match[0],re.DOTALL)
	titulo = re.findall('data-title="(.+?)"',match[0],re.DOTALL)
	duracao = re.findall('<div class="durationContainer"> <span>(.+?)</span>',match[0],re.DOTALL)
	data = re.findall('<div class="dateContainer publishedDate"> <span>(.+?)</span>',match[0],re.DOTALL)
	if url[0] <> 'null' and listagemID <> '2':
		url[0] = url[0].replace('http://videos.cdn.impresa.pt/premium/sicnot/','http://wcm.cdn.impresa.pt/premium/sicnot/')
		premium = re.compile('http://wcm.cdn.impresa.pt/(.+?)/sicnot/').findall(url[0])
		if premium:				
			addDir('[COLOR green]'+data[0]+':[/COLOR] [COLOR red][UPPERCASE]'+premium[0]+':[/UPPERCASE][/COLOR] '+subststring(titulo[0])+' ('+duracao[0]+')',url[0],2,img[0],False)
		else:
			addDir('[COLOR green]'+data[0]+':[/COLOR] '+subststring(titulo[0])+' ('+duracao[0]+')',url[0],2,img[0],False)
	elif listagemID == '0' or listagemID == '2':
		urllink = re.findall('<div class="imageContainer landscape"> <a href="(.+?)" class="">',match[0],re.DOTALL)
		codigo_fonte = abrir_url(siteurl+urllink[0])	
		texto = re.findall('<div class="bodyContainer text">(.+?)</div>',codigo_fonte,re.DOTALL)
		if texto:
			titulo[0]=subststring(titulo[0]) 
			texto[0] = format_texto(texto[0])			
			addDir('[COLOR green]'+data[0]+':[/COLOR][COLOR orange] (Apenas Texto)[/COLOR] '+titulo[0],texto[0],6,img[0],False)
	if level == 1:
		match[0] = match[0]+'<div class="sideColumn'	
		next = re.findall('</div> </div> </div> </div> <div id="(.+?)<div class="sideColumn', match[0], re.DOTALL)
	elif level == 2:
		match[0] = match[0]+'Mais Artigos'	
		next = re.findall('</div> </div> </div> </div> <div id="(.+?)Mais Artigos', match[0], re.DOTALL)		
	if next:
		reconstruct_list_videos(next,level)
	else:
		return

def reconstruct_list_programs(match):
	print match[0]
	img = re.findall('data-thumbnail="(.+?)"',match[0],re.DOTALL)
	url = re.findall('<h3> <a href="(.+?)">.+?</a> </h3>',match[0],re.DOTALL)
	titulo = re.findall('<h3> <a href=".+?">(.+?)</a> </h3>',match[0],re.DOTALL)	
	if url[0] <> 'null':
		addDir('[COLOR green]'+subststring(titulo[0])+'[/COLOR] ',siteurl+url[0],1,img[0],True)
	match[0] = match[0]+'</span> </div> </div> </div> </div> </div> <script type="text/javascript">'	
	next = re.findall('</span> </div> </div> </div> </div> <div id="(.+?)</span> </div> </div> </div> </div> </div> <script type="text/javascript">', match[0], re.DOTALL)
	if next:
		reconstruct_list_programs(next)
	else:
		return
		
def listar_videosBeta(url):
	codigo_fonte = abrir_url(url)	
	tituloSic = re.compile('<title>(.+?)</title>').findall(codigo_fonte)
	if tituloSic:
		addDir('[B][UPPERCASE][COLOR gray]'+tituloSic[0]+'[/COLOR][/UPPERCASE][/B]','','','',False)	
	else:
		tituloP = re.compile('data-sectionname="(.+?)"').findall(codigo_fonte)
		if tituloP:
			addDir('[B][UPPERCASE][COLOR gray]'+tituloP[0]+'[/COLOR][/UPPERCASE][/B]','','','',False)	
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True)	
	match=re.findall('PortalCommon.reloadToggle(.+?)<div class="sideColumn', codigo_fonte, re.DOTALL)
	if match:
		reconstruct_list_videos(match,1)
	else:
		match=re.findall('PortalCommon.reloadToggle(.+?)Mais Artigos', codigo_fonte, re.DOTALL)
		if match:
			reconstruct_list_videos(match,2)
		else:
			addDir('[B][UPPERCASE][COLOR red]Secção sem videos[/COLOR][/UPPERCASE][/B]','','','',False)	
	#Get Next Page
	match = re.compile('class="nextSelector" href="(.+?)">Mais Artigos</a>').findall(codigo_fonte)	
	if match:
		match2 = re.compile('"&section=(.+?)"').findall(codigo_fonte)
		if match2:
			addDir('[COLOR yellow]Seguinte >>[/COLOR]',match[0]+'&section='+subststringSpace(match2[0]),1,'',True)			
		else:
			addDir('[COLOR yellow]Seguinte >>[/COLOR]',match[0],1,'',True)

def listar_programasBeta(url):
	codigo_fonte = abrir_url(url)
	addDir('[B][UPPERCASE][COLOR gray]'+name+'[/COLOR][/UPPERCASE][/B]','','','',False)		
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True)	
	addDir('','','','',False)	
	match = re.compile('class="portlet-title" value="Programas de A - Z"(.+?)</span> </div> </div> </div> </div> </div> <script type="text/javascript">').findall(codigo_fonte)	
	if match:
		print match[0]
		reconstruct_list_programs(match)

def play(url,name):
  listitem = xbmcgui.ListItem()
  listitem.setPath(url)
  listitem.setInfo('video', {'Title': name})
  listitem.setProperty('IsPlayable', 'true')
  try:
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(url)
  except:
   pass
   self.message("Couldn't play item.")
			
def subststring(titulo):
	titulo = titulo.replace('&quot;','"')		
	titulo = titulo.replace('&#034;','"')		
	titulo = titulo.replace('&#039;','')		
	titulo = titulo.replace('&#x27;s','')			
	return titulo

def subststringSpace(titulo):
	titulo = titulo.replace(' ','%20')		
	return titulo
	
def format_texto(texto):
	texto = texto.replace('</p>','\n')
	texto = texto.replace('<p>','\n')
	texto = texto.replace('&quot;','"')	
	texto = texto.replace('<em>','')		
	texto = texto.replace('</em>','')			
	return texto
	
def listar_texto(name,url):
	TextBoxes(name,url) 

########sicnoticias.videos.pt

def listar_videos(url):
	print 'listar_videos'
	codigo_fonte = abrir_url(url)	
	tituloSic = re.compile('title="sicnot - (.+?)"').findall(codigo_fonte)
	if tituloSic:
		addDir('[B][UPPERCASE][COLOR gray]'+tituloSic[0]+'[/COLOR][/UPPERCASE][/B]','','','',False)	
	else:
		tituloP = re.compile('SUN-(.+?) AT').findall(codigo_fonte)
		if tituloP:
			addDir('[B][UPPERCASE][COLOR gray]'+tituloP[0]+'[/COLOR][/UPPERCASE][/B]','','','',False)		
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True)	
	match = re.compile('<a href=\'(.+?)\'>\n<img title=\'(.+?)\' height=\'\d+\' alt=\'.+?\' width=\'\d+\' src=\'(.+?)w80/\'/>').findall(codigo_fonte)
	if not match:
		match = re.compile('<a href=\'(.+?)\'>\n<img title=\'(.+?)\' height=\'\d+\' alt=\'.+?\' width=\'\d+\' src=\'(.+?)w220/\'/>').findall(codigo_fonte)	
		if not match:
			match = re.compile('<a href=\'(.+?)\'>\n<img title=\'(.+?)\' height=\'\d+\' alt=\'.+?\' width=\'\d+\' src=\'(.+?)w220.+?/\'/>').findall(codigo_fonte)	
			if not match:
				match = re.compile('<a href=\'(.+?)\'>\n<img title=\'(.+?)\' height=\'\d+\' alt=\'.+?\' width=\'\d+\' src=\'(.+?)w130.+?/\'/>').findall(codigo_fonte)			
	for url2,titulo,img in match:
		url3,data,texto = encontrar_tipo_da_fonte(url2)
		if texto <> '-':
			titulo = subststring(titulo)		
			addDir(data+' [COLOR orange](Apenas Texto)[/COLOR] '+titulo,texto,6,img+'w220',False)
		elif url3 <> 'notfound' and listagemID <> '2':
			titulo = subststring(titulo)
			premium = re.compile('http://wcm.cdn.impresa.pt/(.+?)/sicnot/').findall(url3)
			if premium:	
				addDir(data+'[UPPERCASE][COLOR red]'+premium[0]+' [/COLOR][/UPPERCASE]'+titulo,url3,2,img+'w220',False)
			else:
				addDir(data+titulo,url3,2,img+'w220',False)
		
	match = re.compile('<div onclick=\'\' class=\'nextPage\'>\s+<a href=\'(.+?)\'>').findall(codigo_fonte)	
	if match:
		nexturl = match[0]
		matchnum = re.compile('<span class="pageX">(\d+)</span> de <span class="pageY">(\d+)</span>').findall(codigo_fonte)
		for pageX,pageY in matchnum:
			addDir('[COLOR yellow]'+pageX+' de '+pageY+'[/COLOR]','','','',False)							
		addDir('[COLOR yellow]Seguinte >>[/COLOR]',nexturl,4,'',True)
	else:
		match = re.compile('<div class=\'text\'>\n</div>\n</div>\n</div>\n<div id=\'listagem(\d+)-index-\d+\'').findall(codigo_fonte)	
		if match:
			match2 = re.compile('<div onclick=\'\' class=\'pageNumberItem disabled current\'>\n<span class=\'name\'>\n(.+?)\n</span>').findall(codigo_fonte)			
			if match2:
				match3 = re.compile('(.+?)pageIndex.+?').findall(url)
				if match3:
					countm = match2[0]
					#nexturl = match3[0]+'pageIndex'+match[0]+'='+str(int(countm)+1)
					nexturl = match3[0]+'pageIndex'+match[0]+'='+match2[0]
				else:
					countm = match2[0]
					programas = re.compile('programas').findall(url)
					if programas:	
						nexturl = url+'&pageIndex'+match[0]+'='+match2[0]
					else:
						nexturl = url+'&pageIndex'+match[0]+'='+str(int(countm)+1)
					#nexturl = url+'&pageIndex'+match[0]+'='+match2[0]
				matchnum = re.compile('<span class="pageX">(\d+)</span> de <span class="pageY">(\d+)</span>').findall(codigo_fonte)
				for pageX,pageY in matchnum:
					addDir('[COLOR yellow]'+pageX+' de '+pageY+'[/COLOR]','','','',False)					
				addDir('[COLOR yellow]Seguinte >>[/COLOR]',nexturl,4,'',True)	

def listar_programas(url):
	codigo_fonte = abrir_url(url)
	addDir('[B][UPPERCASE][COLOR gray]'+name+'[/COLOR][/UPPERCASE][/B]','','','',False)		
	addDir('[COLOR yellow]Inicio[/COLOR]','',0,'',True)	
	addDir('','','','',False)	
	match = re.compile('<li>\n<div class="Name">\n<a href="(.+?)" class=" ">\n(.+?)\n</a>\n</div>\n</li>').findall(codigo_fonte)	
	for url,titulo in match:
		titulo = subststring(titulo)
		codigo_fonte = abrir_url(url)
		match = re.compile('<li id="tabs-1-1">\n<a href="(.+?)" class="tabMenuItem"><span>').findall(codigo_fonte)	
		if match:
			print match[0]
			addDir(titulo,match[0],4,'',True)	
					
def encontrar_tipo_da_fonte(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('file:\'(.+?)\'').findall(codigo_fonte)
	if match:
		match2 = re.compile('<p class="publishedDate">\n(.+?)\n</p>').findall(codigo_fonte)
		if match2:
			return match[0],' [COLOR green]'+match2[0]+': [/COLOR]','-'
	elif listagemID == '0' or listagemID == '2':
		codigo_fonte = codigo_fonte.replace('\n','')
		match3 = re.compile('<div class="widget storyContent article widget-editable viziwyg-section-58 inpage-widget-548" ><div class="body ">(.+?)</div>').findall(codigo_fonte)
		if match3:
			match3[0]=format_texto(match3[0])
			match2 = re.compile('<p class="publishedDate">(.+?)</p>').findall(codigo_fonte)
			if match2:
				return '-',' [COLOR green]'+match2[0]+': [/COLOR]',match3[0]
	return 'notfound','-','-'

#####################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addDir(name,url,mode,iconimage,pasta):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
        return ok
		
def TextBoxes(heading,anounce):
	class TextBox():
		"""Thanks to BSTRDMKR for this code:)"""
		# constants
		WINDOW = 10147		
		CONTROL_LABEL = 1
		CONTROL_TEXTBOX = 5
		
		def __init__( self, *args, **kwargs):
			# activate the text viewer window
			xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
			# get window
			self.win = xbmcgui.Window( self.WINDOW )
			# give window time to initialize
			xbmc.sleep( 500 )
			self.setControls()

		def setControls( self ):
			# set heading
			self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
			self.win.getControl( self.CONTROL_TEXTBOX ).setText(anounce)
			return
	TextBox()

##############################
#GET PARAMS

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


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

#################################
#MODOS

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: listar_videosBeta(url)
elif mode==2: play(url,name)
elif mode==3: listar_programasBeta(url)
elif mode==4: listar_videos(url)
elif mode==5: listar_programas(url)
elif mode==6: listar_texto(name,url)
elif mode==7: 
	selfAddon.openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))