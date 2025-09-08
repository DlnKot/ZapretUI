from FileManager import FileManager
from UpdateChecker import UpdateChecker
from views.App import App

GITHUB_REPO = "Flowseal/zapret-discord-youtube"

def update(update_checker):
    update_checker.fetch_latest_version()
    update_checker.download_latest_release()
    update_checker.update_current_version_in_config(update_checker.latest_version)
    print("Update done!")

def start():
    update_checker = UpdateChecker(GITHUB_REPO)
    file_manager = FileManager()
    current_version = update_checker.check_current_version()
    is_app_exist = file_manager.check_app()

    # Если нет скачанного репозитория или конфиг невалиден — обновляем
    if current_version == "0.0.0" or not is_app_exist:
        update(update_checker)
        current_version = update_checker.check_current_version()

# TODO: Сделать вывод модального окна обновления
    # if update_checker.is_update_available():


    app = App(lambda: update(update_checker), current_version)
    app.mainloop()

if __name__ == "__main__":
    start()