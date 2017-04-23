#!/usr/bin/env python

import os
import argparse

import bm_modules.mstat
import bm_modules.mexec

def execute(args):
    """
    Runs the specified module of batch-mode. 
    NOTE: No error check on args - see parse_cli_args for expected
    values if running this from another script.
    """
    config = {}
    config["working_directory"] = os.path.expanduser("~/.batch-mode")

    if args["module"] == "stat":
        bm_modules.mstat.execute(config, args)
    elif args["module"] == "exec":
        bm_modules.mexec.execute(config, args)

    
    return True

def parse_cli_args():
    """
    Batch-Mode supports two different modules.
    - stat - gets output, statuses or configuration details of a session
    - exec - creates/run a session
    """ 
    parser = argparse.ArgumentParser()

    # Global arguments
    parser.add_argument("-v", "--verbose", help="Show status output for batch-mode.", default=False, action="store_true")

    subparsers = parser.add_subparsers(dest="module", help="The support submodules.")
    stat_parser = subparsers.add_parser("stat", help="Shows details about existing sessions.\n")
    exec_parser = subparsers.add_parser("exec", help="Creates or runs new sessions.")

    # Stat arguments
    stat_parser.add_argument("-s", "--session", help="The session specifier. If no other args are use this will print the output of the session.", default="") 
    stat_parser.add_argument("-r", "--resume", help="Resume the specified session.", default=False, action="store_true")
    stat_parser.add_argument("-c", "--configuration", help="Print the configuration for the specified session.", default=False, action="store_true")

    # Exec arguments
    exec_parser.add_argument("-c", "--command", help="The command to execute.", default="")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = vars(parse_cli_args())
    print(args)
    execute(args)
