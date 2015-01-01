# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import basic,links,json,tmdb,threading,xbmcaddon,os

def listmovies(url,index,cachePath):
	basic.log(u"trakt.listmovies url: %s" % url)
	mainlist = []
	sendlist = [] 
	result = []
	threads = []
	order = 0
	if 'popular' in url: headers = { 'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': '', 'page': index, 'limit': '30' }
	elif 'trending' in url: headers = { 'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': links.link().trakt_apikey, 'page': index, 'limit': '30' }	
	print headers,url
	jsonpage = basic.open_url_headers(url,headers)
	print 'jsonpage %s' % jsonpage
	j = json.loads(jsonpage)
	for list in j:
		order += 1
		if 'trending' in url: sendlist.append([order,list['movie']['ids']['tmdb']])
		elif 'popular' in url: sendlist.append([order,list['ids']['tmdb']])
	chunks=[sendlist[x:x+5] for x in xrange(0, len(sendlist), 5)]
	print 'chunks',chunks
	for i in range(len(chunks)): threads.append(threading.Thread(name='listmovies'+str(i),target=tmdb.searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	result = sorted(result, key=basic.getKey)
	for id,lists in result: mainlist.append(lists)
	basic.log(u"trakt.listmovies mainlist: %s" % mainlist)	
	return mainlist