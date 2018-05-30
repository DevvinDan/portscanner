import tkinter as tk
from tkinter import messagebox
import portscanner
from datetime import datetime

class App(tk.Frame):

    default_x_padding = 100
    default_y_padding = 20
    background_color = "white"

    main_label_text = "Port Scanner"
    ip_label_text = "Enter IP range to scan:"
    port_label_text = "Enter ports to scan:"
    default_ip_text = "127.0.0.1"
    default_port_text = "1-1025"
    scan_button_text = "Scan"
    checkbox_text = "Parse input as 'IP/Mask'"


    def __init__(self, master=None):


        self.ps = portscanner.PortScanner()

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
        """Sets some default settings

        :return:
        """
        self.ip_entry.insert(0, self.default_ip_text)
        self.port_entry.insert(0, self.default_port_text)

    def select_all(self, widget):
        widget.select_range(0, 'end')
        widget.icursor('end')

    def callback(self, event):
        self.after(50, self.select_all, event.widget)

    def start_scan(self):
        """Start scanning the network

        :return:
        """

        if self.checkbox_state.get() == 1:
            try:
                ip_string = str(self.ip_entry.get())
                addr, mask = ip_string.split('/')
                ip_range = list(self.ps.get_subnet_addresses(addr, mask))
                self.ip_entry.delete(0, tk.END)
                self.ip_entry.insert(0, "{}-{}".format(ip_range[0], ip_range[-1]))
            except:
                messagebox.showinfo("Error", "Wrong IP/subnet mask")
                return


        self.results_textbox.delete(1.0, tk.END)

        start_time = datetime.now()

        try:
            ip_string = self.ip_entry.get()
            port_string = self.port_entry.get()
            ip_range = list(self.ps.get_ip_range(ip_string))
            port_range = list(self.ps.get_port_range(port_string))
        except:
            messagebox.showinfo("Error", "Wrong input")
            return

        try:
            for ip in ip_range:

                t_start = datetime.now()

                self.results_textbox.insert(tk.END,
                    "-" * 60 + "\n")
                self.results_textbox.insert(tk.END,
                    "Scanning remote host {}\n".format(ip))
                self.results_textbox.insert(tk.END,
                    "-" * 60 + "\n")
                for port in port_range:
                    port_is_open = self.ps.scan_port(ip, port)
                    if port_is_open:
                        self.results_textbox.insert(tk.END,
                            "Port {} is open, service: {}\n".format(port,
                                                            self.ps.get_service_name(port)))
                t_end = datetime.now()
                self.results_textbox.insert(tk.END,
                    "-" * 60 + "\n")
                self.results_textbox.insert(tk.END,
                    "Scanning completed in {}\n".format(t_end - t_start))
                self.results_textbox.insert(tk.END,
                    "-" * 60 + "\n")

        except:
            messagebox.showinfo("Error", "An error occured during scanning")
            return

        end_time = datetime.now()

        messagebox.showinfo("Port Scanning", "Scanning is completed in {}".format(
            end_time - start_time
        ))


    def create_widgets(self):
        """Creating and showing all GUI widgets

        :return:
        """

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
                                 width=30
                                 )

        self.ip_entry.pack(
            expand=0
        )

        self.ip_entry.bind('<Control-a>', self.callback)

        # Empty label for spacing

        self.before_subnet_spacer = tk.Label(self,
                                    text="",
                                    padx=self.default_x_padding,
                                    pady=5,
                                    bg=self.background_color
                                      )

        self.before_subnet_spacer.pack(
            expand=0
        )


        # Subnet scan checkbox


        self.checkbox_state = tk.IntVar()

        self.subnet_scan_checkbox = tk.Checkbutton(self,
                                                   font="Helvetica 12",
                                                   bd=7,
                                                   bg=self.background_color,
                                                   text=self.checkbox_text,
                                                   variable=self.checkbox_state,
                                                   onvalue=1,
                                                   offvalue=0
                                                   )

        self.subnet_scan_checkbox.deselect()

        self.subnet_scan_checkbox.pack(
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
                                 width=30
                                 )

        self.port_entry.pack(
            expand=0
        )

        self.port_entry.bind('<Control-a>', self.callback)

        # Empty label for spacing

        self.before_button_spacer = tk.Label(self,
                                    text="",
                                    padx=self.default_x_padding,
                                    pady=5,
                                    bg=self.background_color
                                      )

        self.before_button_spacer.pack(
            expand=0
        )


        # Scan button

        self.scan_button = tk.Button(self,
                                     bd=2,
                                     bg="violet",
                                     activebackground="white",
                                     font="Helvetica 12",
                                     text=self.scan_button_text,
                                     command=self.start_scan)

        self.scan_button.pack(
            expand=0
        )

        # Empty label for spacing

        self.after_button_spacer = tk.Label(self,
                                    text="",
                                    padx=self.default_x_padding,
                                    pady=5,
                                    bg=self.background_color
                                      )

        self.after_button_spacer.pack(
            expand=0
        )

        # Scanning results

        self.results_textbox = tk.Text(self,
                                       bd=2,
                                       bg="white",
                                       font="Times 12",
                                       height=15,
                                       width=80)

        self.results_textbox.pack(
            expand=0
        )


root = tk.Tk()
root.title("Port Scanner v1.0")
img = tk.Image("photo", file="spy.png")
root.tk.call('wm','iconphoto',root._w,img)
app = App(master=root)
app.mainloop()