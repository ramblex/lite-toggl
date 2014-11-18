from Tkinter import BOTH
from ttk import Notebook

from lite_toggl.login_widget import LoginWidget
from lite_toggl.workspace_widget import WorkspaceWidget
from lite_toggl.idle_tracker import IdleChecker
from lite_toggl.app_config import AppConfig

class ApplicationWidget(Notebook):
    def __init__(self, parent, user):
        Notebook.__init__(self, parent)

        self.pack(fill=BOTH, expand=1)

        for wid, workspace in user.workspaces.iteritems():
            widget = WorkspaceWidget(self, workspace)
            self.add(widget, text=workspace.name)

        checkIdleThread = IdleChecker(user)
        checkIdleThread.start()

class MainWindow(object):
    def __init__(self, root):
        super(MainWindow, self).__init__()
        self.root = root
        self.root.title("Lite Toggl")

        self.config = AppConfig()

        self.loginWidget = LoginWidget(root, self.config)
        self.loginWidget.onLoggedIn(self.onLogin)

    def onLogin(self, user):
        self.loginWidget.pack_forget()
        self.loginWidget.destroy()
        ApplicationWidget(self.root, user)
