from UpdateChecker import UpdateChecker
from views.App import App


def update():
    update_checker = UpdateChecker("Flowseal/zapret-discord-youtube")
    update_checker.check_current_version()
    update_checker.fetch_latest_version()

    if update_checker.is_update_available():
        update_checker.download_latest_release()
        print("Update done!")
    else:
        print("It is latest version")

if __name__ == "__main__":
    app = App(update)
    app.mainloop()