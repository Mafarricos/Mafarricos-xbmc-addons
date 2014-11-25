﻿# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,re,threading,json,os,xbmcaddon,xbmcgui,xbmc
	
addon_id = 'plugin.video.funvideos'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
sitesfile = os.path.join(os.path.join(addonfolder, 'resources'),'sites.txt')
progress = xbmcgui.DialogProgress()
	
def getpages(id):
	list = []
	ins = open(sitesfile, "r" )
	progress.create('Fun Videos', 'A Obter dados...')
	i = 1
	t = 0
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
			else:
				startsection = parameters['startsection']
				endsection = parameters['endsection']
				list2 = grablinks(site+pageindex+str(id+starton),prettyname,startsection,endsection)
				if list2: list.extend(list2)
		if progress.iscanceled():
			progress.close()
			xbmcgui.Dialog().ok('ERROR','Cancelled.')
			return ''	
	ins.close()
	progress.close()
	unique_stuff = { each['url'] : each for each in list }.values()
	return unique_stuff

def grabiframes(mainURL,prettyname,results=None,index=None):
	list = []
	page = open_url(mainURL)
	blocker = re.findall('data-videoid="(.+?)"', page, re.DOTALL)
	if blocker:
		fakeframe='<iframe src="http//www.youtube.com/embed/'+blocker[0]+'"</iframe>'
		html_source_trunk = re.findall('<iframe(.*?)</iframe>', fakeframe, re.DOTALL)	
	else: html_source_trunk = re.findall('<iframe(.*?)</iframe>', page, re.DOTALL)
	for trunk in html_source_trunk:
			try: iframe = re.compile('src="(.+?)"').findall(trunk)[0]
			except: 
				try: iframe = re.compile("src='(.+?)'").findall(trunk)[0]
				except: iframe = ''
			if iframe:
				if iframe.find('ad120m.com') > -1 or iframe.find('facebook') > -1 or iframe.find('metaffiliation') > -1 or iframe.find('banner600') > -1 or iframe.find('engine.adbooth.com') > -1 or iframe.find('www.lolx2.com') > -1 or iframe.find('jetpack.wordpress.com') > -1: pass
				else:
					print "##funvideos-grabiframes: "+iframe
					if iframe.find('youtube') > -1:
						resolver_iframe = youtube_resolver(iframe,prettyname)
						if resolver_iframe: 	
							if index: results.append(resolver_iframe)
							else: list.append(resolver_iframe)
					elif iframe.find('dailymotion') > -1:
						resolver_iframe = daily_resolver(iframe,prettyname)
						if resolver_iframe: 							
							if index: results.append(resolver_iframe)
							else: list.append(resolver_iframe)
					elif iframe.find('vimeo') > -1:
						resolver_iframe = vimeo_resolver(iframe,prettyname)
						if resolver_iframe: 							
							if index: results.append(resolver_iframe)
							else: list.append(resolver_iframe)							
					elif iframe.find('sapo') > -1:
						resolver_iframe = sapo_resolver(iframe,prettyname)
						if resolver_iframe: 							
							if index: results.append(resolver_iframe)
							else: list.append(resolver_iframe)	
					elif iframe.find('videolog') > -1:
						resolver_iframe = videolog_resolver(iframe,prettyname)
						if resolver_iframe: 							
							if index: results.append(resolver_iframe)
							else: list.append(resolver_iframe)						
					else: print '##ERROR-funvideos:frame on server not supported: '+iframe
	if not index: return list
		
def grablinks(mainURL,prettyname,sectionstart,sectionend):
	list = []
	page = open_url(mainURL)
	html_source_trunk = re.findall(sectionstart+'(.*?)'+sectionend, page, re.DOTALL)
	threads = []
	results = []
	for i in range(0, len(html_source_trunk)): 
		print "##funvideos-grablinks: "+html_source_trunk[i]
		threads.append(threading.Thread(name=mainURL+str(i),target=grabiframes,args=(html_source_trunk[i], prettyname, results, i, )))	
	[i.start() for i in threads]
	[i.join() for i in threads]
	return results

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
			list.append(json.loads('{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(id)+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumb+'"}', encoding="utf-8"))
		if list: return list
	except BaseException as e:
		print '##ERROR-funvideos:VitaminL_resolver: '+url+' '+str(e)
		pass

def sapo_resolver(url,prettyname):
	match = re.compile('file=http://.+?/(.+?)/mov/').findall(url)
	if match: 
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
			urlfinal = re.compile('<sapo:videoFile>(.+?)</sapo:videoFile>').findall(sapoAPI)
			return json.loads('{"prettyname":"'+prettyname+'","url":"'+urlfinal[0]+'","title":"'+title[1].decode("utf-8")+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail[0]+'"}', encoding="utf-8")			
		except BaseException as e:
			print '##ERROR-funvideos:sapo_resolver: '+url+' '+str(e)
			pass
	
def youtube_resolver(url,prettyname):
	match = re.compile('.*?youtube.com/embed/(.+?)\?').findall(url)
	if not match: match = re.compile('.*?youtube.com/embed/(.*)').findall(url)
	if match:
		try:
			data=open_url('https://gdata.youtube.com/feeds/api/videos/' + str(match[0]) +'?v2&alt=json')
			parameters = json.loads(data)
			title = ''
			duration = ''
			thumbnail = ''
			title = parameters['entry']['title']['$t']
			duration = parameters['entry']['media$group']['yt$duration']['seconds']
			thumbnail = parameters['entry']['media$group']['media$thumbnail'][0]['url']
			return json.loads('{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}', encoding="utf-8")
		except BaseException as e:
			print '##ERROR-funvideos:youtube_resolver: '+str(match[0])+' '+str(e)
			pass
    
def daily_resolver(url,prettyname):
	if url.find('?') > -1: match = re.compile('/embed/video/(.+?)\?').findall(url)
	else: match = re.compile('/embed/video/(.*)').findall(url)
	if match:
		try:
			data=open_url('https://api.dailymotion.com/video/' + str(match[0]) +'?fields=title,duration,thumbnail_url,description')
			parameters = json.loads(data)
			title = ''
			duration = ''
			thumbnail = ''
			title = cleanTitle(parameters['title'])
			duration = parameters['duration']
			thumbnail = parameters['thumbnail_url']
			return json.loads('{"prettyname":"'+prettyname+'","url":"plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + str(match[0])+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}', encoding="utf-8")
		except BaseException as e:
			print '##ERROR-funvideos:daily_resolver: '+str(match[0])+' '+str(e)
			pass

def vimeo_resolver(url,prettyname):
	if url.find('?') > -1: match = re.compile('vimeo.com/video/(.+?)\?').findall(url)
	else: match = re.compile('vimeo.com/video/(.*)').findall(url)
	if match:
		try:
			data=open_url('http://player.vimeo.com/video/'+str(match[0])+'/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com')
			parameters = json.loads(data)
			title = ''
			duration = ''
			thumbnail = ''
			title = parameters['video']['title']
			duration = parameters['video']['duration']
			thumbnail = parameters['video']['thumbs']['640']
			try: url = parameters['request']['files']['h264']['hd']['url']
			except: url = parameters['request']['files']['h264']['sd']['url']		
			return json.loads('{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumbnail+'"}', encoding="utf-8")
		except BaseException as e:
			print '##ERROR-funvideos:vimeo_resolver: '+str(match[0])+' '+str(e)
			pass

def videolog_resolver(url,prettyname):
	try:
		ID = re.compile('id_video=(.+?)&amp').findall(url[0])
		videoID = ID[0]
		content = abrir_url("http://videolog.tv/"+videoID)
		match = re.compile('<meta property="og:image" content="http://videos.videolog.tv/(.+?)/(.+?)/g_'+id+'_\d+').findall(content)
		image = re.compile('<meta property="og:image" content="(.+?)">').findall(content)
		title = re.compile('<meta property="og:title" content="(.+?)">').findall(content)
		title = cleanTitle(title[0])
		url='http://videos.videolog.tv/'+match[0]+'/'+match[1]+'/'+id+'.mp4'
		return json.loads('{"prettyname":"'+prettyname+'","url":"' + url +'","title":"'+title+'","duration":"60","thumbnail":"'+image[0]+'"}', encoding="utf-8")		
	except BaseException as e:
		print '##ERROR-funvideos:videolog_resolver: '+str(id)+' '+str(e)
		pass

def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", "\"").replace("&ndash;", "-")
	title = title.replace('"',"")
	title = title.strip()
	return title

def open_url(url):
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