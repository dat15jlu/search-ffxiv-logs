from os import listdir
import regex as re
import sys


def main():
    if len(sys.argv) > 2:
        files = [sys.argv[1] + "/" + file for file in listdir(sys.argv[1])]
        regex = sys.argv[2]
        all_matches = find_all_matches(files, regex)
        print_matches(all_matches)
    else:
        print_error_message()


def print_error_message():
    print()
    print("Not enough input parameters. Expected 2, got " + str(len(sys.argv) - 1) + ".")
    print("First parameter: directory with the log files. For example: \"log\".")
    print("Second parameter: text to search. For example: \"Annie Keito\".")
    print("You can run this program in PowerShell like this:")
    print()
    print(".\\search_ffxiv_logs.exe log \"Annie Keito\" > output.txt")
    print()
    print("If you are running it like this, make sure the log directory is")
    print("in the same directory as this .exe file.")


def print_matches(all_matches):
    for key in all_matches.keys():
        if len(all_matches[key]) > 0:
            print()
            print("#################### " + key + ":")
            print()
            for match in all_matches[key]:
                print(match)


def find_all_matches(files, regex):
    all_matches = {}
    for file in files:
        matches_in_file = []
        contents = read_file_to_string(file)
        matches = re.finditer(regex, contents)
        for match in matches:
            span = match.span()[0]
            start = span
            end = span + 120
            if start < 0:
                start = 0
            if end >= len(contents):
                end = len(contents) - 1
            matches_in_file.append(contents[start:end])
        # exit(0)
        all_matches[file] = matches_in_file
    return all_matches


def read_file_to_string(file):
    interesting_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()[],.?!:' "
    f = open(file, encoding="ISO-8859-1")
    contents = ""
    while True:
        try:
            c = f.read(1)
        except UnicodeDecodeError:
            c = ' '
        if not c:  # EOF
            break
        if c in interesting_chars:
            contents += c
        else:
            contents += ' '
    contents = re.sub(' +', ' ', contents)
    return contents


main()
