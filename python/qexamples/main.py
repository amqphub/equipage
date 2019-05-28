#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import commandant as _commandant
import plano as _plano
import sys as _sys

_description = "Build messaging example projects"

_epilog = """
operations:
  list        Show the available example projects
  build       Copy the example projects to a working directory and build them
  clean       Clean the project working directories

example usage:
  $ qexamples list
  $ qexamples build qpid-jms    # Build the 'qpid-jms' project
  $ qexamples clean qpid-jms    # Clean up build artifacts for the 'qpid-jms' project
"""

_call = _plano.call
_join = _plano.join
_working_dir = _plano.working_dir

class ExamplesCommand(_commandant.Command):
    def __init__(self, home):
        super(ExamplesCommand, self).__init__(home, "qexamples")

        self.description = _description.lstrip()
        self.epilog = _epilog.lstrip()

        self.add_argument("operation", metavar="OPERATION",
                          choices=["list", "build", "clean"],
                          help="Either 'list', 'build', or 'clean'. "
                          "See the 'operations' section below.")
        self.add_argument("projects", metavar="PROJECT", nargs="*",
                          help="A named project containing example programs. "
                          "If no projects are specified, the operation is applied to all of them.")

        self.projects = [
            _PooledJms(self, "pooled-jms"),
            _QpidJms(self, "qpid-jms"),
            _QpidProtonCpp(self, "qpid-proton-cpp"),
            _QpidProtonPython(self, "qpid-proton-python"),
            _QpidProtonRuby(self, "qpid-proton-ruby"),
            _Rhea(self, "rhea"),
            _VertxProton(self, "vertx-proton"),
        ]

    def init(self):
        super(ExamplesCommand, self).init()

        self.operation = self.args.operation

        # XXX Check for bad project names

        if self.args.projects:
            self.selected_projects = [x for x in self.projects if x.name in self.args.projects]
        else:
            self.selected_projects = self.projects

    def run(self):
        if self.operation == "list":
            print("{0:20} {1}".format("NAME", "SOURCE"))

            for project in self.selected_projects:
                print("{0:20} {1}".format(project.name, project.source_dir))

        if self.operation == "build":
            for project in self.selected_projects:
                _plano.copy(project.source_dir, project.work_dir)

                with _working_dir(project.work_dir):
                    project.build()

        if self.operation == "clean":
            for project in self.selected_projects:
                with _working_dir(project.work_dir):
                    project.clean()

class _Project:
    def __init__(self, command, name):
        self.command = command
        self.name = name

        self.source_dir = _join(self.command.home, name)
        self.work_dir = _join(_plano.get_user_temp_dir(), "qexamples", name)

    def build(self):
        pass

    def clean(self):
        pass

class _MavenProject(_Project):
    def build(self):
        _call("mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests")

    def clean(self):
        _call("mvn clean")

class _PooledJms(_MavenProject):
    pass

class _QpidJms(_MavenProject):
    pass

class _QpidProtonCpp(_Project):
    def build(self):
        _call("make build")

    def clean(self):
        _call("make clean")

class _QpidProtonPython(_Project):
    def clean(self):
        for path in _plano.find("*.pyc"):
            _plano.remove(path)

class _QpidProtonRuby(_Project):
    pass

class _Rhea(_Project):
    pass

class _VertxProton(_MavenProject):
    pass
