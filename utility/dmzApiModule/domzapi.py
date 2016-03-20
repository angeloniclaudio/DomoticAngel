
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from os.path import dirname

#inizializzazione impostazioni
config = ConfigParser()
config.read('domoticx.ini')

curdir = dirname(__file__)
dmzurl = ConfigParser()
dmzurl.read(curdir+'/'+'domoticzUrls.ini')


#------------------------------------- LIGHTS ------------------------------------------------------------------

# recupero elenco luci e prese
def obtainLights(callback):

    def serverResponse(req, results):
        if results['status'] == 'OK':
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'lights'), serverResponse)



# recupero elenco luci e prese per stanza IDX
def obtainLightsPerRoom(roomidx,callback):

    def serverLightResponse(req, results):
        if results['status'] == 'OK':
            #print(results)
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('ROOM', 'devices').replace("$IDX", roomidx), serverLightResponse)
    #print(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('ROOM', 'devices').replace("$IDX", roomidx))

# recupero stato lampada
def obtainLightStatus(idx,callback):

    def serverLightStatusResponse(req, results):
        if 'result' in results:
            if results['status'] == 'OK':
                if results['result'][0]['SubType']=='Switch':
                    callback(results['result'][0])
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIGHT', 'getStatus').replace("$IDX", idx), serverLightStatusResponse)
    #print(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIGHT', 'getStatus').replace("$IDX", idx))


# toggle light
def toggleLight(idx, instance):

    def serverResponse(req, results):
            if results['status'] == 'OK':
                print('Status changed on the switch '+str(idx))

    action = dmzurl.get('LIGHT', 'toggle').replace("$IDX", str(idx))
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + action, serverResponse)


#------------------------------------- SCENES ------------------------------------------------------------------

# recupero elenco scene
def obtainScenes(callback):

    def serverResponse(req, results):
        if results['status'] == 'OK':
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'scenes'), serverResponse)


# activate scene
def activateScene(idx, instance):

    def serverResponse(req, results):
            if results['status'] == 'OK':
                print('Scene '+str(idx)+' activated')

    action = dmzurl.get('SCENE', 'activation').replace("$IDX", str(idx)).replace("$STATUS", 'On')
    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + action, serverResponse)



#------------------------------------- TEMPERATURES ------------------------------------------------------------------

# recupero elenco scene
def obtainTemps(callback):

    def serverResponse(req, results):
        if results['status'] == 'OK':
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'statuses').replace("$FILTER", 'temp'), serverResponse)



#------------------------------------- ROOMS ------------------------------------------------------------------
# recupero elenco scene
def obtainRooms(callback):

    def serverResponse(req, results):
        if results['status'] == 'OK':
            callback(results['result'])

    req = UrlRequest(config.get('CONNECTION', 'url') + ':' + config.get('CONNECTION', 'port') + dmzurl.get('LIST', 'rooms'), serverResponse)