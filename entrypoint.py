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
import subprocess
import logging 

log = logging.getLogger('entrypoint') 

class CrateObj():
    def __init__(self, crate_dir):
        self.crate_dir = crate_dir
        self.metadata_path = os.path.join(self.crate_dir, 'ro-crate-metadata')  
        self.metadata_exists = False 
        self.preview_path  = os.path.join(self.crate_dir, 'ro-crate-preview.html')
        self.preview_exists = False
        self.crate_valid = None
        self.metadata_valid = None
        self.preview_valid = None

        # TODO:
        # self.preview_valid = False
        # self.metadata_valid = False

    def check_rocrate_valid(self):
        # Checks if there are rocrate objects in directory
        log.debug('Checking that rocrate files exist...') 
        if os.path.exists(os.path.join(self.metadata_path,'.json')):
            log.info('ROCrate metadata json file exists: {0}'.format(self.metadata_path))
            self.metadata_path = os.path.join(self.metadata_path,'.json')
            self.metadata_exists = True
        elif os.path.exists(os.path.join(self.metadata_path,'.jsonld')):
            log.info('ROCrate metadata jsonld file exists: {0}'.format(self.metadata_altpath))
            self.metadata_path = os.path.join(self.metadata_path,'.jsonld')
            self.metadata_exists = True
        else:
            log.error('ROCrate metadata file DOES NOT exist: {0}'.format(self.metadata_path))
            self.metadata_exists = False
            self.crate_valid = False
            exit(1)

        if os.path.exists(self.preview_path):
            log.info('ROCrate preview file exists: {0}'.format(self.preview_path))
            self.preview_exists = True
        else: 
            log.warning('ROCrate preview file DOES NOT exist: {0}'.format(self.preview_path)) 
            self.preview_exists = False
            #TODO Create default html file here. 

        # Check if those objects are valid.
        # --------------
        # TODO 
        # --------------
        # Some Test:
        self.check_metadata()
        self.check_preview()
        if self.metadata_valid and self.preview_valid:
            log.info('Crate passes validity checks.')
            self.crate_valid = True
        return 
    
    def check_metadata(self):
        log.info('Checking if metadata is valid...')
        #some test
        self.metadata_valid = True
        return

    def check_preview(self):
        log.info('Checking if preview is valid...')
        #some test
        self.preview_valid = True
        return

def create_symlink(dst, src):
    # This creates a symbolic link on python in tmp directory
    log.debug(f'Creating symlink between {src} and {dst}')
    os.symlink(src, dst)
    return

def create_preview_html(crate_obj):
    ''' 
    This uses https://github.com/UTS-eResearch/ro-crate-html-js to create a preview.html 
    from a rocrate json file. 

    rochtml rocrate_datacrate_test/ro-crate-metadata.json
    '''
    metadata_file = crate_obj.metadata_path
    subprocess.check_call(f'rochtml {metadata_file}', shell=True)

def publish_rocrate(crate_dir): 
    # steps to follow to create the correct files to publish to GH-Pages
    log.debug('Preparing to publish ROCrate.')

    this_crate = CrateObj(crate_dir)
    this_crate.check_rocrate_valid()

    if this_crate.preview_exists:
        create_symlink(os.path.join(crate_dir, 'index.html'), this_crate.preview_path)
    else: 
        #Create index.html page
        pass

    if this_crate.metadata_exists:
        ## Create symlink between the .json >> .jsonld file extensions depending on which exists
        if os.path.splitext(this_crate.metadata_path) == '.json':
            create_symlink(os.path.join(crate_dir, 'ro-crate-metadata.jsonld'), this_crate.metadata_path) 
        elif os.path.splitext(this_crate.metadata_path) == '.jsonld':
            create_symlink(os.path.join(crate_dir, 'ro-crate-metadata.json'), this_crate.metadata_path) 
    log.debug('ROCrate ready to publish')

if __name__ == "__main__" :
    # Rename these variables to something meaningful
    crate_path = sys.argv[1]
    loglevel = sys.argv[2]

    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=getattr(logging, loglevel))
    log.setLevel(getattr(logging, loglevel))

    # The work:
    publish_rocrate(crate_path) 