# Crunchyviewer
Wrapper script for liveviewer. Solely purpose is to view crunchyroll's videos. 

22.12.2016: Added separate configuration file for setting up livestreamer executable path, separate player and defining quality.
            as well added support for running crunchyviewer with series-name.

How to use:
            1. Clone repository
            2. Install following modules (eq. via pip):
                        - livestreamer
                        - json
                        - bs4 (beautiful soup)
                        - subprocess
                        - requests
            3. Run crunchyviewer.py, and follow instructions.
            
            
You can change default player by changing 'pl' -parameter in crunchyviewer.ini. Just remember to use full filepath to the executable (it should work with Linux as well.). And use a player which supports media streaming from network. 

For the whilebeing, please ignore chromecast scripts. They should work as 'standalone' scripts, but i need to change the program structure, so that crunchyviewer.py can straight call for chromecaster.py, and send video to chromecast.
