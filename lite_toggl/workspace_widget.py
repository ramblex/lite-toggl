from Tkinter import Frame
from lite_toggl.time_entry_widget import TimeEntryWidget
from lite_toggl.time_entry_list_widget import TimeEntryListWidget

class WorkspaceWidget(Frame):
    def __init__(self, parent, workspace):
        Frame.__init__(self, parent)

        self.timeEntryList = TimeEntryListWidget(self, workspace.timeEntries())
        self.timeEntry = TimeEntryWidget(self, workspace.projects(),
                                         onCreation=self.timeEntryList.insertTimeEntry)

        self.timeEntry.pack(expand=True, pady=10)
        self.timeEntryList.pack(expand=True)

