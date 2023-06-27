# this file will contain all functions that will make the necessary calls
#   using the git python library
import json
import os
import shutil

import git
import requests

from utils.singleton.logger import get_logger

logger = get_logger()


# function to check if a given repo is a valid git repo
def is_valid_git_repo(repo):
    try:
        git.Repo(repo)
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


# function to get all the branches of a given repo
def get_branches(repo):
    branches = []
    for branch in repo.branches:
        branches.append(branch.name)
    return branches


# function to get all the tags of a given repo path
def get_tags(repo):
    tags = []
    repo_path = repo
    # check if the repo is a valid git repo
    if is_valid_git_repo(repo):
        # get the repo object
        repo = git.Repo(repo)
        # get all the tags
        for tag in repo.tags:
            tags.append(tag.name)
    else:
        logger.error("repo is not a valid git repo")

    if len(tags) == 0:
        logger.error("No tags found for repo: {}".format(repo))
        # try and get the tags from the remote
        remote_tags = get_remote_tags(repo_path)
        tags = remote_tags

    return tags


def get_remote_tags(repo):
    logger.info("Getting remote tags for repo: {}".format(repo))
    owner, repo_name = get_owner_and_repo_name_repo(repo)
    repo_url = (
        "https://api.github.com/repos/" + owner + "/" + repo_name + "/tags"
    )
    tags = requests.get(repo_url).json()
    tags = [tag["name"] for tag in tags]
    return tags


# function to get owner and repo name from a given repo pat
def get_owner_and_repo_name_repo(repo):
    # get the repo object
    repo_url = get_remote_url(repo)
    repo = git.Repo(repo)
    # get the owner and repo name
    owner_repo = repo_url.split("github.com/")[1]
    owner_repo = owner_repo.split(".git")[0]
    owner_repo = owner_repo.split("/")
    owner = owner_repo[0]
    repo_name = owner_repo[1]
    return owner, repo_name


# function to get all releases of a given repo
def get_releases(repo):
    releases = []
    if is_valid_git_repo(repo):
        # get the owner and repo name
        owner, repo_name = get_owner_and_repo_name_repo(repo)
        # get the repo object
        repo = git.Repo(repo)
        repo_url = (
            "https://api.github.com/repos/"
            + owner
            + "/"
            + repo_name
            + "/releases"
        )
        releases = requests.get(repo_url).json()
        # get release tag_name and sha for each release
        releases = [release["tag_name"] for release in releases]
    return releases


# function to download a given release of a given repo to a given location
def download_release(repo, release_tag, location):
    # get the owner and repo name
    owner, repo_name = get_owner_and_repo_name_repo(repo)
    # get the release url
    repo_url = (
        "https://api.github.com/repos/" + owner + "/" + repo_name + "/releases"
    )
    releases = requests.get(repo_url).json()
    for release in releases:
        if release["tag_name"] == release_tag:
            logger.debug(json.dumps(release, indent=4, sort_keys=True))
            logger.info(f"downloading release {release_tag} of {repo}")
            release_url = release["zipball_url"]
            break
    # download the release
    r = requests.get(release_url, allow_redirects=True)
    open(os.path.join(location, "release.zip"), "wb").write(r.content)
    # extract the release
    try:
        shutil.unpack_archive(os.path.join(location, "release.zip"), location)
    except Exception as e:
        logger.exception(e)
    # delete the zip file
    os.remove(os.path.join(location, "release.zip"))
    # get the name of the extracted folder
    try:
        extracted_folder = os.listdir(location)[0]
        if extracted_folder == "release.zip":
            extracted_folder = os.listdir(location)[1]
        # move the contents of the extracted folder to the location
        for file in os.listdir(os.path.join(location, extracted_folder)):
            try:
                shutil.move(
                    os.path.join(location, extracted_folder, file), location
                )
            except shutil.Error:
                logger.info(f"file {file} already exists in {location}")
        # delete the extracted folder
        os.rmdir(os.path.join(location, extracted_folder))
        return True
    except Exception as e:
        logger.exception(e)
        return False


def download_tag(repo, tag, location):
    tag_name = tag
    owner, repo_name = get_owner_and_repo_name_repo(repo)
    repo_url = (
        "https://api.github.com/repos/" + owner + "/" + repo_name + "/tags"
    )
    tags = requests.get(repo_url).json()
    for tag in tags:
        logger.debug(json.dumps(tag, indent=4, sort_keys=True))
        logger.debug(tag["name"])
        if tag["name"] == tag_name:
            logger.debug(json.dumps(tag, indent=4, sort_keys=True))
            logger.info(f"downloading tag {tag_name} of {repo}")
            tag_url = tag["zipball_url"]
            break
    # download the tag
    r = requests.get(tag_url, allow_redirects=True)
    open(os.path.join(location, "tag.zip"), "wb").write(r.content)
    # extract the tag
    try:
        shutil.unpack_archive(os.path.join(location, "tag.zip"), location)
    except Exception as e:
        logger.exception(e)
    # delete the zip file
    os.remove(os.path.join(location, "tag.zip"))
    # get the name of the extracted folder
    try:
        extracted_folder = os.listdir(location)[0]
        if extracted_folder == "tag.zip":
            extracted_folder = os.listdir(location)[1]
        # move the contents of the extracted folder to the location
        for file in os.listdir(os.path.join(location, extracted_folder)):
            try:
                shutil.move(
                    os.path.join(location, extracted_folder, file), location
                )
            except shutil.Error:
                logger.info(f"file {file} already exists in {location}")

        # in the location folder check if there is a file named
        #   ro-crate-metadata.json
        # if there is then open it and loop over the @graph array ,
        #   if the @id is ./ => add downloadUrl: repo_url to it
        # if it already exists then replace it
        try:
            # OPEN THE METADATA FILE
            with open(
                os.path.join(location, "ro-crate-metadata.json"), "r"
            ) as f:
                metadata = json.load(f)
            # LOOP OVER THE @graph ARRAY
            for item in metadata["@graph"]:
                if item["@id"] == "./":
                    item["downloadUrl"] = tag_url
                    break
            # SAVE THE METADATA FILE
            with open(
                os.path.join(location, "ro-crate-metadata.json"), "w"
            ) as f:
                json.dump(metadata, f)
        except Exception as e:
            logger.exception(e)

        # delete the extracted folder
        os.rmdir(os.path.join(location, extracted_folder))
        return True
    except Exception as e:
        logger.exception(e)
        return False


# function to clone a given repo with a given commit-hash to a given location
def clone_repo(repo, commit_hash, location):
    try:
        git.Repo.clone_from(repo, location, no_checkout=True)
        repo = git.Repo(location)
        repo.git.checkout(commit_hash)
        return True
    except git.exc.GitCommandError:
        logger.error("commit hash {} does not exist".format(commit_hash))
        return False


# function to get the remote url of a given repo
def get_remote_url(repo):
    # get the repo object
    repo = git.Repo(repo)
    # get the remote url
    remote_url = repo.remotes.origin.url
    return remote_url


def get_hash_from_tag(repo, tag):
    logger.info("getting commit hash of tag {}".format(tag))
    repo_path = repo
    # get the repo object
    repo = git.Repo(repo)
    # get the commit hash of the given tag
    try:
        commit_hash = repo.tags[tag].commit.hexsha
    except IndexError:
        logger.error("tag {} does not exist".format(tag))
        commit_hash = get_hash_from_tag_remote(repo_path, tag)
    return commit_hash


def get_hash_from_tag_remote(repo, tag):
    logger.info("getting commit hash of tag {} from remote".format(tag))
    # get the owner and repo name
    owner, repo_name = get_owner_and_repo_name_repo(repo)
    repo_url = (
        "https://api.github.com/repos/" + owner + "/" + repo_name + "/tags"
    )
    tags = requests.get(repo_url).json()
    for tag in tags:
        if tag["name"] == tag:
            return tag["commit"]["sha"]
    return None


# function to get the latest commit hash of a given repo
def get_latest_commit_hash(repo):
    repo_path = repo
    try:
        repo = git.Repo(repo)
        return repo.head.object.hexsha
    except Exception as e:
        logger.error("repo {} does not exist".format(repo_path))
        logger.exception(e)
        return None
