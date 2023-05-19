# this file will do all necessary checks on the config file and load it

import os
import sys
import yaml

def check_config(config):
    # do the following checks:
    # 1. check if the config file has this structure:
    # multiple_rocrates: false
    # RELEASE_management: true
    #    RELEASE_verioning: tag #by major tag or by release
    #    INCLUDE_draft: true #include draft release which is the latest commit on the main branch 
    # if multiple_rocrates is true, then RELEASE_management must be false
    # if RELEASE_management is true, then RELEASE_versioning must be either tag or release
    # if RELEASE_management is true, then INCLUDE_draft must be true or false
    # if RELEASE_management is false, then RELEASE_versioning and INCLUDE_draft must not be present
    if "multiple_rocrates" not in config:
        print("multiple_rocrates is not present in the config file")
        return False
    if "RELEASE_management" not in config:
        print("RELEASE_management is not present in the config file")
        return False
    
    if config["multiple_rocrates"] == True and config["RELEASE_management"] == True:
        print("multiple_rocrates and RELEASE_management cannot both be true")
        return False

    if config["multiple_rocrates"] == False and config["RELEASE_management"] == False:
        print("multiple_rocrates and RELEASE_management cannot both be false")
        return False
            
    if config["RELEASE_management"] == True:
        if "RELEASE_versioning" not in config:
            print("RELEASE_versioning is not present in the config file")
            return False
        if config["RELEASE_versioning"] not in ["tag", "release"]:
            print("RELEASE_versioning must be either tag or release")
            return False
        if "INCLUDE_draft" not in config:
            print("INCLUDE_draft is not present in the config file")
            return False
        if config["INCLUDE_draft"] not in [True, False]:
            print("INCLUDE_draft must be either true or false")
            return False
    
    return True

def yaml_to_dict(config):
    '''
    convert the config file to a dictionary
    :param config: the config file
    :return: the dictionary of the config file
    '''
    config_dict = {}
    yaml_dict = yaml.safe_load(config)
    for key, value in yaml_dict.items():
        config_dict[key] = value
    return config_dict
