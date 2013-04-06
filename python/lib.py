import httplib, urllib
import config

configPath = "../data/config.txt"
dataPath   = "../data/data.txt"

def postSubmit(params, headers, config):
    connection = httplib.HTTPConnection(config.host)
    connection.request("POST", config.post, params, headers)
    response = connection.getresponse()
    string = response.read()
    connection.close()
    print string

def getSubmit(params, headers, config):
    path = "http://%s%s?%s" % (config.host, config.get, params)
    response = urllib.urlopen(path)
    print response.read()
