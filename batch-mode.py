#!/usr/bin/env python
import os
import argparse

import bm_modules.msession
import bm_modules.mnew
import bm_modules.mrun

def execute(args):
    """
    Runs the specified module of batch-mode. 
    NOTE: No error check on args - see parse_cli_args for expected
    values if running this from another script.
    """
    config = {}
    config["working_directory"] = os.path.expanduser("~/.batch-mode")
    config["verbose"] = args["verbose"]
    config["sessiondir_prefix"] = "bmsession."
    config["session_stdout_file"] = "stdout.dat"
    config["session_stderr_file"] = "stderr.dat"
    config["session_status_file"] = "status.dat"

    if args["module"] == "session":
        bm_modules.msession.execute(config, args)
    elif args["module"] == "new":
        # Create it.
        success = bm_modules.mnew.execute(config, args)
        # Run it.
        if success:
            run_args = {}
            run_args["session"] = args["name"]
            bm_modules.mrun.execute(config, run_args)
    elif args["module"] == "run":
        bm_modules.mrun.execute(config, args)
    
    return True

def parse_cli_args():
    """
    Batch-Mode supports two different modules.
    - session - gets output, statuses or configuration details of a session
    - new - creates a session
    - run - runs a session
    """ 
    parser = argparse.ArgumentParser()

    # Global arguments
    parser.add_argument("-v", "--verbose", help="Show status output for batch-mode.", default=False, action="store_true")

    subparsers = parser.add_subparsers(dest="module", help="The support submodules.")
    session_parser = subparsers.add_parser("session", help="Shows details about existing sessions.\n")
    new_parser = subparsers.add_parser("new", help="Creates or runs new sessions.")
    run_parser = subparsers.add_parser("run", help="Runs a session.")

    # Run arguments
    run_parser.add_argument("-s", "--session", help="Run the specified session.", default="")
    run_parser.add_argument("-v", "--verbose", help="Show status output for batch-mode.", default=False, action="store_true")

    # session arguments
    session_parser.add_argument("-s", "--session", help="The session specifier. If no other args are use this will print the output of the session.", default="") 
    session_parser.add_argument("-c", "--configuration", help="Print the configuration for the specified session.", default=False, action="store_true")
    session_parser.add_argument("-e", "--stderr", help="Print the stderr for the session.", default=False, action="store_true")
    session_parser.add_argument("-o", "--stdout", help="Print the stdout for the session.", default=False, action="store_true")
    session_parser.add_argument("-b", "--batches", help="Print the batch-information for the session.", default=False, action="store_true")
    session_parser.add_argument("-v", "--verbose", help="Show status output for batch-mode.", default=False, action="store_true")

    # new arguments
    new_parser.add_argument("-c", "--command", help="The command to execute.", required=True)
    new_parser.add_argument("-n", "--name", help="The name of the new session. If nothing specified, defaults to 'yyyy-mm-dd.<cmd>'", default="")
    new_parser.add_argument("-b", "--batch_size", help="The number of jobs per batch.", default=100, type=int)
    new_parser.add_argument("-f", "--force", help="If this already exists, this flag forces the removal of the old and the creation of the new.", default=False, action="store_true")
    new_parser.add_argument("-r", "--read", help="Read jobs from the specified file. (If nothing specified, reads from STDIN.", default="")
    new_parser.add_argument("-v", "--verbose", help="Show status output for batch-mode.", default=False, action="store_true")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = vars(parse_cli_args())
    execute(args)
