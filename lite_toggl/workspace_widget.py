from Tkinter import Frame, LEFT, BOTH, END, Button, Label, StringVar, Entry, OptionMenu, Listbox
from ttk import Combobox
import datetime
import time
from lite_toggl import toggl_api

class WorkspaceWidget(Frame):
    def __init__(self, parent, workspace):
        Frame.__init__(self, parent)

        self.taskbar = TaskBar(self, workspace.projects())
        self.taskbar.pack()

class TimeEntryCreator(Frame):
    def __init__(self, parent, projects):
        Frame.__init__(self, parent)

        self.projects = projects

        self.description = StringVar()
        e = Entry(self, text="Description", textvariable=self.description)
        e.pack(side=LEFT)

        values = map(lambda x: x.name, self.projects)
        self.projectChooser = Combobox(parent, values=values)
        self.projectChooser.current(0)
        self.projectChooser.pack(side=LEFT)

    def getDescription(self):
        return self.description.get()

    def selectedProject(self):
        return self.projects[self.projectChooser.current()]

class TimeEntryClock(Label):
    def __init__(self, parent):
        self.time = ""
        Label.__init__(self, textvariable=self.time)
        self.timeEntry = None
        self.job = None

    def setTimeEntry(self, timeEntry):
        self.timeEntry = timeEntry
        self._tick()
        self.job = self.after(1000, self._tick)

    def stop(self):
        self.time = ""
        self.timeEntry.stop()
        self.job.after_cancel()

    def _tick(self):
        duration = datetime.datetime.now() - self.timeEntry.start
        self.time = time.strftime("%H:%M:%S", time.gmtime(duration.seconds))

class TaskBar(Frame):
    def __init__(self, parent, projects):
        Frame.__init__(self, parent)

        projects.sort(key=lambda x: x.name)

        self.timeEntryCreator = TimeEntryCreator(self, projects)
        self.timeEntryCreator.pack(side=LEFT)

        self.taskControlButton = Button(self, text="Start", command=self.start)
        self.taskControlButton.pack(side=LEFT)

        self.timeEntryClock = TimeEntryClock(self)
        self.timeEntryClock.pack(side=LEFT)

        # Show the currently running time entry if there is one
        currentTimeEntry = toggl_api.currentTimeEntry()
        if currentTimeEntry:
            self._onTimeEntryStart(currentTimeEntry)

    def _onTimeEntryStart(self, entry):
        pass

    def start(self):
        project = self.timeEntryCreator.selectedProject()
        entry = project.startTimeEntry(self.timeEntryCreator.getDescription())
        self._onTimeEntryStart(entry)

    def stop(self):
        pass
