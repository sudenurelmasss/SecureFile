import os
import time
from datetime import datetime

import customtkinter as ctk
from PIL import Image

from tkinter import filedialog, messagebox

from crypto_utils import (
    encrypt_file,
    decrypt_file,
    calculate_sha256
)


# =========================================================
# GENEL AYARLAR
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# RENKLER
# =========================================================

APP_BG = "#07111C"
SIDEBAR_BG = "#061321"
CONTENT_BG = "#0A1724"
CARD_BG = "#0B1D2C"
INPUT_BG = "#071A29"

BLUE = "#168BFF"
BLUE_HOVER = "#0872D9"

GREEN = "#00C875"
GREEN_HOVER = "#00A962"

PURPLE = "#7258FF"
PURPLE_HOVER = "#5942DD"

TEXT = "#F4F8FF"
MUTED = "#9EB8CE"

BORDER = "#138ED1"

DANGER = "#FF5252"
WARNING = "#FFB020"


# =========================================================
# UYGULAMA
# =========================================================

class SecureFileApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SecureFile")
        self.geometry("1500x850")
        self.minsize(1100, 700)

        self.selected_file = None
        self.saved_hash = None
        self.last_output_path = None
        self.password_visible = False

        # Ana pencereyi ilk anda gizle
        self.withdraw()

        # Splash ekranını göster
        self.show_splash()

        # 3 saniye sonra ana uygulamayı aç
        self.after(
            3000,
            self.start_main_app
        )


    # =====================================================
    # SPLASH SCREEN
    # =====================================================

    def show_splash(self):

        self.splash = ctk.CTkToplevel(self)

        self.splash.overrideredirect(True)

        splash_width = 900
        splash_height = 520

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int(
            (screen_width - splash_width) / 2
        )

        y = int(
            (screen_height - splash_height) / 2
        )

        self.splash.geometry(
            f"{splash_width}x{splash_height}+{x}+{y}"
        )

        # -------------------------------------------------
        # ARKA PLAN GÖRSELİ
        # -------------------------------------------------

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        background_path = os.path.join(
            base_dir,
            "assets",
            "background.jpg"
        )

        if os.path.exists(background_path):

            image = Image.open(
                background_path
            )

            self.splash_bg_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(
                    splash_width,
                    splash_height
                )
            )

            bg_label = ctk.CTkLabel(
                self.splash,
                image=self.splash_bg_image,
                text=""
            )

            bg_label.place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

        else:

            self.splash.configure(
                fg_color=APP_BG
            )

        # -------------------------------------------------
        # ORTA KOYU PANEL
        # -------------------------------------------------

        center_frame = ctk.CTkFrame(
            self.splash,
            width=520,
            height=250,
            corner_radius=25,
            fg_color="#071421",
            border_width=1,
            border_color=BORDER
        )

        center_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        center_frame.pack_propagate(
            False
        )

        lock_label = ctk.CTkLabel(
            center_frame,
            text="🔐",
            font=(
                "Segoe UI Emoji",
                54
            )
        )

        lock_label.pack(
            pady=(30, 5)
        )

        title_label = ctk.CTkLabel(
            center_frame,
            text="SecureFile",
            font=(
                "Segoe UI",
                38,
                "bold"
            ),
            text_color=TEXT
        )

        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            center_frame,
            text=(
                "Dosya Şifreleme ve "
                "Bütünlük Kontrol Sistemi"
            ),
            font=(
                "Segoe UI",
                14
            ),
            text_color=MUTED
        )

        subtitle_label.pack(
            pady=(4, 15)
        )

        loading_label = ctk.CTkLabel(
            center_frame,
            text="Güvenli ortam hazırlanıyor...",
            font=(
                "Segoe UI",
                12
            ),
            text_color="#4ACBFF"
        )

        loading_label.pack()


    # =====================================================
    # ANA UYGULAMAYI BAŞLAT
    # =====================================================

    def start_main_app(self):

        if hasattr(
            self,
            "splash"
        ):

            self.splash.destroy()

        self.deiconify()

        self.configure(
            fg_color=APP_BG
        )

        self.create_sidebar()

        self.create_content()

        self.create_statusbar()


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=190,
            corner_radius=0,
            fg_color=SIDEBAR_BG,
            border_width=1,
            border_color=BORDER
        )

        self.sidebar.place(
            x=0,
            y=0,
            relheight=1
        )

        self.sidebar.pack_propagate(
            False
        )

        logo = ctk.CTkLabel(
            self.sidebar,
            text="🔐",
            font=(
                "Segoe UI Emoji",
                40
            )
        )

        logo.pack(
            pady=(35, 5)
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="SecureFile",
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            text_color=TEXT
        )

        title.pack(
            pady=(0, 35)
        )

        self.create_nav_button(
            "⌂",
            "Ana Sayfa",
            lambda: self.scroll_to(
                0.0
            ),
            True
        )

        self.create_nav_button(
            "▣",
            "Dosya İşlemleri",
            lambda: self.scroll_to(
                0.05
            )
        )

        self.create_nav_button(
            "◆",
            "Bütünlük\nKontrolü",
            lambda: self.scroll_to(
                0.45
            )
        )

        self.create_nav_button(
            "◷",
            "İşlem Geçmişi",
            lambda: self.scroll_to(
                1.0
            )
        )

        self.create_nav_button(
            "⚙",
            "Ayarlar",
            self.show_settings
        )

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True
        )

        about_button = ctk.CTkButton(
            self.sidebar,
            text="ⓘ\nHakkında",
            width=115,
            height=65,
            fg_color="transparent",
            hover_color="#0D3654",
            text_color=MUTED,
            command=self.show_about
        )

        about_button.pack(
            pady=30
        )


    def create_nav_button(
        self,
        icon,
        text,
        command,
        selected=False
    ):

        if selected:
            fg = "#104E7B"
            border = BLUE
        else:
            fg = "transparent"
            border = SIDEBAR_BG

        button = ctk.CTkButton(
            self.sidebar,
            text=f"{icon}\n{text}",
            command=command,
            width=115,
            height=75,
            corner_radius=12,
            fg_color=fg,
            hover_color="#0D4168",
            border_width=1,
            border_color=border,
            text_color=TEXT,
            font=(
                "Segoe UI",
                13
            )
        )

        button.pack(
            pady=8,
            padx=15
        )


    # =====================================================
    # NAVBAR SCROLL
    # =====================================================

    def scroll_to(self, position):

        try:

            self.content._parent_canvas.yview_moveto(
                position
            )

        except Exception:

            pass


    # =====================================================
    # AYARLAR / HAKKINDA
    # =====================================================

    def show_settings(self):

        messagebox.showinfo(
            "Ayarlar",
            (
                "SecureFile v1.0\n\n"
                "Tema: Dark Mode\n"
                "Şifreleme: Fernet\n"
                "Anahtar Türetme: PBKDF2 + SHA-256\n"
                "Bütünlük Kontrolü: SHA-256"
            )
        )


    def show_about(self):

        messagebox.showinfo(
            "SecureFile Hakkında",
            (
                "SecureFile\n\n"
                "Dosya Şifreleme ve "
                "Bütünlük Kontrol Sistemi\n\n"
                "Sürüm: 1.0"
            )
        )


    # =====================================================
    # ANA İÇERİK
    # =====================================================

    def create_content(self):

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color=CONTENT_BG,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

        self.content.place(
            relx=0.155,
            rely=0.035,
            relwidth=0.82,
            relheight=0.89
        )

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 20)
        )

        lock = ctk.CTkLabel(
            header,
            text="🔐",
            font=(
                "Segoe UI Emoji",
                48
            )
        )

        lock.pack(
            side="left",
            padx=(0, 15)
        )

        text_box = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        text_box.pack(
            side="left"
        )

        title = ctk.CTkLabel(
            text_box,
            text="SecureFile",
            font=(
                "Segoe UI",
                38,
                "bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            text_box,
            text=(
                "Dosya Şifreleme ve "
                "Bütünlük Kontrol Sistemi"
            ),
            font=(
                "Segoe UI",
                14
            ),
            text_color=MUTED
        )

        subtitle.pack(
            anchor="w"
        )

        self.create_file_card()

        self.create_hash_card()

        self.create_history_card()


    # =====================================================
    # DOSYA KARTI
    # =====================================================

    def create_file_card(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD_BG,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            padx=25,
            pady=12
        )

        title = ctk.CTkLabel(
            card,
            text="📁   Dosya İşlemleri",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(22, 3)
        )

        desc = ctk.CTkLabel(
            card,
            text=(
                "Dosya seçin, güçlü bir parola ile "
                "şifreleyin veya şifresini çözün."
            ),
            font=(
                "Segoe UI",
                12
            ),
            text_color=MUTED
        )

        desc.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        select_button = ctk.CTkButton(
            card,
            text="📂   Dosya Seç",
            command=self.select_file,
            width=250,
            height=47,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        select_button.pack(
            anchor="w",
            padx=25,
            pady=7
        )

        file_box = ctk.CTkFrame(
            card,
            fg_color=INPUT_BG,
            corner_radius=10,
            border_width=1,
            border_color="#155B83"
        )

        file_box.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.file_label = ctk.CTkLabel(
            file_box,
            text="Henüz dosya seçilmedi",
            font=(
                "Segoe UI",
                14,
                "bold"
            ),
            text_color=TEXT
        )

        self.file_label.pack(
            anchor="w",
            padx=17,
            pady=(13, 2)
        )

        self.file_info_label = ctk.CTkLabel(
            file_box,
            text="",
            font=(
                "Segoe UI",
                11
            ),
            text_color=MUTED
        )

        self.file_info_label.pack(
            anchor="w",
            padx=17,
            pady=(0, 13)
        )

        password_row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        password_row.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.password_entry = ctk.CTkEntry(
            password_row,
            placeholder_text="🔒  Parolanızı girin",
            show="*",
            height=45,
            fg_color=INPUT_BG,
            border_color="#25668D"
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.password_entry.bind(
            "<KeyRelease>",
            self.check_password_strength
        )

        self.show_password_button = ctk.CTkButton(
            password_row,
            text="◉  Göster",
            command=self.toggle_password,
            width=110,
            height=45,
            fg_color=INPUT_BG,
            border_width=1,
            border_color="#25668D",
            hover_color="#123C58"
        )

        self.show_password_button.pack(
            side="right"
        )

        self.password_strength_label = ctk.CTkLabel(
            card,
            text="Parola gücü: -",
            text_color=MUTED
        )

        self.password_strength_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 12)
        )

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        encrypt = ctk.CTkButton(
            buttons,
            text="🔒  Dosyayı Şifrele",
            command=self.encrypt,
            height=47,
            fg_color=GREEN,
            hover_color=GREEN_HOVER,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        encrypt.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 6)
        )

        decrypt = ctk.CTkButton(
            buttons,
            text="🔓  Şifreyi Çöz",
            command=self.decrypt,
            height=47,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        )

        decrypt.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        folder = ctk.CTkButton(
            buttons,
            text="📂  Son Çıktı Klasörünü Aç",
            command=self.open_output_folder,
            height=47,
            fg_color="#102B40",
            hover_color="#194762"
        )

        folder.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(6, 0)
        )


    # =====================================================
    # HASH KARTI
    # =====================================================

    def create_hash_card(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD_BG,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            padx=25,
            pady=12
        )

        title = ctk.CTkLabel(
            card,
            text="🛡   Bütünlük Kontrolü",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            text_color=TEXT
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(22, 3)
        )

        desc = ctk.CTkLabel(
            card,
            text=(
                "SHA-256 ile dosyanın değiştirilip "
                "değiştirilmediğini kontrol edin."
            ),
            text_color=MUTED
        )

        desc.pack(
            anchor="w",
            padx=25
        )

        calculate = ctk.CTkButton(
            card,
            text="#   SHA-256 Hesapla",
            command=self.calculate_hash,
            width=250,
            height=45,
            fg_color=PURPLE,
            hover_color=PURPLE_HOVER
        )

        calculate.pack(
            anchor="w",
            padx=25,
            pady=15
        )

        self.hash_label = ctk.CTkLabel(
            card,
            text="SHA-256 değeri henüz hesaplanmadı.",
            fg_color=INPUT_BG,
            corner_radius=10,
            text_color="#B4D5EC",
            font=(
                "Consolas",
                11
            ),
            wraplength=700
        )

        self.hash_label.pack(
            fill="x",
            padx=25,
            pady=7,
            ipady=15
        )

        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=(10, 25)
        )

        save = ctk.CTkButton(
            row,
            text="▣  Hash Değerini Kaydet",
            command=self.save_hash,
            fg_color="#102B40",
            hover_color="#194762"
        )

        save.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 6)
        )

        verify = ctk.CTkButton(
            row,
            text="✓  Dosya Bütünlüğünü Kontrol Et",
            command=self.verify_hash,
            fg_color="#102B40",
            hover_color="#194762"
        )

        verify.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(6, 0)
        )


    # =====================================================
    # GEÇMİŞ KARTI
    # =====================================================

    def create_history_card(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD_BG,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            padx=25,
            pady=(12, 30)
        )

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 8)
        )

        title = ctk.CTkLabel(
            header,
            text="◷   İşlem Geçmişi",
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            text_color=TEXT
        )

        title.pack(
            side="left"
        )

        clear = ctk.CTkButton(
            header,
            text="Geçmişi Temizle",
            command=self.clear_history,
            width=140,
            fg_color="#102B40"
        )

        clear.pack(
            side="right",
            padx=(8, 0)
        )

        save = ctk.CTkButton(
            header,
            text="TXT Olarak Kaydet",
            command=self.save_history_to_txt,
            width=150,
            fg_color=BLUE
        )

        save.pack(
            side="right"
        )

        self.history_box = ctk.CTkTextbox(
            card,
            height=160,
            fg_color="#03101B",
            border_width=1,
            border_color="#155B83",
            text_color="#AFD0E7",
            font=(
                "Consolas",
                11
            )
        )

        self.history_box.pack(
            fill="x",
            padx=25,
            pady=(5, 25)
        )

        self.history_box.insert(
            "end",
            "SecureFile işlem geçmişi\n"
            "===============================================\n"
        )

        self.history_box.configure(
            state="disabled"
        )


    # =====================================================
    # STATUS BAR
    # =====================================================

    def create_statusbar(self):

        bar = ctk.CTkFrame(
            self,
            height=45,
            corner_radius=0,
            fg_color="#03101B",
            border_width=1,
            border_color=BORDER
        )

        bar.place(
            relx=0,
            rely=1,
            relwidth=1,
            anchor="sw"
        )

        dot = ctk.CTkLabel(
            bar,
            text="●",
            text_color=GREEN
        )

        dot.pack(
            side="left",
            padx=(20, 6)
        )

        self.status_label = ctk.CTkLabel(
            bar,
            text="Hazır",
            text_color=TEXT
        )

        self.status_label.pack(
            side="left"
        )

        version = ctk.CTkLabel(
            bar,
            text="SecureFile v1.0",
            text_color=MUTED
        )

        version.pack(
            side="left",
            padx=25
        )

        secure = ctk.CTkLabel(
            bar,
            text="🛡  Verileriniz Güvende",
            text_color="#21D9FF",
            font=(
                "Segoe UI",
                12,
                "bold"
            )
        )

        secure.pack(
            side="right",
            padx=25
        )


    # =====================================================
    # PAROLA
    # =====================================================

    def toggle_password(self):

        self.password_visible = (
            not self.password_visible
        )

        if self.password_visible:

            self.password_entry.configure(
                show=""
            )

            self.show_password_button.configure(
                text="◉  Gizle"
            )

        else:

            self.password_entry.configure(
                show="*"
            )

            self.show_password_button.configure(
                text="◉  Göster"
            )


    def check_password_strength(
        self,
        event=None
    ):

        password = self.password_entry.get()

        score = 0

        if len(password) >= 8:
            score += 1

        if any(
            c.isupper()
            for c in password
        ):
            score += 1

        if any(
            c.islower()
            for c in password
        ):
            score += 1

        if any(
            c.isdigit()
            for c in password
        ):
            score += 1

        if any(
            not c.isalnum()
            for c in password
        ):
            score += 1

        if password == "":

            strength = "-"
            color = MUTED

        elif score <= 2:

            strength = "Zayıf"
            color = DANGER

        elif score <= 4:

            strength = "Orta"
            color = WARNING

        else:

            strength = "Güçlü"
            color = GREEN

        self.password_strength_label.configure(
            text=f"Parola gücü: {strength}",
            text_color=color
        )


    # =====================================================
    # DOSYA SEÇ
    # =====================================================

    def select_file(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        self.selected_file = path
        self.saved_hash = None

        name = os.path.basename(
            path
        )

        size = os.path.getsize(
            path
        )

        if size < 1024:

            size_text = (
                f"{size} byte"
            )

        elif size < (
            1024 * 1024
        ):

            size_text = (
                f"{size / 1024:.2f} KB"
            )

        else:

            size_text = (
                f"{size / (1024 * 1024):.2f} MB"
            )

        extension = os.path.splitext(
            name
        )[1]

        if extension:

            extension = (
                extension
                .replace(
                    ".",
                    ""
                )
                .upper()
            )

        else:

            extension = "Uzantısız"

        self.file_label.configure(
            text=name
        )

        self.file_info_label.configure(
            text=(
                f"{extension} Dosyası"
                f"   •   {size_text}"
            )
        )

        self.hash_label.configure(
            text="SHA-256 değeri henüz hesaplanmadı."
        )

        self.status_label.configure(
            text="Dosya seçildi"
        )

        self.add_history(
            "Dosya seçildi",
            name
        )


    # =====================================================
    # ŞİFRELE
    # =====================================================

    def encrypt(self):

        if not self.selected_file:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir dosya seçin."
            )

            return

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen parola girin."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Zayıf Parola",
                "Parola en az 6 karakter olmalıdır."
            )

            return

        try:

            start = time.perf_counter()

            output = encrypt_file(
                self.selected_file,
                password
            )

            duration = (
                time.perf_counter()
                - start
            )

            self.last_output_path = (
                output
            )

            name = os.path.basename(
                self.selected_file
            )

            self.add_history(
                "Şifrelendi",
                name,
                duration
            )

            self.status_label.configure(
                text="Dosya başarıyla şifrelendi"
            )

            messagebox.showinfo(
                "Başarılı",
                (
                    "Dosya başarıyla şifrelendi.\n\n"
                    f"{output}\n\n"
                    f"İşlem süresi: "
                    f"{duration:.3f} saniye"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Hata",
                str(error)
            )


    # =====================================================
    # ŞİFRE ÇÖZ
    # =====================================================

    def decrypt(self):

        if not self.selected_file:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir dosya seçin."
            )

            return

        password = self.password_entry.get()

        if not password:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen parola girin."
            )

            return

        try:

            start = time.perf_counter()

            output = decrypt_file(
                self.selected_file,
                password
            )

            duration = (
                time.perf_counter()
                - start
            )

            self.last_output_path = (
                output
            )

            name = os.path.basename(
                self.selected_file
            )

            self.add_history(
                "Şifresi çözüldü",
                name,
                duration
            )

            self.status_label.configure(
                text="Dosyanın şifresi çözüldü"
            )

            messagebox.showinfo(
                "Başarılı",
                (
                    "Dosyanın şifresi başarıyla çözüldü.\n\n"
                    f"{output}\n\n"
                    f"İşlem süresi: "
                    f"{duration:.3f} saniye"
                )
            )

        except Exception as error:

            self.status_label.configure(
                text="Şifre çözme başarısız"
            )

            messagebox.showerror(
                "Hata",
                str(error)
            )


    # =====================================================
    # HASH
    # =====================================================

    def calculate_hash(self):

        if not self.selected_file:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir dosya seçin."
            )

            return

        value = calculate_sha256(
            self.selected_file
        )

        self.hash_label.configure(
            text=(
                "SHA-256:\n\n"
                f"{value}"
            )
        )

        self.add_history(
            "SHA-256 hesaplandı",
            os.path.basename(
                self.selected_file
            )
        )

        self.status_label.configure(
            text="SHA-256 hesaplandı"
        )


    def save_hash(self):

        if not self.selected_file:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir dosya seçin."
            )

            return

        self.saved_hash = calculate_sha256(
            self.selected_file
        )

        self.hash_label.configure(
            text=(
                "Kaydedilen SHA-256:\n\n"
                f"{self.saved_hash}"
            )
        )

        self.add_history(
            "Hash kaydedildi",
            os.path.basename(
                self.selected_file
            )
        )

        messagebox.showinfo(
            "Hash Kaydedildi",
            "SHA-256 değeri referans olarak kaydedildi."
        )


    def verify_hash(self):

        if not self.selected_file:

            messagebox.showwarning(
                "Uyarı",
                "Lütfen önce bir dosya seçin."
            )

            return

        if not self.saved_hash:

            messagebox.showwarning(
                "Uyarı",
                "Önce hash değerini kaydedin."
            )

            return

        current = calculate_sha256(
            self.selected_file
        )

        name = os.path.basename(
            self.selected_file
        )

        if current == self.saved_hash:

            self.add_history(
                "Bütünlük doğrulandı",
                name
            )

            self.status_label.configure(
                text="Dosya bütünlüğü doğrulandı"
            )

            messagebox.showinfo(
                "Dosya Güvenli",
                "Dosyada değişiklik tespit edilmedi."
            )

        else:

            self.add_history(
                "DEĞİŞİKLİK TESPİT EDİLDİ",
                name
            )

            self.status_label.configure(
                text="Dosya değişikliği tespit edildi"
            )

            messagebox.showwarning(
                "Dosya Değiştirilmiş",
                "Dosyanın içeriğinde değişiklik tespit edildi."
            )


    # =====================================================
    # GEÇMİŞ
    # =====================================================

    def add_history(
        self,
        operation,
        file_name,
        duration=None
    ):

        now = datetime.now().strftime(
            "%d.%m.%Y %H:%M:%S"
        )

        text = (
            f"[{now}]   "
            f"{operation}   -   "
            f"{file_name}"
        )

        if duration is not None:

            text += (
                f"   -   "
                f"{duration:.3f} saniye"
            )

        text += "\n"

        self.history_box.configure(
            state="normal"
        )

        self.history_box.insert(
            "end",
            text
        )

        self.history_box.see(
            "end"
        )

        self.history_box.configure(
            state="disabled"
        )


    def clear_history(self):

        self.history_box.configure(
            state="normal"
        )

        self.history_box.delete(
            "1.0",
            "end"
        )

        self.history_box.insert(
            "end",
            "SecureFile işlem geçmişi\n"
            "===============================================\n"
        )

        self.history_box.configure(
            state="disabled"
        )

        self.status_label.configure(
            text="Geçmiş temizlendi"
        )


    def save_history_to_txt(self):

        text = self.history_box.get(
            "1.0",
            "end"
        )

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                (
                    "Metin Dosyası",
                    "*.txt"
                )
            ]
        )

        if not path:
            return

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                text
            )

        messagebox.showinfo(
            "Başarılı",
            "İşlem geçmişi TXT olarak kaydedildi."
        )


    # =====================================================
    # ÇIKTI KLASÖRÜ
    # =====================================================

    def open_output_folder(self):

        if not self.last_output_path:

            messagebox.showwarning(
                "Uyarı",
                "Henüz oluşturulmuş bir çıktı yok."
            )

            return

        folder = os.path.dirname(
            self.last_output_path
        )

        os.startfile(
            folder
        )


# =========================================================
# PROGRAMI BAŞLAT
# =========================================================

if __name__ == "__main__":

    app = SecureFileApp()

    app.mainloop()