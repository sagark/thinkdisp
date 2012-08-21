import ConfigParser
from custom_res import CustomResolution

class UserConfig(object):
    """A Module to load user configs and act on them"""
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('/etc/thinkdisp/config.ini')
        self.res = self.config.get("User Defaults", 'resolution')
        self.side = self.config.get("User Defaults", 'side')
        self.rotation = self.config.get("User Defaults", 'rotation')
        self.custom_res = self.config.items("Custom Resolutions")
        try: #take care of upgrade case where perm_fixed doesn't exist
            self.perm_fixed = self.config.get("First Run", 'perm_fixed')
        except:
            self.perm_fixed = "False"
        #print(res)
        #print(side)
        #print(custom_res)
        #print(self.rotation)

    def get_settings(self):
        return [self.res, self.side, self.rotation]

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
                
    def write_settings(self, settingsdict):
        #take in thinkdisp's settings dict and write it all to file
        self.config.set('User Defaults', 'resolution', settingsdict["RESOLUTION"])
        self.config.set('User Defaults', 'side', settingsdict["SIDE"])
        self.config.set('User Defaults', 'rotation', settingsdict["ROTATION"])
        setfile = file('/etc/thinkdisp/config.ini', 'w')
        self.config.write(setfile)
   
    def done_first_run(self):
        try: # try to add section, catch the exception if it already exists
            self.config.add_section("First Run")
        except:
            pass
        self.config.set("First Run", "perm_fixed", "True")
        setfile = file('/etc/thinkdisp/config.ini', 'w')
        self.config.write(setfile)

if __name__ == '__main__':
    a = UserConfig()
    print(a.initialize_customs())
