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
"""Gsrest client tests
"""

# pylint: disable=redefined-outer-name

import pytest  # type: ignore

from gsrest import client, yaml
from gsrest.elements import style, workspace


def test_readiness(gsclient):
    "Test: readiness"
    assert gsclient.ready()  # nosec


def test_list_workspaces(gsclient):
    "Test: list workspaces"
    wsp_names = gsclient.list(workspace.WorkSpace)
    assert isinstance(wsp_names, list)  # nosec
    # First time this list will be empty
    assert not bool(wsp_names)  # nosec


def test_crud_workspace(gsclient):
    "Test: CRUD workspace"
    # CREATE
    wsp = workspace.WorkSpace("wsp1")
    wsp.uri = "uri1"
    # create will perform an implicit read
    gsclient.create(wsp)
    wsp = gsclient.read(wsp)
    assert isinstance(wsp, workspace.WorkSpace)  # nosec
    assert wsp.uri == "uri1", "Error in workspace attr properties"  # nosec
    # LIST
    wsp_names = gsclient.list(workspace.WorkSpace)
    assert wsp.prefix in wsp_names  # nosec
    with pytest.raises(client.GsElementAlreadyExists):
        gsclient.create(wsp)
    wsp = workspace.WorkSpace("wsp2")
    with pytest.raises(client.GsElementMissingInfo):
        gsclient.create(wsp)
    # READ
    wsp = gsclient.read(workspace.WorkSpace, "wsp1")
    assert isinstance(wsp, workspace.WorkSpace)  # nosec
    assert wsp.uri == "uri1"  # nosec
    with pytest.raises(client.GsElementDoesNotExist):
        gsclient.read(workspace.WorkSpace, "wsp2")
    # UPDATE
    isolated_after = not wsp.isolated
    wsp.isolated = isolated_after
    gsclient.update(wsp)
    wsp = gsclient.read(workspace.WorkSpace, "wsp1")
    assert wsp.isolated == isolated_after  # nosec
    # DELETE
    gsclient.delete(workspace.WorkSpace, "wsp1")
    wsp_names_after = gsclient.list(workspace.WorkSpace)
    assert "wsp1" not in wsp_names_after  # nosec


def test_style(gsclient):
    "Test Style."
    style_name = "sty_name"
    mystyle = style.Style(name=style_name, filename="sty_filename")
    gsclient.create(mystyle)
    restyle = gsclient.read(mystyle)
    assert restyle == mystyle  # nosec
    sty_names = gsclient.list(style.Style)
    assert style_name in sty_names  # nosec
    with open("tests/data/sample.sld") as sld:
        content = sld.read()
    styledata = style.Sld10("sty_name", content)
    assert styledata.identity == style_name  # nosec
    gsclient.update(styledata)
    resld = gsclient.read(style.Sld10, name=style_name)
    # does not match size, because geoserver reformats it
    assert len(resld.content) > 1000  # nosec
    gsclient.delete(mystyle)
    sty_names = gsclient.list(style.Style)
    assert style_name not in sty_names  # nosec


def test_style_in_workspace(gsclient):
    "Test element (style) in workspace."
    wsp_name = "wsp1"
    sty_name = "sty1"
    wsp = workspace.WorkSpace(prefix=wsp_name, uri="uri1")
    gsclient.create(wsp)
    wsp = gsclient.read(wsp)
    sty = style.Style(
        name=sty_name, filename="sty_filename", workspace=wsp_name
    )
    gsclient.create(sty)
    sty_names = gsclient.list(style.Style, workspace=wsp_name)
    assert sty_names == [sty_name]  # nosec
    with open("tests/data/sample.sld") as sld:
        content = sld.read()
    styledata = style.Sld10(sty_name, content, workspace=wsp_name)
    gsclient.update(styledata)
    resld = gsclient.read(style.Sld10, name=sty_name, workspace=wsp_name)
    # does not match size, because geoserver reformats it
    assert len(resld.content) > 1000  # nosec
    # probar a borrar el workspace
    gsclient.delete(sty)
    sty_names = gsclient.list(style.Style)
    assert sty_name not in sty_names  # nosec
    # TODO: make an specialized test for recurse deletion
    gsclient.delete(wsp, query={"recurse": "true"})
    wsp_names = gsclient.list(workspace.WorkSpace)
    assert wsp_name not in wsp_names  # nosec


def test_yaml(gsclient):
    "Test basic Yaml Import."
    elems = yaml.read("tests/data/sample_elems.yml")
    elems.sync()
    workspace_names = gsclient.list(workspace.WorkSpace)
    assert "yaml_wsp_name" in workspace_names  # nosec
