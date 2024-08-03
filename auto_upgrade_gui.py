import customtkinter
from PIL import ImageTk
from PIL import Image
import os
import webbrowser
# import asyncio Need for reset after console result

# @formatter:off

def callback(url):
    webbrowser.open_new(url)

class UpgradeAndResetButton(customtkinter.CTkButton):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, text="UPGRADE", corner_radius=10, font=("Roboto",21, "bold"), width=550, height=50, fg_color="#569cf9",border_width=1, border_color="black")


class BannedPackagesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.label_list = []
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

        borderframe.grid(row=len(self.label_list)+1, column=0, pady=(0, 10), sticky="w")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        # Wont need later when we destroy the frame itself and not the widgets within
        self.label_list.append(banned_p_lbl)
        self.button_list.append(button)

        
class UpgradablePackagesFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=0)

        # Wont need later when we destroy the frame itself and not the widgets within
        self.command = command
        self.label_list = []
        self.button_list = []
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
        self.label_list.append(p_type_lbl)
        self.button_list.append(ban_button)
        self.chkbox_list.append(chkbox)



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
    master.protocol("WM_DELETE_WINDOW", close_signout(master))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.font = ("Roboto",21, "bold")
        self.title("auto_upgrade_gui")
        self.iconpath = ImageTk.PhotoImage(file=os.path.join(os.getcwd(), "title_icon_python.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        # for index in range(7):
        #     self.columnconfigure(index, weight=1)
        #     self.rowconfigure(index, weight=1)

        self.rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(master=self, width=100, corner_radius=10, fg_color="#242424")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "title_icon_python.png")),size=(36, 36))
        header_logo = customtkinter.CTkLabel(self.header_frame, text="", image=self.logo_image, anchor='w')
        header_logo.grid(row=0, rowspan=2,column=0, sticky='w', padx=(18, 0), pady=(15, 15))
        header_title = customtkinter.CTkLabel(self.header_frame, text="auto_upgrade_gui", font=("Roboto",21, "bold"), anchor='w')
        header_title.grid(row=0, column=1, sticky='w', padx=(13, 0), pady=(15, 13))

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(os.getcwd(), "github_logo.png")),size=(128, 64))
        header_github = customtkinter.CTkButton(self.header_frame, text="", image=self.logo_image, anchor='nsew', hover_color="#242424", fg_color="transparent", command=lambda: callback(url="https://github.com/Dylgod/auto_upgrade_gui"))
        header_github.grid(row=0,column=4, sticky='e', padx=(140, 18), pady=(15, 13))

        self.header_frame.grid(row=0, column=1, padx=(18, 0), pady=0, sticky="nsew")

        self.upgrade_frame = UpgradablePackagesFrame(master=self, width=525, corner_radius=10)
        self.upgrade_frame.grid(row=1,rowspan=2, column=1, padx=(18,0), pady=0, sticky="nsew")
        
        self.banned_frame = BannedPackagesFrame(master=self, width=525, corner_radius=10)
        self.banned_frame.grid(row=3, column=1, padx=(18,0), pady=(10, 0), sticky="nsew")

        self.create_frame_channel(self.upgrade_frame, self.banned_frame)

        self.upgrade_button = UpgradeAndResetButton(self)
        self.upgrade_button.grid(row=5, column=1, padx=(18, 0), pady=(10, 10), sticky="nsew")
        

        packages = ["Selenium,10.4,10.6,wheel", "pyinstaller-hooks-contrib,10.0.33,10.0.63,wheel", "customtkinter,12.0,16.1,wheel",
                    "darkdetect,0.8.0,1.0,wheel","packaging,24.1,24.2,wheel","pywinstyles,1.8,1.9,wheel","pillow,10.4.0,10.5.1,wheel"]
        for pack in packages:
            p_name,p_current,p_latest,p_type = [item.strip() for item in pack.split(",")]
            self.upgrade_frame.add_package(p_name,p_current,p_latest,p_type)


    def create_frame_channel(self, upgradablepackagesframe, bannedpackagesframe):
        """
        Links UpgradablePackagesFrame & BannedPackagesFrame classes
        in order to send packages back and forth.
        """

        self.upgrade_frame.set_class_channel(self.banned_frame)
        self.banned_frame.set_class_channel(self.upgrade_frame)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    set_window_default_settings(app)
    app.mainloop()