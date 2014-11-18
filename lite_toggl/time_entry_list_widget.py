from Tkinter import Frame, Label
from ttk import Treeview
import time

class TimeEntryListWidget(Treeview):

    def __init__(self, parent, timeEntries):
        columns = ("project", "start", "stop", "duration")
        Treeview.__init__(self, parent, columns=columns)

        for col in columns:
            self.heading(col, text=col, command=lambda: self.sort_column(col, False))

        [self.insertTimeEntry(e) for e in timeEntries.values()]

        self.sort_column("start", True)

    def insertTimeEntry(self, e):
        duration = time.strftime("%H:%M:%S", time.gmtime(int(e.duration)))
        if e.description == None:
            text = "(no description)"
        else:
            text = e.description
        self.insert('', 'end', text=text,
                    values=(e.project.name, e.start, e.stop, duration))

    def sort_column(self, col, reverse):
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.move(k, '', index)

        # reverse sort next time
        self.heading(col, command=lambda: \
                   self.sort_column(col, not reverse))
