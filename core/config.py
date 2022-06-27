import sys
from dotenv import dotenv_values

from vault_lib.core.file import LocalFile
from vault_lib.server.server import VAULTServer, LocalVAULTServer

class Config(LocalFile):
    def __init__(self, config_file="{}/.env".format(sys.path[0])):
        super(Config, self).__init__(config_file)

        self._values = dotenv_values(config_file)

        self.mongo_ip = None
        self.mongo_port = None

        self.plex_ip = None
        self.plex_port = None
        self.plex_token = None

        self.rest_ip = None
        self.rest_port = None

        self._build_config()
    
    def _build_config(self):
        for key in self._values:
            value = self._values[key]

            key = key.lower()

            if hasattr(self, key):
                setattr(self, key, value)

    def get_connection(self, direct=False):
        if direct is False:
            if (self.rest_ip is not None and self.rest_port is not None):
                return VAULTServer(self.rest_ip, int(self.rest_port))
        else:
            if (self.mongo_ip and self.mongo_port):
                if (self.plex_ip and self.plex_port and self.plex_token):
                    server = LocalVAULTServer(self.mongo_ip, int(self.mongo_port), self.plex_ip, int(self.plex_port), self.plex_token)
                    server.connect()
                    return server

    def print_config(self):
        print("==> Config File")
        print("Config File Path: ", self.path)
        print("VAULT Rest: {i}:{p}".format(i=self.rest_ip, p=self.rest_port))
        print("Mongo DB: {i}:{p}".format(i=self.mongo_ip, p=self.mongo_port))
        print("Plex: {i}:{p}/{t}".format(i=self.plex_ip, p=self.plex_port, t=self.plex_token))
    