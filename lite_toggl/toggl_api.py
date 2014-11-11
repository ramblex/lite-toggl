import requests
import json
import datetime

TOGGL_URL = "https://www.toggl.com/api/v8"
AUTH = ('', '')

def getEmail():
    return AUTH[0]

def setAuth(email, password):
    global AUTH
    AUTH = (email, password)

def _apiRequest(path, data=None, requestType="get"):
    url = "%s/%s" % (TOGGL_URL, path)
    resp = getattr(requests, requestType)(url, auth=AUTH, data=data)
    resp.raise_for_status()
    return json.loads(resp.text)

def workspaces():
    return [TogglWorkspace(w) for w in _apiRequest("workspaces")]

class TogglProject(object):
    def __init__(self, data, workspace):
        self.workspace = workspace
        self.id = data["id"]
        self.name = data["name"]

    def startTimeEntry(self, description):
        resp = _apiRequest("time_entries/start",
                           json.dumps({
                               "time_entry": {
                                   "description": description,
                                   "pid": self.id,
                                   "created_with": "lite-toggl"
                               }
                           }),
                           requestType="post")
        return TogglTimeEntry(resp["data"], self)

class TogglWorkspace(object):
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]

    def projects(self):
        resp = _apiRequest("workspaces/%s/projects" % (self.id))
        if resp == None:
            return []
        return [TogglProject(project, self) for project in resp]

class TogglTimeEntry(object):
    def __init__(self, data, project):
        self.project = project
        self.id = data["id"]
        self.start = datetime.datetime.strptime(data["start"], "%Y-%m-%dT%H:%M:%SZ")

    def stop(self):
        return _apiRequest("time_entries/%s/stop" % (self.id),
                           requestType="put")
