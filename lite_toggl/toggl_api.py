import requests
import json
import datetime

TOGGL_URL = "https://www.toggl.com/api/v8"

class TogglUser(object):
    def __init__(self, email, password):
        self._auth = (email, password)
        self.workspaces = {}

    def currentTimeEntry():
        resp = self.apiRequest("time_entries/current")
        if resp["data"] == None:
            return None
        else:
            return TogglTimeEntry(resp["data"], None)

    def fetchData(self):
        """Fetch user data from Toggl and put it into a hierarchicial
        structure"""

        resp = self.apiRequest("me?with_related_data=true")
        for workspace in resp["data"]["workspaces"]:
            self.workspaces[workspace["id"]] = TogglWorkspace(workspace, self)

        for data in resp["data"]["clients"]:
            workspace = self.workspaces[data["wid"]]
            workspace.addClient(data)

        for data in resp["data"]["projects"]:
            workspace = self.workspaces[data["wid"]]
            workspace.addProject(data)

        for data in resp["data"]["time_entries"]:
            workspace = self.workspaces[data["wid"]]
            workspace.addTimeEntry(data)

    def apiRequest(self, path, data=None, requestType="get"):
        url = "%s/%s" % (TOGGL_URL, path)
        resp = getattr(requests, requestType)(url, auth=self._auth, data=data)
        resp.raise_for_status()
        return json.loads(resp.text)

DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",
    # FIXME: This will break if times are not UTC!
    "%Y-%m-%dT%H:%M:%S+00:00"
]

def _parseDate(date):
    """Parse date string from Toggl

    Toggl haven't used the same date format in all of their messages so this
    function attempts to cope with that.
    """
    for dateFormat in DATE_FORMATS:
        try:
            date = datetime.datetime.strptime(date, dateFormat)
            return date
        except ValueError:
            pass

    return None

class TogglProject(object):
    def __init__(self, data, workspace, user):
        self._user = user
        self.workspace = workspace
        self.togglId = data["id"]
        self.name = data["name"]
        self._timeEntries = {}

    def timeEntries(self):
        return self._timeEntries

    def addTimeEntry(self, data):
        self._timeEntries[data["id"]] = TogglTimeEntry(data, self, self._user)

    def startTimeEntry(self, description):
        resp = self._user.apiRequest("time_entries/start",
                                     json.dumps({
                                         "time_entry": {
                                             "description": description,
                                             "pid": self.togglId,
                                             "created_with": "lite-toggl"
                                         }
                                     }),
                                     requestType="post")
        return TogglTimeEntry(resp["data"], self, self._user)

class TogglClient(object):
    def __init__(self, data, workspace, user):
        self._user = user
        self.workspace = workspace
        self.togglId = data["id"]
        self.name = data["name"]
        self._projects = {}

    def addProject(self, project):
        self._projects[project.togglId] = project

class TogglWorkspace(object):
    def __init__(self, data, user):
        self._user = user
        self._projects = {
            "noproject": TogglProject({"id": None, "name": None}, self, self._user)
        }
        self._clients = {
            "noclient": TogglClient({"id": None, "name": None}, self, self._user)
        }
        self.togglId = data["id"]
        self.name = data["name"]

    def addTimeEntry(self, data):
        if "pid" in data:
            project = self._projects[data["pid"]]
        else:
            project = self._projects["noproject"]

        project.addTimeEntry(data)

    def addClient(self, data):
        self._clients[data["id"]] = TogglClient(data, self, self._user)

    def addProject(self, data):
        if "cid" in data:
            client = self._clients[data["cid"]]
        else:
            client = self._clients["noclient"]

        project = TogglProject(data, self, self._user)
        self._projects[data["id"]] = project
        client.addProject(project)

    def clients(self):
        return self._clients

    def projects(self):
        return self._projects

    def timeEntries(self):
        entries = {}
        for project in self.projects().values():
            entries.update(project.timeEntries())
        return entries

class TogglTimeEntry(object):
    def __init__(self, data, project, user):
        self._user = user
        self.project = project
        self.data = data
        self.data["start"] = _parseDate(self.data["start"])

    def stop(self):
        return self._user.apiRequest("time_entries/%s/stop" % (self.data["id"]),
                           requestType="put")
