# -*- coding: utf-8 -*-
#------------------------------------------------------------
# jami
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools
from addon.common.addon import Addon

addonID = 'plugin.video.jami'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

fan01 = 'https://i.ytimg.com/vi/Sb4EwT6yoDE/maxresdefault.jpg'
icon01 = 'http://img.fnac.com.br/Imagens/Produtos/354-647221-0-5-belos-contos-de-fada-para-meninos.jpg'
icon02 = 'http://2.bp.blogspot.com/_7WgaK1xWlsc/SONRoeLP68I/AAAAAAAAARc/0nBqB050ugQ/s400/DARTACAOO.JPG'
icon03 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/7/9/8/9789892309897.jpg'
icon04 = 'http://vignette3.wikia.nocookie.net/pocoyoworld/images/2/2f/Pocoyo-Image-300x300_Pato_Elly_Loula_Sleepy_Bird.jpg'
icon05 = 'http://www.leyaonline.com/fotos/produtos/500_9789892308722_noddy_joga_as_escondidas.jpg'
icon06 = 'https://s-media-cache-ak0.pinimg.com/236x/9e/54/6f/9e546fcdcf39b9c77d4f059ee300a0eb.jpg'
icon07 = 'http://pumpkin.pt/article/12249/featured_large.png'
icon08 = 'http://lh6.ggpht.com/U2HRHrr3p0Y0s-2L0rOtDArAOMs3IDm0P1DWRD19DWPjsCZoRQFFhxdmPIUK07v6mVee=w300'
icon09 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/5/5/1/9789892702155.jpg'
icon10 = 'http://www.childrens-rooms.co.uk/childrensrooms-web/v2/images/products/viewproduct_popup/5281.jpg'
icon10a = 'http://www.animewebradio.it/awr1/data/img/uploads/HEIDI_SPECIAL.jpg'
icon11 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/4/0/9789892315041.jpg'
icon12 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/6/8/0602537176861.jpg'
icon13 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/6/8/6/0602527851686.jpg'
icon13a = 'http://orig13.deviantart.net/4a7c/f/2015/145/6/a/album__va___violetta_l_album_de_la_saison_1_by_hazmanot_azarim-d7q2h6m.jpg'
icon14 = 'http://img.lum.dolimg.com/v1/images/open-uri20150422-20810-1hyxdss_2afe84d9.jpeg'
icon14a = 'http://1.bp.blogspot.com/-0NumVpLuZR4/TVkWAQnr4vI/AAAAAAAABuY/I3YYpAySd4o/s1600/capa.png'
icon15 = 'https://s-media-cache-ak0.pinimg.com/favicons/70f47683076ee0670a2e4b51ba9eea443f005a3cccde9f2ab04da67b.png?027f4656c074a031ee558ec7f584d80b'
icon16 = 'http://img.submarino.com.br/produtos/01/00/item/7043/2/7043215g1.jpg'
icon17 = 'http://img.elo7.com.br/product/zoom/10A1C0E/capa-almofada-snoopy-charlie-brown-presentes.jpg'
icon18 = 'http://vignette4.wikia.nocookie.net/doblaje/images/a/aa/Jelly_Jamm.jpg/revision/latest?cb=20120728140403&path-prefix=es'
icon19 = 'http://image.blingee.com/images18/content/output/000/000/000/768/724757491_332199.gif?4'
icon20 = 'https://pbs.twimg.com/profile_images/500673266097606656/Qt6uwVZ0.jpeg'
icon21 = 'https://f1.bcbits.com/img/a0145682558_10.jpg'


def run():
    plugintools.log("jami.run")
    params = plugintools.get_params()
    if params.get("action") is None: main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()

def main_list(params):
	plugintools.log("jami ===> " + repr(params))
	plugintools.add_item(title = "Contos Infantis [PT]", url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLrH5HKiu5jUe8ZF8jwdtprpucMVEjRON5/", thumbnail = icon02, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Ruca [PT]", url = base + "playlist/PLQOUgVTEqh7mNhuwQpSEEqoarMbA74B9o/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon04, fanart = fan01, folder = True)
	plugintools.add_item(title = "Noddy [PT]", url = base + "channel/UCbJ3FpU6NZ4T4Ca_BxXtaGA/" , thumbnail = icon05, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Ovelha Choné [PT]", url = base + "playlist/PLYbNlr-XymEXbsyrLjyqoZRRFtGiFrGyf/"           , thumbnail = icon06, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Abelha Maia [PT]", url = base + "playlist/PLkodmAlL47W0kgZKcX7XJKd0CC6qknZVV/", thumbnail = icon07, fanart = fan01, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "channel/UCnfjtca0KeZND5e27IO4INg/", thumbnail = icon08, fanart = fan01, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLrH5HKiu5jUd7KNHHylSmu_WvFZ1pyURq/", thumbnail = icon09, fanart = fan01, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLZ-7k3FZDGmm5XODLaqSXX98OME6gk6Um/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "Heidi 3D [PT]", url = base + "playlist/PLnp6B7ujCv2A8aaaa-6niKGW-SoChr88d/", thumbnail = icon10a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLrH5HKiu5jUeWGDGh3EYBvMQ-eU1CSy4J/", thumbnail = icon11, fanart = fan01, folder = True)
	plugintools.add_item(title = "Panda e os Caricas [PT]", url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "user/XanaTocTocVEVO/", thumbnail = icon13, fanart = fan01, folder = True)
	plugintools.add_item(title = "Violeta [Musicais]", url = base + "playlist/PLE308E8FD36F34EAC/", thumbnail = icon13a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Disney [BR]", url = base + "user/DisneyDesenhos/", thumbnail = icon14, fanart = fan01, folder = True)
	plugintools.add_item(title = "Mickey e Donald [BR]", url = base + "playlist/PLvHIdIaG-9g6H-8K3rrUAFd0wKn8BzQ6u/", thumbnail = icon14a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Looney Tunes [BR]", url = base + "playlist/PLpWx6MEwzdl43CvZffNXnYbcUFyB2ZPlz/", thumbnail = icon15, fanart = fan01, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "channel/UCV4XcEqBswMCryorV_gNENw/", thumbnail = icon16, fanart = fan01, folder = True)
	plugintools.add_item(title = "Snoopy [BR]", url = base + "playlist/PLolevrZYo2eGlwPrvK1Nr_rwUGSpbJMYK/", thumbnail = icon17, fanart = fan01, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]"  , url = base + "user/JellyJammPortugues/", thumbnail = icon18, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic X [BR]", url = base + "playlist/PLj0Fsa9q1GRCKN_i_-1zRTM0m9m-GW6E1/", thumbnail = icon19, fanart = fan01, folder = True)
	plugintools.add_item(title = "Marvel x DC [BR]", url = base + "channel/UCBgLQ56vPMX58_5-oflQcTA/", thumbnail = icon20, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tartarugas Ninja [PT]", url = base + "playlist/PL12TUMahWFQR6XqoHTKm5-RvCSYy1EPg1/", thumbnail = icon21, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode()')
	
run()
