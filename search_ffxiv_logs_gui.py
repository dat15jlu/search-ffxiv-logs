from os import listdir

from search_ffxiv_logs import find_all_matches
import tkinter as tk
import datetime


def no_such_dir(dir_name):
    return 'Could not find directory "' + dir_name + '". ' + \
           'Please check the directory name, and verify that it is located in the same directory as this program.'


def write_to(out_file, all_matches):
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
    return "[{:02d}:{:02d}] ".format(time_object.hour, time_object.minute)


def no_matches_for(regex):
    return 'Found no matches for "' + regex + '". Please review your search term and try again.'


def count_occurrences(all_matches):
    nbr_of_matches = 0
    nbr_of_matched_files = 0
    for file in all_matches.keys():
        if len(all_matches[file]) > 0:
            nbr_of_matches += len(all_matches[file])
            nbr_of_matched_files += 1
    return nbr_of_matched_files, nbr_of_matches


class SearchFFXIVLogsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)
        self.title("Search FFXIV Logs")
        self.is_case_sensitive = tk.IntVar()
        self.bg_color = '#36393F'
        self.fg_color = '#FFFFFF'

        widgets = []

        self.l1 = tk.Label(self, text="Directory name:", font=self.font_label)
        self.l1.grid(row=0, sticky='E')
        widgets.append(self.l1)

        self.l2 = tk.Label(self, text="Search term:", font=self.font_label)
        self.l2.grid(row=1, sticky='E')
        widgets.append(self.l2)

        self.l3 = tk.Label(self, text="Output file:", font=self.font_label)
        self.l3.grid(row=3, sticky='E')
        widgets.append(self.l3)

        self.default_e1 = tk.StringVar(self, value="log")
        self.default_e2 = tk.StringVar(self, value="Annie Keito")
        self.default_e3 = tk.StringVar(self, value="output.txt")

        self.e1 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e1)
        self.e1.grid(row=0, column=1)
        widgets.append(self.e1)

        self.e2 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e2)
        self.e2.grid(row=1, column=1)
        widgets.append(self.e2)

        self.case_check = tk.Checkbutton(self, font=self.font_entry, text="Case Sensitive",
                                         variable=self.is_case_sensitive, selectcolor="black")
        self.case_check.select()  # checked by default
        self.case_check.grid(row=2, column=1, sticky='W')
        widgets.append(self.case_check)

        self.e3 = tk.Entry(self, font=self.font_entry, textvariable=self.default_e3)
        self.e3.grid(row=3, column=1)
        widgets.append(self.e3)

        self.button = tk.Button(self, text="SEARCH", font=self.font_label, command=self.search)
        self.button.grid(row=4, columnspan=2, pady=5)
        widgets.append(self.button)

        self.status = tk.Text(self, font=self.font_entry, state='disabled', width=35, height=10, wrap=tk.WORD)
        self.status.grid(row=5, columnspan=2)
        widgets.append(self.status)

        # Apply dark mode
        self.configure(bg=self.bg_color)
        self.case_check.configure(activebackground=self.bg_color)  # stay dark while pressed
        self.button.configure(activebackground=self.bg_color)  # stay dark while pressed
        for widget in widgets:
            widget.configure(bg=self.bg_color)
            widget.configure(fg=self.fg_color)

        self.print_to_console("Press SEARCH to begin ...")

    def print_to_console(self, message):
        self.status['state'] = 'normal'
        time = get_time_of_day()
        formatted_message = time + message + '\n'
        self.status.insert(tk.INSERT, formatted_message)
        self.status['state'] = 'disabled'
        self.status.see("end")  # auto scroll status window
        self.update()

    def search(self):
        dir_name = self.e1.get()
        regex = self.e2.get()
        out_file = self.e3.get()
        is_case_sensitive = self.is_case_sensitive.get()

        try:
            files = [dir_name + "/" + file for file in listdir(dir_name)]
        except FileNotFoundError:
            self.print_to_console(no_such_dir(dir_name))
            return

        self.print_to_console("Searching {} files ...".format(len(files)))

        all_matches = find_all_matches(files, regex, is_case_sensitive)
        nbr_of_matched_files, nbr_of_matches = count_occurrences(all_matches)

        if nbr_of_matches == 0:
            self.print_to_console(no_matches_for(regex))
            return

        self.print_to_console("Search complete. There was {} matches across {} files."
                              .format(nbr_of_matches, nbr_of_matched_files))
        self.print_to_console("Writing matches to file {} ..."
                              .format(out_file))
        write_to(out_file, all_matches)
        self.print_to_console("Done!")


if __name__ == '__main__':
    app = SearchFFXIVLogsApp()
    app.mainloop()
