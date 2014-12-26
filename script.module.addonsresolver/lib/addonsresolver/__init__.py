# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com
import re,xbmcgui,xbmcaddon,xbmc,os,urllib,json,xbmcplugin
import basic,links,search

addon_id 		= 'script.module.addonsresolver'
selfAddon 		= xbmcaddon.Addon(id=addon_id)
getSetting 		= selfAddon.getSetting
setSetting 		= selfAddon.setSetting
installfolder 	= xbmc.translatePath('special://home/addons')
dummy_file		= os.path.join(xbmc.translatePath('special://home/addons/script.module.addonsresolver'), 'dummyclip.mp4')
dataPath		= os.path.join(xbmc.translatePath('special://temp'),'temp.strm')
language		= selfAddon.getLocalizedString

def initsettings():
	if not os.path.exists(os.path.join(installfolder,links.link().genesis_id)) and getSetting("genesis_enabled") == 'true': setSetting("genesis_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().rato_id)) and getSetting("rato_enabled") == 'true': setSetting("rato_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().wt_id)) and getSetting("wt_enabled") == 'true': setSetting("wt_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().sdp_id)) and getSetting("sdp_enabled") == 'true': setSetting("sdp_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().kmediatorrent_id)) and getSetting("kmediatorrent_enabled") == 'true': setSetting("kmediatorrent_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().stream_id)) and getSetting("stream_enabled") == 'true': setSetting("stream_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().ice_id)) and getSetting("ice_enabled") == 'true': setSetting("ice_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().salts_id)) and getSetting("salts_enabled") == 'true': setSetting("salts_enabled",'false')
	if not os.path.exists(os.path.join(installfolder,links.link().abelhas_id)) and getSetting("abelhas_enabled") == 'true': setSetting("abelhas_enabled",'false')	
	
def play(link,external):
	if 'icefilms' in link or 'abelhas' in link:
		xbmc.executebuiltin('activatewindow(video,'+link+')')
	else:
		#basic.writefile(dataPath,'w',link)
		#link = basic.readoneline(dataPath)
		if external <> 'external': xbmc.Player().play(link)
		else:
			playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
			playlist.clear()
			playlist.add(dummy_file)
			playlist.add(link)		
			xbmc.Player().play(playlist)		
			xbmc.executebuiltin("XBMC.ActivateWindow(12005)")
			xbmc.executebuiltin("XBMC.PlayerControl(Play)")
	#old
	#if 'Sites_dos_Portugas' in link: xbmc.Player().play(link)
	#else:
	#	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	#	playlist.clear()
	#	if external == 'external': playlist.add(dummy_file)
	#	playlist.add(link)
	#	xbmc.Player().play(playlist)
	#	xbmc.executebuiltin("XBMC.ActivateWindow(12005)")
	#	if external == 'external': xbmc.executebuiltin("XBMC.PlayerControl(Play)")

def custom_choice(name,url,imdb_id,year):
	initsettings()
	fromwhere = url
	choose1 = False
	addonchoice = xbmcgui.Dialog().select
	qualitychoice = xbmcgui.Dialog().select
	playlink = []
	playurl = ''
	addons = []
	siterato = ''
	sitewt = ''
	magnet = ''
	see = language(30002)
	if getSetting("genesis_enabled") == 'true':
		addons.append(see % 'Genesis')
		playurl = links.link().genesis_play % (urllib.quote_plus(name),urllib.quote_plus(name),year,imdb_id.strip('tt'),url)
		playlink.append(playurl)
	if getSetting("rato_enabled") == 'true': 
		url = search.ratosearch(imdb_id)
		if url:
			addons.append(see % 'RatoTV')
			playurl = links.link().rato_play % (urllib.quote_plus(url),urllib.quote_plus(name))
			playlink.append(playurl)
	if getSetting("wt_enabled") == 'true':
		url = search.wtsearch(name)
		if url:
			addons.append(see % 'WarezTuga')
			playurl = links.link().wt_play % (urllib.quote_plus(url),urllib.quote_plus(name))
			playlink.append(playurl)
	if getSetting("sdp_enabled") == 'true':
		url = search.sdpsearch(name,imdb_id)
		if url == 'MATCH':
			addons.append(see % 'Sites_dos_Portugas')
			if getSetting("pref_sdp_source") == 'All': automatic = ''
			elif getSetting("pref_sdp_source") == 'Any': automatic = 'sim'
			else: automatic = getSetting("pref_sdp_source")
			playurl= links.link().sdp_search % (imdb_id,urllib.quote_plus(name.replace(' ('+year+')','')),automatic)
			playlink.append(playurl)
	if getSetting("kmediatorrent_enabled") == 'true' or getSetting("stream_enabled") == 'true': qual,magnet = search.ytssearch(imdb_id)
	if getSetting("kmediatorrent_enabled") == 'true':
		if magnet:
			addons.append(see % 'KMediaTorrent')
			playurl = links.link().kmediatorrent_play
			playlink.append(playurl)
	if getSetting("stream_enabled") == 'true':
		if magnet:
			addons.append(see % 'Stream')
			playurl = links.link().stream_play
			playlink.append(playurl)
	if getSetting("ice_enabled") == 'true':
		url = search.icesearch(name)
		if url:
			addons.append(see % 'IceFilms')
			playurl = links.link().ice_play % (urllib.quote_plus(url))
			playlink.append(playurl)
	if getSetting("salts_enabled") == 'true':
		addons.append(see % 'SALTS')
		playurl = links.link().salts_play % (urllib.quote_plus(name.split(' (')[0]),year,urllib.quote_plus(name.split(' (')[0]).replace('+','-')+'-'+year)
		playlink.append(playurl)
	if getSetting("abelhas_enabled") == 'true':
		#if search.abelhassearch(name):
		addons.append(see % 'Abelhas')
		playurl = links.link().abelhas_search % (urllib.quote_plus(name))
		playlink.append(playurl)
	if getSetting("pref_addon") == '-':
		if len(addons) == 0: 
			basic.infoDialog(language(30003))
			choose1 = -1
		else: choose1=addonchoice(language(30004),addons)
	else: 
		index = 0
		choose1 = ''
		for addon in addons:	
			if getSetting("pref_addon").lower() in addon.lower():
				choose1 = index
				break
			index += 1
		if choose1 == '':
			if len(addons) == 0: 
				basic.infoDialog(language(30003))
				choose1 = -1			
			else: choose1=addonchoice(language(30004),addons)
	if choose1 > -1:
		if 'kmediatorrent' in addons[choose1].lower() or 'stream' in addons[choose1].lower():
			q = []
			m = []
			for q1 in qual: q.append(qual)
			for m1 in magnet: m.append(magnet)
			choose2=qualitychoice(language(30005),qual)
			if choose2 > -1:
				if 'kmediatorrent' in addons[choose1].lower(): playlink[choose1] = playlink[choose1] % (urllib.quote_plus(magnet[choose2]))
				elif 'stream' in addons[choose1].lower(): playlink[choose1] = playlink[choose1] % (urllib.quote_plus(magnet[choose2]))
				play(playlink[choose1],fromwhere)
		else: play(playlink[choose1],fromwhere)