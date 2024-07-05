







import os
import subprocess
from utils.Terminal import Terminal


def isHBLrunning():
        #self.timer.stop()
        ret = False
        result = subprocess.run(['ps', '-fA'], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        output = output.split("\n")
        
        #self.changeStatus("Detenido")
        for line in output:  
            #if "python3"in line:
            #    print(line)
                
            if "python3"in line and "main.py" in line:
                print(line.split())
                ret = True

        return ret

def getHBLpid():
        #self.timer.stop()
        ret = []
        result = subprocess.run(['ps', '-fA'], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        output = output.split("\n")
        
        #self.changeStatus("Detenido")
        for line in output:  
            #if "python3"in line:
            #    print(line)
                
            if "python3"in line and "main.py" in line:
                ret.append(line.split()[1])
                

        return ret