#!/usr/bin/env python

import session_environment

def execute(config, args):
    """
    Runs the stat module with then specified args and 
    global configuration. 
    For details of contents of config and args -
    see the batch-mode.py main file.
    """
    print("stat")
    env = session_environment.SessionEnvironment(config)

    return True
