# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,re,threading,os,json,xbmcaddon,xbmcgui,xbmc
from HTMLParser import HTMLParser

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cachePath			= os.path.join(dataPath,'cache')
sitesfile 			= os.path.join(os.path.join(addonPath, 'resources'),'sites.txt')
site9gagfile 		= os.path.join(cachePath,'_9gag.txt')
sitecachefile 		= os.path.join(cachePath,'_cache.txt')
getSetting          = xbmcaddon.Addon().getSetting

progress = xbmcgui.DialogProgress()
	
def getpages(id):
	list = []
	progress.create('Fun Videos', 'A Obter dados...')
	i = 1
	t = 0
	ins = open(sitesfile, "r")	
	for line in ins: t = t + 1
	ins.close()
	ins = open(sitesfile, "r" )	
	for line in ins: 
		percent = int( ( i / float(t) ) * 100)	
		parameters = json.loads(line)
		enabled = parameters['enabled']
		pageindex = parameters['pagination']
		prettyname = parameters['prettyname']
		message = "Site: " + prettyname + " ("+ str(i)+'/'+str(t)+")"		
		progress.update( percent, "", message, "" )
		if progress.iscanceled():
			progress.close()
			xbmcgui.Dialog().ok('ERROR','Cancelled.')
			return ''		
		i = i + 1		
		if 'true' in enabled:
			site = parameters['site']
			frame = parameters['frame']
			starton = int(parameters['starton'])
			print '##funvideos-site: '+site+pageindex+str(id+starton)			
			if 'true' in frame: 
				list2 = grabiframes(site+pageindex+str(id+starton),prettyname)
				if list2: list.extend(list2)
			elif 'vit' in frame:
				list2 = grabvit(site+pageindex+str(id+starton),prettyname)
				if list2: list.extend(list2)	
			elif '9gag' in frame:
				list2 = grab9gag(site+pageindex,prettyname,str(id+starton))
				if list2: list.extend(list2)
			elif 'break' in frame:
				list2 = grabbreak(site+pageindex+str(id+starton),prettyname)
				if list2: list.extend(list2)				
			else:
				startsection = parameters['startsection']
				endsection = parameters['endsection']
				list2 = grablinks(site+pageindex+str(id+starton),prettyname,startsection,endsection,site)
				if list2: list.extend(list2)
	ins.close()
	progress.close()
	unique_stuff = []    
	for item in list:
		if item['url'] not in str(unique_stuff): unique_stuff.append(item)
	return unique_stuff

def grablinks(mainURL,prettyname,sectionstart,sectionend,mainsite=None):
	list = []
	page = open_url(mainURL)
	html_source_trunk = re.findall(sectionstart+'(.*?)'+sectionend, page, re.DOTALL)
	threads = []
	results = []
	for i in range(0, len(html_source_trunk)): 
		print "##funvideos-grablinks: "+html_source_trunk[i]
		if mainsite: pageURL=html_source_trunk[i].replace(mainsite,'').replace('/','').replace('.','').encode('utf-8')
		threads.append(threading.Thread(name=mainURL+str(i),target=grabiframes,args=(html_source_trunk[i], prettyname, results, i+1, pageURL, )))	
	[i.start() for i in threads]
	[i.join() for i in threads]
	return results

def grabiframes(mainURL,prettyname,results=None,index=None,pageURL=None):
	list = []
	if pageURL: pagecache = os.path.join(cachePath,pageURL)
	if pageURL and getSetting("cachesites") == 'true' and os.path.isfile(pagecache):
		jsonline = readfiletoJSON2(pagecache)
		jsonloaded = json.loads(jsonline, encoding="utf-8")
		if index: results.append(jsonloaded)
		else: list.append(jsonloaded)
	else:
		try: page = open_url(mainURL)
		except: 
				page = ' '
				pass
		blocker = re.findall('data-videoid="(.+?)"', page, re.DOTALL)
		if blocker:
			fakeframe='<iframe src="http//www.youtube.com/embed/'+blocker[0]+'"</iframe>'
			html = re.findall('<iframe(.*?)</iframe>', fakeframe, re.DOTALL)
		else: html = re.findall('<iframe(.*?)</iframe>', page, re.DOTALL)
		for trunk in html:
				try: iframe = re.compile('src="(.+?)"').findall(trunk)[0]
				except: 
					try: iframe = re.compile("src='(.+?)'").findall(trunk)[0]
					except: iframe = ''
				if iframe:
					if iframe.find('ad120m.com') > -1 or iframe.find('facebook') > -1 or iframe.find('metaffiliation') > -1 or iframe.find('banner600') > -1 or iframe.find('engine.adbooth.com') > -1 or iframe.find('www.lolx2.com') > -1 or iframe.find('jetpack.wordpress.com') > -1: pass
					else:
						print "##funvideos-grabiframes: "+iframe
						try:
							if iframe.find('youtube') > -1:
								textR,resolver_iframe = youtube_resolver(iframe,prettyname)
								if resolver_iframe: 	
									if index: results.append(resolver_iframe)
									else: list.append(resolver_iframe)
									if pageURL and getSetting("cachesites") == 'true': writefile(pagecache,'w',textR)
							elif iframe.find('dailymotion') > -1:
								textR,resolver_iframe = daily_resolver(iframe,prettyname)
								if resolver_iframe: 							
									if index: results.append(resolver_iframe)
									else: list.append(resolver_iframe)
									if pageURL and getSetting("cachesites") == 'true': writefile(pagecache,'w',textR)
							elif iframe.find('vimeo') > -1:
								textR,resolver_iframe = vimeo_resolver(iframe,prettyname)
								if resolver_iframe: 							
									if index: results.append(resolver_iframe)
									else: list.append(resolver_iframe)
									if pageURL and getSetting("cachesites") == 'true': writefile(pagecache,'w',textR)
							elif iframe.find('sapo') > -1:
								textR,resolver_iframe = sapo_resolver(iframe,prettyname)
								if resolver_iframe: 							
									if index: results.append(resolver_iframe)
									else: list.append(resolver_iframe)
									if pageURL and getSetting("cachesites") == 'true': writefile(pagecache,'w',textR)
							elif iframe.find('videolog') > -1:
								textR,resolver_iframe = videolog_resolver(iframe,prettyname)
								if resolver_iframe: 							
									if index: results.append(resolver_iframe)
									else: list.append(resolver_iframe)
									if pageURL and getSetting("cachesites") == 'true': writefile(pagecache,'w',textR)
						except BaseException as e:
							print '##ERROR-##funvideos-grabiframes: '+iframe+' '+str(e)
				else: print '##ERROR-funvideos:frame on server not supported: '+iframe
	if not index: return list

def grab9gag(url,prettyname,id):
	jsondata = []
	list = []
	line = readoneline(site9gagfile)
	idpage = re.findall('::'+id+'::::(.+?)::', line, re.DOTALL)
	if not idpage: page = open_url('http://9gag.tv')
	else: page = open_url(url+idpage[0],'9gag')
	jsondata = re.findall('   postGridPrefetchPosts = (.+?);', page, re.DOTALL)
	j = json.loads(jsondata[0])
	size = len(j)
	e=0
	for data in j:
		e = e + 1
		if e == size:
			line = readoneline(site9gagfile)
			if not '<'+id+'>' in line: writefile(site9gagfile,"a",'::'+str(int(id)+1)+'::::'+data['prevPostId']+'::') 
		try:
			duration = 0
			time = re.findall('PT(\d+)M(\d+)S', data['videoDuration'], re.DOTALL)
			if time:
				for min,sec in time: duration = int(min)*60+int(sec)
			else:
				time = re.findall('PT(\d+)M', data['videoDuration'], re.DOTALL)
				if time: duration = int(time[0])*60
				else:
					time = re.findall('PT(\d+)S', data['videoDuration'], re.DOTALL)
					if time: duration = time[0]
		except: 
			duration = 60
			pass
		title = cleanTitle(data['ogTitle'])	
		videocache = os.path.join(cachePath,data['videoExternalId'])
		jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' +data['videoExternalId']+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+data['thumbnail_360w']+'"}'
		jsonloaded = json.loads(jsontext, encoding="utf-8")
		if getSetting("cachesites") == 'true' and not os.path.isfile(videocache): writefile(videocache,'w',jsontext.encode('utf8'))
		list.append(jsonloaded)
	return list 

def grabbreak(url,prettyname):
	list = []
	try:
		page = open_url(url)
		page = page.replace("\\","")
		ids = re.findall('data-content-id="(\d+)"', page, re.DOTALL)
		for videoid in ids:
			videocache = os.path.join(cachePath,str(videoid))
			if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
				jsonline = readfiletoJSON2(videocache)
				jsonloaded = json.loads(jsonline, encoding="utf-8")
				list.append(jsonloaded)
			else:
				content = open_url("http://www.break.com/embed/"+videoid)
				matchAuth=re.compile('"AuthToken": "(.+?)"', re.DOTALL).findall(content)
				matchURL=re.compile('"uri": "(.+?)".+?"height": (.+?),', re.DOTALL).findall(content)
				matchYT=re.compile('"youtubeId": "(.*?)"', re.DOTALL).findall(content)
				title=re.compile('"contentName": "(.+?)",', re.DOTALL).findall(content)
				title = cleanTitle(title[0])
				title2 = ''				
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2		
				duration=re.compile('"videoLengthInSeconds": "(\d+)",', re.DOTALL).findall(content)	
				thumb = re.compile('"thumbUri": "(.+?)",', re.DOTALL).findall(content)				
				finalUrl=""
				if matchYT and matchYT[0]!="":
					finalUrl = "plugin://plugin.video.youtube/?action=play_video&videoid=" + matchYT[0]
					videocache2 = os.path.join(cachePath,str(matchYT[0]))				
					if getSetting("cachesites") == 'true' and not os.path.isfile(videocache): 
						jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration[0])+'","thumbnail":"'+thumb[0]+'"}'
						jsonloaded = json.loads(jsontext, encoding="utf-8")			
						writefile(videocache2,'w',jsontext.encode('utf8'))
				else:
					max=0
					for url, height in matchURL:
						height=int(height)
						if height>max: 
							finalUrl=url.replace(".wmv",".flv")+"?"+matchAuth[0]
							max=height
				jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration[0])+'","thumbnail":"'+thumb[0]+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true' and not os.path.isfile(videocache): writefile(videocache,'w',jsontext.encode('utf8'))
				list.append(jsonloaded)
		if list: return list
	except BaseException as e:
		print '##ERROR-funvideos:Break_resolver: '+url+' '+str(e)

def grabvit(url,prettyname):
	list = []
	try:
		content = open_url(url)
		spl = content.split('<div class="videoListItem">')
		for i in range(1, len(spl), 1):
			entry = spl[i]
			match = re.compile('data-youtubeid="(.+?)"', re.DOTALL).findall(entry)
			id = match[0]
			match = re.compile('<div class="duration">(.+?)</div>', re.DOTALL).findall(entry)
			duration = match[0].strip()
			splDuration = duration.split(":")
			duration = str(int(splDuration[0])*60+int(splDuration[1]))
			thumb = "http://img.youtube.com/vi/"+id+"/0.jpg"
			match = re.compile('alt="(.+?)"', re.DOTALL).findall(entry)
			title = match[0]
			title = cleanTitle(title)
			videocache = os.path.join(cachePath,str(id))
			title2 = ''		
			try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
			except: pass
			if title2 <> '': title = title2
			jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(id)+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumb+'"}'
			jsonloaded = json.loads(jsontext, encoding="utf-8")
			if getSetting("cachesites") == 'true' and not os.path.isfile(videocache): writefile(videocache,'w',jsontext.encode('utf8'))
			list.append(jsonloaded)
		if list: return list
	except BaseException as e:
		print '##ERROR-funvideos:VitaminL_resolver: '+url+' '+str(e)
		pass

def sapo_resolver(url,prettyname):
	match = re.compile('file=http://.+?/(.+?)/mov/').findall(url)
	if match: 
		videocache = os.path.join(cachePath,str(match[0]))
		if os.path.isfile(videocache):
			jsonline = readfiletoJSON2(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				sapoAPI = open_url('http://rd3.videos.sapo.pt/'+match[0]+'/rss2')	
				title = ''
				duration = ''
				thumbnail = ''	
				urlfinal = 	''
				duration = re.compile('<sapo:time>(\d+):(\d+):(\d+)</sapo:time').findall(sapoAPI)
				for horas,minutos,segundos in duration: duration = (int(segundos))+(int(minutos)*60)+(int(horas)*3600)
				thumbnail = re.compile('img src="(.+?)"').findall(sapoAPI)
				title = re.compile('<title>(.+?)</title>').findall(sapoAPI)
				title2 = ''
				title = title[1]
				try: title2 = title[1].decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2			
				urlfinal = re.compile('<sapo:videoFile>(.+?)</sapo:videoFile>').findall(sapoAPI)
				jsontext = '{"prettyname":"'+prettyname+'","url":"'+urlfinal[0]+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail[0]+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': writefile(videocache,'w',jsontext.encode('utf8'))
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:sapo_resolver: '+url+' '+str(e)
				pass
	
def youtube_resolver(url,prettyname):
	match = re.compile('.*?youtube.com/embed/(.+?)\?').findall(url)
	if not match: match = re.compile('.*?youtube.com/embed/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = readfiletoJSON2(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				data=open_url('https://gdata.youtube.com/feeds/api/videos/' + str(match[0]) +'?v2&alt=json')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = parameters['entry']['title']['$t']
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2
				duration = parameters['entry']['media$group']['yt$duration']['seconds']
				thumbnail = parameters['entry']['media$group']['media$thumbnail'][0]['url']
				jsontext= '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads('{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}', encoding="latin-1")
				if getSetting("cachesites") == 'true': writefile(videocache,'w',jsontext)
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:youtube_resolver: '+str(match[0])+' '+str(e)
				pass
    
def daily_resolver(url,prettyname):
	if url.find('?') > -1: match = re.compile('/embed/video/(.+?)\?').findall(url)
	else: match = re.compile('/embed/video/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = readfiletoJSON2(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			try:
				data=open_url('https://api.dailymotion.com/video/' + str(match[0]) +'?fields=title,duration,thumbnail_url,description')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = cleanTitle(parameters['title'])
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2				
				duration = parameters['duration']
				thumbnail = parameters['thumbnail_url']
				jsontext = '{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + str(match[0])+'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': writefile(videocache,'w',jsontext.encode('utf8'))				
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:daily_resolver: '+str(match[0])+' '+str(e)
				pass

def vimeo_resolver(url,prettyname):
	if url.find('?') > -1: match = re.compile('vimeo.com/video/(.+?)\?').findall(url)
	else: match = re.compile('vimeo.com/video/(.*)').findall(url)
	if match:
		videocache = os.path.join(cachePath,str(match[0]))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = readfiletoJSON2(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:	
			try:
				data=open_url('http://player.vimeo.com/video/'+str(match[0])+'/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com')
				parameters = json.loads(data)
				title = ''
				duration = ''
				thumbnail = ''
				title = parameters['video']['title']
				title2 = ''	
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2				
				duration = parameters['video']['duration']
				thumbnail = parameters['video']['thumbs']['640']
				try: url = parameters['request']['files']['h264']['hd']['url']
				except: url = parameters['request']['files']['h264']['sd']['url']
				jsontext = '{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if getSetting("cachesites") == 'true': writefile(videocache,'w',jsontext.encode('utf8'))
				return jsontext,jsonloaded
			except BaseException as e:
				print '##ERROR-funvideos:vimeo_resolver: '+str(match[0])+' '+str(e)
				pass

def videolog_resolver(url,prettyname):
	try:
		ID = re.compile('id_video=(.+?)&amp').findall(url[0])
		videoID = ID[0]		
		videocache = os.path.join(cachePath,str(videoID))
		if getSetting("cachesites") == 'true' and os.path.isfile(videocache):
			jsonline = readfiletoJSON2(videocache)
			jsonloaded = json.loads(jsonline, encoding="utf-8")
			return jsonline,jsonloaded
		else:
			content = abrir_url("http://videolog.tv/"+videoID)
			match = re.compile('<meta property="og:image" content="http://videos.videolog.tv/(.+?)/(.+?)/g_'+id+'_\d+').findall(content)
			image = re.compile('<meta property="og:image" content="(.+?)">').findall(content)
			title = re.compile('<meta property="og:title" content="(.+?)">').findall(content)
			title = cleanTitle(title[0])
			title2 = ''	
			try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
			except: pass
			if title2 <> '': title = title2			
			url='http://videos.videolog.tv/'+match[0]+'/'+match[1]+'/'+id+'.mp4'
			jsontext = '{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title.encode('ascii','xmlcharrefreplace')+'","duration":"60","thumbnail":"'+image[0]+'"}'
			jsonloaded = json.loads(jsontext, encoding="utf-8")
			if getSetting("cachesites") == 'true': writefile(videocache,'w',jsontext.encode('utf8'))			
			return jsontext,jsonloaded
	except BaseException as e:
		print '##ERROR-funvideos:videolog_resolver: '+str(id)+' '+str(e)
		pass

def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-")
	title = title.replace('"',"")
	title = title.strip()
	return title

def open_url(url,type=None):
	if type=='9gag':
		try:
			import requests
			page = requests.get(url)
			return page.text
		except BaseException as e: print '##ERROR-funvideos:open_url: '+str(url)+' '+str(e)		
	else:
		try:
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
			req = urllib2.Request(url)
			req.add_header('User-Agent', user_agent)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			return link
		except BaseException as e: print '##ERROR-funvideos:open_url: '+str(url)+' '+str(e)	
	
def listsites():
	list = []
	ins = open(sitesfile, "r" )	
	for line in ins: 
		parameters = json.loads(line)
		url=parameters['site']
		enabled=parameters['enabled']		
		list.append(json.loads('{"url":"'+url+'","enabled":"'+enabled+'"}'))						
	return list

def readoneline(file):
	f = open(file,"r")
	line = f.read()
	f.close()
	return line

def readalllines(file):
	f = open(file,"r")
	lines = f.readlines()
	f.close()
	return lines

def readfiletoJSON(file):
	parser = HTMLParser()
	f = open(file,"r")
	line = str(f.read().strip('\n')).decode('utf-8').encode('ascii','xmlcharrefreplace')
	print '##line',line
	jsoncache = json.loads(line,encoding='utf-8')
	f.close()
	title = parser.unescape(jsoncache['title'])
	duration = jsoncache['duration']
	thumbnail = jsoncache['thumbnail']
	url = jsoncache['url']
	return title,duration,thumbnail,url

def readfiletoJSON2(file):
	f = open(file,"r")
	line = f.read().strip('\n')
	f.close()	
	return line
	
def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()

def removecache():
	for root,dir,files in os.walk(cachePath):
		for f in files:
			if not '_cache' in f and not '_9gag' in f: os.unlink(os.path.join(root, f))
	xbmcgui.Dialog().ok('Cache','Eliminação Completa.')