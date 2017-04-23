#!/usr/bin/env python

import logger
import session_environment

def execute(config, args):
    """
    Runs the stat module with then specified args and 
    global configuration. 
    For details of contents of config and args -
    see the batch-mode.py main file.
    """
    env = session_environment.SessionEnvironment(config)
    log = logger.Logger(config)

    session_name = args["session"]
    if session_name == "":
        log.log(logger.INFO, "No session specified.")
        print("Existing sessions: ")
        sessions = env.list_sessions()
        for session in sessions:
            print(session)
        return False
    else:
        session = env.get_session(session_name)
        if session == None:
            log.log(logger.ERROR, "Failed to load session '%s'" % session_name)
            return False
    
    configuration = args["configuration"]
    stdout = args["stdout"]
    stderr = args["stderr"]
    batches = args["batches"]

    if configuration:
        print("TODO")

    if stderr:
        data = session.get_stderr()
        print(data)

    if stdout:
        data = session.get_stdout()
        print(data)

    if batches:
        all_batches = session.get_batches()
        incomplete_batches = session.get_incomplete_batches()
        print("%d/%d batches remaining." % (len(incomplete_batches), len(all_batches)))
        
    

    return True
