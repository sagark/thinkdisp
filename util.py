import ConfigParser
from custom_res import CustomResolution

class UserConfig(object):
    """A Module to load user configs and act on them"""
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('config.ini')
        self.res = config.get("User Defaults", 'resolution')
        self.side = config.get("User Defaults", 'side')
        self.custom_res = config.items("Custom Resolutions")
        #print(res)
        #print(side)
        #print(custom_res)

    def initialize_customs(self):
        initialized = []
        for respair in self.custom_res:
            try:
                CustomResolution(respair[1])
                #initialized.append(respair[1])
            except:
                pass
            initialized.append('"' + respair[1] + '_59.90"')
        return initialized
                


if __name__ == '__main__':
    a = UserConfig()
    print(a.initialize_customs())
