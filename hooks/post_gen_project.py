"""
    Given that this cookiecutter will run to create a pipeline
    to an existing project we will remove the generated folder
    and copy only what we are interested in.
"""

from __future__ import print_function

import os
import shutil

TERMINATOR = "\x1b[0m"
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "
HINT = "\x1b[3;33m"


def copy_files_to(path):
    filenames = ["buildspec.yaml", "pipeline.yaml",
                 "Pipeline-Instructions.md", "pipeline-sample.png"]
    buildspec_exists = os.path.join(path, 'buildspec.yaml')

    # Don't override buildspec if one exists in the current folder
    if os.path.isfile(buildspec_exists):
        filenames.pop(0)
        print(INFO + "Ignoring buildspec.yaml copy as one already exists" +
              TERMINATOR)

    for file in filenames:
        if os.path.isfile(file):
            print(INFO + "Copying {} to current directory...".format(file) +
                  TERMINATOR)
            shutil.copy(file, path)

    return True


def remove_generated_project(path):
    if os.path.exists(path):
        print(INFO + "Cleaning up leftovers..." + TERMINATOR)
        shutil.rmtree(path)
    else:
        print(HINT + "Folder {} doesn't exist... aborting clean up".format(
            path) + TERMINATOR)

    return True


def main():

    project_folder = os.getcwd()
    parent_folder = os.path.abspath(os.path.dirname(project_folder))

    # Don't touch generated files if we are running a functional test
    if "--pytest-cookies--" in '{{ cookiecutter.project_name }}':
        return

    if copy_files_to(parent_folder):
        if remove_generated_project(project_folder):
            print(SUCCESS + "Project initialized successfully!" + TERMINATOR)


if __name__ == '__main__':
    main()
