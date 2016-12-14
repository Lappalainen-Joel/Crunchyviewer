# Crunchyviewer
Wrapper script for liveviewer. Solely purpose is to view crunchyroll's videos. 

Liveviewer is required for running this script. Should work fine within linux or windows. Check comments in code for details.


USAGE:
  $ crunchyviewer.py
      Do tell the series you want to watch
      Case sensitive, eq. Naruto Shippuden:
      Gintama
      ...
      4 /gintama/episode-4-watch-out-weekly-shonen-jump-sometimes-comes-out-on-saturdays-510148
      3 /gintama/episode-3-nobody-with-naturally-wavy-hair-can-be-that-bad-510126
      2 /gintama/episode-2-you-guys-do-you-even-have-a-gintama-part-2-510096
      1 /gintama/episode-1-you-guys-do-you-even-have-a-gintama-part-1-510074
      Which episode would you like to watch?
      3
      [cli][info] Found matching plugin crunchyroll for URL http://www.crunchyroll.com/gintama/episode-3-nobody-with-naturally-wavy-hair-         can-be-that-bad-510126
      [plugin.crunchyroll][warning] No authentication provided, you won't be able to access premium restricted content
      [cli][info] Available streams: high, low (worst), mid, ultra (best)
      [cli][info] Opening stream: ultra (hls)
      [cli][info] Starting player: "C:\Program Files\VideoLAN\VLC\vlc.exe"



On next release:
  - Separate configuration file, for declaring some additional options (such as. player, quality and so on.. ) 
  - tinydb for storing episode urls
  - case insensitive series searching
