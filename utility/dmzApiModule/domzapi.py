
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from os.path import dirname

#inizializzazione impostazioni
config = ConfigParser()
config.read('config.ini')

curdir = dirname(__file__)
dmzurl = ConfigParser()
dmzurl.read(curdir+'/'+'domoticzUrls.ini')


# recupero elenco luci e prese
def obtainLights(callback):
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'lights'), callback)
    return req

def toggleLight(idx, instance):
    action = dmzurl.get('LIGHT', 'toggle').replace("$IDX", str(idx))
    print('Status changed on the switch '+str(idx))
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + action)
    app.populate_light_page()