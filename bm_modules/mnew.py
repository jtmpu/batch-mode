#!/usr/bin/env python

import sys
import time

import logger
import session_environment

def execute(config, args):
    """
    Runs the exec module with the given args and
    global configuration.
    For details of contents of config and args -
    see the batch-mode.py main file.
    - command
    - name
    - batch_size
    - force
    - read
    """
    env = session_environment.SessionEnvironment(config)
    log = logger.Logger(config)

    command = args["command"]
    command_list = command.split(" ")
    name = args["name"]
    batch_size = args["batch_size"]
    force = args["force"]
    read = args["read"]

    # The default format for a new session.
    if name == "":
        name = command_list[0] + "." + time.strftime("%Y-%m-%d")
        args["name"] = name
    
    # Tries to create the new session
    session = None
    if env.session_exists(name):
        log.log(logger.WARNING, "Session with that name already exists.")
        if force:
            log.log(logger.WARNING, "Deleting old session and forcing a new session.")
            env.delete_session(name)
            session = env.create_empty_session(name)
        else:
            log.log(logger.ERROR, "Not using '--force' flag, aborting.")
            return False
    else:
        log.log(logger.INFO, "Creating session '%s'." % name)
        session = env.create_empty_session(name)

    if session == None:
        log.log(logger.ERROR, "Failed to create new session.")
        return False

    session.create(config, args)

    # Generate the batches.
    jobstream = None
    if read == "":
        jobstream = sys.stdin
    else:
        jobstream = open(read, "r")

    session.generate_batches(jobstream)

    if read != "":
        jobstream.close()

    session.save()
    return True
