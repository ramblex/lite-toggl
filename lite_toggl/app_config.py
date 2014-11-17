import ConfigParser
import keyring
from os import path

CONFIG_FILE = path.expanduser("~/.litetoggl")

class AppConfig(ConfigParser.ConfigParser):
    """Config that stores the user's password in the keyring"""

    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)

        if not self.read(CONFIG_FILE):
            self._writeDefaultConfig()

    def get(self, section, name):
        if section == "credentials" and name == "password":
            return keyring.get_password("lite-toggl", "password")
        else:
            return ConfigParser.ConfigParser.get(self, section, name)

    def set(self, section, name, value):
        if section == "credentials" and name == "password":
            keyring.set_password("lite-toggl", "password", value)
        else:
            ConfigParser.ConfigParser.set(self, section, name, value)

        with open(CONFIG_FILE, "w") as cfgfile:
            self.write(cfgfile)

    def _writeDefaultConfig(self):
        self.add_section("credentials")
        self.set("credentials", "email", "<your email>")
