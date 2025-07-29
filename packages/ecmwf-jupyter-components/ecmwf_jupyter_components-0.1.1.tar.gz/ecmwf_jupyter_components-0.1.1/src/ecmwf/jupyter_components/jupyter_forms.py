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

import abc
import json
from typing import Any, Callable, Dict, List, Optional

import cdsapi
import ipywidgets as widgets
from IPython.display import clear_output as _clear_output
from IPython.display import display as _display

from ecmwf.datastores import Client as DssClient
from ecmwf.datastores import Collections as DssCollections


# Override IPython methods with typeset version
def clear_output(*args: Any, **kwargs: Any) -> None:
    return _clear_output(*args, **kwargs)  # type: ignore


def display(*args: Any, **kwargs: Any) -> None:
    return _display(*args, **kwargs)  # type: ignore


# Abstract base class for download forms
class AbstractDownloadForm(abc.ABC):
    """Abstract base class for download forms.

    This class provides a common interface for creating and managing download forms.
    It is not intended to be used directly.
    """

    @abc.abstractmethod
    def __init__(self) -> None:
        """Initialize the download form."""
        pass

    @abc.abstractmethod
    def _build_form(self, collection_id: str) -> None:
        """Build the form for the specified collection ID.

        This method should be implemented by subclasses to create the form widgets
        based on the collection's metadata.
        """
        pass

    @abc.abstractmethod
    def debug(self) -> None:
        """Print the current internal state of the form."""
        pass


class DownloadForm(AbstractDownloadForm):
    """Abstract base class for download forms.

    This class provides a common interface for creating and managing download forms.
    It is not intended to be used directly.
    """

    def __init__(self) -> None:
        raise NotImplementedError("This is an abstract base class.")

    def _build_form(self, collection_id: str) -> None:
        """Build the form for the specified collection ID.

        This method should be implemented by subclasses to create the form widgets
        based on the collection's metadata.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


class DssDownloadForm(DownloadForm):
    """Interactive selection form for collections in a Jupyter Notebook using ipywidgets.

    Automatically builds form widgets from a collection's metadata and tracks user selections.
    """

    def __init__(
        self,
        client: DssClient | None = None,
        output: Optional[widgets.Output] = None,
        **client_kwargs: Any,
    ) -> None:
        if client is None:
            try:
                client = DssClient(**client_kwargs)
            except FileNotFoundError:
                try:
                    client = cdsapi.Client(**client_kwargs).client
                except Exception:
                    raise ValueError(
                        "No DSS client provided and no default client found."
                    )
        if isinstance(client, cdsapi.Client):
            client = client.client
        assert client is not None, "client must be a DssClient instance"

        self.client: DssClient = client
        self.output: widgets.Output = output or widgets.Output()
        self.collection_id: Optional[str] = None
        self.request: Dict[str, str | list[str]] = {}

        self.collection_widget: widgets.Dropdown = widgets.Dropdown(
            options=self.collections,
            description="Dataset",
            value=None,
        )
        self.widget_defs: Dict[str, widgets.Widget] = {}
        self.selection_output: widgets.Output = widgets.Output()

        self.main_box = widgets.Box(
            [self.output], layout=widgets.Layout(position="relative")
        )

        self.collection_widget.observe(self._on_collection_change, names="value")

        self._display_initial_prompt()
        self._update_selection_state()
        display(self.main_box)

    @property
    def collections(self) -> List[str]:
        """Return the list of available collection IDs."""
        collection_ids: List[str] = []
        collections: DssCollections | None = self.client.get_collections(sortby="id")
        while collections is not None:
            collection_ids += collections.collection_ids
            collections = collections.next
        return collection_ids

    def _display_initial_prompt(self) -> None:
        self.output.clear_output()
        with self.output:
            display(
                widgets.VBox(
                    [
                        widgets.HTML("<b>Select a dataset to begin</b>"),
                        self.collection_widget,
                    ]
                )
            )

    def _build_form(self, collection_id: str) -> None:
        self.output.clear_output()
        self.selection_output.clear_output()
        self.widget_defs.clear()
        self.request = {}

        with self.output:
            display(widgets.HTML("Please wait while your download form is created..."))

        collection = self.client.get_collection(collection_id)
        form_widgets: Dict[str, Dict[str, Any]] = self._form_json_to_widgets_dict(
            collection.form
        )

        def update_selection_display() -> None:
            with self.selection_output:
                self.selection_output.clear_output()
                print(f"dataset = {self.collection_id}")
                print(f"request = {self._pretty_request(self.request)}")

        def on_change(change: Dict[str, Any]) -> None:
            for key, widget in self.widget_defs.items():
                if hasattr(widget, "_get_value"):
                    self.request[key] = widget._get_value()
            allowed_options: Dict[str, List[str]] = collection.apply_constraints(
                {k: v for k, v in self.request.items() if v}
            )

            for key, values in allowed_options.items():
                f_widget: Dict[str, Any] = form_widgets.get(key, {})
                labels: Dict[str, str] = f_widget.get("labels", {})
                if key in self.widget_defs:
                    widget = self.widget_defs[key]
                    if hasattr(widget, "children") and isinstance(
                        widget.children[1], widgets.GridBox
                    ):
                        for tb in widget.children[1].children:
                            tb.layout.display = "none"
                        for tb, opt in zip(
                            widget.children[1].children, f_widget["values"]
                        ):
                            if opt in values:
                                tb.layout.display = ""
                    elif isinstance(widget, widgets.RadioButtons):
                        widget.options = [(labels.get(v, v), v) for v in values]
                        if widget.value not in values:
                            widget.value = None
                    elif isinstance(widget, widgets.SelectMultiple):
                        widget.options = values
                        widget.value = tuple(
                            [x for x in self.request[key] if x in values]
                        )

            self._update_selection_state()
            update_selection_display()

        for key, f_widget in form_widgets.items():
            widget_type: str = f_widget.get("type", "checkbox")
            options: List[str] = f_widget["values"]
            labels: Dict[str, str] = f_widget.get("labels", {})
            columns: int = f_widget.get("columns", 4)

            buttons: List[widgets.ToggleButton] = [
                widgets.ToggleButton(
                    value=False,
                    description=labels.get(opt, opt),
                    layout=widgets.Layout(width="auto"),
                    button_style="",
                )
                for opt in options
            ]
            get_value: Callable[[], List[str]]

            if widget_type == "checkbox":

                def get_value(
                    tb_list: List[widgets.ToggleButton] = buttons,
                    opts: List[str] = options,
                ) -> List[str]:
                    return [opt for opt, tb in zip(opts, tb_list) if tb.value]

                for tb in buttons:
                    tb.observe(on_change, names="value")
            elif widget_type == "radio":
                f_widget["title"] += " (select one)"

                def on_radio_click(
                    change: Dict[str, Any],
                    tb_list: List[widgets.ToggleButton] = buttons,
                ) -> None:
                    if change["new"]:
                        for tb in tb_list:
                            if tb is not change["owner"]:
                                tb.value = False
                        on_change(change)

                for tb in buttons:
                    tb.observe(
                        lambda change, tb_list=buttons: on_radio_click(change, tb_list),
                        names="value",
                    )

                def get_value(
                    tb_list: List[widgets.ToggleButton] = buttons,
                    opts: List[str] = options,
                ) -> List[str]:
                    for opt, tb in zip(opts, tb_list):
                        if tb.value:
                            return [opt]
                    return []
            else:
                raise ValueError(f"Unsupported widget type: {widget_type}")

            widget = widgets.VBox(
                [
                    widgets.HTML(f"<h3>{f_widget['title']}</h3>"),
                    widgets.GridBox(
                        children=buttons,
                        layout=widgets.Layout(
                            grid_template_columns=f"repeat({columns}, auto)"
                        ),
                    ),
                ]
            )

            for tb, opt in zip(buttons, options):
                tb.value = opt in f_widget.get("default", [])

            widget._get_value = get_value
            self.widget_defs[key] = widget

        self._update_selection_state()

        with self.output:
            self.output.clear_output()
            with self.selection_output:
                print(f"dataset = {self.collection_id}")
                print(f"request = {self._pretty_request(self.request)}")
            selection_box = widgets.Accordion(children=[self.selection_output])
            selection_box.set_title(0, "View current Selection")
            selection_box.selected_index = None

            display(
                widgets.VBox(
                    [
                        self.collection_widget,
                        widgets.HTML(f"<h2>{collection.title}</h2>"),
                        *[self.widget_defs[key] for key in self.widget_defs],
                        widgets.HTML("<br>"),
                        selection_box,
                    ]
                )
            )

    def _on_collection_change(self, change: Dict[str, Any]) -> None:
        if change["name"] == "value" and change["new"] != change["old"]:
            self._build_form(change["new"])

    def _update_selection_state(self) -> None:
        self.collection_id = self.collection_widget.value
        self.request = {
            key: widget._get_value()
            for key, widget in self.widget_defs.items()
            if hasattr(widget, "_get_value") and widget._get_value()
        }

    def _form_json_to_widgets_dict(
        self,
        form: List[Dict[str, Any]],
        ignore_widget_names: List[str] = ["download_format", "data_format"],
        ignore_widget_types: List[str] = [
            "ExclusiveGroupWidget",
            "FreeEditionWidget",
            "GeographicExtentWidget",
            "GeographicLocationWidget",
            "LicenceWidget",
        ],
    ) -> Dict[str, Dict[str, Any]]:
        out_widgets: Dict[str, Dict[str, Any]] = {}
        widget_map: Dict[str, str] = {
            "StringListWidget": "checkbox",
            "StringListArrayWidget": "checkbox",
            "StringChoiceWidget": "radio",
        }
        for widget in form:
            widget_name: str = widget.get("name", "")
            widget_type: str = widget.get("type", "")
            if widget_name in ignore_widget_names or widget_type in ignore_widget_types:
                continue
            if widget_name in out_widgets:
                continue
            out_widgets[widget_name] = {
                k: widget[k] for k in ["label", "type"] if k in widget
            }
            details: Dict[str, Any] = widget.get("details", {})
            if "groups" in details:
                labels: Dict[str, str] = {}
                values: List[str] = []
                columns: int = 1
                for group in details["groups"]:
                    labels.update(group.get("labels", {}))
                    values += [v for v in group.get("values", []) if v not in values]
                    columns = max(columns, group.get("columns", 1))
            else:
                labels = details.get("labels", {})
                values = details.get("values", [])
                columns = details.get("columns", 1)
            out_widgets[widget_name]["labels"] = labels
            out_widgets[widget_name]["values"] = values
            out_widgets[widget_name]["title"] = widget.get("label", "")
            out_widgets[widget_name]["type"] = widget_map.get(widget_type, widget_type)
            out_widgets[widget_name]["columns"] = columns
            if "default" in details:
                out_widgets[widget_name]["default"] = details["default"]
        return out_widgets

    def _pretty_request(self, request: dict[str, str | list[str]]) -> str:
        """Return a pretty-printed JSON string of the request.

        This method should be implemented by subclasses to format the request
        in a human-readable way.
        """
        output: str = "{\n"
        for k, v in request.items():
            if isinstance(v, str):
                output += f'  "{k}": "{v}",\n'
            elif isinstance(v, list):
                if len(v) == 1:
                    output += f'  "{k}": "{v[0]}",\n'
                elif k not in ["time", "date", "month", "year", "day", "step"]:
                    # Put each item on a new line
                    output += f'  "{k}": [\n'
                    for x in v:
                        output += f'    "{x}",\n'
                    output += "  ],\n"
                elif len(v) <= 4:
                    # Put on a single line
                    output += f'  "{k}": ['
                    output += ", ".join(f'"{x}"' for x in v)
                    output += "],\n"
                else:
                    # Put list on lines of 3
                    output += f'  "{k}": [\n'
                    for i in range(0, len(v), 3):
                        output += "    " + ", ".join(f'"{x}"' for x in v[i : i + 3])
                        output += ",\n"
                    output += "  ],\n"

        return output

    def debug(self) -> None:
        """Print the current internal state of the form."""
        print("Collection ID:", self.collection_id)
        print("Request:")
        print(json.dumps(self.request, indent=2))
