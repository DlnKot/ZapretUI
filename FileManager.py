import os


class FileManager:
    def __init__(self, default_path="./zapret"):
        self.default_path = default_path

    def check_app(self):
        return os.path.exists(self.default_path) and len(os.listdir(self.default_path)) > 0

