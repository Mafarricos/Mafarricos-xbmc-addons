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
icon01 = 'https://s-media-cache-ak0.pinimg.com/236x/e1/ab/c1/e1abc18c7f77ff62d8f67d3e6b2a1839.jpg'
icon02 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/7/9/8/9789892309897.jpg'
icon03 = 'http://www.bulhosa.pt/images/products/9789892313405.jpg'
icon03a = 'https://i.ytimg.com/sh/sWYhfbn3Tf4/showposter.jpg'
icon03b = 'http://mco-s1-p.mlstatic.com/octonautas-octonauts-4-figuras-accion-serie-tv-578511-MCO20594470018_022016-O.jpg'
icon04 = 'http://www.leyaonline.com/fotos/produtos/500_9789892308722_noddy_joga_as_escondidas.jpg'
icon05 = 'http://vignette3.wikia.nocookie.net/pocoyoworld/images/2/2f/Pocoyo-Image-300x300_Pato_Elly_Loula_Sleepy_Bird.jpg'
icon06 = 'http://www.animewebradio.it/awr1/data/img/uploads/HEIDI_SPECIAL.jpg'
icon07 = 'http://pumpkin.pt/article/12249/featured_large.png'
icon08 = 'http://lh6.ggpht.com/U2HRHrr3p0Y0s-2L0rOtDArAOMs3IDm0P1DWRD19DWPjsCZoRQFFhxdmPIUK07v6mVee=w300'
icon09 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/5/5/1/9789892702155.jpg'
icon10 = 'http://www.childrens-rooms.co.uk/childrensrooms-web/v2/images/products/viewproduct_popup/5281.jpg'
icon10a = 'http://d1oklq6066osfz.cloudfront.net/feelslikesummer_0.jpg'
icon10b = 'https://lh4.ggpht.com/VRO98y4Ug9Z_LnnGHQM7v1pSXV8ZBoXo9bjbFB-dHQzdFJ_el5tLzIaFd_9QSqlAr6m1=w300'
icon11 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/4/0/9789892315041.jpg'
icon12 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/1/6/8/0602537176861.jpg'
icon13 = 'http://static.fnac-static.com/multimedia/PT/images_produits/PT/ZoomPE/6/8/6/0602527851686.jpg'
icon13a = 'http://orig13.deviantart.net/4a7c/f/2015/145/6/a/album__va___violetta_l_album_de_la_saison_1_by_hazmanot_azarim-d7q2h6m.jpg'
icon14 = 'http://img.lum.dolimg.com/v1/images/open-uri20150422-20810-1hyxdss_2afe84d9.jpeg'
icon15 = 'http://img.elo7.com.br/product/zoom/10A1C0E/capa-almofada-snoopy-charlie-brown-presentes.jpg'
icon16 = 'http://img.submarino.com.br/produtos/01/00/item/7043/2/7043215g1.jpg'
icon17 = 'https://pbs.twimg.com/profile_images/378800000465332857/aa5cc860371f39fa7e1569dea0264ac0.png'
icon18 = 'http://vignette4.wikia.nocookie.net/doblaje/images/a/aa/Jelly_Jamm.jpg/revision/latest?cb=20120728140403&path-prefix=es'
icon19 = 'http://image.blingee.com/images18/content/output/000/000/000/768/724757491_332199.gif?4'
icon20 = 'https://f1.bcbits.com/img/a0145682558_10.jpg'
icon21 = 'http://img.fnac.com.br/Imagens/Produtos/354-647221-0-5-belos-contos-de-fada-para-meninos.jpg'
icon22 = 'http://2.bp.blogspot.com/_7WgaK1xWlsc/SONRoeLP68I/AAAAAAAAARc/0nBqB050ugQ/s400/DARTACAOO.JPG'
icon23 = 'http://image.slidesharecdn.com/eraumavezohomem-pt0001-nasceaterra1995-150901134452-lva1-app6892/95/era-uma-vez-o-homem-nasce-a-terra-1995-2-638.jpg?cb=1441115162'
icon24 = 'http://image.slidesharecdn.com/eraumavezocorpohumano-pt0002-apele-150828112451-lva1-app6892/95/era-uma-vez-o-corpo-humano-a-pele-2-638.jpg?cb=1440761174'
icon25 = 'http://1.bp.blogspot.com/-PwpeifffzX0/UHlLJAIRp1I/AAAAAAAACX0/3qSdzoIQZCo/s1600/os_Inventores.jpg'
icon26 = 'http://image.slidesharecdn.com/eraumavezoespaco-pt0001-oplanetaomega-150902161657-lva1-app6891/95/era-uma-vez-o-espaco-o-planeta-omega-1-638.jpg?cb=1441210669'


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
	plugintools.add_item(title = "[ Angry Birds ]", url = base + "playlist/PLTR8zrKWyBqj8zgoDhKhXgRha2CUNGAuT/", thumbnail = icon01, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ruca - T01 a T12 [PT]", url = base + "playlist/PLo38DhqHYWY0gJAKJe-onxyIS9X17RRLt/", thumbnail = icon02, fanart = fan01, folder = True)
	plugintools.add_item(title = "Ruca - T13 a T24 [PT]", url = base + "playlist/PLo38DhqHYWY259zbKwaNYmSqA4f4YJqiH/", thumbnail = icon03, fanart = fan01, folder = True)
	plugintools.add_item(title = "PJ Masks [PT]", url = base + "playlist/PLlYGGSWIiHx2P_XBQuwQzpQJ2VSfYGnQ7/", thumbnail = icon03a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Octonautas [PT]", url = base + "playlist/PLjRUOcyjSeAxv2ITxi2CVbNKUz-cK9YfA/", thumbnail = icon03b, fanart = fan01, folder = True)
	plugintools.add_item(title = "Noddy [PT]", url = base + "playlist/PLrH5HKiu5jUeEVAVEctaHl1qud4zbYg5O/" , thumbnail = icon04, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Pocoyo [PT]", url = base + "user/childrenvideos/", thumbnail = icon05, fanart = fan01, folder = True)
	plugintools.add_item(title = "Heidi 3D [PT]", url = base + "playlist/PLnp6B7ujCv2A8aaaa-6niKGW-SoChr88d/", thumbnail = icon06, fanart = fan01, folder = True)	
	plugintools.add_item(title = "Abelha Maia 3D [PT]", url = base + "playlist/PLTf5zA07OijMLjuAJGYQ_dT7s8fgo7kpN/", thumbnail = icon07, fanart = fan01, folder = True)
	plugintools.add_item(title = "Herois da Cidade [PT]", url = base + "playlist/PLFepGKlvmn74D95OwZkSSQR3uk4T2ReHD/", thumbnail = icon08, fanart = fan01, folder = True)
	plugintools.add_item(title = "Bob o Construtor [PT]", url = base + "playlist/PLrH5HKiu5jUd7KNHHylSmu_WvFZ1pyURq/", thumbnail = icon09, fanart = fan01, folder = True)
	plugintools.add_item(title = "Thomas e Amigos [PT]", url = base + "playlist/PLZ-7k3FZDGmm5XODLaqSXX98OME6gk6Um/", thumbnail = icon10, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Ovelha Choné - T01 ]", url = base + "playlist/PLzAgPTA2_pP1Ja1CUN86lGLyI7JMc2-Uc/"           , thumbnail = icon10a, fanart = fan01, folder = True)
	plugintools.add_item(title = "[ Ovelha Choné - T02 ]", url = base + "playlist/PLzAgPTA2_pP3uLW-FczIgRn1bDkfdfOdi/"           , thumbnail = icon10b, fanart = fan01, folder = True)
	plugintools.add_item(title = "Vila Moleza [PT]", url = base + "playlist/PLrH5HKiu5jUeWGDGh3EYBvMQ-eU1CSy4J/", thumbnail = icon11, fanart = fan01, folder = True)
	plugintools.add_item(title = "Panda e os Caricas [PT]", url = base + "channel/UCvw-R-r3p6Hc-yj1qyoPslQ/", thumbnail = icon12, fanart = fan01, folder = True)
	plugintools.add_item(title = "Xana Toc Toc [PT]", url = base + "user/XanaTocTocVEVO/", thumbnail = icon13, fanart = fan01, folder = True)
	plugintools.add_item(title = "Violeta [Musicais]", url = base + "playlist/PLE308E8FD36F34EAC/", thumbnail = icon13a, fanart = fan01, folder = True)
	plugintools.add_item(title = "Disney [BR]", url = base + "user/DisneyDesenhos/", thumbnail = icon14, fanart = fan01, folder = True)
	plugintools.add_item(title = "Snoopy [BR]", url = base + "playlist/PLolevrZYo2eGlwPrvK1Nr_rwUGSpbJMYK/", thumbnail = icon15, fanart = fan01, folder = True)
	plugintools.add_item(title = "Turma da Mónica [BR]", url = base + "playlist/PLWduEF1R_tVZYNTH8ajFOEDkDT_hfIQL9/", thumbnail = icon16, fanart = fan01, folder = True)
	plugintools.add_item(title = "Masha e o Urso [BR]", url = base + "channel/UCJKBSfD5JSUxGhriFeoPCCg/", thumbnail = icon17, fanart = fan01, folder = True)
	plugintools.add_item(title = "Jelly Jamm [BR]"  , url = base + "playlist/PL-CfLd2XMlrw7Cq-LT4UMNJrzLr9OjMpk/", thumbnail = icon18, fanart = fan01, folder = True)
	plugintools.add_item(title = "Sonic X [BR]", url = base + "playlist/PLj0Fsa9q1GRCKN_i_-1zRTM0m9m-GW6E1/", thumbnail = icon19, fanart = fan01, folder = True)
	plugintools.add_item(title = "Tartarugas Ninja [PT]", url = base + "playlist/PL12TUMahWFQR6XqoHTKm5-RvCSYy1EPg1/", thumbnail = icon20, fanart = fan01, folder = True)
	plugintools.add_item(title = "Contos Infantis [PT]", url = base + "channel/UCOre4lsfRMaC62bOHUjPp2Q/", thumbnail = icon21, fanart = fan01, folder = True)
	plugintools.add_item(title = "Dartacão [PT]", url = base + "playlist/PLrH5HKiu5jUe8ZF8jwdtprpucMVEjRON5/", thumbnail = icon22, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez: o Homem", url = base + "playlist/PLQOUgVTEqh7lC6rOH9nBCCouKUHz_MAvC/", thumbnail = icon23, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez: o Corpo [PT]", url = base + "playlist/PLQOUgVTEqh7mgd3QGat4A0MgFkVnrmA4g/", thumbnail = icon24, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez: Inventores [PT]", url = base + "playlist/PLQOUgVTEqh7kr1tcxWPJyfldtNuXKhopw/", thumbnail = icon25, fanart = fan01, folder = True)
	plugintools.add_item(title = "Era uma vez: o Espaço [PT]", url = base + "playlist/PLe3xGiBq_EhMMeiBXg5cW53JY_X41t1SR/", thumbnail = icon26, fanart = fan01, folder = True)
	plugintools.add_item(title = "Fim da Lista", thumbnail = icon, fanart = fan01, folder = True)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode()')
	
run()
