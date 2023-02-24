enable_log = False

class Logger:
    __instance = None
    
    @staticmethod
    def instance():
        if Logger.__instance == None:
            Logger()
        return Logger.__instance
    
    def __init__(self):
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            global enable_log
            self.enabled = enable_log
            Logger.__instance = self
    
    def log(self, message):
        if self.enabled:
            print(message)
