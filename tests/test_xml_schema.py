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
"""Tests for attributes and xml.
"""

from xml.etree import ElementTree as Et  # nosec

from gsrest.xml import converter as c
from gsrest.xml import schema


def test_schemadata():
    "Tests for SchemaData."
    scdx = schema.SchemaData(schema.Schema(attr1={}, attr2={}))
    assert hasattr(scdx, "attr1")  # nosec
    assert hasattr(scdx, "attr2")  # nosec
    scdx.attr1 = "val1"
    scdx.attr2 = "val2"
    assert scdx.attr1 == "val1"  # nosec
    assert scdx.attr2 == "val2"  # nosec
    scdy = schema.SchemaData(schema.Schema(attr1={}, attr2={}))
    scdy.attr1 = "val1"
    scdy.attr2 = "val2"
    assert scdx == scdy  # nosec


DIMENSION_SCHEMA = dict(
    name={},
    description={},
    range={
        "converter": schema.Schema(
            min=schema.SchemaItem("min", c.DoubleConverter),
            max=dict(converter=c.DoubleConverter),
        ),
    },
    null_values=schema.SchemaItem(
        ["nullValues", {"tag": "double", "many": True}], c.DoubleConverter,
    ),
    dimension_type={"path": "dimensionType/name"},
)

SCHEMA = schema.Schema(
    dimensions={
        "path": ["dimensions", {"tag": "coverageDimension", "many": True}],
        "converter": DIMENSION_SCHEMA,
    }
)


def test_schema_read():
    "Test schema read"
    coverage_reduced_xml = """\
<coverage>
  <dimensions>
    <coverageDimension>
      <name>elhierro</name>
      <description>GridSampleDimension[-3.4,3.4]</description>
      <range>
        <min>-3.8</min>
        <max>3.8</max>
      </range>
      <nullValues>
        <double>25.0</double>
      </nullValues>
      <dimensionType>
        <name>REAL_32BITS</name>
      </dimensionType>
    </coverageDimension>
  </dimensions>
</coverage>
"""
    root = Et.XML(coverage_reduced_xml)
    data = SCHEMA.from_node(root)
    assert "dimensions" in data  # nosec
    assert isinstance(data["dimensions"], list)  # nosec
    assert "null_values" in data["dimensions"][0]  # nosec
    assert isinstance(data["dimensions"][0]["null_values"], list)  # nosec
    assert isinstance(data["dimensions"][0]["null_values"][0], float)  # nosec


def test_schema_write():
    "Test schema write"
    dimension_data = {
        "name": "dim1",
        "description": "desc1",
        "range": {"min": 0.1, "max": 0.9},
        "null_values": [3, 5],
        "dimension_type": "REAL",
    }
    ddata2coverage_xml = (
        "<coverage><dimensions><coverageDimension>"
        "<name>dim1</name><description>desc1</description>"
        "<range><min>0.1</min><max>0.9</max></range>"
        "<nullValues><double>3</double><double>5</double></nullValues>"
        "<dimensionType><name>REAL</name></dimensionType>"
        "</coverageDimension></dimensions></coverage>"
    )
    root = Et.Element("coverage")
    SCHEMA.to_node({"dimensions": [dimension_data]}, root)
    xml = Et.tostring(root, encoding="unicode")
    assert ddata2coverage_xml == xml  # nosec
