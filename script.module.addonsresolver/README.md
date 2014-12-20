Instructions how to interact this addon with others.

To import the addon:
import addonsresolver

Add a entry to setup the addon in your own:
import xbmc
xbmc.executebuiltin('Addon.OpenSettings('script.module.addonsresolver')

Function to call:
addonsresolver.custom_choice(originalname,url,imdb_id,year)

Parameters:
originalname -> Original Name of movie
imdb_id -> imdb ID
year -> Release Year of movie
url -> still optional, should be sent as '' if not used.

Working with:
Portuguese addons:
- Wareztuga;
- RatoTV;
- Sites_dos_Portugas.
International addons:
- Genesis;
- KmediaTorrent;
- Stream.
