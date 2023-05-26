# ROcrate-to-pages

This is a gh-action to generate a GitHub Pages site from a github repo containing a RO-Crate.

## index

- [index](#index)
- [Overview of the action](#overview-of-the-action)
- [Usage](#usage)
- [Example config.yml](#example-configyml)
- [Outputs](#outputs)
- [License](#license)

## Overview of the action

![global_overview_action](documentation/global_overview_action.svg)

## Usage

Construct a config.yml file using the flowchart below. The config.yml file should be in the root of the repo.

![flowchart](documentation/decision_tree_config_yml.svg)

### action part

```yaml
- name: RO-Crate to Pages
  uses:
    - ro-crate-to-pages@v1
    with:
        config: .config.yml
```

### full workflow example

full yml example of a workflow file that will run the action on push 

```yaml
name: RO-Crate to Pages
on:
  push:
    branches:
      - main
jobs:
    build:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout
            uses: actions/checkout@v3
        - name: RO-Crate to Pages
            uses: vliz-be-opsci/rocrate-to-pages@latest
            with:
              config: .config.yml
        # Deploy to GH-Pages branch
        - name: Deploy
            uses: peaceiris/actions-gh-pages@v3
            with:
              github_token: ${{ secrets.GITHUB_TOKEN }}
              publish_dir: ./unicornpages
```

## Example config.yml

### example config.yml explanation

- `multiple_rocrates`: if true, the action will look for multiple rocrates in the repo, and generate a page for each of them. If false, it will only look for one rocrate in the repo, and generate a page for that one.
- `RELEASE_management`: if true, the action will look for a release, and generate a page for that release. If false, it will generate a page for the latest commit on the main branch.

- `RELEASE_verioning`: if `RELEASE_management` is true, this will determine how the action will look for the release. If `tag`, it will look for the latest release by tag. If `release`, it will look for the latest release by release. 
- `INCLUDE_draft`: if `RELEASE_management` is true, this will determine if the action will include the draft release. If `true`, it will include the draft release. If `false`, it will not include the draft release.
- index_html: if `true`, the action will generate an index.html file for each rocrate. If `false`, it will not generate an index.html file for each rocrate.
- draft_folder_name: if `RELEASE_management` is true, and `INCLUDE_draft` is true, this will determine the name of the folder for the draft release. If `draft`, the folder will be named `draft`. If `draft_release`, the folder will be named `draft_release`.

!**important note: multiple_rocrates and RELEASE_management are mutually exclusive. If multiple_rocrates is true, RELEASE_management will be ignored.**!

### config.yml examples

#### config.yml example 1

1. `multiple_rocrates`: false
2. `RELEASE_management`: true
3. `RELEASE_versioning`: tag
4. `INCLUDE_draft`: true
5. `index_html`: true
6. `draft_folder_name`: draft

```yaml
# config.yml
multiple_rocrates: false
RELEASE_management: true
RELEASE_versioning: tag #by major tag or by release
INCLUDE_draft: true #include draft release which is the latest commit on the main branch 
index_html: true #generate an index.html file for each rocrate
draft_folder_name: draft #name of the folder for the draft release
```

#### config.yml example 2

1. `multiple_rocrates`: true
2. `RELEASE_management`: false
3. `index_html`: false


```yaml

# config.yml
multiple_rocrates: true
RELEASE_management: false
index_html: false
```

## Outputs

The action will generate documents for the gh-pages branch.
Depending on the configuration, the action will generate a page for each rocrate in the repo, or a page for the latest release.

### Outputs example
 
#### Outputs example 1

1. `multiple_rocrates`: false
2. `RELEASE_management`: true
3. `RELEASE_verioning`: tag
4. `INCLUDE_draft`: true
5. `index_html`: true

```yaml
# outputs
gh-pages (branch)
    - 0.1 (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
    - 0.2 (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
    - draft (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
    - index.html
```

#### Outputs example 2

1. `multiple_rocrates`: true
2. `RELEASE_management`: false
3. `index_html`: false

```yaml
# outputs
gh-pages (branch)
    - rocrate1 (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
    - rocrate2 (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
    - rocrate3 (folder)
        - index.html
        - ro-crate-metadata.jsonld
        - ro-crate-preview.html
        - all_folders_and_files_in_repo
```

## License

The action and documentation in this project are released under the [MIT License](LICENSE)
