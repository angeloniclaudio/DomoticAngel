
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from os.path import dirname

#inizializzazione impostazioni
config = ConfigParser()
config.read('config.ini')

curdir = dirname(__file__)
dmzurl = ConfigParser()
dmzurl.read(curdir+'domoticzUrls.ini')


# recupero elenco luci e prese
def loadLights():
    def response(req, results):
        if results['status'] == 'OK':
            #print(results['result'][2]['idx'])
            return results['result']
        else:
            return []

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'lights'), response)
