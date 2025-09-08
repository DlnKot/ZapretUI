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
    update_checker.fetch_latest_version()
    is_update_available = update_checker.is_update_available()

    # Если нет скачанного репозитория или конфиг невалиден — обновляем
    if current_version == "0.0.0" or not is_app_exist:
        update(update_checker)
        current_version = update_checker.check_current_version()
        update_checker.fetch_latest_version()
        is_update_available = update_checker.is_update_available()

    app = App(
        update_method=lambda: update(update_checker),
        current_version=current_version,
        is_update_available=is_update_available,
        zapret_path=file_manager.get_zapret_path()
    )
    app.mainloop()

if __name__ == "__main__":
    start()