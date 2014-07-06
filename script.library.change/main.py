#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
import urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,os,xbmcvfs,re,shutil

addon_id = 'script.library.change'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artsfolder = '/resources/img/'
mensagemok = xbmcgui.Dialog().ok
mensagemyesno = xbmcgui.Dialog().yesno
libraryfolder = os.path.join(selfAddon.getSetting('movielibraryfolder'),'')
libraryfolder_change = os.path.join(selfAddon.getSetting('movielibraryfolder_tochange'),'')

################################################## 
#MENUS
def CATEGORIES():
	addDir('Trocar Streams',1,addonfolder+artsfolder+'/folder.png')
	addDir('Recuperar Streams Originais',2,addonfolder+artsfolder+'/folder.png')

##################################################
#FUNCOES

def changestreams():
	nameoriginal = ''
	nametochange = ''
	dir,files = xbmcvfs.listdir(libraryfolder_change)
	for directories in dir:
		libfolder = os.path.join(libraryfolder,directories)
		libfolder_change = os.path.join(libraryfolder_change,directories)
		if xbmcvfs.exists(libfolder):
			for root2, dirs2, files2 in os.walk(libfolder_change):
				for name2 in files2:
					if '.strm' in name2:
						nametochange = name2;
			for root, dirs, files in os.walk(libfolder):
				for name in files:
					if '.strm' in name:
						nameoriginal = name;					
			if nametochange and nameoriginal:
				xbmcvfs.rename(os.path.join(libfolder,nameoriginal),os.path.join(libfolder,nameoriginal[:-4]+'bak'))
				xbmcvfs.copy(os.path.join(libfolder_change,nametochange),os.path.join(libfolder,nameoriginal))
	ok = mensagemok('Trocar Streams','Processo terminado')

def recoverbackups(path):
	for root, dirs, files in os.walk(path):
		for name in files:
			if '.bak' in name:
				fullpath = os.path.join(os.path.join(path,name[:-4]),name)
				xbmcvfs.copy(fullpath,fullpath[:-3]+'strm')
				xbmcvfs.delete(fullpath)				
	
######################################################FUNCOES JÁ FEITAS
def addDir(name,mode,iconimage,pasta=False):
        if sys.argv[0] < 0: sys.argv[0] = 1
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
elif mode==1: changestreams()
elif mode==2: recoverbackups(libraryfolder)

xbmcplugin.endOfDirectory(int(sys.argv[1]))