
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from os.path import dirname

#inizializzazione impostazioni
config = ConfigParser()
config.read('domoticx.ini')

curdir = dirname(__file__)
dmzurl = ConfigParser()
dmzurl.read(curdir+'/'+'domoticzUrls.ini')


# recupero elenco luci e prese
def obtainLights(callback):

    def serverResponse(req, results):
        if results['status'] == 'OK':
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'lights'), serverResponse)




# toggle light
def toggleLight(idx, instance):

    def serverResponse(req, results):
            if results['status'] == 'OK':
                print('Status changed on the switch '+str(idx))

    action = dmzurl.get('LIGHT', 'toggle').replace("$IDX", str(idx))
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + action, serverResponse)
