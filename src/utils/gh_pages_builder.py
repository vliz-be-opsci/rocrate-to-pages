# this file will be responsible for building the gh-pages branch ,
#   by making html files according to the config file settings
# the output will be located in ./src/build folder

import os
import shutil
import sys
import time

from utils.config_utils import check_forbidden_characters
from utils.git_utils import (
    clone_repo,
    download_release,
    download_tag,
    get_latest_commit_hash,
    get_releases,
    get_tags,
    is_valid_git_repo,
)
from utils.html_build_util import fill_template_file, setup_build_folder
from utils.singleton.location import Location
from utils.singleton.logger import get_logger

logger = get_logger()


def build_gh_pages(config, data_path):
    """
    this function will build the gh-pages branch based on the config file
    :param config: the config file
    :param data: the path to the data folder
    """
    # first thing is to setup the build folder
    setup_build_folder()

    # check if config["theme"] exists , if it doesn check if it is one of the
    #   allowed themes, if not then set it to default (main)
    if "theme" not in config:
        config["theme"] = "main"
    else:
        if config["theme"] not in [
            "dark",
            "light",
            "high_contrast",
            "rocrate",
        ]:
            logger.warning(
                "theme must be either dark, light, high_contrast or rocrate"
            )
            logger.info("using default theme: main")
            config["theme"] = "main"

    # check what type of build it is (multiple rocrates or single rocrate)
    if config["multiple_rocrates"] is True:
        # perform multiple rocrates build function
        build_multiple_rocrates(data_path, config)
    if config["RELEASE_management"] is True:
        # perform release management build function
        build_single_rocrate(data_path, config)
    if config["INCLUDE_draft"] is True:
        # perform draft build function
        build_draft(data_path, config)
    if config["index_html"] is True:
        # perform index html build function
        build_index_html(config)


def build_multiple_rocrates(data_path, config):
    """
    this function will build the gh-pages branch based on the config file
    :param data: the path to the data folder
    """
    # first check out the data folder and find all the rocrates
    all_rocrates = find_rocrates(data_path)
    # for each rocrate, make a folder in the build folder
    for rocrate in all_rocrates:
        logger.info("Building rocrate at {}".format(rocrate))
        build_folder_for_rocrate(rocrate, config)


def find_rocrates(data_path):
    """
    this function will find all the rocrates in the data folder
    :param data: the path to the data folder
    :return: a list of all paths where ro-crate-metadata.json files were found
    """
    all_rocrates = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file == "ro-crate-metadata.json":
                # found a rocrate
                # append only the relavent path to the list
                rel_path = os.path.relpath(root, data_path)
                all_rocrates.append(rel_path)

    # if no rocrates were found, exit with error
    if len(all_rocrates) == 0:
        logger.error("No rocrates were found in the data folder")
        sys.exit(1)

    # for each path in all_rocrates, check if they are not a child of
    #   another path in all_rocrates
    # if they are make error and exit
    for path in all_rocrates:
        for path2 in all_rocrates:
            if path != path2:
                if path.startswith(path2):
                    error_msg = (
                        f"Error: rocrate at {path} is a child of"
                        "another rocrate at {path2}"
                    )
                    logger.error(error_msg)
                    sys.exit(1)
    logger.info("Found {} rocrates".format(len(all_rocrates)))
    return all_rocrates


def build_folder_for_rocrate(rocrate_path, config):
    """
    this function will build the folder for a rocrate
    :param rocrate_path: the path to the rocrate
    """
    # first thing is to make the folder in the build folder
    # the name of the folder will be the name of the rocrate
    rocrate_name = os.path.basename(rocrate_path)
    try:
        os.mkdir(
            os.path.join(Location().get_location(), "build", rocrate_name)
        )
    except FileExistsError:
        logger.warning(
            "rocrate {} already exists in build folder".format(rocrate_name)
        )
    # then copy the rocrate into the folder
    shutil.copytree(
        os.path.join(Location().get_location(), "data", rocrate_path),
        os.path.join(Location().get_location(), "build", rocrate_name),
        dirs_exist_ok=True,
    )
    # then make the html file for the rocrate
    make_html_file_for_rocrate(rocrate_path, config)


def make_html_file_for_rocrate(rocrate_path, config):
    """
    this function will make the html file for a rocrate
    :param rocrate_path: the path to the rocrate
    """
    # make a simple index.html file with the folder of the rocrate relative to
    #   the build folder
    rocrate_name = os.path.basename(rocrate_path)
    kwargs = {
        "title": str(config["repo"]),
        "version": str(rocrate_name),
        "description": "Preview page for the RO-Crate: " + rocrate_name,
        "theme": config["theme"],
        "space_to_pages_homepage": config["space_to_pages_homepage"],
    }

    html_file = fill_template_file("index.html", **kwargs)

    with open(
        os.path.join(
            Location().get_location(), "build", rocrate_name, "index.html"
        ),
        "w",
    ) as f:
        f.write(html_file)

    # make a copy of the index.html and name it ro-crate-metadata-preview.html
    shutil.copyfile(
        os.path.join(
            Location().get_location(), "build", rocrate_name, "index.html"
        ),
        os.path.join(
            Location().get_location(),
            "build",
            rocrate_name,
            "ro-crate-metadata-preview.html",
        ),
    )


def build_index_html(config):
    """
    This function will loop over the build folder and make an index.html file
    """
    # check if there is already an index.html file in the root of the build
    #   folder
    if os.path.isfile(
        os.path.join(Location().get_location(), "build", "index.html")
    ):
        logger.error("Index.html already exists in build folder")
        sys.exit(1)

    all_index_html_files = []
    for root, dirs, files in os.walk(
        os.path.join(Location().get_location(), "build")
    ):
        for file in files:
            if file == "index.html":
                # add rel path to build folder to list
                rel_path = os.path.relpath(
                    root, os.path.join(Location().get_location(), "build")
                )
                all_index_html_files.append(rel_path)

    kwargs = {
        "title": str(config["repo"]),
        "description": "Index page for the rocrates in this repository",
        "theme": config["theme"],
        "rocrates": all_index_html_files,
        "config": config,
        "space_to_pages_homepage": config["space_to_pages_homepage"],
    }

    # check in the config["base_uri"] is if ends with a /, if not add it
    if config["base_uri"][-1] != "/":
        config["base_uri"] += "/"

    # Make distinction here between a rocrate that has multiple versions
    # and a dataset catalogue of multiple rocrates

    if config["dataset_catalogue"] is True:

        # html_file
        html_file = fill_template_file(
            "dataset_catalogue_index.html", **kwargs
        )

        # metadata
        # change description and adding timestap for dc:modified
        kwargs["description"] = (
            "Dataset catalogue for the rocrates in this repository"
        )
        kwargs["timestamp"] = time.strftime(
            "%Y-%m-%dT%H:%M:%S.000", time.gmtime()
        )
        metadata_file = fill_template_file(
            "dataset_catalogue_metadata.ttl", **kwargs
        )

        # write metadata file to build folder
        with open(
            os.path.join(Location().get_location(), "build", "metadata.ttl"),
            "w",
        ) as f:
            f.write(metadata_file)

    if config["dataset_catalogue"] is False:
        html_file = fill_template_file("overarching_index.html", **kwargs)

    with open(
        os.path.join(Location().get_location(), "build", "index.html"), "w"
    ) as f:
        f.write(html_file)

    """
    #make the index.html file by referencing all the index.html files in
        the build folder
    with open(os.path.join(Location().get_location(),"build", "index.html"),
            "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n<h1>Index</h1>\n")
        for index_html_file in all_index_html_files:
            f.write("<p><a href=\"./{}\">{}</a></p>\n".format(index_html_file,
                index_html_file))
        f.write("</body>\n</html>")
    """


# function to build html files for a single rocrate
def build_single_rocrate(rocrate_path, config):
    """
    this function will build the gh-pages branch based on the config file
    :param rocrate_path: the path to the rocrate
    """
    # first thing is to setup the build folder
    setup_build_folder()
    # check if the rocrate exists
    if os.path.exists(rocrate_path) is False:
        logger.error("rocrate does not exist")
        sys.exit(1)
    # check if the rocrate is a child of another rocrate
    all_rocrates = find_rocrates(
        os.path.join(Location().get_location(), "data")
    )
    for rocrate in all_rocrates:
        if rocrate_path.startswith(rocrate):
            logger.error("rocrate is a child of another rocrate")
            sys.exit(1)

    # check what type of release management is being used (tag or release)
    if config["RELEASE_versioning"] == "tag":
        build_single_rocrate_tag(rocrate_path, config)

    if config["RELEASE_versioning"] == "release":
        build_single_rocrate_release(rocrate_path, config)


# function to make build folder from single ro-crate with
#   tag release management
def build_single_rocrate_tag(rocrate_path, config):
    logger.info("Building rocrate with tag release management")
    # first check if the given rocrate_path is a valid git repo
    if is_valid_git_repo(rocrate_path) is False:
        logger.error("rocrate_path is not a valid git repo")
        sys.exit(1)

    # get all the tags for the repo
    tags = get_tags(rocrate_path)

    for tag in tags:
        logger.info("Building rocrate for tag: {}".format(tag))
        build_single_tag(tag, rocrate_path, config)


def build_single_tag(tag, rocrate_path, config):
    # first make the folder for the tag
    os.mkdir(os.path.join(Location().get_location(), "build", tag))
    build_folder_tag = os.path.join(Location().get_location(), "build", tag)
    # get the commit hash for the tag
    # commit_hash = get_hash_from_tag(rocrate_path, tag)
    # clone_repo(rocrate_path, commit_hash, build_folder_tag)
    download_tag(rocrate_path, tag, build_folder_tag)
    # then make the html file for the rocrate
    make_html_file_for_rocrate(build_folder_tag, config)


def build_single_rocrate_release(rocrate_path, config):
    logger.info("Building rocrate with release release management")
    # first check if the given rocrate_path is a valid git repo
    if is_valid_git_repo(rocrate_path) is False:
        logger.error("rocrate_path is not a valid git repo")
        sys.exit(1)

    # get all the releases for the repo
    releases = get_releases(rocrate_path)
    for release in releases:
        logger.info("Building rocrate for release: {}".format(release))
        build_single_release(release, rocrate_path, config)


# function to make folder for a single release
def build_single_release(release, rocrate_path, config):
    # first make the folder for the release
    os.mkdir(os.path.join(Location().get_location(), "build", release))
    build_folder_release = os.path.join(
        Location().get_location(), "build", release
    )
    download_release(rocrate_path, release, build_folder_release)

    # find the path of the rocrate in the release folder
    rocrate_path_in_release = find_rocrates(build_folder_release)[0]
    logger.info("rocrate_path_in_release: {}".format(rocrate_path_in_release))

    # make the html file for the rocrate
    make_html_file_for_rocrate(
        os.path.join(rocrate_path_in_release, release), config
    )


def build_draft(rocrate_path, config):
    # check if draft_fodler_name is good format
    # check if draft_folder_name exists in config
    if "draft_folder_name" not in config:
        logger.error("draft_folder_name not in config")
        logger.warning(
            "draft_folder_name will be set to default value: 'draft'"
        )
        config["draft_folder_name"] = "draft"
    else:
        if not check_forbidden_characters(config["draft_folder_name"]):
            logger.error("draft_folder_name contains forbidden characters")
            logger.warning(
                "draft_folder_name will be set to default value: 'draft'"
            )
            config["draft_folder_name"] = "draft"

    # first make the folder for the draft
    try:
        os.mkdir(
            os.path.join(
                Location().get_location(), "build", config["draft_folder_name"]
            )
        )
    except Exception as e:
        logger.debug("folder already exists")
        
    build_folder_draft = os.path.join(
        Location().get_location(), "build", config["draft_folder_name"]
    )
    # get the head commit hash
    commit_hash = get_latest_commit_hash(rocrate_path)
    if commit_hash is None:
        logger.error("Could not get latest commit hash")
        # copy over all files from the rocrate_path to the build folder
        try:
            # ignore directory errors
            shutil.rmtree(build_folder_draft)
            shutil.copytree(rocrate_path, build_folder_draft)
        except Exception as e:
            logger.error(
                "Could not copy files from rocrate_path to build folder"
            )
            logger.exception(e)

    if commit_hash is not None:
        clone_repo(rocrate_path, commit_hash, build_folder_draft)

    # make the html file for the rocrate
    make_html_file_for_rocrate(build_folder_draft, config)
