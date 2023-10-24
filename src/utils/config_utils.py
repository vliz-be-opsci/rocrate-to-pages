# this file will do all necessary checks on the config file and load it

import yaml

from utils.singleton.logger import get_logger

logger = get_logger()


def check_config(config):
    # do the following checks:
    # 1. check if the config file has this structure:
    # multiple_rocrates: false
    # RELEASE_management: true
    #    RELEASE_verioning: tag #by major tag or by release
    #    INCLUDE_draft: true #include draft release which is the latest commit
    #       on the main branch
    # if multiple_rocrates is true, then RELEASE_management must be false
    # if RELEASE_management is true, then RELEASE_versioning must be either tag
    #   or release
    # if RELEASE_management is true, then INCLUDE_draft must be true or false
    # if RELEASE_management is false, then RELEASE_versioning and INCLUDE_draft
    #   must not be present
    
    logger.info("checking config file")
    logger.info("config file:")
    logger.info(config)
    
    if "multiple_rocrates" not in config:
        logger.error("multiple_rocrates is not present in the config file")

        return False
    if "RELEASE_management" not in config:
        logger.error("RELEASE_management is not present in the config file")
        return False

    if (
        config["multiple_rocrates"] is True
        and config["RELEASE_management"] is True
    ):
        logger.error(
            "multiple_rocrates and RELEASE_management cannot both be true"
        )
        return False

    if (
        config["multiple_rocrates"] is False
        and config["RELEASE_management"] is False
    ):
        logger.error(
            "multiple_rocrates and RELEASE_management cannot both be false"
        )
        return False

    if config["RELEASE_management"] is True:
        if "RELEASE_versioning" not in config:
            logger.error(
                "RELEASE_versioning is not present in the config file"
            )
            return False
        if config["RELEASE_versioning"] not in ["tag", "release"]:
            logger.error("RELEASE_versioning must be either tag or release")
            return False
        if "INCLUDE_draft" not in config:
            logger.error("INCLUDE_draft is not present in the config file")
            return False
        if config["INCLUDE_draft"] not in [True, False]:
            logger.error("INCLUDE_draft must be either true or false")
            return False

        if config["INCLUDE_draft"] is True:
            if "draft_folder_name" not in config:
                logger.warning(
                    "draft_folder_name is not present in the config file,"
                    " using default value 'draft'"
                )

    # if config["theme"] is not null then check if it is one of the available
    #   themes (dark,light,high_contrast)
    if "theme" in config:
        if config["theme"] not in ["dark", "light", "high_contrast"]:
            logger.error("theme must be either dark, light or high_contrast")
            logger.info("using default theme: main")

    return True


def yaml_to_dict(config):
    """
    convert the config file to a dictionary
    :param config: the config file
    :return: the dictionary of the config file
    """
    config_dict = {}
    yaml_dict = yaml.safe_load(config)
    for key, value in yaml_dict.items():
        config_dict[key] = value
    if "draft_folder_name" not in config_dict:
        config_dict["draft_folder_name"] = "draft"
    else:
        # check if the draft folder name contains forbidden characters
        if not check_forbidden_characters(config_dict["draft_folder_name"]):
            logger.warning("draft_folder_name contains forbidden characters")
            logger.warning("using default value 'draft'")
            config_dict["draft_folder_name"] = "draft"
    return config_dict


# function that will check if given string contains forbidden characters
def check_forbidden_characters(string):
    forbidden_characters = [
        " ",
        ",",
        ".",
        "!",
        "?",
        ";",
        ":",
        "/",
        "\\",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "|",
        "`",
        "~",
        "<",
        ">",
        "+",
        "=",
        "_",
    ]
    for char in forbidden_characters:
        if char in string:
            return False
    return True
