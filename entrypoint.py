#!/usr/bin/env -S python3 -B

# NOTE: If you are using an alpine docker image
# such as pyaction-lite, the -S option above won't
# work. The above line works fine on other linux distributions
# such as debian, etc, so the above line will work fine
# if you use pyaction:4.0.0 or higher as your base docker image.

# Steps in this action:
    # - check if correct files exist. 
    # - create symlink for index.html and crate.json
    # - check validation?
import sys
import os
import logging 

log = logging.getLogger('entrypoint') 

class CrateObj():
    def __init__(self, crate_dir):
        self.crate_dir = crate_dir
        self.metadata_path = os.path.join(self.crate_dir, 'ro-crate-metadata.jsonld') 
        self.metadata_exists = False
        self.preview_path  = os.path.join(self.crate_dir, 'ro-crate-preview.html')
        self.preview_exists = False

        # TODO:
        # self.preview_valid = False
        # self.metadata_valid = False

    def check_rocrate_valid(self):
        # Checks if there are rocrate objects in directory
        log.debug('Checking that rocrate files exist...') 
        if os.path.exists(self.metadata_path):
            log.info('ROCrate metadata file exists: {0}'.format(self.metadata_path))
            self.metadata_exists = True
        else:
            log.error('ROCrate metadata file DOES NOT exist: {0}'.format(self.metadata_path))
            self.metadata_exists = False

        if os.path.exists(self.preview_path):
            log.info('ROCrate preview file exists: {0}'.format(self.preview_path))
            self.preview_exists = True
        else: 
            log.warning('ROCrate metadata file exists: {0}'.format(self.metadata_path))
            log.warning('Creating default preview file...')
            self.preview_exists = False
            #TODO Create default html file here. 

        # Check if those objects are valid.
        # --------------
        # TODO 
        # --------------
        return 0

def create_symlink(src, dst):
    # This creates a symbolic link on python in tmp directory
    log.debug(f'Creating symlink between {src} and {dst}')
    os.symlink(src, dst)
    return

def publish_rocrate(crate_dir): 
    # steps to follow to create the correct files to publish to GH-Pages
    log.debug('Preparing to publish ROCrate.')

    this_crate = CrateObj(crate_dir)
    this_crate.check_rocrate_valid()

    if this_crate.preview_exists:
        create_symlink(os.path.join(crate_dir, 'index.html'), this_crate.preview_path)
    if this_crate.metadata_exists:
        create_symlink(os.path.join(crate_dir, 'ro-crate-metadata.json'), this_crate.metadata_path)
    
    log.debug('ROCrate ready to publish')

if __name__ == "__main__" :
    # Rename these variables to something meaningful
    input1 = sys.argv[1]
    loglevel = sys.argv[2]

    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=getattr(logging, loglevel))
    log.setLevel(getattr(logging, loglevel))

    # The work:
    publish_rocrate('.') 