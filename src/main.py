# This file is the main file of the project. It contains the main function
# This file will distribute the work to other files
# first thing is to check the given config file and load it
# based on config file, it will make the necessary calls to other files and make folders for the output files

import os
import sys
import yaml
import argparse
from utils.config_utils import check_config
from utils.gh_pages_builder import build_gh_pages
from utils.singleton.location import Location
from utils.singleton.logger import get_logger

logger = get_logger()
# set the location of the src folder
Location(root=os.path.dirname(os.path.abspath(__file__)))

#read in the first argument that was given with the python main.py command
parser = argparse.ArgumentParser(description="Generate a website from a given config file")
repo = parser.add_argument("repo", help="The repo to generate the website for")

args = parser.parse_args()
repon = args.repo

# check if the config file exists in src/data/config.yml
if not os.path.isfile("data/config.yml"):
    logger.error("Config file not found. Please make sure it exists in src/data/config.yml")
    sys.exit(1)

#load in the config file
with open("data/config.yml", "r") as f:
    config = yaml.safe_load(f)
    config["repo"] = repon

# check if the config file is valid
if not check_config(config):
    logger.error("Config file is not valid. Please make sure it is valid")
    sys.exit(1)

# check if the data folder exists
if not os.path.isdir("data"):
    logger.error("Data folder not found. Please make sure it exists in src/data")
    sys.exit(1)

build_gh_pages(config, os.path.join(Location().get_location(), "data"))