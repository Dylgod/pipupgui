import tkinter as tk
from tkinter import ttk
import sv_ttk
import tkinter.font as tkFont
import pywinstyles, sys

# @formatter:off

class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"

def os_name():
    if "linux" in sys.platform:
        return OSType.LINUX
    elif "darwin" in sys.platform:
        return OSType.MAC
    elif "win32" in sys.platform:
        return OSType.WIN
    else:
        raise Exception("Could not determine the OS type!")

OPERATING_SYSTEM = os_name()
packages = ["Selenium,wheel,10.6,10.4","pyinstaller-hooks-contrib,wheel,10.0.63,10.0.33","customtkinter,wheel,16.1,12.0"]

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
    # win.resizable(False, False)
    # master.minsize(500, 700)
    master.protocol("WM_DELETE_WINDOW", close_signout(master))

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

        # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

class PackageFrame(ttk.Frame):
    def __init__(self, master, package_name, package_type, version_latest, version_current):
        super().__init__(master, borderwidth=2, relief='raised', padding=5)

        normal_font = tkFont.Font(family="Arial", size=12, weight=tkFont.NORMAL)
        self.checked = tk.BooleanVar(self, True)

        if len(package_name)>25:
            package_name = package_name[0:25]+"..."

        self.chk1 = ttk.Checkbutton(self, text=package_name, width=23, variable=self.checked).pack(side='left')
        self.typelbl = ttk.Label(self, text=package_type, font=normal_font, width=6, anchor="e", padding=5).pack(side='right')
        self.latestlbl = ttk.Label(self, text=version_latest, font=normal_font, width=9, anchor="w").pack(side='right')
        self.currentlbl = ttk.Label(self, text=version_current, font=normal_font, width=11, anchor="w").pack(side='right')


class OuterContainer(ttk.LabelFrame):
    def __init__(self, parent, framename):
        super().__init__(parent, text=framename, padding=10)

        self.frame1 = None
        self.var_1 = tk.BooleanVar(self, False)
        self.var_2 = tk.BooleanVar(self, True)

        self.add_widgets()

    def add_widgets(self):
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(row=0, column=0, pady=(0, 10), sticky="w")

        if len(packages)>0:
            for package in packages:
                p_name,p_type,p_latest,p_current = [x.strip() for x in package.split(",")]
                PackageFrame(self.frame1,p_name,p_type,p_latest,p_current).pack()

    def ban_package(self):
        pass

    def unban_package(self):
        pass

class HeaderFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.add_widgets()

    def add_widgets(self):
        ttk.Label(self, text="Package Update Manager", justify="left", anchor="w", font=("Roboto", 20)).pack(side="left")


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        for index in range(12):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        HeaderFrame(self).grid(row=0, column=0, sticky="nsew")
        OuterContainer(self, "Outdated Packages").grid(row=1, column=0, rowspan=5, sticky="nsew")
        OuterContainer(self, "Banned Packages").grid(row=7, column=0, sticky="nsew")
        ttk.Button(self, text="UPGRADE", style="Accent.TButton").grid(row=9, column=0, sticky="nsew")

def main():
    win = tk.Tk()
    win.title("auto_update_gui")

    if OPERATING_SYSTEM == 'win':
        sv_ttk.set_theme("dark")
        icon = tk.PhotoImage(file=r".\title_icon_python.png")
        win.iconphoto(True, icon)

    set_window_default_settings(win)
    App(win).pack(expand=True, fill="y")
    win.mainloop()


if __name__ == "__main__":
    main()
