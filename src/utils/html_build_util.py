#file that contains function to help build and clean build folder

import os
import sys
import shutil
from utils.singleton import location

def setup_build_folder():
    '''
    this function will setup the build folder
    '''
    # check if the build folder exists
    print(location.Location().get_location())
    if not os.path.isdir(os.path.join(location.Location().get_location(), "build")):
        os.mkdir(os.path.join(location.Location().get_location(), "build"))
    else:
        # if it exists, clean it
        clean_build_folder()
        
def clean_build_folder():
    if os.path.isdir(os.path.join(location.Location().get_location(), "build")):
        for file in os.listdir(os.path.join(location.Location().get_location(), "build")):
            try:
                shutil.rmtree(os.path.join(os.path.join(location.Location().get_location(), "build"), file))
            except NotADirectoryError:
                os.remove(os.path.join(os.path.join(location.Location().get_location(), "build"), file))
    else:
        print("{} folder does not exist", os.path.join(location.Location().get_location(), "build"))
        sys.exit(1)