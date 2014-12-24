# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2,xbmcaddon,xbmcgui,re,urllib,json,threading
import links,basic
from BeautifulSoup import BeautifulSoup

addon_id 		= 'script.module.addonsresolver'
selfAddon 		= xbmcaddon.Addon(id=addon_id)
language		= selfAddon.getLocalizedString

def icesearch(title):
	if title.lower().startswith('the '): title2 = title.lower().replace('the ','')
	else: title2 = title
	if title2[0].isalpha(): url = links.link().ice_base + "/movies/a-z/" + title2[0].upper()
	else: url = links.link().ice_base + "/movies/a-z/1"
	html = basic.open_url(url)
	soup = BeautifulSoup(html)
	link = soup.find("a", href=re.compile("ip.php"), text=title)
	if link: return links.link().ice_base+link.parent["href"]
	else: return None
		
def ytssearch(imdb_id):
	try:
		quality = []
		magnet = []
		try:
			yts = basic.open_url(links.link().yts_search % (imdb_id))
			jtys = json.loads(yts)
		except: return '',''
		if 'No movies found' in str(jtys): return '',''
		for j in jtys["MovieList"]:
			quality.append(language(30006) % (j["Quality"],j["TorrentSeeds"],j["TorrentPeers"],j["Size"]))
			magnet.append(j["TorrentMagnetUrl"])
		return quality,magnet
	except BaseException as e: print '##ERROR-addonsresolver:ytssearch: '+str(imdb_id)+' '+str(e)

def ratosearch(imdb_id):
	ratos = basic.open_url(links.link().rato_search % (imdb_id))
	try: siterato = re.compile('<span class="more-btn"><a href="(.+?)" >Ver Agora</a>').findall(ratos)[0]
	except: siterato = False
	return siterato

def wtsearch(name):
	wt = basic.open_url(links.link().wt_search % (urllib.quote_plus(name)))
	try: 
		sitewt = re.compile('<a href="(.+?)" class="movie-name">').findall(wt)[0]
		sitewt = links.link().wt_base % (sitewt)
	except: 
		wt = basic.open_url(links.link().wt_search % (urllib.quote_plus(name.split(' (')[0])))
		try: 
			sitewt = re.compile('<a href="(.+?)" class="movie-name">').findall(wt)[0]
			sitewt = links.link().wt_base % (sitewt)
		except: sitewt = False
	return sitewt

def _sdpsearch(name,link,result):
	sdp = basic.open_url(link % (urllib.quote_plus(name)))
	if sdp:
		if 'Nenhuma mensagem corresponde' in sdp or 'nothing matched' in sdp: result.append('NOTFOUND')
		else: result.append('MATCH')
	
def sdpsearch(name,imdb):
	try: search = name.split(' (')[0]
	except: search = name
	threads = []
	result = []
	for i in range(7): threads.append(threading.Thread(name=name+str(i),target=_sdpsearch,args=(search,links.link().sdp_search_add[i],result, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	if result:	
		for res in result: 
			if 'MATCH' in res: return res