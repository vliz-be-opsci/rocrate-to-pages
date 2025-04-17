# This file is the main file of the project. It contains the main function
# This file will distribute the work to other files
# first thing is to check the given config file and load it
# based on config file, it will make the necessary calls to other files and
#   make folders for the output files

import argparse
import os
import sys

import yaml

from utils.config_utils import check_config
from utils.gh_pages_builder import build_gh_pages
from utils.singleton.location import Location
from utils.singleton.logger import get_logger

logger = get_logger()
# set the location of the src folder
Location(root=os.path.dirname(os.path.abspath(__file__)))

# read in the first argument that was given with the python main.py command
parser = argparse.ArgumentParser(
    description="Generate a website from a given config file"
)
repo = parser.add_argument("repo", help="The repo to generate the website for")
parser.add_argument("multiple_crates", help="true if the repository has multiple crates, false otherwise")
parser.add_argument("release_management", help="true if the repository has release management; Cannot be combined with multiple_crates")
parser.add_argument("release_versioning", help="if true will add all the versions of the gh repo that have a rocrate in them to the website; Cannot be combined with multiple_crates or release_management")
parser.add_argument("include_draft", help="if true will include the last commit of the repo as a draft version in the gh-pages.")
parser.add_argument("draft_folder_name", help="the name of the folder that will contain the draft version of the repo")
parser.add_argument("index_html", help="if true will add an index.html file to the root of the gh-pages")
parser.add_argument("theme", help="the theme to use for the website")
parser.add_argument("space_to_pages_homepage", help="the web-adress for the homepage of the space website")
parser.add_argument("dataset_catalogue", help="boolean value to determine if the overarching index is a dataset catalogue or not")
parser.add_argument("base_uri", help="the base uri for the website")
args = parser.parse_args()
repon = args.repo

#convert all true/false strings to booleans
if args.multiple_crates == "true":
    args.multiple_crates = True
else:
    args.multiple_crates = False

if args.release_management == "true":
    args.release_management = True
else:
    args.release_management = False

if args.include_draft == "true":
    args.include_draft = True
else:
    args.include_draft = False

if args.index_html == "true":
    args.index_html = True
else:
    args.index_html = False
    
if args.dataset_catalogue == "true":
    args.dataset_catalogue = True
else:
    args.dataset_catalogue = False

#log all the arguments
logger.info(f"repo: {repon}")
logger.info(f"multiple_rocrates: {args.multiple_crates}")
logger.info(f"release_management: {args.release_management}")
logger.info(f"release_versioning: {args.release_versioning}")
logger.info(f"include_draft: {args.include_draft}")
logger.info(f"draft_folder_name: {args.draft_folder_name}")
logger.info(f"index_html: {args.index_html}")
logger.info(f"theme: {args.theme}")
logger.info(f"space_to_pages_homepage: {args.space_to_pages_homepage}")
logger.info(f"dataset_catalogue: {args.dataset_catalogue}")
logger.info(f"base_uri: {args.base_uri}")

config_file = True

# check if the config file exists in src/data/config.yml
if not os.path.isfile("data/config.yml"):
    logger.warning(
        "Config file not found. Using backup settings"
        "Please make sure if you meant to use the config file that it exists in src/data/config.yml"
    )
    config = {
        "multiple_rocrates": args.multiple_crates,
        "RELEASE_management": args.release_management,
        "RELEASE_versioning": args.release_versioning,
        "INCLUDE_draft": args.include_draft,
        "index_html": args.index_html,
        "draft_folder_name": args.draft_folder_name,
        "theme": args.theme,
        "repo": repon,
        "space_to_pages_homepage": args.space_to_pages_homepage,
        "dataset_catalogue": args.dataset_catalogue,
        "base_uri": args.base_uri,
    }
    config_file = False

if config_file:
    # load in the config file
    with open("data/config.yml", "r") as f:
        config = yaml.safe_load(f)
        config["repo"] = repon

# check if the config file is valid
if not check_config(config):
    logger.error("Config file is not valid. Please make sure it is valid")
    sys.exit(1)

# check if the data folder exists
if not os.path.isdir("data"):
    logger.error(
        "Data folder not found. Please make sure it exists in src/data"
    )
    sys.exit(1)

build_gh_pages(config, os.path.join(Location().get_location(), "data"))
