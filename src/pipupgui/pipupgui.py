from __future__ import annotations

from json import loads, dumps, JSONDecodeError
import customtkinter
from PIL import ImageTk
from PIL import Image
from webbrowser import open_new
import os
import sys
import subprocess
import re
import platform
import asyncio
from async_tkinter_loop import async_handler
from async_tkinter_loop.mixins import AsyncCTk
from typing import TYPE_CHECKING
from asyncio.subprocess import Process

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def callback(url):
    open_new(url)


def on_startup_ban_list(file_path):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")
            return []
    except PermissionError:
        print("Permission Error when writing to banned list")
        return []

    try:
        with open(file_path, "r") as file:
            b_list = loads(file.read())
        return b_list if isinstance(b_list, list) else []
    except JSONDecodeError:
        return []


def ban_packs(file_path, pack_list):
    try:
        if not os.path.exists(file_path):
            with open(file_path, "a"):
                pass
            return
    except PermissionError:
        return "Permission Error when writing to banned list"

    banned_list_write_to_file = dumps(pack_list)
    with open(file_path, "w") as file:
        file.write(banned_list_write_to_file)


class UpgradeAndResetButton(customtkinter.CTkButton):
    def __init__(self, master, command=None, text="UPGRADE", **kwargs):
        super().__init__(
            master,
            **kwargs,
            text=text,
            corner_radius=10,
            font=("Roboto", 21, "bold"),
            width=550,
            height=50,
            fg_color="#569cf9",
            border_width=1,
            border_color="black",
        )


class BannedPackagesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.button_list = []
        self.font = ("Roboto", 14, "bold")
        self.upgrade_frame = None

        self.placeholder = customtkinter.CTkFrame(self, fg_color="#252626")

        p_name_lbl = customtkinter.CTkLabel(
            self.placeholder,
            text="Banned Packages",
            font=self.font,
            anchor="w",
            width=200,
        )
        p_name_lbl.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")

        self.placeholder.grid(
            row=0, column=0, columnspan=2, padx=(0, 5), pady=(0, 10), sticky="ew"
        )
        self.placeholder.grid_propagate(False)
        self.placeholder.configure(width=520, height=40)

    def set_class_channel(self, upgradablepackagesframe):
        self.upgrade_frame = upgradablepackagesframe

    def add_package(self, package_name, version_current, version_latest, package_type):
        def unban_package(
            self, name_widget, banned_p_current, banned_p_latest, banned_p_type
        ):
            p_name = name_widget.cget("text")
            try:
                banned_list.remove(p_name)
            except ValueError:
                pass
            self.upgrade_frame.add_package(
                package_name=p_name,
                version_current=banned_p_current,
                version_latest=banned_p_latest,
                package_type=banned_p_type,
            )
            borderframe.grid_forget()

        borderframe = customtkinter.CTkFrame(
            self, border_color="dark gray", fg_color="#252626", border_width=1
        )
        borderframe.grid_columnconfigure(0, weight=1)
        borderframe.grid_columnconfigure((1, 2, 3), weight=0)
        # borderframe.grid_columnconfigure(4, weight=0, minsize=70)

        banned_p_current = version_current
        banned_p_latest = version_latest
        banned_p_type = package_type

        banned_p_lbl = customtkinter.CTkLabel(
            borderframe, text=package_name, anchor="w", width=100
        )
        banned_p_lbl.grid(row=0, column=0, padx=(65, 0), pady=7, sticky="w")

        banned_p_v_lbl = customtkinter.CTkLabel(
            borderframe, text=version_current, anchor="e", width=100
        )
        banned_p_v_lbl.grid(row=0, column=1, padx=(0, 20), pady=7, sticky="w")

        button = customtkinter.CTkButton(
            borderframe,
            text="Unban",
            fg_color="#088c08",
            hover_color="#5da763",
            width=50,
            height=24,
            command=lambda: unban_package(
                self, banned_p_lbl, banned_p_current, banned_p_latest, banned_p_type
            ),
        )
        button.grid(row=0, column=0, padx=7, pady=7, sticky="w")

        borderframe.grid(row=len(banned_list) + 1, column=0, pady=(0, 10), sticky="w")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        # Wont need later when we destroy the frame itself and not the widgets within
        banned_list.append(f"{package_name}")
        self.button_list.append(button)


class UpgradablePackagesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=0)

        self.command = command
        self.font = ("Roboto", 14, "bold")
        self.banned_frame = None

        self.placeholder = customtkinter.CTkFrame(self, fg_color="#252626")

        placeholder_name_lbl = customtkinter.CTkLabel(
            self.placeholder, text="Package", font=self.font, anchor="w", width=200
        )
        placeholder_ver_current_lbl = customtkinter.CTkLabel(
            self.placeholder, text="Current", font=self.font, anchor="w", width=80
        )
        placeholder_ver_latest_lbl = customtkinter.CTkLabel(
            self.placeholder, text="Latest", font=self.font, anchor="w", width=70
        )
        placeholder_type_lbl = customtkinter.CTkLabel(
            self.placeholder, text="Type", font=self.font, anchor="w", width=20
        )

        placeholder_name_lbl.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")
        placeholder_ver_current_lbl.grid(
            row=0, column=1, pady=7, padx=(27, 0), sticky="w"
        )
        placeholder_ver_latest_lbl.grid(
            row=0, column=2, pady=7, padx=(5, 0), sticky="w"
        )
        placeholder_type_lbl.grid(row=0, column=3, padx=(20, 10), pady=7, sticky="e")

        self.placeholder.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        self.placeholder.grid_propagate(False)
        self.placeholder.configure(width=525, height=40)

    def set_class_channel(self, bannedpackagesframe):
        self.banned_frame = bannedpackagesframe

    def add_package(self, package_name, version_current, version_latest, package_type):
        def ban_package(
            self, name_widget, v_current_widget, v_latest_widget, type_widget
        ):
            try:
                upgrade_list.remove(name_widget.cget("text"))
            except ValueError:
                pass

            p_name = name_widget.cget("text")
            p_current = v_current_widget.cget("text")
            p_latest = v_latest_widget.cget("text")
            p_type = type_widget.cget("text")
            self.banned_frame.add_package(
                package_name=p_name,
                version_current=p_current,
                version_latest=p_latest,
                package_type=p_type,
            )
            borderframe.grid_forget()

        def checkbox_event_callback(widget):
            if widget.get() == 1:
                try:
                    if widget.cget("text") not in upgrade_list:
                        upgrade_list.append(chkbox.cget("text"))
                except Exception:
                    pass
            elif widget.get() == 0:
                try:
                    upgrade_list.remove(chkbox.cget("text"))
                except ValueError:
                    pass

        borderframe = customtkinter.CTkFrame(
            self, border_color="dark gray", fg_color="#252626", border_width=1
        )
        borderframe.grid_columnconfigure(0, weight=1)
        borderframe.grid_columnconfigure((1, 2, 3), weight=0)
        borderframe.grid_columnconfigure(4, weight=0, minsize=70)

        upgrade_chkbox_var = customtkinter.IntVar(value=1)
        chkbox = customtkinter.CTkCheckBox(
            borderframe, text=package_name, width=300, variable=upgrade_chkbox_var
        )
        chkbox.configure(command=lambda: checkbox_event_callback(chkbox))
        p_ver_current_lbl = customtkinter.CTkLabel(
            borderframe, text=version_current, anchor="e", width=80
        )
        p_ver_latest_lbl = customtkinter.CTkLabel(
            borderframe, text=version_latest, anchor="e", width=80
        )
        p_type_lbl = customtkinter.CTkLabel(
            borderframe, text=package_type, anchor="e", width=80
        )
        ban_button = customtkinter.CTkButton(
            borderframe,
            text="Ban",
            fg_color="#991b1b",
            hover_color="#ff4d52",
            width=50,
            height=24,
            command=lambda: ban_package(
                self, chkbox, p_ver_current_lbl, p_ver_latest_lbl, p_type_lbl
            ),
        )

        chkbox.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")
        p_ver_current_lbl.grid(row=0, column=1, pady=7, sticky="e")
        p_ver_latest_lbl.grid(row=0, column=2, pady=7, sticky="e")
        p_type_lbl.grid(row=0, column=3, padx=(0, 10), pady=7, sticky="e")
        ban_button.grid(row=0, column=4, padx=7, pady=7, sticky="e")

        borderframe.grid(row=len(upgrade_list) + 1, column=0, pady=(0, 10), sticky="ew")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        upgrade_list.append(chkbox.cget("text"))


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

    master.geometry(f"{app_width}x{app_height}+{int(app_x)}+{int(app_y)}")
    master.resizable(False, False)


def determine_pip_list():
    unprocessed_pip_rows = []
    package_query = subprocess.Popen(
        "pip list --outdated",
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for line in package_query.stdout.read().decode().split("\n")[2:]:
        unprocessed_pip_rows.append(line.strip("\r"))

    return unprocessed_pip_rows


def process_pip_result(result_row):
    cleaned_string = result_row.strip()

    # Remove all spaces from string and seperate into groups
    parts = re.findall(r"\S+", cleaned_string)

    # Ensure we have exactly 4 parts. Pip seems to be consistent with this.
    if len(parts) != 4:
        raise ValueError(
            f"Expected 4 parts, but got {len(parts)} in string: {result_row}"
        )

    return parts[0], parts[1], parts[2], parts[3]


async def call_reset_event_text(
    widget: customtkinter.CTkTextbox,
):  # Not working currently
    widget.configure(state="normal")
    old_text = widget.get(0.0, "end")
    new_text = (
        old_text + "\n\nResetting client..\nRefreshing outdated and banned packages..."
    )
    widget.insert('end', new_text)
    widget.configure(state="disabled")

def main():
    global banned_list_file_path
    global console_encoding
    global upgrade_list
    global banned_list
    global startup_banlist
    global pip_result

    banned_list_file_path = os.path.join(os.getcwd(), "pipupgui_banned.txt")
    console_encoding = "utf-8"
    if platform.system() == "Windows":
        from ctypes import windll
        console_code_page = windll.kernel32.GetConsoleOutputCP()
        if console_code_page != 65001:
            console_encoding = f"cp{console_code_page}"

    customtkinter.set_appearance_mode("dark")

    upgrade_list = []
    banned_list = []
    startup_banlist = on_startup_ban_list(banned_list_file_path)
    pip_result = determine_pip_list()

    app = App()
    set_window_default_settings(app)

    try:
        app.async_mainloop()
    except asyncio.CancelledError:
        pass


class App(customtkinter.CTk, AsyncCTk):
    def __init__(self):
        super().__init__()
        self.upgrade_subprocess: Process | None = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.font = ("Roboto", 21, "bold")
        self.title("pipupgui")
        self.iconpath = ImageTk.PhotoImage(file=resource_path("title_icon_python.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.rowconfigure(1, weight=1)

        self.page1_frame = customtkinter.CTkFrame(
            master=self, width=600, height=700, fg_color="#242424"
        )

        self.header_frame = customtkinter.CTkFrame(
            master=self.page1_frame, width=100, corner_radius=10, fg_color="#242424"
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(resource_path("title_icon_python.png")), size=(36, 36)
        )
        header_logo = customtkinter.CTkLabel(
            self.header_frame, text="", image=self.logo_image, anchor="w"
        )
        header_logo.grid(
            row=0, rowspan=2, column=0, sticky="w", padx=(18, 0), pady=(0, 10)
        )
        header_title = customtkinter.CTkLabel(
            self.header_frame,
            text="Pip Upgrade GUI",
            font=("Roboto", 21, "bold"),
            anchor="w",
        )
        header_title.grid(
            row=0, rowspan=1, column=1, sticky="w", padx=(16, 55), pady=(0, 8)
        )

        self.github_image = customtkinter.CTkImage(
            Image.open(resource_path("github_logo.png")), size=(128, 64)
        )
        header_github = customtkinter.CTkButton(
            self.header_frame,
            text="",
            image=self.github_image,
            anchor="nsew",
            hover_color="#242424",
            fg_color="transparent",
            command=lambda: callback(url="https://github.com/Dylgod/auto_upgrade_gui"),
        )
        header_github.grid(
            row=0, column=3, sticky="e", padx=(100, 18)
        )  # , padx=(140, 18), pady=(15, 13)

        self.header_frame.pack(side="top", fill="x")

        self.upgrade_frame = UpgradablePackagesFrame(
            master=self.page1_frame, height=275, width=525, corner_radius=10
        )
        self.upgrade_frame.pack(side="top", fill="x")

        self.banned_frame = BannedPackagesFrame(
            master=self.page1_frame, height=150, width=525, corner_radius=10
        )
        self.banned_frame.pack(side="top", fill="both", pady=(10, 0))

        self.create_frame_channel(self.upgrade_frame, self.banned_frame)

        self.upgrade_button = UpgradeAndResetButton(
            self.page1_frame, text="UPGRADE", command=None
        )
        self.upgrade_button.configure(command=self.start_upgrade_tasks, height=65)
        self.upgrade_button.pack(side="bottom", fill="both", pady=(5, 5))

        # Result Page widgets
        self.page2_frame = customtkinter.CTkFrame(
            master=self, width=600, height=700, fg_color="#242424"
        )
        self.textbox_outer_frame = customtkinter.CTkFrame(self.page2_frame, width=600)
        self.textbox = customtkinter.CTkTextbox(
            self.textbox_outer_frame,
            width=600,
            height=600,
            font=("Roboto", 14),
            activate_scrollbars=True,
        )
        self.reset_button = UpgradeAndResetButton(self.page2_frame, text="RESET")

        for row in pip_result:
            if len(row) > 5:
                name, version, latest, type = process_pip_result(row)
            else:
                continue
            if name not in startup_banlist:
                self.upgrade_frame.add_package(name, version, latest, type)
            else:
                self.banned_frame.add_package(name, version, latest, type)

        self.page1_frame.pack(expand=True, fill="both", padx=20, pady=(10, 10))

    @async_handler
    async def on_close(self):
        await asyncio.sleep(0.5)

        # Safely terminate all active asynchronous operations
        tasks = [
            task for task in asyncio.all_tasks() if task is not asyncio.current_task()
        ]
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self.destroy()

    @async_handler
    async def reset_app(self):
        global upgrade_list
        global banned_list
        upgrade_list = []
        banned_list = []

        if self.upgrade_subprocess is not None:
            try:
                self.upgrade_subprocess.kill()
            except ProcessLookupError:
                pass
            except Exception as e:
                print("line 351", type(e))

        for child in self.upgrade_frame.winfo_children():
            if child.winfo_children()[0].cget("text") != "Package":
                child.destroy()

        for child in self.banned_frame.winfo_children():
            if child.winfo_children()[0].cget("text") != "Banned Packages":
                child.destroy()

        await self.reset_pip_packages()

        self.page2_frame.pack_forget()
        self.page1_frame.pack(expand=True, fill="both", padx=20, pady=(10, 10))

        self.textbox.delete(0.0, "end")

    async def reset_pip_packages(self):
        startup_banlist = on_startup_ban_list(banned_list_file_path)
        pip_result = determine_pip_list()

        for row in pip_result:
            if len(row) > 1:
                name, version, latest, type = process_pip_result(row)
            else:
                continue
            if name not in startup_banlist:
                self.upgrade_frame.add_package(name, version, latest, type)
            else:
                self.banned_frame.add_package(name, version, latest, type)

    def load_upgrade_scrn(self):
        self.page1_frame.pack_forget()

        self.textbox_outer_frame.pack(side="top", expand=True, fill="both")
        self.textbox.pack(expand=True, fill="both")
        self.reset_button.configure(command=self.reset_app, height=65, state="disabled")
        self.reset_button.pack(side="bottom", fill="both", pady=(15, 5))
        self.page2_frame.pack(expand=True, fill="both", padx=20, pady=(10, 10))

    @async_handler
    async def start_upgrade_tasks(self):
        self.load_upgrade_scrn()

        ban_packs(banned_list_file_path, banned_list)
        if len(upgrade_list) > 0:
            for pack in upgrade_list:
                if pack == "pip":
                    cmd = "python.exe -m pip install --upgrade pip"
                else:
                    cmd = f"pip install {pack} --upgrade"

                self.upgrade_subprocess = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                while self.upgrade_subprocess.returncode is None:
                    stdout = asyncio.create_task(self.upgrade_subprocess.stdout.readline())
                    stderr = asyncio.create_task(self.upgrade_subprocess.stderr.readline())

                    done, pending = await asyncio.wait(
                        {stdout, stderr}, return_when=asyncio.FIRST_COMPLETED
                    )

                    if stdout in done:
                        result_text = stdout.result().decode(console_encoding)
                        self.textbox.insert("end", result_text)

                    if stderr in done:
                        result_text = stderr.result().decode(console_encoding)
                        self.textbox.insert("end", result_text, "red_text")

                    for item in pending:
                        item.cancel()

                self.upgrade_subprocess = None

        elif len(upgrade_list) == 0:
            self.textbox.insert(
                "end", "You are up to date!\nYou may close this window.\n"
            )

        if len(banned_list) > 0:
            self.textbox.insert("end", "\nBanned Packages:\n----------------\n")
            for pack in banned_list:
                self.textbox.insert("end", pack + "\n")

        self.textbox.insert("end", "\nProcess Complete.")
        self.reset_button.configure(state="normal")

    def create_frame_channel(self, upgradablepackagesframe, bannedpackagesframe):
        """
        Links UpgradablePackagesFrame & BannedPackagesFrame classes
        in order to send packages back and forth.
        """

        self.upgrade_frame.set_class_channel(self.banned_frame)
        self.banned_frame.set_class_channel(self.upgrade_frame)


if __name__ == "__main__":
    main()
