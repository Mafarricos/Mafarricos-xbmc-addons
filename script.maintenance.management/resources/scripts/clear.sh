#!/bin/bash
if [ -e /*/.xbmc/addons/packages/* ]; then
rm -r /*/.xbmc/addons/packages/*
echo "- Packages removidos."
fi
if [ -d /*/.xbmc/userdata/Thumbnails/0 ]; then
rm -r /*/.xbmc/userdata/Thumbnails/*
echo "- Cache das Thumbnails removida."
fi
if [ -e /*/.xbmc/userdata/Database/Textures13.db ]; then
rm -r /*/.xbmc/userdata/Database/Textures13.db
echo "- BD Textures removida."
fi
if [ -d /*/.xbmc/userdata/addon_data/script.module.metahandler/meta_cache ]; then
rm -r /*/.xbmc/userdata/addon_data/script.module.metahandler/meta_cache
echo "- Cache metahandler removida."
fi
if [ -e /*/.xbmc/temp/* ]; then
rm -r /*/.xbmc/temp/*
echo "- Pasta temporária removida."
fi
echo "====A Limpar cache de Serviços de Legendas.===="
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.subscene/temp ]; then
echo "- Cache subscene removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.subscene/temp
fi
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.legendasdivx/temp ]; then
echo "- Cache Legendasdivx removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.legendasdivx/temp
fi
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.podnapisi/temp ]; then
echo "- Cache podnapisi removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.podnapisi/temp
fi
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.pipocas/temp ]; then
echo "- Cache pipocas removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.pipocas/temp
fi
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.opensubtitles/temp ]; then
echo "- Cache opensubtitles removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.opensubtitles/temp
fi
if [ -d /*/.xbmc/userdata/addon_data/service.subtitles.legendaszone/temp ]; then
echo "- Cache LegendasZone removida."
rm -r /*/.xbmc/userdata/addon_data/service.subtitles.legendaszone/temp
fi
echo "Reboot em 5 segundos!"
x=1
while [ $x -le 5 ]
do
    echo "$x"
    sleep 1
    x=$(( $x + 1 ))
done
echo "Reboot!"
reboot