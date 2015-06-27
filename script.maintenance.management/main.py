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
packagesfolder = os.path.join(addonsfolder,'packages')
userdatafolder = xbmc.translatePath(os.path.join('special://userdata','addon_data'))
thumbnailsfolder = xbmc.translatePath('special://thumbnails')
tempfolder = xbmc.translatePath('special://temp')
databasefolder = xbmc.translatePath('special://database')
installfolder = xbmc.translatePath('special://xbmc')

################################################## 
#MENUS
def CATEGORIES():
	addDir('Limpar Cache',1,addonfolder+artsfolder+'/cleancache.png')
	addDir('Limpar userdata de Addons já desinstalados',5,addonfolder+artsfolder+'/cleancache.png')
	addDir('Desinstalar Addons',9,addonfolder+artsfolder+'/cleancache.png',True)
	addDir('Backup Biblioteca Filmes/Séries',6,addonfolder+artsfolder+'/cleancache.png')
	addDir('Restore Biblioteca Filmes/Séries',7,addonfolder+artsfolder+'/cleancache.png')
	try:
		if 'OpenELEC' in os.uname(): addDir('FIQ FSM',8,addonfolder+artsfolder+'/fiqfsmCHECK.png',True)	
	except: pass

def FIQ_FSM():		
	addDir('Verificar FIQ FSM',4,addonfolder+artsfolder+'/fiqfsmCHECK.png')	
	addDir('Activar FIQ FSM',2,addonfolder+artsfolder+'/fiqfsmON.png')
	addDir('Desactivar FIQ FSM',3,addonfolder+artsfolder+'/fiqfsmOFF.png')

def desinstalar():
	names =['metadata','module','common','packages']
	addonsize = 0
	userdatasize = 0
	dir,files = xbmcvfs.listdir(addonsfolder)
	for directories in sorted(dir):
		found = False
	        if re.search('metadata',directories) or re.search('module',directories) or re.search('common',directories) or re.search('packages',directories): found = True
		if not found: 
			content = openfile(os.path.join(addonsfolder+directories,'addon.xml'))
			if content:
				nome=re.compile('name="(.+?)"').findall(content)
				addonsize = returnsize(os.path.join(addonsfolder,directories))
				userdatasize = returnsize(os.path.join(userdatafolder,directories))
				addDir(directories+" - [COLOR green]"+nome[0]+"[/COLOR] (Espaço: "+str(round(addonsize,2)+round(userdatasize,2))+" MB)",10,addonfolder+artsfolder+'/cleancache.png',False,directories)

##################################################
#FUNCOES
def limpacache():
	if espacoocupado():
		msgtext = ''
		thumbsDel = False
		if selfAddon.getSetting('subtitles_folder') == 'true':
			foldersdeleted = cleansubtitlesdata() 
			if foldersdeleted: msgtext = msgtext + foldersdeleted
		if selfAddon.getSetting('packages_folder') == 'true': 
			if deletefolderfiles(packagesfolder): msgtext = msgtext + packagesfolder+'\n'
		if selfAddon.getSetting('thumbnails_folder') == 'true':
			if deletesubfolders(thumbnailsfolder): msgtext = msgtext + thumbnailsfolder+'\n'
			if deletefolderfiles(databasefolder,'Textures'): msgtext = msgtext + databasefolder+'TexturesXX.db'+'\n'
			thumbsDel = True
		if selfAddon.getSetting('temp_folder') == 'true':
			if (deletesubfolders(tempfolder) and deletefolderfiles(tempfolder)) or (deletesubfolders(tempfolder) or deletefolderfiles(tempfolder)): msgtext = msgtext + tempfolder+'\n'
		if selfAddon.getSetting('metacache_folder'):	
			if deletesubfolders(os.path.join(userdatafolder,'script.module.metahandler')): msgtext = msgtext + userdatafolder+'script.module.metahandler'+'\n'	
		if not msgtext:
			msgtext = 'Nada a limpar'
		ok = mensagemok('Limpeza de cache',msgtext)
		if thumbsDel:
			rebootorexit()
			if sys.platform == 'win32': os.system(addonfolder+scriptsfolder+'winbat.bat')			
		else: ok = mensagemok('Concluido','Operação Terminada')

def fiqfsm(OnOff):
	ok = mensagemok('Limpeza de cache','em desenvolvimento')
	
def checkfiqfsm():
	ok = mensagemok('Limpeza de cache','em desenvolvimento')

def backupRestore(OnOff):
	ok = mensagemok('Limpeza de cache','em desenvolvimento')

def espacoocupado():
	sizeMB = 0
	if selfAddon.getSetting('subtitles_folder') == 'true': sizeMB = sizeMB +subtitlesdatasize()
	if selfAddon.getSetting('packages_folder') == 'true': sizeMB = sizeMB + returnsize(packagesfolder)
	if selfAddon.getSetting('thumbnails_folder') == 'true': sizeMB = sizeMB + returnsize(thumbnailsfolder) + returnsize(databasefolder,'Textures')
	if selfAddon.getSetting('temp_folder') == 'true': sizeMB = sizeMB + returnsize(tempfolder)
	if selfAddon.getSetting('metacache_folder') == 'true': sizeMB = sizeMB + returnsize(os.path.join(userdatafolder,'script.module.metahandler/meta_cache'))
	ok = mensagemyesno('Verificação de Espaço','Pode libertar: '+str(round(sizeMB,2))+' MB\nDeseja continuar?')
	return ok
	
def cleanuserdata():
	textmsg = ''
	sizeMB = 0
	dir,files = xbmcvfs.listdir(userdatafolder)
	for directories in dir:
		if not 'service.openelec.settings' in directories and not 'pvr.iptvsimple' in directories:
			if not xbmcvfs.exists(os.path.join(addonsfolder,directories+'/')):
				textmsg = textmsg+directories+'\n'
				sizeMB = sizeMB + returnsize(os.path.join(userdatafolder,directories))
	ok = mensagemyesno('Pastas a serem eliminadas do userdata:',textmsg+str(round(sizeMB,2))+' MB\nDeseja Continuar?')
	if ok and textmsg:
		for directories in dir:
			if not 'service.openelec.settings' in directories and not 'pvr.iptvsimple' in directories:
				if not xbmcvfs.exists(os.path.join(addonsfolder,directories+'/')): shutil.rmtree(os.path.join(userdatafolder,directories+'/'))
		ok = mensagemok('Concluido','Operação Terminada')

def cleansubtitlesdata():
	foldersdeleted = ''
	subtfolder = ''
	dir,files = xbmcvfs.listdir(userdatafolder)
	for directories in dir:
		if 'subtitles' in directories:
			subtfolder = os.path.join(os.path.join(userdatafolder,directories),'temp')
			if xbmcvfs.exists(subtfolder): 
				foldersdeleted = foldersdeleted + subtfolder+'\n'
				shutil.rmtree(subtfolder)
	return foldersdeleted

def subtitlesdatasize():
	sizeMB = 0
	subtfolder = ''
	dir,files = xbmcvfs.listdir(userdatafolder)
	for directories in dir:
		if 'subtitles' in directories:
			subtfolder = os.path.join(userdatafolder+directories,'temp')
			if xbmcvfs.exists(subtfolder): sizeMB = sizeMB + returnsize(subtfolder)
	return sizeMB

def deletefolderfiles(path,oneFile=None):
	deleted = False
	file = addonfolder+scriptsfolder
	file = os.path.join(file,'winbat.bat')
	for root, dirs, files in os.walk(path):
		for name in files:
			if oneFile:
				if oneFile in name: 
					if sys.platform == 'win32': createandwritebatch(file,'Taskkill /IM XBMC.exe /F\ntimeout 3\n','del '+os.path.join(path,name)+'\npause')
					else:
						try: deleted = deletefile(os.path.join(path,name))
						except: 
							deleted = os.remove(os.path.join(path,name))
							pass
			else:
				if ".log" not in name: deleted = deletefile(os.path.join(path,name))
	return deleted

def deletesubfolders(path):
	deleted = False
	dir,files = xbmcvfs.listdir(path)
	for directories in dir:
		shutil.rmtree(path+directories)
		deleted = True
	return deleted

def deleteaddon(addon):
	ok = mensagemyesno('Desinstalar Addon',"Vai remover toda a informação (addon+userdata) do addon:\n"+addon+'\nDeseja continuar?')
	if ok:
		try: shutil.rmtree(os.path.join(userdatafolder,addon))
		except: pass
		shutil.rmtree(os.path.join(addonsfolder,addon))
		ok = deletefolderfiles(databasefolder,'Addons')
		xbmc.executebuiltin("Container.Refresh")
		rebootorexit()
		if sys.platform == 'win32': os.system(addonfolder+scriptsfolder+'winbat.bat')

def deletefile(path):
	deleted = False
	try: 
		xbmcvfs.delete(path)
		deleted = True
	except:
		print 'failed deleting file'
		pass
	return deleted

def returnsize(path,oneFile=None):
	sizebites = 0
	for root, dirs, files in os.walk(path):
		for name in files:
			if oneFile:
				if oneFile in name:	sizebites = sizebites + float(os.path.getsize(os.path.join(root, name)))
			else: sizebites = sizebites + float(os.path.getsize(os.path.join(root, name)))
	return (sizebites / 1024 / 1024)

def rebootorexit():
	if selfAddon.getSetting('auto_reboot-exit') == 'true' or sys.platform == 'win32':
		ok = mensagemok('Reiniciar/Sair do XBMC','O XBMC vai fechar ou reiniciar conforme o sistema')
		try:
			if 'OpenELEC' in os.uname(): xbmc.restart()
			else:
				try: xbmc.executebuiltin("Quit")
				except: 
					xbmc.restart()
					pass
		except:
			try: xbmc.executebuiltin("Quit")
			except: 
				xbmc.restart()
				pass
			pass
	else: ok = mensagemok('Reiniciar o XBMC','Deve reiniciar o XBMC')

def openfile(filename):
	try:
		fh = open(filename, 'rb')
		contents=fh.read()
		fh.close()
		return contents
	except:
		print "Nao abriu o ficheiro: %s" % filename
		return None

def createandwritebatch(filename,command1,command2):
	ok = deletefile(filename)
	try:
		fh = open(filename, 'w')
		fh.write(command1)
		fh.write(command2)
		fh.close()
	except:
		print "Nao gravou o ficheiro: %s" % filename
		pass
		
######################################################FUNCOES JÁ FEITAS
def addDir(name,mode,iconimage,pasta=False,folderDel=None):
        if sys.argv[0] < 0: sys.argv[0] = 1
        u=sys.argv[0]+"?folderDel="+str(folderDel)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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
folderDel=None
name=None
mode=None
iconimage=None

try: folderDel=urllib.unquote_plus(params["folderDel"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "folderDel: "+str(folderDel)

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
elif mode==8: FIQ_FSM()
elif mode==9: desinstalar()
elif mode==10: deleteaddon(folderDel)

xbmcplugin.endOfDirectory(int(sys.argv[1]))