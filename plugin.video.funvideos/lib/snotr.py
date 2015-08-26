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
		j = json.loads(page)
		for vid in j['videos']['video']:
			ids = vid['id']
			videocache = os.path.join(cachePath,str(ids))
			if cacheE == 'true' and os.path.isfile(videocache):
				jsonline = basic.readfiletoJSON(videocache)
				jsonloaded = json.loads(jsonline, encoding="utf-8")			
			else:
				title=basic.cleanTitle(vid['title'])
				title2 = ''				
				try: title2 = title.decode('utf8').encode('ascii','xmlcharrefreplace')
				except: pass
				if title2 <> '': title = title2	
				decomp = re.compile('(\d+):(\d+)', re.DOTALL).findall(vid['length'])
				duration = int(decomp[0][0])*60+int(decomp[0][1])
				thumb = 'http://videos.snotr.com/'+str(ids)+'-large.jpg'
				finalUrl='http://videos.snotr.com/'+str(ids)+'.mp4'
				jsontext = '{"prettyname":"'+prettyname+'","url":"'+finalUrl+'","title":"'+title+'","duration":"'+str(duration)+'","thumbnail":"'+thumb+'"}'
				jsonloaded = json.loads(jsontext, encoding="utf-8")
				if cacheE == 'true' and not os.path.isfile(videocache): basic.writefile(videocache,'w',jsontext.encode('utf8'))
			list.append(jsonloaded)
		return list
	except BaseException as e: print '##ERROR-funvideos:Snotr_resolver: '+url+' '+str(e)