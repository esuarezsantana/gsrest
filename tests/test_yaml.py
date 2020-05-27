# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Gsrest YAML tests
"""

from gsrest.elements import workspace
from gsrest import yaml

# pylint: disable=redefined-outer-name


def test_yaml():
    "Test basic Yaml Import."
    elems = yaml.read("tests/data/sample_elems.yml")
    wsp = next(iter(elems))
    assert isinstance(wsp, workspace.WorkSpace)  # nosec
    assert wsp.prefix == "yaml_wsp_name"  # nosec
