"""Spikely - an application built on top of SpikeInterface to create and run
extracellular data processing pipelines

The application is designed to allow users to load an extracellular recording,
run preprocessing on the recording, run an installed spike sorter, and then perform
postprocessing on the results. All results are saved into a folder.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tk_filedialog

# Initialize Tk
root = tk.Tk()

# Tk magic globals to dynamically get/set widget text
recording_selection = tk.StringVar()
filter_selections = [tk.StringVar()]
sorter_selection = tk.StringVar()

# First UI rows for recording, filter, and sorter segments
RECORDING_ROW = 0
FILTER_ROW = 1
SORTER_ROW = 19  # Leaves room for multiple filters


# UI Construction Routines

def insert_segment_ui(row, prompt, select_cb, selection, settings_cb,
                      append_cb):
    """ Place a segment (recording, filter, sorter) row in the main window of
    the application
    """

    # Segments have the option to append subsegments - enables multiple filters
    if append_cb is not None:
        w = ttk.Button(mainframe, text="+", command=append_cb,
                       width=1)
        w.grid(column=0, row=row, padx=5, pady=5)

    w = ttk.Label(mainframe, text=prompt, foreground="green")
    w.grid(column=1, row=row, sticky=tk.E, padx=5, pady=5)

    w = ttk.Button(mainframe, text="Select", command=select_cb)
    w.grid(column=2, row=row, sticky=tk.W, padx=5, pady=5)

    w = ttk.Label(mainframe, textvariable=selection)
    w.grid(column=3, row=row, sticky=tk.W, padx=5, pady=5)

    w = ttk.Button(mainframe, text="Settings", command=settings_cb)
    w.grid(column=4, row=row, sticky=tk.W, padx=5, pady=5)


# Recording specific callbacks for Select and Settings
def recording_select():
    # Open dialog to select source file for sort transformation
    recording_selection.set(tk_filedialog.askopenfilename())


def recording_settings():
    pass


# Filter specific callbacks for Select and Settings, and Append
def filter_select():
    pass


def filter_settings():
    pass


def filter_append():
    next_FILTER_ROW = FILTER_ROW + len(filter_selections)
    filter_selections.append(tk.StringVar())
    filter_selections[-1].set("<No Filter selected>")
    insert_segment_ui(row=next_FILTER_ROW, prompt="",
                      select_cb=filter_select,
                      selection=filter_selections[-1],
                      settings_cb=filter_settings, append_cb=None)


# Sorter specific callbacks for Select and Settings, and Append
def sorter_select():
    pass


def sorter_settings():
    pass


root.title("Spikely 1.0")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

recording_selection.set("<No Recording File Selected>")
insert_segment_ui(row=RECORDING_ROW, prompt="Recording",
                  select_cb=recording_select, selection=recording_selection,
                  settings_cb=recording_settings, append_cb=None)

filter_selections[0].set("<No Filter selected>")
insert_segment_ui(row=FILTER_ROW, prompt="Filter(s)",
                  select_cb=filter_select, selection=filter_selections[0],
                  settings_cb=filter_settings, append_cb=filter_append)

sorter_selection.set("<No Sorter selected>")
insert_segment_ui(row=SORTER_ROW, prompt="Sorter", select_cb=sorter_select,
                  selection=sorter_selection, settings_cb=sorter_settings,
                  append_cb=None)

w = ttk.Separator(mainframe)
w.grid(column=0, columnspan=5, row=SORTER_ROW+1, sticky=(tk.N, tk.W, tk.E),
       padx=5, pady=5)

w = ttk.Button(mainframe, text="Run", command=None)
w.grid(column=2, columnspan=2, row=21, sticky=(tk.N, tk.W, tk.E, tk.S),
       padx=5, pady=5)

w = ttk.Button(mainframe, text="Clear", command=None)
w.grid(column=4, row=SORTER_ROW+2, sticky=(tk.N, tk.W, tk.E, tk.S),
       padx=5, pady=5)

# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# Create a menu bar and associate it with main window
mbar = tk.Menu(root)
root.config(menu=mbar)
root.resizable(False, False)

# Create a menu and associate it with menu bar
filemenu = tk.Menu(mbar, tearoff=0)
mbar.add_cascade(label="File", menu=filemenu)

# create entries in the menu for commands
filemenu.add_command(label="Save Pipeline", command=None)
filemenu.add_command(label="Load Pipeline", command=None)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# Enter the event loop of the application
root.mainloop()
