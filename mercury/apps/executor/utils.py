import json
import nbformat as nbf


def get_test_notebook(markdown=[], code=[]):
    nb = nbf.v4.new_notebook()
    nb["cells"] = []
    for m in markdown:
        nb["cells"] += [nbf.v4.new_markdown_cell(m)]
    for c in code:
        nb["cells"] += [nbf.v4.new_code_cell(c)]

    return nb


def one_cell_notebook(code=""):
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_code_cell(code)]
    return nb

def parse_params(nb, params={}):
    # nb in nbformat
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            if "outputs" in cell:
                for output in cell["outputs"]:

                    if (
                        "data" in output
                        and "application/mercury+json" in output["data"]
                    ):
                        view = output["data"]["application/mercury+json"]
                        print(view)
                        view = json.loads(view)
                        widget_type = view.get("widget")
                        if widget_type is None:
                            continue
                        if widget_type == "App":
                            if view.get("title") is not None:
                                params["title"] = view.get("title")
                            if view.get("description") is not None:
                                params["description"] = view.get("description")
                            if view.get("show_code") is not None:
                                params["show-code"] = view.get("show_code")
                        if widget_type == "Slider":
                            if "params" not in params:
                                params["params"] = {}
                            params["params"]["w1"] = {
                                "input": "slider",
                                "value": view.get("value", 0),
                                "min": view.get("min", 0),
                                "max": view.get("max", 100),
                                "label": view.get("label", "")
                            }
