from Tkinter import Frame
from lite_toggl.time_entry_widget import TimeEntryWidget

class WorkspaceWidget(Frame):
    def __init__(self, parent, workspace):
        Frame.__init__(self, parent)

        self.timeEntry = TimeEntryWidget(self, workspace.projects())
        self.timeEntry.pack()
