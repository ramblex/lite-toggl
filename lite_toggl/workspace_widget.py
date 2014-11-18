from Tkinter import Frame
from lite_toggl.time_entry_widget import TimeEntryWidget
from lite_toggl.time_entry_list_widget import TimeEntryListWidget

class WorkspaceWidget(Frame):
    def __init__(self, parent, workspace):
        Frame.__init__(self, parent)

        self.timeEntry = TimeEntryWidget(self, workspace.clients(), workspace.projects())
        self.timeEntry.pack(expand=True)

        self.timeEntryList = TimeEntryListWidget(self, workspace.timeEntries())
        self.timeEntryList.pack(expand=True)
