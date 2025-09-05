import os
import requests
import json

class UpdateChecker():

    def __init__(self, GITHUB_REPO): 
        self.GITHUB_REPO = GITHUB_REPO
        self.current_version = None
        self.latest_version = None
        self.url = f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest"


    def check_current_version(self):
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
                self.current_version = config.get("version", "0.0.0")
        except Exception as e:
            print(f"Error reading config.json: {e}")
            self.current_version = "0.0.0"
        return self.current_version

    def fetch_latest_version(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.latest_version = response.json().get("tag_name", "0.0.0")
            else:
                print(f"Error fetching latest version: {response.status_code}")
                self.latest_version = "0.0.0"
        except Exception as e:
            print(f"Error fetching latest version: {e}")
            self.latest_version = "0.0.0"
        return self.latest_version
    
    # TODO: Доделать метод обновления конфига
    # def update_current_version_in_config():
    #     try:
    #         with open("config.json", "r") as file:
    #             config = json.load(file)
    #             self.current_version = config.get("version", "0.0.0")
    #     except Exception as e:
    #         print(f"Error reading config.json: {e}")
    #         self.current_version = "0.0.0"
    #     return self.current_version

    def is_update_available(self):
        if self.current_version is None or self.latest_version is None:
            print("Versions not checked yet.")
            return False
        if self.current_version < self.latest_version:
            print("A new version is available")
            return True
        else:
            print("You have the latest version.")
            return False
    
    def download_latest_release(self, download_dir="./zapret"):

        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            # Берём ссылку на архив (zipball или tarball)
            download_url = data.get("zipball_url")
            if not download_url:
                print("Не найден zipball_url в релизе")
                return None

            os.makedirs(download_dir, exist_ok=True)
            file_path = os.path.join(download_dir, f"{self.latest_version}.zip")

            # Скачиваем файл
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print(f"Скачано: {file_path}")

            return file_path

        except Exception as e:
            print(f"Ошибка скачивания: {e}")
            return None
