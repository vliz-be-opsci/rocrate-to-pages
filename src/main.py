# This file is the main file of the project. It contains the main function
# This file will distribute the work to other files
# first thing is to check the given config file and load it
# based on config file, it will make the necessary calls to other files and make fodlers for the output files

import os
import sys
import yaml
from utils.config_utils import check_config
from utils.gh_pages_builder import build_gh_pages
from utils.singleton.location import Location

# set the location of the src folder
Location(root=os.path.dirname(os.path.abspath(__file__)))

# check if the config file exists in src/data/config.yml
if not os.path.isfile("data/config.yml"):
    print("Config file not found. Please make sure it exists in src/data/config.yml")
    sys.exit(1)

#load in the config file
with open("data/config.yml", "r") as f:
    config = yaml.safe_load(f)

# check if the config file is valid
if not check_config(config):
    print("Config file is not valid. Please make sure it is valid")
    sys.exit(1)

# check if the data folder exists
if not os.path.isdir("data"):
    print("Data folder not found. Please make sure it exists in src/data")
    sys.exit(1)

build_gh_pages(config, os.path.join(Location().get_location(), "data"))