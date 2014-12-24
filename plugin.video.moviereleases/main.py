# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,threading,re,urllib,json,time
from BeautifulSoup import BeautifulSoup
from resources.libs import links,tmdb,imdb,youtube,basic
AddonsResolver = True
try: import addonsresolver
except BaseException as e:
	basic.log(u"main.AddonsResolver ##Error: %s" % str(e))
	AddonsResolver = False
try:
	from metahandler import metahandlers
	metaget = metahandlers.MetaData(preparezip=False)
except: pass

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cachePath			= os.path.join(dataPath,'cache')
sitesfile 			= os.path.join(os.path.join(addonPath, 'resources'),'sites.txt')
sitecachefile 		= os.path.join(cachePath,'_cache.txt')
getSetting          = xbmcaddon.Addon().getSetting
language            = xbmcaddon.Addon().getLocalizedString

if not os.path.exists(dataPath): os.makedirs(dataPath)
if not os.path.exists(cachePath): os.makedirs(cachePath)

def MAIN():
	addDir(language(30000),'LatestReleases',3,'',True,4,'',0,'','','')
	addDir(language(30001),'TMDB',6,'',True,4,'',0,'','','')	
	addDir(language(30002),'IMDB',4,'',True,4,'',0,'','','')
	addDir(language(30003),'search',7,'',True,4,'',0,'','','')	
	addDir(language(30004),'Tools',9,'',True,4,'',0,'','','')
	menus_view()
	
def ToolsMenu():
	addDir(language(30005),'CleanCache',8,'',False,2,'',0,'','','')
	if AddonsResolver: addDir(language(30006),'script.module.addonsresolver',10,'',False,2,'',0,'','','')
	addDir(language(30068),'script.module.metahandler',10,'',False,2,'',0,'','','')
	menus_view()
	
def IMDBmenu():
	addDir(language(30007),'top250',11,'',True,8,'','','','','')
	addDir(language(30008),'bot100',11,'',True,8,'','','','','')	
	addDir(language(30009),'theaters',11,'',True,8,'','','','','')
	addDir(language(30010),'comming_soon',11,'',True,8,'','','','','')
	addDir(language(30011),'boxoffice',11,'',True,8,'',1,'','','')
	addDir(language(30012),'most_voted',11,'',True,8,'',1,'','','')
	addDir(language(30013),'oscars',11,'',True,8,'',1,'','','')
	addDir(language(30014),'popular',11,'',True,8,'',1,'','','')
	addDir(language(30015),'popularbygenre',11,'',True,8,'',1,'','','')	
	menus_view()
	
def TMDBmenu():
	addDir(language(30009),'Theaters',7,'',True,5,'',1,'','','')
	addDir(language(30010),'Upcoming',7,'',True,5,'',1,'','','')
	addDir(language(30014),'Popular',7,'',True,5,'',1,'','','')
	addDir(language(30012),'TopRated',7,'',True,5,'',1,'','','')
	addDir(language(30016),'discoverpop',7,'',True,5,'',1,'','','')	
	menus_view()
	
def TMDBlist(index,url):
	listdirs = []
	if url == 'search':
		keyb = xbmc.Keyboard('', language(30017))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			encode=urllib.quote(search)
			listdirs = tmdb.listmovies(links.link().tmdb_search % (encode),cachePath)	
	elif url == 'discoverpop': listdirs = tmdb.listmovies(links.link().tmdb_discover % (index),cachePath)
	elif url == 'Theaters': listdirs = tmdb.listmovies(links.link().tmdb_theaters % (index),cachePath)
	elif url == 'Popular': listdirs = tmdb.listmovies(links.link().tmdb_popular % (index),cachePath)
	elif url == 'Upcoming': listdirs = tmdb.listmovies(links.link().tmdb_upcoming % (index),cachePath)
	elif url == 'TopRated': listdirs = tmdb.listmovies(links.link().tmdb_top_rated % (index),cachePath)
	for j in listdirs: addDir(j['label'],j['imdbid'],2,j['poster'],False,len(listdirs)+1,j['info'],'',j['imdbid'],j['year'],j['originallabel'],j['fanart_image'])
	if url <> 'search': addDir(language(30018)+'>>',url,7,'',True,len(listdirs)+1,'',int(index)+1,'','','')
	movies_view()
	
def IMDBlist2(index,url,originalname):
	listdirs = []
	if url == 'top250': listdirs = imdb.listmovies(links.link().imdb_top250,cachePath)
	elif url == 'bot100': listdirs = imdb.listmovies(links.link().imdb_bot100,cachePath)	
	elif url == 'boxoffice': listdirs = imdb.listmovies(links.link().imdb_boxoffice % (index),cachePath)
	elif url == 'most_voted': listdirs = imdb.listmovies(links.link().imdb_most_voted % (index),cachePath)
	elif url == 'oscars': listdirs = imdb.listmovies(links.link().imdb_oscars % (index),cachePath)
	elif url == 'popular': listdirs = imdb.listmovies(links.link().imdb_popular % (index),cachePath)
	elif url == 'theaters': listdirs = imdb.listmovies(links.link().imdb_theaters,cachePath)
	elif url == 'comming_soon': listdirs = imdb.listmovies(links.link().imdb_comming_soon,cachePath)	
	elif url == 'popularbygenre': 
		if index == '1': originalname = imdb.getgenre(links.link().imdb_genre)
		listdirs = imdb.listmovies(links.link().imdb_popularbygenre % (index,originalname),cachePath)	
	for j in listdirs: addDir(j['label'],j['imdbid'],2,j['poster'],False,len(listdirs)+1,j['info'],'',j['imdbid'],j['year'],j['originallabel'],j['fanart_image'])
	if url <> 'top250' and url <> 'bot100' and url <> 'theaters' and url <> 'comming_soon': 
		if url == 'popularbygenre': addDir(language(30018)+'>>',url,11,'',True,len(listdirs)+1,'',int(index)+30,'','',originalname,'')
		else: addDir(language(30018)+'>>',url,11,'',True,len(listdirs)+1,'',int(index)+30,'','','','')
	movies_view()
	
def IMDBlist(name,url):
	results = imdb.getlinks(url,[],1,'IMDB')
	populateDir(results,1)
	
def latestreleases(index):
	sites = []
	threads = []
	results = []
	f = 1
	paging = 1	
	for i in range(1, 16):
		siteon = getSetting("site"+str(i)+"on")	
		site = getSetting("site"+str(i))
		pageind = getSetting("site"+str(i)+"pag").replace('/','')
		seclist = []
		if siteon == 'true' and site <> '' and pageind <> '':
			sections = getSetting("site"+str(i)+"sec")
			if sections <> '':
				seclist = sections.split('|')
				for section in seclist: sites.append(site+section+'/'+pageind+'/')
			else: sites.append(site+pageind+'/')		
	for i in range(1, 6):
		siteon = getSetting("custsite"+str(i)+"on")	
		site = getSetting("custsite"+str(i))
		pageind = getSetting("custsite"+str(i)+"pag").replace('/','')
		seclist = []
		if siteon == 'true' and site <> '' and pageind <> '':
			sections = getSetting("custsite"+str(i)+"sec")	
			if sections <> '':
				seclist = sections.split('|')
				for section in seclist: sites.append(site+section+'/'+pageind+'/')
			else: sites.append(site+pageind+'/')
	try: ranging = int(index)+1
	except: ranging = 1
	if ranging ==1: open(sitecachefile, 'w').close()
	totalpass = int(getSetting('pages-num')) * len(sites)
	progress = xbmcgui.DialogProgress()
	a = time.time()
	for i in range(ranging, ranging+int(getSetting('pages-num'))):
		for site in sites:
			threads.append(threading.Thread(name=site+str(i),target=imdb.getlinks,args=(site+str(i)+'/',results,f*100, )))
			f += 1
	ranging = i
	[i.start() for i in threads]
	[i.join() for i in threads]	
	populateDir(results,ranging,True)
	addDir(language(30018)+'>>','Next',3,'',True,1,'',ranging,'','','')
	movies_view()
	elapsedTime = '%s %.2f seconds' % ('Carregado em ', (time.time() - a))     
	basic.infoDialog(elapsedTime)

def populateDir(results,ranging,cache=False):
	unique_stuff = []
	threads2 = []	
	result = []
	order = 0	
	results = sorted(results, key=basic.getKey)
	for order,link in results:
		if link not in str(unique_stuff): unique_stuff.append([order, link])
	chunks=[unique_stuff[x:x+10] for x in xrange(0, len(unique_stuff)+1, 10)]
	for i in range(len(chunks)): threads2.append(threading.Thread(name='listmovies'+str(i),target=tmdb.searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads2]
	[i.join() for i in threads2]
	result = sorted(result, key=basic.getKey)
	basic.log(u"main.populateDir result: %s" % result)
	if cache: linecache= basic.readalllines(sitecachefile)
	for id,lists in result:
		if cache:
			if lists['label'].encode('utf-8') not in str(linecache):
				basic.writefile(sitecachefile,"a",'::pageindex::'+str(ranging)+'::'+lists['label'].encode('utf-8')+'::\n')
				if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
			elif '::pageindex::'+str(ranging)+'::'+lists['label'].encode('utf-8') in str(linecache): 
				if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
		else:
			if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
	
def addDir(name,url,mode,poster,pasta,total,info,index,imdb_id,year,originalname,fanart=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('ascii','xmlcharrefreplace'))+"&originalname="+urllib.quote_plus(originalname.encode('ascii','xmlcharrefreplace'))+"&index="+str(index)+"&imdb_id="+str(imdb_id)+"&year="+str(year)
	ok=True
	context = []
	playcount = 0
	liz=xbmcgui.ListItem(name, iconImage=poster, thumbnailImage=poster)
	liz.setProperty('fanart_image',fanart)
	try:
		playcount = metaget._get_watched('movie', imdb_id, '', '')
		if playcount == 7: info.update({'playcount': 1, 'overlay': 7})
		else: info.update({'playcount': 0, 'overlay': 6})
	except: pass
	if info <> '': 
		liz.setInfo( type="Video", infoLabels=info )
		try:
			trailer = info['trailer'].split('videoid=')[1]
			context.append((language(30019), 'RunPlugin(%s?mode=1&url=%s&name=%s)' % (sys.argv[0],trailer,originalname)))
		except: pass
		context.append((language(30020), 'Action(Info)'))
	if playcount == 7: context.append((language(30064), 'RunPlugin(%s?mode=13&url=%s&originalname=%s&year=%s&imdb_id=%s)' % (sys.argv[0],url,originalname,year,imdb_id)))
	else: context.append((language(30063), 'RunPlugin(%s?mode=12&url=%s&originalname=%s&year=%s&imdb_id=%s)' % (sys.argv[0],url,originalname,year,imdb_id)))
	try: title = originalname.split(' (')[0]
	except: title = originalname
	context.append((language(30310), 'RunPlugin(%s?mode=14&url=%s&originalname=%s&year=%s&imdb_id=%s)' % (sys.argv[0],url,title,year,imdb_id)))
	if AddonsResolver == True: context.append((language(30006), 'RunPlugin(%s?mode=10&url=%s)' % (sys.argv[0],'script.module.addonsresolver')))	
	liz.addContextMenuItems(context, replaceItems=False)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def menus_view():
	setting = getSetting('menu-view')
	if setting =="0": xbmc.executebuiltin("Container.SetViewMode(50)")
	elif setting =="1": xbmc.executebuiltin("Container.SetViewMode(51)")
	return

def movies_view():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	setting = getSetting('movies-view')
	if setting == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
	elif setting == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
	elif setting == "2": xbmc.executebuiltin("Container.SetViewMode(500)")
	elif setting == "3": xbmc.executebuiltin("Container.SetViewMode(501)")
	elif setting == "4": xbmc.executebuiltin("Container.SetViewMode(508)")
	elif setting == "5": xbmc.executebuiltin("Container.SetViewMode(504)")
	elif setting == "6": xbmc.executebuiltin("Container.SetViewMode(503)")
	elif setting == "7": xbmc.executebuiltin("Container.SetViewMode(515)")
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	return

def whattoplay(originalname,url,imdb_id,year):
	if url <> 'external':
		try: url = xbmc.getInfoLabel('ListItem.Trailer').split('videoid=')[1]
		except: url = ''
	if AddonsResolver == False: youtube.playtrailer(url,originalname)
	else:
		if getSetting("playwhat") == 'Trailer': youtube.playtrailer(url,originalname)
		else: addonsresolver.custom_choice(originalname,url,imdb_id,year)
	
def playcount_movies(title, year, imdb, watched):
	title = title.split(' (')[0]
	basic.log(u"main.playcount_movies %s, %s, %s, %s" % (title, year, imdb, watched))
	try:
		metaget.get_meta('movie', title ,year=year)
		metaget.change_watched('movie', '', imdb, season='', episode='', year='', watched=watched)
	except: pass
	try:
		if getSetting("trakt_sync") == 'true':	
			if (links.link().trakt_user == '' or links.link().trakt_password == ''): raise Exception()
			if not imdb.startswith('tt'): imdb = 'tt' + imdb
			if watched == 7: url = links.link().trakt_seen
			else: url = links.link().trakt_unseen
			post = {"movies": [{"imdb_id": imdb}], "username": links.link().trakt_user, "password": links.link().trakt_password}
			result = basic.open_url(url, post=json.dumps(post))
			basic.log(u"main.playcount_movies trakt result %s" % (result))
	except: pass
	xbmc.executebuiltin("Container.Refresh")
	
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
originalname=None
mode=None
iconimage=None
index=None
imdb_id=None
year=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: originalname=urllib.unquote_plus(params["originalname"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass
try: imdb_id=urllib.unquote_plus(params["imdb_id"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "OriginalName: "+str(originalname)
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)
print "imdb_id: "+str(imdb_id)
print "year: "+str(year)

if mode==None or url==None or len(url)<1: MAIN()
elif mode==1: youtube.playtrailer(url,name)
elif mode==2: whattoplay(originalname,url,imdb_id,year)
elif mode==3: latestreleases(index)
elif mode==4: IMDBmenu()
elif mode==5: IMDBlist(name,url)
elif mode==6: TMDBmenu()
elif mode==7: TMDBlist(index,url)
elif mode==8: xbmcgui.Dialog().ok('Cache',basic.removecache(cachePath))
elif mode==9: ToolsMenu()
elif mode==10: basic.settings_open(url)
elif mode==11: IMDBlist2(index,url,originalname)
elif mode==12: playcount_movies(originalname, year, imdb_id, 7)
elif mode==13: playcount_movies(originalname, year, imdb_id, 6)
elif mode==14: basic.library_movie_add(originalname, url, imdb_id, year)
xbmcplugin.endOfDirectory(int(sys.argv[1]))