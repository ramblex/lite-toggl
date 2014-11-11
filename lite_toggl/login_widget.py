import toggl_api
import requests
from PySide import QtGui, QtCore

class LoginWidget(QtGui.QWidget):

    loggedIn = QtCore.Signal(list)

    def __init__(self, parent):
        super(LoginWidget, self).__init__(parent)
        self.parent = parent

        layout = QtGui.QVBoxLayout()

        self.message = QtGui.QLabel("")
        layout.addWidget(self.message)

        layout.addWidget(QtGui.QLabel("Email:"))
        self.email = QtGui.QLineEdit(toggl_api.getEmail())
        layout.addWidget(self.email)

        layout.addWidget(QtGui.QLabel("Password:"))
        self.password = QtGui.QLineEdit()
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        layout.addWidget(self.password)

        self.submit = QtGui.QPushButton("Login")
        self.submit.clicked.connect(self.login)
        layout.addWidget(self.submit)

        self.password.returnPressed.connect(self.submit.clicked)

        self.setLayout(layout)

    def login(self):
        self.submit.setText("Logging in...")
        self.submit.setEnabled(False)

        QtGui.qApp.processEvents()

        toggl_api.setAuth(self.email.text(), self.password.text())
        try:
            workspaces = toggl_api.workspaces()
            self.loggedIn.emit(workspaces)
        except requests.exceptions.HTTPError:
            self.message.setText("Invalid credentials")
            self.submit.setEnabled(True)
            self.submit.setText("Login")

