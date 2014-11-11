from PySide import QtGui, QtCore
import datetime
import time

class WorkspaceWidget(QtGui.QWidget):
    def __init__(self, parent, workspace):
        super(WorkspaceWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        taskbar = TaskBar(self, workspace.projects())
        layout.addWidget(taskbar)
        self.setLayout(layout)

class TimeEntryCreator(QtGui.QWidget):
    def __init__(self, parent, projects):
        super(TimeEntryCreator, self).__init__(parent)

        self.projects = projects

        layout = QtGui.QHBoxLayout(self)

        self.description = QtGui.QLineEdit(self)
        self.description.setPlaceholderText("Description")
        layout.addWidget(self.description)

        self.projectChooser = QtGui.QComboBox(self)
        for project in self.projects:
            self.projectChooser.addItem(project.name)
        layout.addWidget(self.projectChooser)

        self.setLayout(layout)

    def getDescription(self):
        return self.description.text()

    def selectedProject(self):
        return self.projects[self.projectChooser.currentIndex()]

class TimeEntryMonitor(QtGui.QLCDNumber):
    def __init__(self, parent):
        super(TimeEntryMonitor, self).__init__(parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._tick)

    def setTimeEntry(self, timeEntry):
        self.timeEntry = timeEntry
        self.timer.start(1000)

    def stop(self):
        self.timeEntry.stop()
        self.timer.stop()

    def _tick(self):
        duration = datetime.datetime.now() - self.timeEntry.start
        self.display(time.strftime("%H:%M:%S", time.gmtime(duration.seconds)))

class TaskBar(QtGui.QWidget):
    def __init__(self, parent, projects):
        super(TaskBar, self).__init__(parent)
        self.currentTimeEntry = None

        projects.sort(key=lambda x: x.name)
        layout = QtGui.QHBoxLayout(self)

        self.setFont(QtGui.QFont("Ubuntu Sans", 16))

        self.timeEntryCreator = TimeEntryCreator(self, projects)
        layout.addWidget(self.timeEntryCreator)

        self.timeEntryMonitor = TimeEntryMonitor(self)
        self.timeEntryMonitor.setVisible(False)
        layout.addWidget(self.timeEntryMonitor)

        self.taskControlButton = QtGui.QPushButton("Start")
        self.taskControlButton.clicked.connect(self.start)
        layout.addWidget(self.taskControlButton)

        self.setLayout(layout)

    def start(self):
        project = self.timeEntryCreator.selectedProject()
        entry = project.startTimeEntry(self.timeEntryCreator.getDescription())

        self.timeEntryCreator.setEnabled(False)

        self.timeEntryMonitor.setTimeEntry(entry)
        self.timeEntryMonitor.setVisible(True)

        self.taskControlButton.setText("Stop")
        self.taskControlButton.clicked.disconnect()
        self.taskControlButton.clicked.connect(self.stop)

    def stop(self):
        self.timeEntryMonitor.stop()
        self.timeEntryMonitor.setVisible(False)
        self.timeEntryCreator.setEnabled(True)

        self.taskControlButton.setText("Start")
        self.taskControlButton.clicked.disconnect()
        self.taskControlButton.clicked.connect(self.start)
