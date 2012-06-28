import subprocess
import time

class CustomResolution(object):
    def __init__(self, resstring, debug=False):
        self.wid = resstring.split("x")[0]
        #self.wid = 1280
        self.hei = resstring.split("x")[1]
        #self.hei = 1024
        if debug:
            return
        a = subprocess.check_output(["gtf", str(self.wid), str(self.hei), "59.9"])
        a = a.split("Modeline ")[1]
        a = a.replace("\n", "")
        print(a)
        a = a.replace("  ", " ")
        a = a.split(" ")
        cmdstr = ["xrandr", "--newmode"]
        for piece in a:
            cmdstr.append(piece)
        b = subprocess.check_output(cmdstr)
        print(b)
        print("reached here")
        subprocess.check_output(["xrandr", "--addmode", "VIRTUAL", a[0]])
        #print(a)


    def removemode(self):
        rmstring = "'" + '"' + str(self.wid) + "x" + str(self.hei) + '_59.90"' + "'"
        subprocess.check_output(["xrandr", "--rmmode", rmstring])

    def removedispmode(self):
        rmstring = "--delmode OUTPUT resname"

if __name__ == '__main__':
    a = CustomResolution("asdf", True)
    #time.sleep(10)
    a.removemode()
