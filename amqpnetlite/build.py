#!/usr/bin/python3

import os
import fnmatch
import subprocess

project_dirs = list()

for root, dirs, files in os.walk("."):
    if fnmatch.filter(files, "*.csproj"):
        project_dirs.append(root)

for project_dir in project_dirs:
    subprocess.check_call(["dotnet", "build", project_dir])
