# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import links,json,basic,re,xbmcaddon,os,localdb

getSetting          = xbmcaddon.Addon().getSetting

def listmovies(url):
	basic.log(u"omdbapi.listmovies url: %s" % url)
	mainlist = []
	sendlist = [] 
	result = []
	threads = []
	order = 0
	jsonpage = basic.open_url(url)
	j = json.loads(jsonpage)
	for list in j['results']: 
		order += 1
		sendlist.append([order,list['id']])
	chunks=[sendlist[x:x+5] for x in xrange(0, len(sendlist), 5)]
	for i in range(len(chunks)): threads.append(threading.Thread(name='listmovies'+str(i),target=searchmovielist,args=(chunks[i],result, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	result = sorted(result, key=basic.getKey)
	for id,lists in result: mainlist.append(lists)
	basic.log(u"omdbapi.listmovies mainlist: %s" % mainlist)	
	return mainlist

def searchmovielist(list,result):
	basic.log(u"omdbapi.searchmovielist list: %s" % list)
	for num,id in list: 
		moviedata = searchmovie(id)
		if moviedata: result.append([num,moviedata])
	basic.log(u"omdbapi.searchmovielist result: %s" % result)
	
def searchmovie(id,cache=True):
	basic.log(u"omdbapi.searchmovie id: %s" % id)
	listgenre = []
	listcast = []
	listcastr = []	
	genre = ''
	title = ''
	plot = ''
	tagline = ''
	director = ''
	writer = ''
	credits = ''
	poster = ''
	fanart = ''
	trailer = ''
	year = ''
	dur = 0
	if cache:
		if getSetting("cachesites") == 'true':
			cached = localdb.get_cache(id)
			if cached:
				response = { "label": cached[2], "originallabel": cached[3], "poster": cached[4], "fanart_image": cached[5], "imdbid": cached[0], "year": cached[6], "info": json.loads(cached[7]) }
				return response		
	jsonpage = basic.open_url(links.link().omdbapi_info % (id))
	jdef = json.loads(jsonpage)
	title = jdef['Title']
	poster = jdef['Poster']
	fanart = poster
	genre = jdef['Genre']
	plot = jdef['Plot']
	tagline = plot
	try: year = re.findall('(\d+)', jdef['Year'], re.DOTALL)[0]
	except: year = jdef['Year']
	listcast = jdef['Actors'].split(', ')
	director = jdef['Director']
	writer = jdef['Writer']
	duration = re.findall('(\d+) min', jdef['Runtime'], re.DOTALL)
	if duration: dur = int(duration[0])
	else: 
		duration = re.findall('(\d) h', jdef['Runtime'], re.DOTALL)
		if duration: dur = int(duration[0])*60
	info = {
			"genre": genre, 
			"year": year,
			"rating": jdef['imdbRating'], 
			"cast": listcast,
			"castandrole": listcast,
			"director": director,
			"plot": plot,
			"plotoutline": plot,
			"title": title,
			"originaltitle": title,
			"duration": dur,
			"studio": '',
			"tagline": tagline,
			"writer": writer,
			"premiered": '',
			"code": id,
			"credits": '',
			"votes": jdef['imdbVotes'],
			"trailer": ''
			}		
	response = {
		"label": '%s (%s)' % (title,year),
		"originallabel": '%s (%s)' % (title,year),
		"poster": poster,
		"fanart_image": fanart,
		"imdbid": id,
		"year": year,
		"info": info
		}
	if cache:
		if getSetting("cachesites") == 'true': localdb.save_cache(id,'','%s (%s)' % (title,year),'%s (%s)' % (originaltitle,year),poster,fanart,year,json.dumps(info))
	return response