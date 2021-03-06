from Tkinter import Frame, LEFT, BOTH, END, Button, Label, StringVar, Entry, OptionMenu, Listbox, W
from ttk import Combobox
import datetime
import time
from lite_toggl import toggl_api

class TimeEntryWidget(Frame):
    """Widget to handle starting and stopping the current time entry"""

    def __init__(self, parent, projects, onCreation=None):
        Frame.__init__(self, parent)

        self.onCreation = onCreation

        self.time = StringVar()
        self.time.set("00:00:00")
        self.timeEntry = None

        self.projects = projects.values()
        self.projects.sort(key=lambda x: x.name)

        l = Label(self, text="Description")
        l.grid(row=0, column=0)

        self.description = StringVar()
        e = Entry(self, textvariable=self.description, font=("Helvetica", 16))
        e.grid(row=1, column=0)

        l = Label(self, text="Project")
        l.grid(row=0, column=1)

        values = map(lambda x: x.name, self.projects)
        self.projectChooser = Combobox(self, values=values, font=("Helvetica", 16))
        self.projectChooser.grid(row=1, column=1)

        self.timeEntryClock = Label(self, textvariable=self.time, font=("Helvetica", 16))
        self.timeEntryClock.grid(row=1, column=2)

        self.submitText = StringVar()
        self.submitText.set("Start")
        self.submit = Button(self, textvariable=self.submitText, command=self.start, font=("Helvetica", 16))
        self.submit.grid(row=1, column=3, padx=10)

    def selectedProject(self):
        return self.projects[self.projectChooser.current()]

    def start(self):
        self.submitText.set("Stop")
        self.submit["command"] = self.stop
        project = self.selectedProject()
        self.timeEntry = project.startTimeEntry(self.description.get())
        self.onCreation(self.timeEntry)
        self._tick()

    def stop(self):
        self.submitText.set("Start")
        self.submit["command"] = self.start
        self.timeEntry.stop()
        self.timeEntry = None
        self.description.set("")

    def _tick(self):
        if self.timeEntry:
            duration = datetime.datetime.now() - self.timeEntry.data["start"]
            self.time.set(time.strftime("%H:%M:%S", time.gmtime(duration.seconds)))
            self.after(1000, self._tick)
        else:
            self.time.set("00:00:00")
