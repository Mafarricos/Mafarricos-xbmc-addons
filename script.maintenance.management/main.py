#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,os,xbmcvfs,re,shutil

addon_id = 'script.maintenance.management'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
scriptsfolder = '/resources/scripts/'
artsfolder = '/resources/img/'
mensagemok = xbmcgui.Dialog().ok
mensagemyesno = xbmcgui.Dialog().yesno
addonsfolder = addonfolder.replace(addon_id,'');
packagesfolder = addonsfolder+'packages/'
userdatafolder = addonsfolder.replace('/addons/','/userdata/addon_data/')
thumbnailsfolder = addonsfolder.replace('/addons/','/userdata/Thumbnails/')
tempfolder = addonsfolder.replace('/addons/','/temp/')

################################################## 
#MENUS
def CATEGORIES():
	#addDir('Verificar Espaço Ocupado',5,addonfolder+artsfolder+'/cleancache.png')
	addDir('Limpar Cache',1,addonfolder+artsfolder+'/cleancache.png')
	addDir('Limpar userdata de Addons já desinstalados',5,addonfolder+artsfolder+'/cleancache.png')
	addDir('Backup Biblioteca Filmes/Séries',6,addonfolder+artsfolder+'/cleancache.png')
	addDir('Restore Biblioteca Filmes/Séries',7,addonfolder+artsfolder+'/cleancache.png')	
	addDir('Verificar FIQ FSM',4,addonfolder+artsfolder+'/fiqfsmCHECK.png')	
	addDir('Activar FIQ FSM',2,addonfolder+artsfolder+'/fiqfsmON.png')
	addDir('Desactivar FIQ FSM',3,addonfolder+artsfolder+'/fiqfsmOFF.png')
		
##################################################
#FUNCOES
def limpacache():
	if espacoocupado():
		msgtext = ''
		file = addonfolder+scriptsfolder+'tam.txt'
		if xbmcvfs.exists(file): xbmcvfs.delete(file)
		if selfAddon.getSetting('subtitles_folder') == 'true':
			os.system('sh '+addonfolder+scriptsfolder+'subtitlesT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'subtitles.sh')
		if selfAddon.getSetting('packages_folder') == 'true': 
			if deletefolderfiles(packagesfolder) == 'true': msgtext = msgtext + packagesfolder+'\n'
		if selfAddon.getSetting('thumbnails_folder') == 'true':	
			if deletesubfolders(thumbnailsfolder) == 'true': msgtext = msgtext + thumbnailsfolder+'\n'
		if selfAddon.getSetting('temp_folder') == 'true':
			if deletefolderfiles(tempfolder) == 'true' or deletesubfolders(tempfolder) == 'true': msgtext = msgtext + tempfolder+'\n'
		if selfAddon.getSetting('metacache_folder') == 'true':		
			os.system('sh '+addonfolder+scriptsfolder+'metacacheT.sh >> '+file)
			os.system('sh '+addonfolder+scriptsfolder+'metacache.sh')
		#conteudo = openfile(file)
		if not msgtext:
			msgtext = 'Nada a limpar'
		ok = mensagemok('Limpeza de cache',msgtext)
		if xbmcvfs.exists(file): xbmcvfs.delete(file)

def espacoocupado():
	sizeMB = 0
	if selfAddon.getSetting('subtitles_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'subtitlesT.sh >> '+file)
	if selfAddon.getSetting('packages_folder') == 'true': sizeMB = sizeMB + returnsize(packagesfolder)
	if selfAddon.getSetting('thumbnails_folder') == 'true':	 sizeMB = sizeMB + returnsize(thumbnailsfolder)
	if selfAddon.getSetting('temp_folder') == 'true': sizeMB = sizeMB + returnsize(tempfolder)
	if selfAddon.getSetting('metacache_folder') == 'true': os.system('sh '+addonfolder+scriptsfolder+'metacacheT.sh >> '+file)
	ok = mensagemyesno('Verificação de Espaço','Pode libertar: '+str(round(sizeMB,2))+' MB','Deseja continuar?')
	return ok
	
def fiqfsm(OnOff):
	ok = mensagemok('Limpeza de cache','em desenvolvimento')
	
def checkfiqfsm():
	ok = mensagemok('Limpeza de cache','em desenvolvimento')

def cleanuserdata():
	textmsg = ''
	sizeMB = 0
	file = addonfolder+scriptsfolder+'tam.txt'	
	dir,files = xbmcvfs.listdir(userdatafolder)
	for directories in dir:
		if not xbmcvfs.exists(addonsfolder+directories):
			textmsg = textmsg+directories+'\n'
			sizeMB = sizeMB + returnsize(userdatafolder+directories)
	ok = mensagemyesno('Pastas a serem eliminadas do userdata',textmsg+'\n'+str(round(sizeMB,2))+' MB')
	if ok:
		for directories in dir:
			if not xbmcvfs.exists(addonsfolder+directories): shutil.rmtree(userdatafolder+directories)

def returnsize(path):
	sizebites = 0
	for root, dirs, files in os.walk(path):
		for name in files:
			sizebites = sizebites + float(os.path.getsize(os.path.join(root, name)))
	return (sizebites / 1024 / 1024)

def deletefolderfiles(path):
	deleted = "false"
	for root, dirs, files in os.walk(path):
		for name in files: 
			try: 
				xbmcvfs.delete(path+name)
				deleted = 'true'
			except:
				print 'failed deleting file'
				pass
	return deleted

def deletesubfolders(path):
	deleted = 'false'
	dir,files = xbmcvfs.listdir(path)
	for directories in dir:
		shutil.rmtree(path+directories)
		deleted = 'true'
	return deleted
	
def backupRestore(OnOff):
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
elif mode==6: backupRestore(True)
elif mode==7: backupRestore(False)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
