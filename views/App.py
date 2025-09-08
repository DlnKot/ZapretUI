import customtkinter as ctk
import json

class App(ctk.CTk):
    def __init__(self, update_method, current_version):
        super().__init__()
        self.geometry("300x400")
        self.current_version = current_version
        self.setup_ui(update_method)

    def setup_ui(self, update_method):
        default_font = ctk.CTkFont(size=24)
        Ltitle = ctk.CTkLabel(self, text="Zapret", font=default_font)
        Ltitle.grid(row=0, column=0, padx=20, pady=20)

        self.Lversion = ctk.CTkLabel(self, text=self.current_version)
        self.Lversion.grid(row=0, column=1, padx=20, pady=20)

        update_button = ctk.CTkButton(self, text="Update", command=lambda: self.on_update(update_method))
        update_button.grid(row=1, column=0, padx=20, pady=20)


    def on_update(self, update_method):
        update_method()
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                config = json.load(file)
                new_version = config.get("version", "0.0.0")
                self.Lversion.configure(text=new_version)
        except Exception:
            self.Lversion.configure(text="0.0.0")

