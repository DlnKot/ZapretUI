import os


class FileManager():
    
    def __init__(self):
        isExist = self.check_app()

        if isExist:
            for file in os.listdir(self.default_path):
                print(file)



    def check_app(self, default_path="./zapret"):
        if os.path.exists(default_path):
            self.default_path = default_path
            return True
        else: 
            return False
        
