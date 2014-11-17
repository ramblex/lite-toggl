import ctypes
import os
import time
import threading
from lite_toggl import toggl_api

IDLE_TIMEOUT = 5 * 60 # Seconds

class XScreenSaverInfo(ctypes.Structure):
    """ typedef struct { ... } XScreenSaverInfo; """
    _fields_ = [('window',      ctypes.c_ulong), # screen saver window
                ('state',       ctypes.c_int),   # off,on,disabled
                ('kind',        ctypes.c_int),   # blanked,internal,external
                ('since',       ctypes.c_ulong), # milliseconds
                ('idle',        ctypes.c_ulong), # milliseconds
                ('event_mask',  ctypes.c_ulong)] # events

class IdleChecker(threading.Thread):
    """Monitors whether the user is idle"""

    def __init__(self, workspaces):
        super(IdleChecker, self).__init__()
        self.workspaces = workspaces
        self.daemon = True

        self.xlib = ctypes.cdll.LoadLibrary('libX11.so.6')
        self.display = self.xlib.XOpenDisplay(os.environ['DISPLAY'])
        self.xss = ctypes.cdll.LoadLibrary('libXss.so.1')
        self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
        self.xssinfo = self.xss.XScreenSaverAllocInfo()

    def getIdleTime(self):
        """Get user idle time in ms"""
        self.xss.XScreenSaverQueryInfo(self.display,
                                       self.xlib.XDefaultRootWindow(self.display),
                                       self.xssinfo)
        return self.xssinfo.contents.idle

    def run(self):
        while True:
            idleTime = self.getIdleTime() / 1000
            if idleTime >= IDLE_TIMEOUT and toggl_api.currentTimeEntry():
                print "Why you no work?"
            time.sleep(IDLE_TIMEOUT)
