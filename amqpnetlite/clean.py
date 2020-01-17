#!/usr/bin/python3

import os
import fnmatch
import shutil

project_dirs = list()

for root, dirs, files in os.walk("."):
    if fnmatch.filter(files, "*.csproj"):
        project_dirs.append(root)

for project_dir in project_dirs:
    bin_path = os.path.join(project_dir, "bin")
    obj_path = os.path.join(project_dir, "obj")

    if (os.path.exists(bin_path)):
        shutil.rmtree(bin_path)

    if (os.path.exists(obj_path)):
        shutil.rmtree(obj_path)
