#!/usr/env/python
import requests
import subprocess
from bs4 import BeautifulSoup
url = "http://www.crunchyroll.com"

# Defines program to be executed via subprocess, with windows use full path.
# eq. of windows version
pr = "C:\Program Files (x86)\Livestreamer\livestreamer.exe"
# eq. of linux version
# pr = "livestreamer"

# Defines player. Use only with linux. On Windows, define default player to livestreamer config file.
#pl = "-p mplayer"

# Defines quality, in crunchyroll choices are low, mid and ultra
qa = "ultra"

# Defines hls to be passed through to player, this enables forwarding and rewinding the stream within mediaplayer.
ar = "--player-passthrough hls"

def listseries(na):
    r = requests.get(url+"/videos/anime")
    s = BeautifulSoup(r.content, "html.parser")
    po = s.find_all("ul", {"class": "portrait-grid cf"})
    for i in po:
        pu = i.find_all("a",{"title":na})
        if (len(pu) != 0):
            u = pu[0].get("href")
            return u
        elif (len(pu) > 1 ):
            print("Too many matches found, be more specific")
            exit(0)
        else:
            print("Not found, try again")
            exit(0)

def listepisodes(se):
    r = requests.get(url+se)
    s = BeautifulSoup(r.content,"html.parser")
    po = s.find_all("div",{"class": "wrapper container-shadow hover-classes"})
    a = []
    for i in po:
        pu = i.find("a").get("href")
        a.append(pu)
    return a

def selectepisode(ep):
    c = len(ep)
    for i in ep:
        print(c,i)
        c -= 1
    # Not sure why expects the value to be string.
    k = False
    while not k:
        dstr = input("Which episode would you like to watch?\n")
        try:
            d = int(dstr)
            k = True
        except ValueError:
            print("Enter numeric value\n")
    c2 = len(ep) - d
    return ep[c2]

def playepisode(en):
    try:
        pl
    except:
        # This horrible creation was done because subprocess didn't understand 'ar' paramater as a separate parameter.
        # subprocess.call(pr,url+en,qa,ar)
        subprocess.call(pr + " " + " " + url + en + " " + qa + " " + ar)
    else:
        subprocess.call(pr + " " + pl + " " + url + en + " " + qa + " " + ar)

def main():
    print("Do tell the series you want to watch")
    a = input("Case sensitive, eq. Naruto Shippuden:\n")
    v = listseries(a)
    v2 = listepisodes(v)
    v3 = selectepisode(v2)
    playepisode(v3)

main()
