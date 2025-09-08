import customtkinter as ctk
import json
import os
import subprocess
import threading

class App(ctk.CTk):
    def __init__(self, update_method, current_version, is_update_available=False, zapret_path=None):
        super().__init__()
        self.geometry("600x800")
        self.title("Zapret")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.current_version = current_version
        self.update_method = update_method
        self.is_update_available = is_update_available
        self.zapret_path = zapret_path
        self.setup_ui()
        if self.is_update_available:
            self.show_update_modal()

    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#232a36")
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Title
        title_font = ctk.CTkFont(size=32, weight="bold")
        Ltitle = ctk.CTkLabel(self.main_frame, text="Zapret", font=title_font, text_color="#b8c7e0")
        Ltitle.pack(pady=(20, 10))

        # Version
        version_font = ctk.CTkFont(size=18, weight="bold")
        self.Lversion = ctk.CTkLabel(self.main_frame, text=f"Версия: {self.current_version}", font=version_font, text_color="#7fa1e3")
        self.Lversion.pack(pady=(0, 20))

        # Update button
        update_btn = ctk.CTkButton(
            self.main_frame, text="Обновить", command=self.on_update,
            fg_color="#3a4a63", hover_color="#5b7bd5", corner_radius=12, font=ctk.CTkFont(size=16)
        )
        update_btn.pack(pady=(0, 10))

        # Open folder button
        open_btn = ctk.CTkButton(
            self.main_frame, text="Открыть папку zapret", command=self.open_zapret_folder,
            fg_color="#2d3542", hover_color="#5b7bd5", corner_radius=12, font=ctk.CTkFont(size=15)
        )
        open_btn.pack(pady=(0, 20))

        # Files list
        files_frame = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color="#2d3542")
        files_frame.pack(fill="both", expand=True, padx=10, pady=10)
        files_title = ctk.CTkLabel(files_frame, text="Файлы в ./zapret", font=ctk.CTkFont(size=18, weight="bold"), text_color="#b8c7e0")
        files_title.pack(pady=(10, 5))

        self.files_list_frame = ctk.CTkFrame(files_frame, fg_color="transparent")
        self.files_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.populate_files_list()

    def populate_files_list(self):
        # Очистить старые виджеты
        for widget in self.files_list_frame.winfo_children():
            widget.destroy()
        zapret_path = self.zapret_path
        if not zapret_path or not os.path.exists(zapret_path):
            empty_label = ctk.CTkLabel(self.files_list_frame, text="Папка не найдена", text_color="#7fa1e3")
            empty_label.pack()
            return

        files = [f for f in os.listdir(zapret_path) if f.lower().endswith(".bat")]
        if not files:
            empty_label = ctk.CTkLabel(self.files_list_frame, text="Нет .bat файлов", text_color="#7fa1e3")
            empty_label.pack()
            return

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.files_list_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)

        def shorten_filename(fname, max_len=36):
            if len(fname) <= max_len:
                return fname
            part_len = (max_len - 3) // 2
            return fname[:part_len] + "..." + fname[-part_len:]

        for fname in files:
            file_row = ctk.CTkFrame(scroll_frame, fg_color="#232a36", corner_radius=8)
            file_row.pack(fill="x", pady=4, padx=4)
            display_name = shorten_filename(fname)
            file_label = ctk.CTkLabel(file_row, text=display_name, font=ctk.CTkFont(size=15), text_color="#b8c7e0")
            file_label.pack(side="left", padx=10, pady=6)
            full_path = os.path.abspath(os.path.join(zapret_path, fname))
            run_btn = ctk.CTkButton(
                file_row, text="Запустить", fg_color="#3a4a63", hover_color="#5b7bd5",
                corner_radius=10, font=ctk.CTkFont(size=14),
                command=lambda f=full_path: self.run_bat_file(f)
            )
            run_btn.pack(side="right", padx=10)

    def run_bat_file(self, path):
        def run():
            command = f'Start-Process "{path}" -Verb RunAs'
            subprocess.Popen(['powershell', '-Command', command], shell=True)
        threading.Thread(target=run, daemon=True).start()

    def on_update(self):
        self.update_method()
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                config = json.load(file)
                new_version = config.get("version", "0.0.0")
                self.Lversion.configure(text=f"Версия: {new_version}")
        except Exception:
            self.Lversion.configure(text="Версия: 0.0.0")
        self.populate_files_list()

    def show_update_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Доступно обновление")
        modal.geometry("350x200")
        modal.transient(self)
        modal.grab_set()
        modal.configure(fg_color="#232a36")
        modal.resizable(False, False)

        label = ctk.CTkLabel(modal, text="Доступна новая версия приложения!", font=ctk.CTkFont(size=18, weight="bold"), text_color="#b8c7e0")
        label.pack(pady=(30, 10))

        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=20)

        def do_update():
            modal.destroy()
            self.on_update()

        update_btn = ctk.CTkButton(btn_frame, text="Обновить", command=do_update, fg_color="#3a4a63", hover_color="#5b7bd5", corner_radius=10)
        update_btn.pack(side="left", padx=10)

        later_btn = ctk.CTkButton(btn_frame, text="Позже", command=modal.destroy, fg_color="#232a36", hover_color="#5b7bd5", corner_radius=10)
        later_btn.pack(side="left", padx=10)

        close_btn = ctk.CTkButton(btn_frame, text="Закрыть", command=self.destroy, fg_color="#232a36", hover_color="#5b7bd5", corner_radius=10)
        close_btn.pack(side="left", padx=10)

    def open_zapret_folder(self):
        if self.zapret_path and os.path.exists(self.zapret_path):
            os.startfile(self.zapret_path)

