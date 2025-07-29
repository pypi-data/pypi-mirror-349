# Copyright 2025, European Centre for Medium-Range Weather Forecasts (ECMWF)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, List
from unittest.mock import Mock

import pytest
from ipywidgets import Output, ToggleButton, VBox

from ecmwf.jupyter_components.jupyter_forms import DssDownloadForm


@pytest.fixture
def mock_client() -> Mock:
    mock = Mock()

    # Create two pages of collections
    page2 = Mock()
    page2.collection_ids = ["dataset2"]
    page2.next = None

    page1 = Mock()
    page1.collection_ids = ["dataset1"]
    page1.next = page2

    mock.get_collections.return_value = page1

    mock.get_collection.return_value = Mock(
        form=[
            {
                "name": "var",
                "type": "StringListWidget",
                "label": "Variables",
                "details": {
                    "labels": {"t2m": "2m temperature", "u10": "10m wind"},
                    "values": ["t2m", "u10"],
                    "default": ["t2m"],
                    "columns": 2,
                },
            }
        ],
        apply_constraints=lambda sel: {"var": ["t2m", "u10"]},
        title="Test Dataset",
    )
    return mock


# @pytest.mark.skipif(not _IPYWIDGETS, reason="ipywidgets is not available")
def test_form_initialization(mock_client: Mock) -> None:
    form = DssDownloadForm(client=mock_client)
    assert form.client == mock_client
    assert isinstance(form.output, Output)
    assert form.collection_widget.options == ("dataset1", "dataset2")
    assert form.collection_id is None
    assert form.request == {}


# @pytest.mark.skipif(not _IPYWIDGETS, reason="ipywidgets is not available")
def test_collection_selection_triggers_build(mock_client: Mock) -> None:
    form = DssDownloadForm(client=mock_client)
    form.collection_widget.value = "dataset1"
    assert form.collection_id == "dataset1"
    assert "var" in form.widget_defs
    widget = form.widget_defs["var"]
    assert isinstance(widget, VBox)


# @pytest.mark.skipif(not _IPYWIDGETS, reason="ipywidgets is not available")
def test_widget_creation_from_metadata(mock_client: Mock) -> None:
    form = DssDownloadForm(client=mock_client)
    form._build_form("dataset1")

    widget = form.widget_defs["var"]
    assert hasattr(widget, "_get_value")

    # Simulate ToggleButton click
    gridbox = widget.children[1]
    buttons = gridbox.children
    assert isinstance(buttons[0], ToggleButton)

    buttons[0].value = True  # Simulate user clicking
    value = widget._get_value()
    assert value == ["t2m"]


# @pytest.mark.skipif(not _IPYWIDGETS, reason="ipywidgets is not available")
def test_static_form_parser_filters() -> None:
    form: List[Dict[str, Any]] = [
        {
            "name": "format",
            "type": "LicenceWidget",  # Ignored
        },
        {
            "name": "valid",
            "type": "StringChoiceWidget",
            "label": "Choose one",
            "details": {"labels": {"a": "A", "b": "B"}, "values": ["a", "b"]},
        },
    ]
    dummy = DssDownloadForm(
        url="https://cds.climate.copernicus.eu/api",
        key="00112233-4455-6677-c899-aabbccddeeff",  # Public test key
    )
    parsed = dummy._form_json_to_widgets_dict(form)
    assert "valid" in parsed
    assert parsed["valid"]["type"] == "radio"
    assert "format" not in parsed
