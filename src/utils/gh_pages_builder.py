# this file will be responsible for building the gh-pages branch , by making html files according to the config file settings
# the output will be located in ./src/build folder

import os
import sys
import yaml
import shutil
from utils.html_build_util import setup_build_folder
from utils.singleton.location import Location

def build_gh_pages(config, data_path):
    '''
    this function will build the gh-pages branch based on the config file
    :param config: the config file
    :param data: the path to the data folder
    '''
    
    #first thing is to setup the build folder
    setup_build_folder()
    #check what type of build it is (multiple rocrates or single rocrate)
    if config["multiple_rocrates"] == True:
        #perform multiple rocrates build function
        build_multiple_rocrates(data_path)
    if config["RELEASE_management"] == True:
        #perform release management build function
        pass
    if config["index_html"] == True:
        #perform index html build function
        build_index_html()
    
def build_multiple_rocrates(data_path):
    '''
    this function will build the gh-pages branch based on the config file
    :param data: the path to the data folder
    '''
    #first check out the data folder and find all the rocrates
    all_rocrates = find_rocrates(data_path)
    #for each rocrate, make a folder in the build folder
    for rocrate in all_rocrates:
        build_folder_for_rocrate(rocrate)
    
def find_rocrates(data_path):
    '''
    this function will find all the rocrates in the data folder
    :param data: the path to the data folder
    :return: a list of all paths where ro-crate-metadata.json files were found
    '''
    all_rocrates = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file == "ro-crate-metadata.json":
                #found a rocrate
                #append only the relavent path to the list
                rel_path = os.path.relpath(root, data_path)
                all_rocrates.append(rel_path)
    
    #if no rocrates were found, exit with error 
    if len(all_rocrates) == 0:
        print("Error: no rocrates were found in the data folder")
        sys.exit(1)
                
    #for each path in all_rocrates, check if they are not a child of another path in all_rocrates
    #if they are make error and exit
    for path in all_rocrates:
        for path2 in all_rocrates:
            if path != path2:
                if path.startswith(path2):
                    print("Error: rocrate at {} is a child of another rocrate at {}".format(path, path2))
                    sys.exit(1)
    print(all_rocrates)
    return all_rocrates

def build_folder_for_rocrate(rocrate_path):
    '''
    this function will build the folder for a rocrate
    :param rocrate_path: the path to the rocrate
    '''
    #first thing is to make the folder in the build folder
    #the name of the folder will be the name of the rocrate
    rocrate_name = os.path.basename(rocrate_path)
    os.mkdir(os.path.join(Location().get_location(),"build", rocrate_name))
    #then copy the rocrate into the folder
    shutil.copytree(os.path.join(Location().get_location(),"data",rocrate_path), os.path.join(Location().get_location(),"build", rocrate_name), dirs_exist_ok=True)
    #then make the html file for the rocrate
    make_html_file_for_rocrate(rocrate_path)
    
def make_html_file_for_rocrate(rocrate_path):
    '''
    this function will make the html file for a rocrate
    :param rocrate_path: the path to the rocrate
    '''
    #make a simple index.html file with the folder of the rocrate relative to the build folder
    rocrate_name = os.path.basename(rocrate_path)
    with open(os.path.join(Location().get_location(),"build", rocrate_name, "index.html"), "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>RO-Crate: {}</h1>\n<p>RO-Crate folder: <a href=\"./{}\">{}</a></p>\n</body>\n</html>".format(rocrate_name, "ro-crate-metadata.json", "ro-crate-metadata.json"))
    
    #make a copy of the index.html and name it ro-crate-metadata-preview.html
    shutil.copyfile(os.path.join(Location().get_location(),"build", rocrate_name, "index.html"), os.path.join(Location().get_location(),"build", rocrate_name, "ro-crate-metadata-preview.html"))
    
def build_index_html():
    '''
    This function will loop over the build folder and make an index.html file
    '''
    all_index_html_files = []
    for root, dirs, files in os.walk(os.path.join(Location().get_location(),"build")):
        for file in files:
            if file == "index.html":
                #add rel path to build folder to list
                rel_path = os.path.relpath(root, os.path.join(Location().get_location(),"build"))
                all_index_html_files.append(rel_path)
    
    #make the index.html file by referencing all the index.html files in the build folder
    with open(os.path.join(Location().get_location(),"build", "index.html"), "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>Index</h1>\n")
        for index_html_file in all_index_html_files:
            f.write("<p><a href=\"./{}\">{}</a></p>\n".format(index_html_file, index_html_file))
        f.write("</body>\n</html>")
    