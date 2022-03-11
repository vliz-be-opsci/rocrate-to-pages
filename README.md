# Github Action to publish rocrate objects as Github Pages
This takes the [files files from research object](https://www.researchobject.org/) and publishes them as a github pages. This allows the human readable preview file to be hosted as a html page and the machine readable json file to be reachable from anywhere. 

## Steps
This action is to be used on git projects that include rocrate files that comply to the [rocrate standard](https://www.researchobject.org/ro-crate/1.0/):

  - The project *must* include a metadata file named "ro-crate-metadata.jsonld"
  - The project *may* include a human-readable preview file that *must* be called "ro-crate-preview.html"
  - In this first iteration of the action it is assumed that the preview file does exist. In future versions a fallback process could create a standard preview file using the metadata file. 
   
Gitlab pages routes traffic to an "index.html" file by default and is incapable of handling content negotiation. Due to these (and other) GL-Pages limitations the following steps are taken:
  
  - Some preperation steps are handled by other actions
  - A symbolic link is created that maps an "index.html" file to "ro-crate-preview.html"
  - A symbolic link is created that maps "ro-crate-metadata.json" to "ro-crate-metadata.jsonld"
  - Some publishing and cleanup steps are handled by other actions

## Example

Below is an example yaml file that once copied to "/.github/workflow/rocrate_to_pages.yml" would trigger the publishing to github pages action on push to the "main" branch.

```yml

name: RoCrate to GitHub Pages
on:
  push:
    branches:
      - main  # Set a branch name to trigger deployment
  pull_request:
jobs:
  deploy:
    runs-on: ubuntu-20.04
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
    steps:
      - uses: actions/checkout@v2
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod
          
      - name: Setup Python
        uses: actions/setup-python@v3
        with: 
          python-version: '3.x'

      - name: Build Pages
        uses: vliz-be-opsci/rocrate-to-pages

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: ${{ github.ref == 'refs/heads/main' }}
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public

```


## Other files in this project:
### Dockerfile

The `Dockerfile` in this template pulls an image that
includes Python, and then sets the entrypoint to `entrypoint.py`.
If you rename `entrypoint.py` (or need additional files) then
don't forget to edit the `Dockerfile`.

Additionally, you will need to decide which docker image to start
with. There are two that I commonly use that I also maintain,
both of which can be pulled from either Docker Hub or the Github Container
Registry. Uncomment/comment as appropriate in the Dockerfile
as desired. Or if you'd rather not pull one of my images, you can 
see the source repository for the details.  Here are the options
found in the Dockerfile comments:
* An image with Alpine Linux and Python only to keep image small for fast loading: `FROM cicirello/pyaction-lite:3`
* An image with Alpine Linux, Python, and git, which is also relatively small: `FROM cicirello/pyaction:3`
* Beginning with version 4, the pyaction image no longer uses Alpine as the 
  base. It now uses python:3-slim, which is built on Debian (the slim version is 
  small but not nearly as small as Alpine), on
  which we have installed the GitHub CLI : `FROM cicirello/pyaction:4`
* To pull from the Github Container Registry instead of Docker Hub: `FROM ghcr.io/cicirello/pyaction:4` (and likewise for the other images).

The source repositories for these images:
* https://github.com/cicirello/pyaction-lite
* https://github.com/cicirello/pyaction

### action.yml

Edit the `action.yml` file to define your action's inputs and outputs
(see examples in the file).

### entrypoint.py

You can rename this Python file to whatever you want, provided you change
its name in all other files above that reference it.  The template version
includes examples of accessing Action inputs and producing outputs.  Make
sure it is executable (the one in the template is already executable). If
you simply rename the file, it should keep the executable bit set. However,
if you delete it and replace it with a new file, you'll need to set it
executable.

### tests/tests.py

Python unit test cases could go here.

### tests/integration.py

Ideally, after unit testing the Python functions, methods, 
etc (see above), you should also test the action itself.
This involves running the action locally in a workflow
within the action's own repository. If the action generates
any files, or alters any files, then you can add a step
to run the tests in `tests/integration.py` to validate the
action's output. Although you don't necessarily need to do
this with Python, it may be convenient since Python would
already be configured in your workflow. 

### .github/workflows/build.yml

This workflow runs on pushes and pull requests against the main branch. It
executes all Python unit tests (see tests/tests.py section above). It verifies that
the docker image for the GitHub Action builds. It then executes the GitHub Action
locally against the action's own repository, as an integration test. Finally, it 
executes the tests in `tests/integration.py` (see earlier section) to validate
any files created or edited by the integration test. You might also add a step
to the workflow to test that outputs are correct as well. 
