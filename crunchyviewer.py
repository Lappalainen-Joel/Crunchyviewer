#!/usr/env/python
from requests import get
from subprocess import call
from bs4 import BeautifulSoup
from sys import argv
from configparser import ConfigParser, NoOptionError

cfg = ConfigParser()
cfg.read('crunchyconfig.ini')
pr = cfg.get('crunchy-settings', 'pr')
qa = cfg.get('crunchy-settings', 'qa')
ar = cfg.get('crunchy-settings', 'ar')
url = "http://www.crunchyroll.com"

try:
    cfg.get('crunchy-settings', 'pl')
except NoOptionError:
    print("No player set, using default one (VLC).")
else:
    pl = cfg.get('crunchy-settings', 'pl')


def listseries(na):
    r = get(url + "/videos/anime")
    s = BeautifulSoup(r.content, "html.parser")
    po = s.find_all("ul", {"class": "portrait-grid cf"})
    for i in po:
        pu = i.find_all("a", {"title": na})
        if len(pu) != 0:
            u = pu[0].get("href")
            return u
        elif len(pu) > 1:
            print("Too many matches found, be more specific")
            exit(0)
        else:
            print("Not found, try again")
            exit(0)


def listepisodes(se):
    r = get(url + se)
    s = BeautifulSoup(r.content, "html.parser")
    po = s.find_all("div", {"class": "wrapper container-shadow hover-classes"})
    a = []
    for i in po:
        pu = i.find("a").get("href")
        a.append(pu)
    return a


def selectepisode(ep):
    c = len(ep)
    for i in ep:
        print(c, i)
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
        call(pr + " " + " " + url + en + " " + qa + " " + ar)
    else:
        call(pr + " " + "-p " + pl + " " + url + en + " " + qa + " " + ar)


def main():
    if len(argv) > 2:
        print("Too many arguments")
        exit(0)

    elif len(argv) == 1:
        print("Do tell the series you want to watch")
        a = input("Case sensitive, eq. Naruto Shippuden:\n")
    else:
        a = argv

    v = listseries(a)
    v2 = listepisodes(v)
    v3 = selectepisode(v2)
    playepisode(v3)


main()
