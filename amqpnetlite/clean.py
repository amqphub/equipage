#!/usr/bin/python3

import os
import fnmatch
import shutil

project_dirs = list()

for root, dirs, files in os.walk("."):
    if fnmatch.filter(files, "*.csproj"):
        project_dirs.append(root)

for project_dir in project_dirs:
    shutil.rmtree(os.path.join(project_dir, "bin"))
    shutil.rmtree(os.path.join(project_dir, "obj"))
