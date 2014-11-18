from Tkinter import Frame, LEFT, BOTH, END, Button, Label, StringVar, Entry, OptionMenu, Listbox, W
from ttk import Combobox
import datetime
import time
from lite_toggl import toggl_api

class TimeEntryWidget(Frame):
    """Widget to handle starting and stopping the current time entry"""

    def __init__(self, parent, clients, projects):
        Frame.__init__(self, parent)

        self.projects = projects.values()
        self.projects.sort(key=lambda x: x.name)

        self.clients = clients.values()
        self.clients.sort(key=lambda x: x.name)

        l = Label(self, text="Description")
        l.grid(row=0, column=0)

        self.description = StringVar()
        e = Entry(self, textvariable=self.description)
        e.grid(row=1, column=0)

        l = Label(self, text="Client")
        l.grid(row=0, column=1)

        values = map(lambda x: x.name, self.clients)
        self.clientChooser = Combobox(self, values=values)
        self.clientChooser.grid(row=1, column=1)

        l = Label(self, text="Project")
        l.grid(row=0, column=2)

        values = map(lambda x: x.name, self.projects)
        self.projectChooser = Combobox(self, values=values)
        self.projectChooser.grid(row=1, column=2)

        self.timeEntryClock = TimeEntryClock(self)
        self.timeEntryClock.grid(row=1, column=3)

        self.submitText = StringVar()
        self.submitText.set("Start")
        self.submit = Button(self, textvariable=self.submitText, command=self.start)
        self.submit.grid(row=1, column=4)

    def start(self):
        self.submitText.set("Stop")
        self.submit["command"] = self.stop
        project = self.selectedProject()
        entry = project.startTimeEntry(self.description.get())
        self.timeEntryClock.setTimeEntry(entry)

    def stop(self):
        self.submitText.set("Start")
        self.submit["command"] = self.start
        self.timeEntryClock.stop()

    def selectedProject(self):
        return self.projects[self.projectChooser.current()]

class TimeEntryClock(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.time = "00:00:00"
        l = Label(self, textvariable=self.time)
        l.pack()
        self.timeEntry = None
        self.job = None

    def setTimeEntry(self, timeEntry):
        self.timeEntry = timeEntry
        self._tick()
        self.job = self.after(1000, self._tick)

    def stop(self):
        self.time = ""
        self.timeEntry.stop()
        self.after_cancel(self.job)

    def _tick(self):
        print "TICK"
        duration = datetime.datetime.now() - self.timeEntry.start
        self.time = time.strftime("%H:%M:%S", time.gmtime(duration.seconds))
