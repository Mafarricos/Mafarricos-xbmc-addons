# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import os,json,re
import basic

def grab(url,prettyname,cachePath,cacheE):
	list = []
	try:
		page = basic.open_url(url)
		links = re.compile('<article class="video-preview" data-viewkey=".+?"><a title=".+?" href="(.+?)">', re.DOTALL).findall(page)
		for link in links:
			spage = basic.open_url('http://www.funnyordie.com'+link)
			title = basic.cleanTitle(re.compile('<meta property="og:title" content="(.+?)">', re.DOTALL).findall(spage)[0])
			thumb = re.compile('<meta property="og:image" content="(.+?)">', re.DOTALL).findall(spage)[0]
			title2 = ''				
			try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
			except: pass
			if title2 <> '': title = title2	
			duration = re.compile('<meta property="video:duration" content="(\d+)"/>', re.DOTALL).findall(spage)[0]
			finalUrl= 'http://'+re.compile('<source src="//(.+?)" type=\'video/mp4\'>', re.DOTALL).findall(spage)[0]
			jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumb+'"}'
			jsonloaded = json.loads(jsontext, encoding="utf-8")
			list.append(jsonloaded)
		return list
	except BaseException as e: print '##ERROR-funvideos:funnyordie_resolver: '+url+' '+str(e)