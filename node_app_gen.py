# Arguments: python ___ { project name }, { port }

import sys
import os
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

def createAppFile(project_name, port):
    filename = project_name + "/" + project_name + ".js"
    app_file = open(filename, "w")
    
    data = {'port' : str(port), 'name' : project_name}
    contents = """var port = {port};
var app = require('./config/{name}.app.js');
var db = require('./config/{name}.db.js');

db = db();
app = app(__homeDir + "/public");

app.set('port', port);
app.listen(app.get('port'), function(){{
    console.log('{name}.js now listening on port ' + app.get('port'));
}});""".format(**data)

    app_file.write(contents);
    
    app_file.close()
    print('Created ' + filename)

def createExpressFile(project_name):
    filename = project_name + "/config/" + project_name + ".app.js"
    express_file = open(filename, "w")
    
    data = {'name' : project_name}
    content = """var {name}_routes = require('{name}.routes.js');
var express = require('express');
var morgan = require('morgan');
var bodyParser = require('body-parser');

module.exports = function(publicDir){{
    console.log("Starting {name}.js...");

    var app = express();
    app.use(morgan('dev'));
    app.use(bodyParser.urlencoded({{
        extended : true
    }}));

    {name}_routes(app, publicDir);
    return app;
}};""".format(**data)
    express_file.write(content)
    express_file.close()
    print('Created ' + filename) 

def createRoutesFile(project_name):
    filename = project_name + "/config/" + project_name + ".routes.js"
    routes_file = open(filename, "w")
    
    data = {'name' : project_name}
    content = """module.exports = function(app, publicDir){{
    console.log('    initializing routes...');

    if (publicDir){{
        app.use(require('express').static(publicDir));
        console.log('        /public directory initialized.'); 
    }}

    var routesDir = '../app/routes/';

//    require(routesDir + 'something.routes.js');

    console.log('    routes initialized.');
}};""".format(**data)
    routes_file.write(content)
    routes_file.close()
    print('Created ' + filename) 

def main():
    args = parse_args()
    project_name = args.project_name
    port = args.port
    print("Creating new Node project '" + project_name + "'")
    makeProjectDirectories(project_name)
    createAppFile(project_name, port)
    createExpressFile(project_name)
    createRoutesFile(project_name)

print(os.getcwd())
main()
