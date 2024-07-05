from multiprocessing import Process
import os

class Terminal():
        def __init__(self,command) -> None:
            self.command = command
            self.p = Process(target=self.__run)
            self.p.start()
            
        def __run(self):
            print(os.system(self.command))