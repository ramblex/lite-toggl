import requests
import json
import datetime

TOGGL_URL = "https://www.toggl.com/api/v8"
AUTH = ('', '')

DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S+00:00"
]

def getEmail():
    return AUTH[0]

def setAuth(email, password):
    global AUTH
    AUTH = (email, password)

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

def _apiRequest(path, data=None, requestType="get"):
    url = "%s/%s" % (TOGGL_URL, path)
    resp = getattr(requests, requestType)(url, auth=AUTH, data=data)
    resp.raise_for_status()
    return json.loads(resp.text)

def currentTimeEntry():
    resp = _apiRequest("time_entries/current")
    if resp["data"] == None:
        return None
    else:
        return TogglTimeEntry(resp["data"], None)

def workspaces():
    return [TogglWorkspace(w) for w in _apiRequest("workspaces")]

class TogglProject(object):
    def __init__(self, data, workspace):
        self.workspace = workspace
        self.togglId = data["id"]
        self.name = data["name"]

    def startTimeEntry(self, description):
        resp = _apiRequest("time_entries/start",
                           json.dumps({
                               "time_entry": {
                                   "description": description,
                                   "pid": self.togglId,
                                   "created_with": "lite-toggl"
                               }
                           }),
                           requestType="post")
        return TogglTimeEntry(resp["data"], self)

class TogglWorkspace(object):
    def __init__(self, data):
        self.togglId = data["id"]
        self.name = data["name"]

    def projects(self):
        resp = _apiRequest("workspaces/%s/projects" % (self.togglId))
        if resp == None:
            return []
        return [TogglProject(project, self) for project in resp]

class TogglTimeEntry(object):
    def __init__(self, data, project):
        self.project = project
        self.togglId = data["id"]
        self.start = _parseDate(data["start"])

    def stop(self):
        return _apiRequest("time_entries/%s/stop" % (self.togglId),
                           requestType="put")
