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
"""Gsrest tests for offline elements.
"""

# pylint: disable=redefined-outer-name

from gsrest.core.schema import ElementSchemaData
from gsrest.elements.workspace import WorkSpace


def test_workspace():
    "Tests for workspaces."
    wsp = WorkSpace("wsp1")
    assert hasattr(wsp, "prefix")  # nosec
    assert isinstance(wsp.attrs, ElementSchemaData)  # nosec

    wsp.isolated = True
    assert wsp.isolated  # nosec

    wsp.uri = "uri1"
    # idstr = str(wsp.xml(just_create=True))
    # expected_idstr = (
    #     "<namespace><prefix>wsp1</prefix><uri>uri1</uri></namespace>"
    # )
    # print(idstr)
    # print(expected_idstr)
    # assert idstr == expected_idstr  # nosec

    fullidstr = str(wsp.xml())
    expected_fullidstr = (
        "<namespace><prefix>wsp1</prefix><uri>uri1</uri>"
        "<isolated>true</isolated></namespace>"
    )
    assert fullidstr == expected_fullidstr  # nosec

    wspx = WorkSpace("wsp1", uri="uri1", isolated=True)
    assert wsp == wspx  # nosec
    wspy = WorkSpace("wsp1", uri="uri1", isolated=False)
    assert wsp != wspy  # nosec
