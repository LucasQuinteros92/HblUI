



import json


class ConfigManager():
    def __init__(self, path) -> None:
        self.configPath = path

        with open(self.configPath, 'r') as f:
                self.configData : dict = json.load(f)
        


    def get(self,key):
        return self.configData.get(key)
    
    def add(self,key,value):
        self.configData[key] = value


    def save(self):
        with open(self.configPath, 'w') as f:
                f.write(json.dumps(self.configData,indent= 4))

    def update(self,key,value):
        if self.configData.get(key) != None:
            self.configData[key] = value
            
            
