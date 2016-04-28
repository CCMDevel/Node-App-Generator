# Arguments: python ___ { project name }, { port }

import sys
import os
import argparse
import subprocess

key_dirname = 'dirname'
key_name = 'name'
key_port = 'port'

def parse_args():
    description = "Creates an empty Node web app project"
    
    help_name = ("The name of the project to be "
        "created. White space will be replaced with underscores (i.e. 'Project"
        "Name' will result in the directory of 'Project_Name' and files of" 
        "'project_name.something.extension'"
    )

    help_port = ("The port that this project will run on. Must be an integer.")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(key_name, help=help_name)
    parser.add_argument(key_port, type=int, help=help_port)

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

def createAppFile(data):
    filename = data[key_dirname] + "/" + data[key_name] + ".js"
    app_file = open(filename, "w")
    
    contents = """var port = {port};
var app = require('./config/{name}.express.js');
var db = require('./config/{name}.mongoose.js');

db = db();
app = app(__dirname + "/public");

app.set('port', port);
app.listen(app.get('port'), function(){{
    console.log('{name}.js now listening on port ' + app.get('port'));
}});""".format(**data)

    app_file.write(contents);
    
    app_file.close()
    print('Created ' + filename)

def createExpressFile(data):
    filename = data[key_dirname] + "/config/" + data[key_name] + ".express.js"
    express_file = open(filename, "w")
    
    content = """var {name}_routes = require('./{name}.routes.js');
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

def createRoutesFile(data):
    filename = data[key_dirname] + "/config/" + data[key_name] + ".routes.js"
    routes_file = open(filename, "w")
    
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

def createMongooseFile(data):
    filename = data[key_dirname] + "/config/" + data[key_name] + ".mongoose.js"
    mongoose_file = open(filename, "w")
    
    content = """var mongoose = require('mongoose');

module.exports = function(){{
    var db = mongoose.connect('mongodb://localhost/{name}_dev');

    var modelsDir = '../app/models/';

//    require(modelsDir + 'something.model.js');

    return db;    
}};""".format(**data)
    mongoose_file.write(content)
    mongoose_file.close()
    print('Created ' + filename) 

def main():
    args = parse_args()
    name = args.name
    port = args.port

    data = { key_dirname : name, key_port : str(port), key_name : name.lower() }
    
    print("Creating new Node project '" + name + "'")
    
    makeProjectDirectories(data[key_dirname])
    createAppFile(data)
    createExpressFile(data)
    createRoutesFile(data)
    createMongooseFile(data)

    print("Done.")

print(os.getcwd())
main()
