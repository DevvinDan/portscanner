import tkinter as tk

class App(tk.Frame):

    default_x_padding = 100
    default_y_padding = 20
    background_color = "white"


    main_label_text = "Port Scanner"
    ip_label_text = "Enter IP range to scan:"
    port_label_text = "Enter ports to scan:"
    default_ip_text = "127.0.0.1"
    default_port_text = "1-1025"


    def __init__(self, master=None):

        super().__init__(master)
        self["bg"] = "white"
        self["padx"] = 30
        self["pady"] = 30
        self.pack(
            expand=1,
            fill=tk.BOTH
        )
        self.create_widgets()
        self.set_defaults()

    def set_defaults(self):
        self.ip_entry.insert(0, self.default_ip_text)
        self.port_entry.insert(0, self.default_port_text)

    def create_widgets(self):

        #Main label

        self.main_label = tk.Label(self,
                                   font="Helvetica 24",
                                   text=self.main_label_text,
                                   fg="purple",
                                   bg=self.background_color,
                                   padx=self.default_x_padding,
                                   pady=0)
        self.main_label.pack(
            expand=0,
            fill=tk.X
        )

        # Label for IP entry

        self.ip_label = tk.Label(self,
                                   font="Helvetica 14",
                                   text=self.ip_label_text,
                                   fg="black",
                                   bg=self.background_color,
                                   padx=self.default_x_padding,
                                   pady=self.default_y_padding)

        self.ip_label.pack(
            expand=0,
            fill=tk.X
        )

        # IP entry

        self.ip_entry = tk.Entry(self,
                                 bg=self.background_color,
                                 bd=4,
                                 font="Helvetica 12",
                                 exportselection=0,
                                 textvariable = tk.StringVar(),
                                 width=20
                                 )

        self.ip_entry.pack(
            expand=0

        )

        # Port label

        self.port_label = tk.Label(self,
                                   font="Helvetica 14",
                                   text=self.port_label_text,
                                   fg="black",
                                   bg=self.background_color,
                                   padx=self.default_x_padding,
                                   pady=self.default_y_padding)

        self.port_label.pack(
            expand=0,
            fill=tk.X
        )

        # Port entry

        self.port_entry = tk.Entry(self,
                                 bg=self.background_color,
                                 bd=4,
                                 font="Helvetica 12",
                                 exportselection=0,
                                 textvariable = tk.StringVar(),
                                 width=20
                                 )

        self.port_entry.pack(
            expand=0
        )

        




root = tk.Tk()
root.title("Port Scanner v1.0")
app = App(master=root)
app.mainloop()