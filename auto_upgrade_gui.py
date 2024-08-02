import customtkinter
import os

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):

    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs, fg_color="#191a1a")
        self.grid_columnconfigure(0, weight=0)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        self.chkbox_list = []

    def add_package(self, package_name, package_type, version_latest, version_current):
        def get_children_data(self, widget):
            print(widget.cget('text'))

        borderframe = customtkinter.CTkFrame(self, border_color='dark gray', fg_color="#252626", border_width=1)
        borderframe.grid_columnconfigure(0, weight=1)
        borderframe.grid_columnconfigure((1, 2, 3), weight=0)
        borderframe.grid_columnconfigure(4, weight=0, minsize=70)

        chkbox = customtkinter.CTkCheckBox(borderframe, text=package_name, width=300)
        label1 = customtkinter.CTkLabel(borderframe, text=package_type, anchor="e", width=80)
        label2 = customtkinter.CTkLabel(borderframe, text=version_latest, anchor="e", width=80)
        label3 = customtkinter.CTkLabel(borderframe, text=version_current, anchor="e", width=80)
        button = customtkinter.CTkButton(borderframe, text="Ban", fg_color="#991b1b", width=50, height=24,
                                         command=lambda: get_children_data(self, chkbox))

        chkbox.grid(row=0, column=0, padx=(7, 0), pady=7, sticky="w")
        label1.grid(row=0, column=1, pady=7, sticky="e")
        label2.grid(row=0, column=2, pady=7, sticky="e")
        label3.grid(row=0, column=3, padx=(0, 10), pady=7, sticky="e")
        button.grid(row=0, column=4, padx=7, pady=7, sticky="e")

        borderframe.grid(row=len(self.chkbox_list), column=0, pady=(0, 10), sticky="ew")
        borderframe.grid_propagate(False)
        borderframe.configure(width=525, height=40)

        self.label_list.append(label1)
        self.button_list.append(button)
        self.chkbox_list.append(chkbox)

    def remove_item(self, item):
        for label1, button in zip(self.label_list, self.button_list):
            if item == label1.cget("text"):
                label1.destroy()
                button.destroy()
                self.label_list.remove(label1)
                self.button_list.remove(button)
                return

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
    # master.minsize(600, 700)
    master.protocol("WM_DELETE_WINDOW", close_signout(master))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("CTkScrollableFrame example")
        # self.grid_rowconfigure(1, weight=1)
        for index in range(7):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=525, corner_radius=10)
        self.scrollable_label_button_frame.grid(row=1, column=1, padx=(18,0), pady=0, sticky="nsew")
        packages = ["Selenium,10.4,10.6,wheel", "pyinstaller-hooks-contrib,10.0.33,10.0.63,wheel", "customtkinter,12.0,16.1,wheel"]
        for i in packages:  # add items with images
            p_name,p_type,p_current,p_latest = [item.strip() for item in i.split(",")]
            self.scrollable_label_button_frame.add_package(p_name,p_type,p_current,p_latest)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    app = App()
    set_window_default_settings(app)
    app.mainloop()