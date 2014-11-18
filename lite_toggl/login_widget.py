from lite_toggl import toggl_api
import requests
from Tkinter import Button, Label, Entry, Frame, BOTH, LEFT, StringVar, NORMAL, DISABLED, X, W, END

class LoginWidget(Frame):

    def __init__(self, parent, config):
        Frame.__init__(self, parent)
        self.loggedIn = None
        self.config = config

        self.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.bind("<Return>", self.login)

        self.message = StringVar()
        l = Label(self, textvariable=self.message)
        l.pack()

        l = Label(self, text="Email:")
        l.pack(anchor=W, pady=(10, 0))

        self.email = StringVar()
        self.email.set(self.config.get("credentials", "email"))

        e = Entry(self, textvariable=self.email, width=40, font=("Helvetica", 16))
        e.pack(fill=X)
        e.focus_set()
        e.icursor(END)
        e.selection_range(0, END)

        l = Label(self, text="Password:", justify=LEFT)
        l.pack(anchor=W, pady=(10, 0))

        self.password = StringVar()
        self.password.set(self.config.get("credentials", "password"))

        e = Entry(self, show="*", textvariable=self.password, font=("Helvetica", 16))
        e.pack(fill=X)

        self.submit = Button(self, text="Login", command=self.login)
        self.submit.pack(ipady=10, pady=10, fill=X)

    def onLoggedIn(self, cb):
        self.loggedIn = cb

    def login(self):
        self.config.set("credentials", "email", self.email.get())
        self.config.set("credentials", "password", self.password.get())
        try:
            user = toggl_api.TogglUser(self.email.get(), self.password.get())
            user.fetchData()
            if self.onLoggedIn != None:
                self.loggedIn(user)
        except requests.exceptions.HTTPError:
            self.message = "Invalid credentials"

