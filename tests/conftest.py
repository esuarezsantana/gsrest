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
"""Pytest general fixtures.
"""

import pytest  # type: ignore

from gsrest import client
from gsrest.core import url

# Just in case you start docker from the Makefile:
#
#     @pytest.fixture(scope="session")
#     def gsclient():
#         """Ensure that Geoserver API is up and responsive."""
#         client = GsClient()
#         return client

# Just in case you copy-paste to interactive interpreter.
#
#     xxxxxxxxxxxxxxxxxxxxxx  # void current command
#     python
#     exit()
#     poetry run python
#
#     gsclient = GsClient()
#     gsclient.base_url = url.gs_base_url(port=48080, context='my/geoserver'))
#     import logging
#     logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="module")
def pause_when_finished(pytestconfig):
    "It just stop tests when finished until enter is pressed."
    yield
    capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")
    capmanager.suspend_global_capture(in_=True)
    print()
    input("Ready for manual inspection, press enter when finished...")  # nosec
    capmanager.resume_global_capture()


@pytest.fixture(scope="session")
def gsclient(docker_ip, docker_services):
    """Ensure that Geoserver API is up and responsive."""
    port = docker_services.port_for("geoserver", 8080)
    myclient = client.GsClient()
    myclient.base_url = url.gs_base_url(host=docker_ip, port=port)
    docker_services.wait_until_responsive(
        check=myclient.ready, timeout=30.0, pause=2.0
    )
    return myclient


# Just in case you use your own instance.
#
#
#     @pytest.fixture(scope="session")
#     def gsclient():
#         """Ensure that Geoserver API is up and responsive."""
#         myclient = client.GsClient()
#         myclient.base_url = url.gs_base_url(
#             host="localhost", port=48080, context="my/geoserver"
#         )
#         # from gsrest import ops
#         # ops.Ops.purge()
#         yield myclient
#         # ops.Ops.purge()
