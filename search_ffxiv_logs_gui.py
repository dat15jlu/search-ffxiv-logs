from os import listdir

import search_ffxiv_logs as util
import tkinter as tk


def write_to(all_matches, out_file):
    f_out = open(out_file, "w")
    for key in all_matches.keys():
        if len(all_matches[key]) > 0:
            f_out.write('\n')
            f_out.write("#################### " + key + ":")
            f_out.write('\n')
            for match in all_matches[key]:
                f_out.write(match + '\n')


class SearchFFXIVLogsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.font_label = ("Helvetica", 16, "bold")
        self.font_entry = ("Helvetica", 16)
        self.title("Search FFXIV Logs")

        tk.Label(self, text="Directory name:", font=self.font_label).grid(row=0, sticky='E')
        tk.Label(self, text="Search term:", font=self.font_label).grid(row=1, sticky='E')
        tk.Label(self, text="Output file:", font=self.font_label).grid(row=2, sticky='E')

        self.default_e1 = tk.StringVar(self, value="log")
        self.default_e2 = tk.StringVar(self, value="Annie Keito")
        self.default_e3 = tk.StringVar(self, value="output.txt")

        self.e1 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e1)
        self.e2 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e2)
        self.e3 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e3)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        self.b1 = tk.Button(self, text="SEARCH", font=self.font_label, command=self.search).grid(row=3, columnspan=2)

    def search(self):
        dir_name = self.e1.get()
        regex = self.e2.get()
        out_file = self.e3.get()

        files = [dir_name + "/" + file for file in listdir(dir_name)]
        all_matches = util.find_all_matches(files, regex)
        write_to(all_matches, out_file)


app = SearchFFXIVLogsApp()
app.mainloop()

