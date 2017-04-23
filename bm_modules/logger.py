#!/usr/bin/env python

INFO=1
DEBUG=2
WARNING=3
ERROR=4

class Logger: 
    
    def __init__(self, config):
        self.verbose = config["verbose"]

    def log(self, level, msg):
        if self.verbose:
            if level == INFO:
                print("[+] %s" % msg)
            elif level == DEBUG:
                print("[?] %s" % msg)
            elif level == WARNING:
                print("[-] %s" % msg)
            elif level == ERROR:
                print("[!] %s" % msg)
