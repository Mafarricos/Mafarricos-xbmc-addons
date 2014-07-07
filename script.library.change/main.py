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
	count = 0
	alreadychanged = False
	dir,files = xbmcvfs.listdir(libraryfolder_change)
	for directories in dir:
		nametochange = ''
		nameoriginal = ''
		alreadychanged = False
		libfolder = os.path.join(libraryfolder,directories)
		libfolder_change = os.path.join(libraryfolder_change,directories)
		ano=directories[len(directories)-5:-1]
		titulo=directories[:-5]		
		if ano:
			yearbefore = int(ano)-1
			yearafter = int(ano)+1
			libfolder1 = os.path.join(libraryfolder,titulo+str(yearbefore)+')')
			libfolder2 = os.path.join(libraryfolder,titulo+str(yearafter)+')')
			if xbmcvfs.exists(libfolder1): libfolder = libfolder1
			if xbmcvfs.exists(libfolder2): libfolder = libfolder2
		if xbmcvfs.exists(libfolder):
			dir2,files2 = xbmcvfs.listdir(libfolder)				
			for name2 in files2:
				if '.strm' in name2:
					nametochange = name2;
				if '.bak' in name2:
					alreadychanged = True;
			if not alreadychanged:
				dir3,files3 = xbmcvfs.listdir(libfolder_change)	
				for name3 in files3:
					if '.strm' in name3:
						nameoriginal = name3;
				if nametochange and nameoriginal:
					count = count + 1
					source = os.path.join(libfolder,nametochange)
					destination = os.path.join(libfolder,nametochange[:-4]+'bak')
					xbmcvfs.rename(source,destination)
					shutil.copy(os.path.join(libfolder_change,nameoriginal),os.path.join(libfolder,nametochange))
		else: print '##falhou'+libfolder
	ok = mensagemok('Trocar Streams','Processo terminado\nForam alterados '+str(count)+' streams')

def recoverbackups(path):
	count = 0
	for root, dirs, files in os.walk(path):
		for name in files:
			if '.bak' in name:
				count = count + 1
				fullpath = os.path.join(os.path.join(path,name[:-4]),name)
				shutil.copy(fullpath,fullpath[:-3]+'strm')
				xbmcvfs.delete(fullpath)				
	ok = mensagemok('Recuperar Streams','Processo terminado\nForam recuperados '+str(count)+' streams')
	
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