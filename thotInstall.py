#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ThotIP Installer v1.0

Usage:
  thotInstall.py install <name> [--dry-run] [--json] [--verbose]
  thotInstall.py remove <name> [--dry-run] [--json] [--verbose]
  thotInstall.py (-h | --help)
  thotInstall.py --version

Options:
  <name>        A package name, full or all.
  -h --help     Show this screen.
  --version     Show version.
  --json        Specify a JSON file to use
  --dry-run     Just load the file and print commands. No execution.
  --verbose     Activate verbose mode for debugging

"""

import os, sys
import json
from docopt import docopt


if __name__ == '__main__':

    # raw_input returns the empty string for "enter"
    yes = set(['yes','y', ''])
    no = set(['no','n'])

    arguments = docopt(__doc__, version='ThotIP Installer 1.0')
    json_file = ""
    print(arguments)

    # Inform user about sudo priviledge for system install
    if os.geteuid() != 0:
        print "INFO: You are not a sudoer."
        print "      Please launch this script with sudo prefix for proper execution"
        sys.exit(0)

    # Start to grab the JSON file path
    if arguments["--json"]  is False:
        if os.path.isfile("./install.json") is not True:
            print "ERROR: Missing JSON file to install a package..."
            sys.exit(1)
        else:
            json_file = "./install.json"
    else:
        if os.path.isfile(arguments["--json"]) is not True:
            print "ERROR: JSON file specified is not there..."
            sys.exit(1)
        else:
            json_file = arguments["--json"]

    if arguments["install"] and not arguments["remove"]:
        docOptCmd = "install"
    else:
        docOptCmd = "remove"

    with open(json_file) as data_file:
        data = json.load(data_file)

    # Parse the package list and proceed to
    # install / uninstall execution
    for k, v in data.items():

        # Status indicates a package can be installed
        # Wait for user answer is package is a user install
        status = "ko"

        if docOptCmd is "install":
            print "Installing", k
        else:
            print "Removing", k

        if v["type"] is "user":
            print k, "is a user package. Do you want to proceed to installation?"
            choice = raw_input().lower()
            if choice in yes:
                status = "ok"

        if status is "ok":
            cmd = v[docOptCmd]
            if arguments["--verbose"]:
                cmd += " > /dev/null 2>&1"
            if arguments["--dry-run"] is False:
                ret = os.system(cmd)
                if ret:
                    print "ERROR: Can't execute install command of", k
                    sys.exit(1)

