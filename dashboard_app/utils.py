from django.conf import settings
from configparser import ConfigParser
import os


class ConfigReader:
    def __init__(self):
        self.configPath = os.path.join(settings.BASE_DIR, "projectConfig.ini")
        self.cf = ConfigParser()
        self.cf.read(self.configPath)

    def get(self, section, key):
        return self.cf.get(section, key)
