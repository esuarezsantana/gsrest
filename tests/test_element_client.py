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
"""Gsrest element client interface.
"""

# from gsrest.elements.style import Sld, Style
from gsrest.elements.style import Style
from gsrest.elements.workspace import WorkSpace


def test_crud_workspace(gsclient):  # pylint: disable=unused-argument
    "Test: CRUD workspace"
    wsp_name = "wsp1"
    wsp = WorkSpace(wsp_name)
    wsp.uri = "uri1"
    # UP
    wsp.sync()
    assert wsp.uri == "uri1", "Error in workspace attr properties"  # nosec
    wsp_names = WorkSpace.list()
    # pylint: disable=no-member
    assert wsp.prefix in wsp_names  # nosec
    # DOWN
    isolated_before = wsp.isolated
    wsp.isolated = not isolated_before
    wsp.sync(down=True)
    assert wsp.isolated == isolated_before  # nosec
    # DELETE
    wsp.delete()
    wsp_names = WorkSpace.list()
    assert wsp_name not in wsp_names  # nosec


#  def test_style(gsclient):
#      "Test basic Yaml Import."
#      style_name = "sty_name"
#      style = Style(name=style_name, filename="sty_filename")
#      restyle = gsclient.create(style)
#      assert restyle == style  # nosec
#      sty_names = gsclient.list(Style)
#      assert style_name in sty_names  # nosec
#      with open("tests/data/sample.sld") as sld:
#          content = sld.read()
#      styledata = Sld("sty_name", content)
#      assert styledata.identity == style_name  # nosec
#      gsclient.update(styledata)
#      resld = gsclient.read(Sld, name=style_name)
#      # does not match size, because geoserver reformats it
#      assert len(resld.content) > 1000  # nosec
#      gsclient.delete(style)
#      sty_names = gsclient.list(Style)
#      assert style_name not in sty_names  # nosec


def test_style_in_workspace(gsclient):
    "Test basic Yaml Import."
    wsp_name = "wsp1"
    sty_name = "sty1"
    wsp = WorkSpace(prefix=wsp_name, uri="uri1")
    sty = Style(name=sty_name, filename="sty_filename", workspace=wsp_name)
    wsp.sync()
    sty.sync()
    sty_names = Style.list(workspace=wsp_name)
    assert sty_names == [sty_name]  # nosec
    # with open("tests/data/sample.sld") as sld:
    #     content = sld.read()
    # styledata = Sld(sty_name, content, workspace=wsp_name)
    # gsclient.update(styledata)
    # resld = gsclient.read(Sld, name=sty_name, workspace=wsp_name)
    # # does not match size, because geoserver reformats it
    # assert len(resld.content) > 1000  # nosec
    # # probar a borrar el workspace
    # gsclient.delete(sty)
    # sty_names = gsclient.list(Style)
    # assert sty_name not in sty_names  # nosec
    # # TODO: make an specialized test for recurse deletion
    wsp.delete(recurse=True)
    wsp_names = WorkSpace.list()
    assert wsp_name not in wsp_names  # nosec
