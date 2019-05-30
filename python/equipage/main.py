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
import equipage.tests as _tests
import sys as _sys

_description = "Build and test messaging example projects"

_epilog = """
operations:
  list        Show the available example projects
  build       Copy the example projects to a working directory and build them
  test        Run tests against the examples
  clean       Clean the project working directories

example usage:
  $ equipage list
  $ equipage build qpid-jms    # Build the 'qpid-jms' project
  $ equipage test qpid-jms     # Run tests for the 'qpid-jms' project
  $ equipage clean qpid-jms    # Clean up build artifacts for the 'qpid-jms' project
"""

_call = _plano.call
_join = _plano.join
_working_dir = _plano.working_dir

class EquipageCommand(_commandant.Command):
    def __init__(self, home):
        super(EquipageCommand, self).__init__(home, "equipage")

        self.work_dir = _join(_plano.get_user_temp_dir(), "equipage")

        self.description = _description.lstrip()
        self.epilog = _epilog.lstrip()

        subparsers = self.add_subparsers()

        list_parser = subparsers.add_parser("list")
        list_parser.set_defaults(func=self.list_command)

        build_parser = subparsers.add_parser("build")
        self.add_project_args(build_parser)
        build_parser.set_defaults(func=self.build_command)

        test_parser = subparsers.add_parser("test")
        self.add_project_args(test_parser)
        test_parser.set_defaults(func=self.test_command)

        clean_parser = subparsers.add_parser("clean")
        self.add_project_args(clean_parser)
        clean_parser.set_defaults(func=self.clean_command)

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
        super(EquipageCommand, self).init()

        if "func" not in self.args:
            _plano.exit("Missing subcommand")

    def run(self):
        self.args.func()

    def list_command(self):
        print("{0:20} {1}".format("NAME", "SOURCE"))

        for project in self.projects:
            print("{0:20} {1}".format(project.name, project.source_dir))

    def build_command(self):
        for project in self.get_selected_projects():
            project.build()

    def test_command(self):
        for project in self.get_selected_projects():
            project.test()

    def clean_command(self):
        for project in self.get_selected_projects():
            project.clean()

    def add_project_args(self, parser):
        parser.add_argument("projects", metavar="PROJECT", nargs="*",
                            help="A named project containing example programs. "
                            "If no projects are specified, the operation is applied to all of them.")

    def get_selected_projects(self):
        if self.args.projects:
            return [x for x in self.projects if x.name in self.args.projects]
        else:
            return self.projects

class _Project(object):
    def __init__(self, command, name):
        self.command = command
        self.name = name

        self.source_dir = _join(self.command.home, name)
        self.work_dir = _join(self.command.work_dir, name)

    def build(self):
        _plano.remove(self.work_dir)
        _plano.copy(self.source_dir, self.work_dir)

    def clean(self):
        pass

    def test(self):
        self.build()

        pattern = "test_{0}*".format(self.name.replace("-", "_"))

        _call("equipage-test {0}", pattern)

class _MavenProject(_Project):
    def build(self):
        super(_MavenProject, self).build()

        with _working_dir(self.work_dir):
            _call("mvn package dependency:copy-dependencies -DincludeScope=runtime -DskipTests")

    def clean(self):
        with _working_dir(self.work_dir):
            _call("mvn clean")

class _PooledJms(_MavenProject):
    pass

class _QpidJms(_MavenProject):
    pass

class _QpidProtonCpp(_Project):
    def build(self):
        super(_QpidProtonCpp, self).build()

        with _working_dir(self.work_dir):
            _call("make build")

    def clean(self):
        with _working_dir(self.work_dir):
            _call("make clean")

class _QpidProtonPython(_Project):
    def clean(self):
        with _working_dir(self.work_dir):
            for path in _plano.find("*.pyc"):
                _plano.remove(path)

class _QpidProtonRuby(_Project):
    pass

class _Rhea(_Project):
    pass

class _VertxProton(_MavenProject):
    pass
