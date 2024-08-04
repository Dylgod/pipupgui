from __future__ import annotations

import customtkinter
from PIL import ImageTk
from PIL import Image
import os, sys
import webbrowser
import subprocess
import re
import platform
import asyncio
from async_tkinter_loop import async_handler
from async_tkinter_loop.mixins import AsyncCTk
from typing import TYPE_CHECKING
from time import sleep

# @formatter:off

if TYPE_CHECKING:
    from asyncio.subprocess import Process

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def callback(url):
    webbrowser.open_new(url)

class UpgradeAndResetButton(customtkinter.CTkButton):
    def __init__(self, master, command=None, text="UPGRADE", **kwargs):
        super().__init__(master, **kwargs, text=text, corner_radius=10, font=("Roboto",21, "bold"), width=550, height=50, fg_color="#569cf9",border_width=1, border_color="black")


class BannedPackagesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.banned_list = []
        self.button_list = []
        self.font = ("Roboto",14, "bold")
        self.upgrade_frame = None

        self.placeholder = customtkinter.CTkFrame(self, fg_color="#252626")

        p_name_lbl = customtkinter.CTkLabel(self.placeholder, text="Banned Packages", font=self.font, anchor="w", width=200)
        p_name_lbl.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")

        self.placeholder.grid(row=0, column=0,columnspan=2, padx=(0,5), pady=(0, 10), sticky="ew")
        self.placeholder.grid_propagate(False)
        self.placeholder.configure(width=520, height=40)

    def set_class_channel(self, upgradablepackagesframe):
        self.upgrade_frame = upgradablepackagesframe

    def add_package(self, package_name, version_current, version_latest, package_type):

        def unban_package(self, name_widget, banned_p_current, banned_p_latest, banned_p_type):
            p_name = name_widget.cget('text')
            self.banned_list.remove(p_name)
            self.upgrade_frame.add_package(package_name=p_name, version_current=banned_p_current, version_latest=banned_p_latest, package_type=banned_p_type)
            borderframe.grid_forget()

        borderframe = customtkinter.CTkFrame(self, border_color='dark gray', fg_color="#252626", border_width=1)
        borderframe.grid_columnconfigure(0, weight=1)
        borderframe.grid_columnconfigure((1, 2, 3), weight=0)
        # borderframe.grid_columnconfigure(4, weight=0, minsize=70)

        banned_p_current = version_current
        banned_p_latest = version_latest
        banned_p_type = package_type

        banned_p_lbl = customtkinter.CTkLabel(borderframe, text=package_name, anchor="w", width=100)
        button = customtkinter.CTkButton(borderframe, text="Unban", fg_color="#088c08", hover_color="#5da763", width=50, height=24,
                                         command=lambda: unban_package(self, banned_p_lbl, banned_p_current, banned_p_latest, banned_p_type))

        banned_p_lbl.grid(row=0, column=0, padx=(65,0), pady=7, sticky="w")
        button.grid(row=0, column=0, padx=7, pady=7, sticky="w")

        borderframe.grid(row=len(self.banned_list)+1, column=0, pady=(0, 10), sticky="w")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        # Wont need later when we destroy the frame itself and not the widgets within
        self.banned_list.append(package_name)
        self.button_list.append(button)

        
class UpgradablePackagesFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=0)

        self.command = command
        self.chkbox_list = []
        self.font = ("Roboto",14, "bold")
        self.banned_frame = None

        self.placeholder = customtkinter.CTkFrame(self, fg_color="#252626")
        
        placeholder_name_lbl = customtkinter.CTkLabel(self.placeholder, text="Package", font=self.font, anchor="w", width=200)
        placeholder_ver_current_lbl = customtkinter.CTkLabel(self.placeholder, text="Current", font=self.font, anchor="w", width=80)
        placeholder_ver_latest_lbl = customtkinter.CTkLabel(self.placeholder, text="Latest", font=self.font, anchor="w", width=70)
        placeholder_type_lbl = customtkinter.CTkLabel(self.placeholder, text="Type", font=self.font, anchor="w", width=20)

        placeholder_name_lbl.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")
        placeholder_ver_current_lbl.grid(row=0, column=1, pady=7, padx=(27,0), sticky="w")
        placeholder_ver_latest_lbl.grid(row=0, column=2, pady=7, padx=(5,0), sticky="w")
        placeholder_type_lbl.grid(row=0, column=3, padx=(20, 10), pady=7, sticky="e")
        
        self.placeholder.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        self.placeholder.grid_propagate(False)
        self.placeholder.configure(width=525, height=40)

    def set_class_channel(self, bannedpackagesframe):
        self.banned_frame = bannedpackagesframe

    def add_package(self, package_name, version_current, version_latest, package_type):

        def ban_package(self, name_widget, v_current_widget, v_latest_widget, type_widget):
            self.chkbox_list.remove(name_widget.cget("text"))
            p_name = name_widget.cget('text')
            p_current = v_current_widget.cget('text')
            p_latest = v_latest_widget.cget('text')
            p_type = type_widget.cget('text')
            self.banned_frame.add_package(package_name=p_name, version_current=p_current, version_latest=p_latest, package_type=p_type)
            borderframe.grid_forget()

        borderframe = customtkinter.CTkFrame(self, border_color='dark gray', fg_color="#252626", border_width=1)
        borderframe.grid_columnconfigure(0, weight=1)
        borderframe.grid_columnconfigure((1, 2, 3), weight=0)
        borderframe.grid_columnconfigure(4, weight=0, minsize=70)

        upgrade_chkbox_var = customtkinter.IntVar(value=1)
        chkbox = customtkinter.CTkCheckBox(borderframe, text=package_name, width=300, variable=upgrade_chkbox_var)
        p_ver_current_lbl = customtkinter.CTkLabel(borderframe, text=version_current, anchor="e", width=80)
        p_ver_latest_lbl = customtkinter.CTkLabel(borderframe, text=version_latest, anchor="e", width=80)
        p_type_lbl = customtkinter.CTkLabel(borderframe, text=package_type, anchor="e", width=80)
        ban_button = customtkinter.CTkButton(borderframe, text="Ban", fg_color="#991b1b", hover_color="#ff4d52", width=50, height=24,
                                         command=lambda: ban_package(self, chkbox, p_ver_current_lbl, p_ver_latest_lbl, p_type_lbl))

        chkbox.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")
        p_ver_current_lbl.grid(row=0, column=1, pady=7, sticky="e")
        p_ver_latest_lbl.grid(row=0, column=2, pady=7, sticky="e")
        p_type_lbl.grid(row=0, column=3, padx=(0, 10), pady=7, sticky="e")
        ban_button.grid(row=0, column=4, padx=7, pady=7, sticky="e")

        borderframe.grid(row=len(self.chkbox_list)+1, column=0, pady=(0, 10), sticky="ew")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        # Wont need later when we destroy the frame itself and not the widgets within
        self.chkbox_list.append(chkbox.cget("text"))


def close_signout(master):
    try:
        master.quit()
    except Exception:
        master.destroy()

def set_window_default_settings(master):
    app_width = 600
    app_height = 700
    monitor_width = master.winfo_screenwidth()
    monitor_height = master.winfo_screenheight()

    app_x = (monitor_width / 2) - (app_width / 2)
    app_y = (monitor_height / 2) - (app_height / 2)

    master.geometry(f'{app_width}x{app_height}+{int(app_x)}+{int(app_y)}')
    master.resizable(False, False)


def determine_pip_list():
    unprocessed_pip_rows = []
    package_query = subprocess.Popen("pip list --outdated",
                                     stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     )

    for line in package_query.stdout.read().decode().split("\n")[2:]:
        unprocessed_pip_rows.append(line.strip("\r"))

    if len(unprocessed_pip_rows) == 0:
        print("Nothing to upgrade!")
        sys.exit(0)

    return unprocessed_pip_rows

def process_pip_result(result_row):
    cleaned_string = result_row.strip()

    # Remove all spaces from string and seperate into groups
    parts = re.findall(r'\S+', cleaned_string)

    # Ensure we have exactly 4 parts. Pip seems to be consistent with this.
    if len(parts) != 4:
        raise ValueError(f"Expected 4 parts, but got {len(parts)} in string: {result_row}")

    return parts[0], parts[1], parts[2], parts[3]

def stop():
    if upgrade_subprocess is not None:
        try:
            upgrade_subprocess.kill()
        except ProcessLookupError:
            pass
        except Exception as e:
            print(type(e))

class App(customtkinter.CTk, AsyncCTk):

    def cleanup(self):
        widgets = [self.upgrade_frame,self.banned_frame,self.header_frame,self.upgrade_button,self.reset_button,self.textbox_outer_frame]
        for w in widgets:
            try:
                w.destroy()
            except Exception:
                continue

        self.destroy()


    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", close_signout(self))
        self.reset_button = None
        self.textbox_outer_frame = None
        self.font = ("Roboto",21, "bold")
        self.title("auto_upgrade_gui")
        self.iconpath = ImageTk.PhotoImage(file=resource_path("title_icon_python.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(master=self, width=100, corner_radius=10, fg_color="#242424")
        self.logo_image = customtkinter.CTkImage(Image.open(resource_path("title_icon_python.png")),size=(36, 36))
        header_logo = customtkinter.CTkLabel(self.header_frame, text="", image=self.logo_image, anchor='w')
        header_logo.grid(row=0, rowspan=2,column=0, sticky='w', padx=(18, 0), pady=(15, 15))
        header_title = customtkinter.CTkLabel(self.header_frame, text="auto_upgrade_gui", font=("Roboto",21, "bold"), anchor='w')
        header_title.grid(row=0, column=1, sticky='w', padx=(13, 0), pady=(15, 13))

        self.logo_image = customtkinter.CTkImage(Image.open(resource_path("github_logo.png")),size=(128, 64))
        header_github = customtkinter.CTkButton(self.header_frame, text="", image=self.logo_image, anchor='nsew', hover_color="#242424", fg_color="transparent", command=lambda: callback(url="https://github.com/Dylgod/auto_upgrade_gui"))
        header_github.grid(row=0,column=4, sticky='e', padx=(140, 18), pady=(15, 13))

        self.header_frame.grid(row=0, column=1, padx=(18, 0), pady=0, sticky="nsew")

        self.upgrade_frame = UpgradablePackagesFrame(master=self, width=525, corner_radius=10)
        self.upgrade_frame.grid(row=1,rowspan=2, column=1, padx=(18,0), pady=0, sticky="nsew")
        
        self.banned_frame = BannedPackagesFrame(master=self, width=525, corner_radius=10)
        self.banned_frame.grid(row=3, column=1, padx=(18,0), pady=(10, 0), sticky="nsew")

        self.create_frame_channel(self.upgrade_frame, self.banned_frame)

        self.upgrade_button = UpgradeAndResetButton(self, text="UPGRADE", command=None)
        self.upgrade_button.configure(command=self.start_upgrade_tasks)
        self.upgrade_button.grid(row=5, column=1, padx=(18, 0), pady=(10, 10), sticky="nsew")

        # for row in pip_result:
        #     if len(row) > 30:
        #         name, version, latest, type = process_pip_result(row)
        #     else:
        #         continue
        #     self.upgrade_frame.add_package(name, version, latest, type)

        #FOR TESTING
        self.upgrade_frame.add_package('name', '12.1', '12.3', 'wheel')
        self.upgrade_frame.add_package('bruh', '12.2', '12.4', 'wheel')


    def load_upgrade_scrn(self):
        self.header_frame.grid_forget()
        self.upgrade_frame.grid_forget()
        self.banned_frame.grid_forget()
        self.upgrade_button.grid_forget()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.textbox_outer_frame = customtkinter.CTkFrame(self)
        self.textbox_outer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_outer_frame.grid_columnconfigure(0, weight=1)
        height = self.textbox_outer_frame.winfo_height()

        textbox = customtkinter.CTkTextbox(self.textbox_outer_frame, width=250, height=600,font=("Roboto", 14), activate_scrollbars=True)
        textbox.pack(expand=True, fill='both')

        self.reset_button = UpgradeAndResetButton(self, text="RESET")
        self.reset_button.configure(command=stop)
        self.reset_button.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        return textbox

    @async_handler
    async def start_upgrade_tasks(self):
        global upgrade_subprocess
        textbox = self.load_upgrade_scrn()

        # for pack in self.banned_frame.banned_list:
        #     pass

        for pack in self.upgrade_frame.chkbox_list:

            cmd = f"pip list"
            upgrade_subprocess = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            while upgrade_subprocess.returncode is None:
                stdout = asyncio.create_task(upgrade_subprocess.stdout.readline())
                stderr = asyncio.create_task(upgrade_subprocess.stderr.readline())

                done, pending = await asyncio.wait({stdout, stderr}, return_when=asyncio.FIRST_COMPLETED)

                if stdout in done:
                    result_text = stdout.result().decode(console_encoding)
                    textbox.insert("end", result_text)

                if stderr in done:
                    result_text = stderr.result().decode(console_encoding)
                    textbox.insert("end", result_text, "red_text")

                for item in pending:
                    item.cancel()

            textbox.insert("end", f"Finished with code {upgrade_subprocess.returncode}\n\n")
            ping_subprocess = None

    def create_frame_channel(self, upgradablepackagesframe, bannedpackagesframe):
        """
        Links UpgradablePackagesFrame & BannedPackagesFrame classes
        in order to send packages back and forth.
        """

        self.upgrade_frame.set_class_channel(self.banned_frame)
        self.banned_frame.set_class_channel(self.upgrade_frame)

if __name__ == "__main__":
    upgrade_subprocess: Process | None = None
    console_encoding = "utf-8"
    if platform.system() == "Windows":
        from ctypes import windll
        console_code_page = windll.kernel32.GetConsoleOutputCP()
        if console_code_page != 65001:
            console_encoding = f"cp{console_code_page}"

    customtkinter.set_appearance_mode("dark")
    # pip_result = determine_pip_list()
    app = App()
    set_window_default_settings(app)
    app.async_mainloop()
