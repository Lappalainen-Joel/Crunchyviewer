import pychromecast
from configparser import ConfigParser, NoOptionError
cfg = ConfigParser()

if (cfg.read('chromecast.ini') == []):
	print("Configuration file 'chromecast.ini' missing. Exiting")
	exit(1)
try:
	dbug = cfg.get('chromecast-settings', 'dbug')
except NoOptionError:
	dbug = 0


def debug(num):
	err_list = {
	"01": "chromecast_name missing. Resuming",
	"02": "chromecast_IP missing. Resuming",
	"11": "Chromecast not found. Check that you can connect to your chromecast",
	"21": "Set just either 'chromecast_name' or 'chromecast_ip', now both are defined.",
	"22": "'chromecast_name' and 'chromecast_ip' are not defined. Define either one. "
	}
	if dbug == 1:
		print(err_list[num])


try:
	cfg.get('chromecast-settings', 'chromecast_name')
except NoOptionError:
	debug("01")
	name = 0
else:
	cast = cfg.get('chromecast-settings', 'chromecast_name')
	name = 1

try:
	cfg.get('chromecast-settings', 'chromecast_IP')
except NoOptionError:
	debug("02")
	ip = 0
else:
	cast = cfg.get('chromecast-settings', 'chromecast_IP')
	ip = 1


def castviaName(url, medtype):
	# Wondering why this function call had to be defined like this.
	namArg = "friendly_name="+cast
	caster = pychromecast.get_chromecast(namArg)
	if caster != None and caster != []:
		stream(caster, url)
	else:
		debug("11")
		exit(1)


def castviaIP(url, medtype):
	caster = pychromecast.get_chromecast(cast)
	if caster != None and caster != []:
		stream(caster, url)
	else:
		debug("11")


def stream(caster, url, medtype):
	caster.wait()
	cmc = caster.media_controller
	# Default for videos medtype = "video/mp4"
	cmc.play_media(url, medtype)


def main():
    

	if ip == 1 and name == 1:
		debug("21")
		exit(1)

	elif ip == 1:
		castviaIP(url, medtype)

	elif name == 1:
		castviaName(url, medtype)
	else:
		debug("22")
		exit(1)


main()
