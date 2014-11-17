from lite_toggl import toggl_api
import requests
from Tkinter import Button, Label, Entry, Frame, BOTH, LEFT, StringVar, NORMAL, DISABLED

class LoginWidget(Frame):

    def __init__(self, parent, config):
        Frame.__init__(self, parent)
        self.loggedIn = None
        self.config = config

        self.pack(fill=BOTH, expand=1)

        self.message = StringVar()
        l = Label(self, textvariable=self.message)
        l.pack()

        l = Label(self, text="Email:")
        l.pack()

        self.email = StringVar()
        self.email.set(self.config.get("credentials", "email"))

        e = Entry(self, textvariable=self.email)
        e.pack()

        l = Label(self, text="Password:")
        l.pack()

        self.password = StringVar()
        self.password.set(self.config.get("credentials", "password"))

        e = Entry(self, show="*", textvariable=self.password)
        e.pack()

        self.submit = Button(self, text="Login", command=self.login)
        self.submit.pack()

    def onLoggedIn(self, cb):
        self.loggedIn = cb

    def login(self):
        toggl_api.getAuth().setCredentials(self.email.get(), self.password.get())
        self.config.set("credentials", "email", self.email.get())
        self.config.set("credentials", "password", self.password.get())
        try:
            workspaces = toggl_api.workspaces()
            if self.onLoggedIn != None:
                self.loggedIn(workspaces)
        except requests.exceptions.HTTPError:
            self.message = "Invalid credentials"

