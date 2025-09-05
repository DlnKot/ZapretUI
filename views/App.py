import customtkinter as ctk


class App(ctk.CTk):

    def __init__(self, update_method):
        super().__init__()
        self.geometry("300x400")
        self.setup_ui(update_method)

    def setup_ui(self, update_method):
        default_font = ctk.CTkFont(size=24)
        title = ctk.CTkLabel(self, text="Zapret", font=default_font)
        title.grid(row=0, column=0, padx=20, pady=20)

        update_button = ctk.CTkButton(self, text="Update", command=update_method)
        update_button.grid(row=1, column=0, padx=20, pady=20)


