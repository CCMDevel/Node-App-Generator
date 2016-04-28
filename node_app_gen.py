# Arguments: python ___ { project name }, { port }

import argparse
import subprocess

def parse_args():
    description = "Creates an empty Node web app project"
    project_name = 'project_name'
    port = 'port'
    

    help_project_name = ("The name of the project to be "
        "created. White space will be replaced with underscores (i.e. 'Project"
        "Name' will result in the directory of 'Project_Name' and files of" 
        "'project_name.something.extension'"
    )

    help_port = ("The port that this project will run on. Must be an integer.")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(project_name, help=help_project_name)
    parser.add_argument(port, type=int, help=help_port)

    return parser.parse_args()

def mkdir(dirname):
    cmd = 'mkdir ' + dirname
    result = subprocess.call(cmd, shell=True)

    if result == 0:
        print("Created Directory '" + dirname + "'")
    else:
        print("Error creating directory '" + dirname + "'")
        sys.exit(1)

def makeProjectDirectories(dirname):
    mkdir(dirname);
    mkdir(dirname + "/app")
    mkdir(dirname + "/app/models")
    mkdir(dirname + "/app/routes")
    mkdir(dirname + "/app/controllers")
    mkdir(dirname + "/config")
    mkdir(dirname + "/public")

def main():
    args = parse_args()
    print("Creating new Node project '" + args.project_name + "'")
    makeProjectDirectories(args.project_name)

main()
