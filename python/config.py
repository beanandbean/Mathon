import os
import lib

class Config(object):
    def __init__(self):
        self.config = dict()
        if os.path.exists(lib.configPath):
            self.read()
        else:
            self.inputConfig()
 
    def read(self):
        f = open(lib.configPath)
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            name, value = line.split(":", 2)
            self.config[name] = value
        self.__dict__.update(self.config)

    def write(self):
        f = open(lib.configPath, "w")
        for name, value in self.config.iteritems():
            line = "%s:%s" % (name, value)
            print >>f, line
        f.close()

    def inputConfig(self):
        self.config["host"] = raw_input("Host? ")
        self.config["get"]  = raw_input("GET method handler? ")
        self.config["post"] = raw_input("POST method handler? ")
        self.config["user"] = raw_input("Username? ")
        self.__dict__.update(self.config)
        self.write()
