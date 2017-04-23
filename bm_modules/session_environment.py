#!/usr/bin/env python
import os

class SessionEnvironment:

    def __init__(self, config):
        self.basepath = config["working_directory"] 
        self.init()

    def init(self):
        """
        Checks that the session environment is setup, otherwise create it.
        """
        if not os.path.isdir(self.basepath):
            os.makedirs(self.basepath)

    def list_sessions(self):
        return [ "1", "w" ]
