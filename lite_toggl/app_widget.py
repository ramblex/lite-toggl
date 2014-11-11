from PySide import QtGui

from lite_toggl.login_widget import LoginWidget
from lite_toggl.workspace_widget import WorkspaceWidget

class ApplicationWidget(QtGui.QWidget):
    def __init__(self, parent, workspaces):
        super(ApplicationWidget, self).__init__(parent)

        tabs = QtGui.QTabWidget(self)
        for workspace in workspaces:
            widget = WorkspaceWidget(self, workspace)
            tabs.addTab(widget, workspace.name)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(tabs)

        self.setLayout(layout)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.loginWidget = LoginWidget(self)
        self.loginWidget.loggedIn.connect(self.onLogin)

        self.setCentralWidget(self.loginWidget)
        self.setWindowTitle("Toggl")
        self.show()

    def onLogin(self, workspaces):
        appWidget = ApplicationWidget(self, workspaces)
        self.setCentralWidget(appWidget)
        self.resize(600, 50)
