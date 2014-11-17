from lite_toggl import toggl_api
import requests
from Tkinter import Button, Label, Entry, Frame, BOTH, LEFT, StringVar, NORMAL, DISABLED

class LoginWidget(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.loggedIn = None

        self.pack(fill=BOTH, expand=1)

        self.message = Label(self, text="")
        self.message.pack()

        l = Label(self, text="Email:")
        l.pack()

        self.email = StringVar()
        self.email.set(toggl_api.getAuth().email)

        e = Entry(self, textvariable=self.email, text="")
        e.pack()

        l = Label(self, text="Password:")
        l.pack()

        self.password = StringVar()
        e = Entry(self, show="*", textvariable=self.password, text="")
        e.pack()

        self.submit = Button(self, text="Login", command=self.login)
        self.submit.pack()

    def onLoggedIn(self, cb):
        self.loggedIn = cb

    def login(self):
        toggl_api.getAuth().setCredentials(self.email.get(), self.password.get())
        try:
            workspaces = toggl_api.workspaces()
            if self.onLoggedIn != None:
                self.loggedIn(workspaces)
        except requests.exceptions.HTTPError:
            self.message["text"] = "Invalid credentials"

