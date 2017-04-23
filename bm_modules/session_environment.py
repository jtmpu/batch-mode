#!/usr/bin/env python
import os
import shutil

import session

class SessionEnvironment:

    def __init__(self, config):
        self.basepath = config["working_directory"] 
        self.sessiondir_prefix = config["sessiondir_prefix"]
        self.init()

    def init(self):
        """
        Checks that the session environment is setup, otherwise create it.
        """
        if not os.path.isdir(self.basepath):
            os.makedirs(self.basepath)

    def get_session(self, name):
        if self.session_exists(name):
            s = session.Session(self.get_session_path(name))
            return s
        else:
            return None

    def list_sessions(self):
        nodes = os.listdir(self.basepath) 
        nodes = filter(lambda x: os.path.isdir(self.basepath + "/" + x), nodes)
        nodes = filter(lambda x: x.startswith(self.sessiondir_prefix), nodes)
        nodes = map(lambda x: x[len(self.sessiondir_prefix):], nodes)
        return nodes

    def session_exists(self, name):
        sessions = self.list_sessions()
        return name in sessions 

    def create_empty_session(self, name):
        p = self.get_session_path(name)
        if not os.path.isdir(p):
            os.makedirs(p)
            s = session.Session(p)
            return s
        else:
            return None

    def delete_session(self, name):
        p = self.get_session_path(name)
        if os.path.isdir(p):
            shutil.rmtree(p) 
            return True
        else:
            return False

    def get_session_path(self, name):
        return self.basepath + "/" + self.get_session_dirname(name)
    
    def get_session_dirname(self, name):
        return self.sessiondir_prefix + name
