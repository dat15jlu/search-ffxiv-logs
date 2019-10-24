from os import listdir

import search_ffxiv_logs as util
import tkinter as tk
import datetime


def write_to(all_matches, out_file):
    f_out = open(out_file, "w")
    for key in all_matches.keys():
        if len(all_matches[key]) > 0:
            f_out.write('\n')
            f_out.write("#################### " + key + ":")
            f_out.write('\n')
            for match in all_matches[key]:
                f_out.write(match + '\n')


def get_time_of_day():
    time_object = datetime.datetime.now()
    return "[{}:{}] ".format(time_object.hour, time_object.minute)


class SearchFFXIVLogsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)
        self.title("Search FFXIV Logs")
        self.is_case_sensitive = tk.IntVar()

        tk.Label(self, text="Directory name:", font=self.font_label)\
            .grid(row=0, sticky='E')
        tk.Label(self, text="Search term:", font=self.font_label)\
            .grid(row=1, sticky='E')
        tk.Label(self, text="Output file:", font=self.font_label)\
            .grid(row=3, sticky='E')

        self.default_e1 = tk.StringVar(self, value="log")
        self.default_e2 = tk.StringVar(self, value="Annie Keito")
        self.default_e3 = tk.StringVar(self, value="output.txt")

        self.e1 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e1)
        self.e2 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e2)
        self.e3 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e3)
        self.case = tk.Checkbutton(self, font=self.font_entry, text="Case Sensitive", variable=self.is_case_sensitive)
        self.case.select()  # checked by default

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.case.grid(row=2, column=1, sticky='W')
        self.e3.grid(row=3, column=1)

        tk.Button(self, text="SEARCH", font=self.font_label, command=self.search)\
            .grid(row=4, columnspan=2, pady=5)

        self.status = tk.Text(self, font=self.font_entry, state='disabled', width=35, height=10)
        self.status.grid(row=5, columnspan=2)
        self.print_to_console("Press SEARCH to begin...")

    def print_to_console(self, message):
        self.status['state'] = 'normal'
        time = get_time_of_day()
        formatted_message = time + message + '\n'
        self.status.insert(tk.INSERT, formatted_message)
        self.status['state'] = 'disabled'

    def search(self):
        dir_name = self.e1.get()
        regex = self.e2.get()
        out_file = self.e3.get()
        is_case_sensitive = self.is_case_sensitive.get()

        self.print_to_console("Searching ...")
        self.update()

        files = [dir_name + "/" + file for file in listdir(dir_name)]
        all_matches = util.find_all_matches(files, regex, is_case_sensitive)
        write_to(all_matches, out_file)

        self.print_to_console("Done ...")
        self.print_to_console("Press SEARCH to begin once more...")
        self.update()


app = SearchFFXIVLogsApp()
app.mainloop()

