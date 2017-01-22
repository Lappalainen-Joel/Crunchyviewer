from requests import get
from subprocess import call
from bs4 import BeautifulSoup
from sys import argv
from configparser import ConfigParser, NoOptionError, NoSectionError
from livestreamer import PluginError, streams
from json import loads

cfg = ConfigParser()
url = "http://www.crunchyroll.com"

try:
    cfg.read('crunchyconfig.ini')
except NoSectionError:
    print("Configuration file missing. Exiting")
    exit(1)

try:
    qa = cfg.get('crunchy-settings', 'qa')
except NoOptionError:
    print("Cannot read required parameters from configuration file. Exiting")
    exit(1)

try:
    qu = cfg.get('crunchy-settings', 'qu')
except NoOptionError:
    qu = "0"


def debug(err):
    if qu != "0":
        print(err)

try:
    cfg.get('crunchy-settings', 'pl')
except NoOptionError:
    debug("No player set, using default one (VLC).")
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
            debug("Too many matches found, be more specific")
            exit(1)
        else:
            debug("Not found, try again")
            exit(1)


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
        call(pl + " " + en)


def getStreams(url, qa):
    print(url)
    try:
        streams(url)
    except PluginError as e:
        val = str(e)
    else:
        ste = streams(url)
        return ste[qa]
    try:
        val
    except NameError:
        debug("This should not ever trigger.")
    else:
        debug("Catched PluginError. Let's try to get the url for " + qa + " -Quality")
        val = cleanJSON(val)
        val = parseJSON(val)
        return val


def cleanJSON(v):
    v = v[56:]
    v = v[:-137]
    v = v.replace("'", '"')
    v = v.replace('None', '"None"')
    v = "{" + v + "}"
    return v


def parseJSON(u):
    qua_list = [" ", "low", "mid", "high", "ultra"]
    d = loads(u)
    for i in d['stream_data']['streams']:
        if i['quality'] == qa:
            return i['url']
    print("Quality not found with '" + qa + "' -quality. Trying to find other qualities, and using highest quality among them.")
    qua = 0
    for i in d['stream_data']['streams']:
        if i['quality'] == 'ultra':
            qua = 4
        elif i['quality'] == 'high' and qua < 3:
            qua = 3
        elif i['quality'] == 'mid' and qua < 2:
            qua = 2
        elif i['quality'] == 'low' and qua < 1:
            qua = 1
    if qua == 0:
        print("No qualities detected. Exiting")
        exit(1)
    for i in d['stream_data']['streams']:
        if i['quality'] == qua_list[qua]:
            print(i['quality'])
            return i['url']


def main():
    if len(argv) > 2:
        debug("Too many arguments")
        exit(0)

    elif len(argv) == 1:
        print("Do tell the series you want to watch")
        a = input("Case sensitive, eq. Naruto Shippuden:\n")
    else:
        a = argv

    v = listseries(a)
    v2 = listepisodes(v)
    v3 = selectepisode(v2)
    v4 = getStreams(url + v3, qa)
    playepisode(v4)


main()

