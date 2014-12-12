# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib,urllib2,xbmcplugin,xbmcgui,xbmc,re,xbmcaddon,os

addonId             = xbmcaddon.Addon().getAddonInfo("id")
getSetting          = xbmcaddon.Addon().getSetting
language            = xbmcaddon.Addon().getLocalizedString
wtpath 				= xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
art 				= '/resources/art/'

def MAIN():
	addDir('http://jell.yfish.us/ - '+language(30017).encode('utf-8'),'http://jell.yfish.us/',3,wtpath + art + 'iconJF.png',True,'','')
	addDir('http://bigbuckbunny.org - '+language(30018).encode('utf-8'),'http://peach.blender.org/',4,wtpath + art + 'iconBBB.png',True,'','')	
	addDir('http://tearsofsteel.org/ - '+language(30020).encode('utf-8'),'http://tearsofsteel.org/',6,wtpath + art + 'iconTOS.png' ,True,'','')
	addDir('http://sintel.org/ - '+language(30020).encode('utf-8'),'http://sintel.org/',7,wtpath + art + 'iconST.jpg',True,'','')	
	addDir('http://elephantsdream.org - '+language(30019).encode('utf-8'),'http://peach.blender.org/',5,wtpath + art + 'iconED.jpg' ,True,'','')
	
def sintel():
	filetypes = ['mkv','ogv','mp4','divx','mov']
	html = open_url('https://download.blender.org/durian/movies/')
	data = re.findall('<a href="(.+?)">(.+?)</a>', html, re.DOTALL)
	for url,name in data:
		for filetype in filetypes:
			if filetype in name and not'.md5' in name:
				information = { "Title": name}
				width = re.findall('_(\d+)p_', name, re.DOTALL)
				try: information2 = { 'Width' : width[0] }
				except: information2 = ''
				addDir(name,'https://download.blender.org/durian/movies/'+url,1,'',False,information,information2)
	addDir('sintel-2048-surround.mp4','http://mirrorblender.top-ix.org/movies/sintel-2048-surround.mp4',1,'',False,information,information2)
	addDir('sintel-1280-surround.mp4','http://mirrorblender.top-ix.org/movies/sintel-1280-surround.mp4',1,'',False,information,information2)
	addDir('sintel-1024-surround.mp4','http://mirrorblender.top-ix.org/movies/sintel-1024-surround.mp4',1,'',False,information,information2)
	html = open_url('https://download.blender.org/durian/trailer/')
	data = re.findall('<a href="(.+?)">(.+?)</a>', html, re.DOTALL)
	for url,name in data:
		for filetype in filetypes:
			if filetype in name and not '.md5' in name:
				information = { "Title": name}	
				width = re.findall('_(\d+)p_', name, re.DOTALL)
				try: information2 = { 'Width' : width[0] }
				except: information2 = ''
				addDir(name,'https://download.blender.org/durian/trailer/'+url,1,'',False,information,information2)	

def bbb():
	filetypes = ['mov','ogg','avi']
	html = open_url('http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/')
	data = re.findall('<a href="(.+?)">(.+?)</a>', html, re.DOTALL)
	for url,name in data:
		for filetype in filetypes:
			if filetype in name:
				information = { "Title": name}
				width = re.findall('_(\d+)p_', name, re.DOTALL)
				try: information2 = { 'Width' : width[0] }
				except: information2 = ''
				addDir(name,'http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/'+url,1,'',False,information,information2)	
	html = open_url('http://distribution.bbb3d.renderfarming.net/video/mp4/')
	data = re.findall('<a href="(.+?)">(.+?)</a>', html, re.DOTALL)
	for url,name in data:
		if not 'torrent' in name:
			if '.mp4' in name:
				information = { "Title": name}	
				width = re.findall('_(\d+)p_', name, re.DOTALL)
				try: information2 = { 'Width' : width[0] }
				except: information2 = ''
				addDir(name,'http://distribution.bbb3d.renderfarming.net/video/mp4/'+url,1,'',False,information,information2)	

def ed():
	import urllib
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
	html = open_url('http://video.blendertestbuilds.de/download.blender.org/ED/')
	data = re.findall('<a href="(.+?)">(.+?)</a>', html, re.DOTALL)
	for url,name in data:
		if '.avi' in name:
			information = { "Title": name}
			addDir(name,'http://video.blendertestbuilds.de/download.blender.org/ED/'+url+'|User-Agent='+urllib.quote_plus(user_agent),1,'',False,information,'')	

def tearsofsteel():
	filetypes = ['mov','MKV']
	html = open_url('http://mango.blender.org/download/')
	html = html.replace('<strong>HD </strong>','<strong>4k HD</strong>').replace('<strong>4K</strong>','<strong>4K HD</strong>').replace('1920 pixels wide',' 1920 pixels wide') .replace('pixels wide ','').replace('|','').replace(' :: ','_').replace(' :: ','_')
	data = re.findall('<li><strong>(.+?)</strong> (.+?)_<a href="(.+?)">(.+?)</a>.+?</li>', html, re.DOTALL)
	for quality,data,url,name in data:
		for filetype in filetypes:
			print '##aki',quality,data,url,name		
			if filetype in data:
				if '3840' in data: url = url+'tearsofsteel_4k.mov'
				information = { "Title": quality+' '+data}
				addDir(quality+' '+data,url,1,'',False,information,'')
					
def jellyfish():
	html = open_url('http://jell.yfish.us/')
	data = re.findall('<td class="file"><a href="(.+?)">(.+?)</a></td>\s+<td>(.+?)</td>\s+<td>(\d+) <span class="faded">Mbps</span></td>\s+<td><b>(\d+)</b> <span class="faded">Mbps</span></td>\s+<td>(\d+) <span class="faded">Mbps</span></td>\s+<td>:(\d+)</td>\s+<td>(\d+) <span class="faded">MB</span></td>', html, re.DOTALL)
	for url,name,profile,bitmin,bitavg,bitmax,seconds,size in data:
		information = { "Title": name}		
		information2 = { 'duration': seconds }
		addDir(name+' [Profile Level:'+profile+', Bitrate Min:'+bitmin+' Mbps, Bitrate Avg:'+bitavg+' Mbps, Bitrate Max.:'+bitmax+' Mbps, Size:'+size+' MB]','http://jell.yfish.us/'+url,1,'',False,information,information2)
	original = re.findall('<table id="original" cellpadding="0" cellspacing="0">(.+?)</table>', html, re.DOTALL)
	urlname = re.findall('<td class="file"><a href="(.+?)">(.+?)</a></td>', original[0], re.DOTALL)
	for url,name in urlname:
		urltext=url
		nametext=name
	profile = re.findall('<td class="profile">(.+?)</td>', original[0], re.DOTALL)
	bitmin = re.findall('<td class="bitrate">(\d+) <span class="faded">Mbps</span></td>', original[0], re.DOTALL)
	bitmavg = re.findall('<td class="bitrate"><b>(\d+)</b> <span class="faded">Mbps</span></td>', original[0], re.DOTALL)
	bitmax = re.findall('<td class="bitrate">(\d+) <span class="faded">Mbps</span></td>', original[0], re.DOTALL)	
	seconds = re.findall('<td class="runtime">:(\d+)</td>', original[0], re.DOTALL)	
	size = re.findall('<td class="size">(\d+) <span class="faded">MB</span></td>', original[0], re.DOTALL)	
	information = { "Title": name}			
	information2 = { "duration": seconds[0], "width": 1280 }
	addDir(nametext+' [Profile Level:'+profile[0]+', Bitrate Min:'+bitmin[0]+' Mbps, Bitrate Avg:'+bitavg[0]+' Mbps, Bitrate Max.:'+bitmax[0]+' Mbps, Size:'+size[0]+' MB]','http://jell.yfish.us/'+urltext,1,'',False,information,information2)

def open_url(url,type=None):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
	req = urllib2.Request(url)
	req.add_header('User-Agent', user_agent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def play(url):
	playlist = xbmc.PlayList(1)
	playlist.clear()             
	playlist.add(url,xbmcgui.ListItem(name, thumbnailImage=str(iconimage))) 
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	except: pass

def download(url,name):
	cookie = '';
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
	referer = ''
	folder = xbmc.translatePath(getSetting("downloads"))
	if folder == '':
		yes = xbmcgui.Dialog().yesno(language(30001).encode('utf-8'), language(30000).encode('utf-8'))
		if yes: xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonId)
		return	
	dest = os.path.join(folder, name.rsplit(' [', 1)[0])
	import commondownloader
	commondownloader.download(url, dest, 'Jellyfish', referer=referer, agent=user_agent, cookie=cookie)

def addDir(name,url,mode,iconimage,pasta,information,information2):
	context = []
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	context.append((language(30016).encode('utf-8'), 'XBMC.RunPlugin(%s?mode=2&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))	
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels=information )
	if information2: liz.addStreamInfo("Video", information2 )
	liz.addContextMenuItems(context, replaceItems=False) 
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
	return ok
		
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
index=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)

if mode==None or url==None or len(url)<1: MAIN()
elif mode==1: play(url)
elif mode==2: download(url,name)
elif mode==3: jellyfish()
elif mode==4: bbb()
elif mode==5: ed()
elif mode==6: tearsofsteel()
elif mode==7: sintel()
xbmcplugin.endOfDirectory(int(sys.argv[1]))