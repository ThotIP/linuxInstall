#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Installer v1.0

Usage:
  thotInstall.py install <name> [--dry-run] [--json] [--verbose]
  thotInstall.py remove <name> [--dry-run] [--json] [--verbose]
  thotInstall.py list [--json] [--verbose]
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

    if arguments["--verbose"]:
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

    # Check if we need to install or remove the package
    if arguments["list"]:
        docOptCmd = "list"
    elif arguments["install"] and not arguments["remove"]:
        docOptCmd = "install"
    else:
        docOptCmd = "remove"

    # Load the JSON file
    with open(json_file) as data_file:
        data = json.load(data_file)

    if docOptCmd == "list":
        print "This is the packages available to install:"

    # Parse the package list and proceed to
    # install / uninstall execution
    for k, v in data.items():

        # Only print the package name
        if docOptCmd == "list":
            print "    ->", k

        # Else proceed to install/remove
        else:
            if arguments["<name>"] ==  k or arguments["<name>"] == "all":

                # Status indicates a package can be installed
                # Wait for user answer is package is a user install
                status = "ko"

                if docOptCmd == "install":
                    print "Installing", k
                else:
                    print "Removing", k

                # Ask to the user if he wants to install in his home the
                # package
                choice = "y"
                if v["type"] == "user":
                    print k, "is a user package. Do you want to proceed to " + docOptCmd + " ? [Y/n]"
                    choice = raw_input().lower()
                    if choice in yes:
                        status = "ok"

                # If the user wants to proceed, execute the command
                if status == "ok":
                    cmd = v[docOptCmd]
                    # TODO: execution with subprocess to remove STDOUT
                    # The new line doesn't work
                    if arguments["--verbose"]:
                        cmd += " > /dev/null 2>&1"
                    if arguments["--dry-run"] is False:
                        ret = os.system(cmd)
                        if ret:
                            print "ERROR: Can't execute install command of", k
                            sys.exit(1)

                    # Print the setup command to help the user to configure
                    if v["setup"] != "":
                        print k, "is installed. Setup your new package with the follwong command:"
                        print v["setup"]


