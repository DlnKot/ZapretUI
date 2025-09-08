import os
from zipfile import ZipFile

class FileManager:
    def __init__(self, default_path="./zapret"):
        self.default_path = default_path

    def check_app(self):
        return os.path.exists(self.default_path) and len(os.listdir(self.default_path)) > 0

    def unzip_app(self, path):
        with ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(self.default_path)
        if path.endswith('.zip'):
            os.remove(path)

    def get_zapret_path(self):
        # Находит первую папку внутри 
        if not os.path.exists(self.default_path):
            return None
        for entry in os.listdir(self.default_path):
            full_path = os.path.join(self.default_path, entry)
            if os.path.isdir(full_path):
                return full_path
        return self.default_path