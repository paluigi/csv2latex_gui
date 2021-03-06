# PySimpleGUI application to select CSV files
# and create Latex tables out of them

import pandas as pd
import PySimpleGUI as sg
import webbrowser
import pyperclip

# Constant definition
VERSION = "0.1"
BUILD_DATE = "2022-05-06"
WEBSITE = "https://randomds.com"
REPO = "https://github.com/paluigi/csv2latex_gui"

sg.set_options(font="Default 16")


# Function definition
def make_main_window():
    layout = [
        [sg.Text("CSV File to Latex table")],
        [
            sg.Text("Version: {}".format(VERSION), font="_ 12"),
            sg.Text("Date: {}".format(BUILD_DATE), font="_ 12"),
        ],
        [sg.Button("Select CSV", key="-SELECT-")],
        [
            sg.Text(
                "Please select a CSV file", size=(40, 3), key="-FILENAME-", font="_ 12"
            )
        ],
        [
            sg.Button("Create table", key="-POPUP-"),
            sg.Button("Copy Table to clipboard", key="-CLIP-"),
        ],
        [
            sg.Frame(
                "Info links",
                [
                    [
                        sg.Text(
                            "RandomDataScience Website",
                            key="-RDS-",
                            enable_events=True,
                            font="_ 16 underline",
                        ),
                        sg.Text(
                            "GitHub Repo",
                            key="-GIT-",
                            enable_events=True,
                            font="_ 16 underline",
                        ),
                    ]
                ],
            )
        ],
        [
            sg.Button("Exit"),
        ],
    ]

    window = sg.Window(
        "CSV 2 Latex",
        layout,
    )
    return window


window = make_main_window()
filename = None

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == "-SELECT-":
        filename = sg.popup_get_file(
            "What is the CSV file?", "Filename", no_window=True
        )
        window["-FILENAME-"].update("Selected file:\n{}".format(filename))
    if event in ["-POPUP-", "-CLIP-"]:
        if filename is not None:
            try:
                df = pd.read_csv(filename)
                latex_table = df.to_latex(index=False)
                if event == "-POPUP-":
                    sg.popup_scrolled(latex_table, title="Latex Table", size=(50, 40))
                else:
                    pyperclip.copy(latex_table)
            except:
                sg.popup_error(
                    "Something went terribly wrong.\nTry with another file or open an issue on GitHub",
                    title="ERROR",
                )
        else:
            sg.popup_error("Please select a CSV file.", title="ERROR")
    if event == "-RDS-":
        webbrowser.open(WEBSITE)
    if event == "-GIT-":
        webbrowser.open(REPO)

window.close()
