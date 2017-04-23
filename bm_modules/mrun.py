#!/usr/bin/env python
import os
import signal
import subprocess

import logger
import session_environment


def execute(config, args):
    """
    Runs the run module with thje specified args and 
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

    # Run the session.
    signal.signal(signal.SIGINT, sigint_handler)

    all_batches = session.get_batches()
    incomplete_batches = session.get_incomplete_batches()
    
    log.log(logger.INFO, "%d/%d batches remaining." % (len(incomplete_batches), len(all_batches)))
    for batch in incomplete_batches:
        command = session.configuration["command"]
        command_array = command.split(" ")

        batch_data = session.get_batch(batch)
        proc = subprocess.Popen(command_array, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=preexec)
        stdout_value, stderr_value = proc.communicate(batch_data)
        session.save_status(batch, stdout_value, stderr_value)
        log.log(logger.INFO, "Batch '%s' complete." % batch)

        global stop_running
        if stop_running:
            log.log(logger.INFO, "Quitting.")
            break

    return True

stop_running = False
def sigint_handler(signal, frame):
    global stop_running
    stop_running = True

def preexec():
    # Avoid sending interrupt signals to child.
    os.setpgrp()
