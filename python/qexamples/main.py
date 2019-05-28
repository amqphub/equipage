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
example usage:
  $ qexamples list-projects
  $ qexamples build qpid-jms
  $ qexamples clean qpid-jms
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
                          choices=["list-projects", "build", "clean"],
                          help="'list-projects', 'build', or 'clean'")
        self.add_argument("projects", metavar="PROJECT", nargs="*",
                          help="A named project containing example programs")

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
        if self.operation == "list-projects":
            for project in self.selected_projects:
                print(project.name)

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
        self.work_dir = _join(_plano.user_temp_dir(), "qexamples", name)

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
