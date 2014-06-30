#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,os,xbmcvfs,re

addon_id = 'script.maintenance.management'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
scriptsfolder = '/resources/scripts/'
artsfolder = '/resources/img/'
mensagemok = xbmcgui.Dialog().ok
mensagemyesno = xbmcgui.Dialog().yesno

################################################## 
#MENUS
def CATEGORIES():
	#addDir('Verificar Espaço Ocupado',5,addonfolder+artsfolder+'/cleancache.png')
	addDir('Limpar Cache',1,addonfolder+artsfolder+'/cleancache.png')
	addDir('Limpar userdata de Addons já desinstalados',5,addonfolder+artsfolder+'/cleancache.png')
	addDir('Verificar FIQ FSM',4,addonfolder+artsfolder+'/fiqfsmCHECK.png')	
	addDir('Activar FIQ FSM',2,addonfolder+artsfolder+'/fiqfsmON.png')
	addDir('Desactivar FIQ FSM',3,addonfolder+artsfolder+'/fiqfsmOFF.png')
		
##################################################
#FUNCOES
def limpacache():
	if espacoocupado():
		file = addonfolder+scriptsfolder+'tam.txt'
		if xbmcvfs.exists(file): xbmcvfs.delete(file)
		if selfAddon.getSetting('subtitles_folder') == 'true':
			os.system('sh '+addonfolder+scriptsfolder+'subtitlesT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'subtitles.sh')
		if selfAddon.getSetting('packages_folder') == 'true':
			os.system('sh '+addonfolder+scriptsfolder+'packagesT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'packages.sh')
		if selfAddon.getSetting('thumbnails_folder') == 'true':	
			os.system('sh '+addonfolder+scriptsfolder+'ThumbnailsT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'Thumbnails.sh')	
		if selfAddon.getSetting('temp_folder') == 'true':
			os.system('sh '+addonfolder+scriptsfolder+'tempT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'temp.sh')
		if selfAddon.getSetting('metacache_folder') == 'true':		
			os.system('sh '+addonfolder+scriptsfolder+'metacacheT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'metacache.sh')
		conteudo = openfile(file)
		if not conteudo:
			conteudo = 'Nada a limpar'
		ok = mensagemok('Limpeza de cache',conteudo)
		if xbmcvfs.exists(file): xbmcvfs.delete(file)

def espacoocupado():
	file = addonfolder+scriptsfolder+'tam.txt'
	sizesfloat = 0
	if xbmcvfs.exists(file): xbmcvfs.delete(file)
	if selfAddon.getSetting('subtitles_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'subtitlesT.sh >> '+file)
	if selfAddon.getSetting('packages_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'packagesT.sh >> '+file)
	if selfAddon.getSetting('thumbnails_folder') == 'true':	 os.system('sh '+addonfolder+scriptsfolder+'ThumbnailsT.sh >> '+file)
	if selfAddon.getSetting('temp_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'tempT.sh >> '+file)
	if selfAddon.getSetting('metacache_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'metacacheT.sh >> '+file)
	conteudo = openfile(file)
	size = re.findall('(\d+.\d+[GMK])\t',conteudo,re.DOTALL)
	for sizes in size:
		if 'K' in sizes: sizesfloat = sizesfloat+float(sizes[:-1])/1024
		if 'M' in sizes: sizesfloat = sizesfloat+float(sizes[:-1])
		if 'G' in sizes: sizesfloat = sizesfloat+float(sizes[:-1])*1024
	if not conteudo:
		conteudo = '0MB'
	ok = mensagemyesno('Verificação de Espaço','Pode libertar: '+str(round(sizesfloat,2))+' MB','Deseja continuar?')
	if xbmcvfs.exists(file): xbmcvfs.delete(file)
	return ok
	
def fiqfsm(OnOff):
	ok = mensagemok('Limpeza de cache','em desenvolvimento')
	
def checkfiqfsm():
	ok = mensagemok('Limpeza de cache','em desenvolvimento')

def cleanuserdata():
	ok = mensagemok('Limpeza de cache','em desenvolvimento')

def openfile(filename):
	try:
		fh = open(filename, 'rb')
		contents=fh.read()
		fh.close()
		return contents
	except:
		print "Nao abriu o ficheiro: %s" % filename
		return None

######################################################FUNCOES JÁ FEITAS
def addDir(name,mode,iconimage,pasta=False):
        u=sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',addonfolder+'/fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
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
name=None
mode=None
iconimage=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

#################################
#MODOS

if mode==None: CATEGORIES()
elif mode==1: limpacache()
elif mode==2: fiqfsm(True)
elif mode==3: fiqfsm(False)
elif mode==4: checkfiqfsm()
elif mode==5: cleanuserdata()

xbmcplugin.endOfDirectory(int(sys.argv[1]))