import os
import yaml as pyyaml


class Attribute:
    """
    Attribute class.

    An attribute is a defined property of a generic model.
    """

    def __init__(self, name, data):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict")

        self.name = name
        if "identifier" in data.keys():
            self.identifier = data["identifier"]

        self.description = ""
        if "description" in data.keys():
            self.description = data["description"]

        self.alias = ""
        if "alias" in data.keys():
            self.alias = data["alias"]

        self.type = ""
        if "type" in data.keys():
            self.type = data["type"]

    def __str__(self):
        return f"Attribute: {self.name} - ({self.identifier}) - {self.alias} - {self.type} - {self.description}"


class GenericModelTemplate:
    """
    Generic model class
    """

    def __init__(self, yaml: str):
        if not isinstance(yaml, str):
            raise ValueError("Input yaml must be a string")
        if os.path.isfile(yaml):
            with open(yaml, "r") as f:
                data = pyyaml.safe_load(f)
        else:
            data = pyyaml.safe_load(yaml)

        if "model" in data.keys():
            data = data["model"]

        self.model_owner = data.get("owner")
        self.model_name = data.get("name")
        self.model_description = data.get("description")
        self.model_version = data.get("version")

        self.attributes = []
        if "attribute" in data.keys():
            attributes = data["attribute"]
            for attkey in attributes.keys():
                self.attributes.append(Attribute(attkey, attributes[attkey]))
                # if curr_attribute.get("type") == "timeseries":
                #     self.attributes.append(Timeseries(curr_attribute))
                # elif curr_attribute.get("type") == "constant":
                #     self.attributes.append(Constant(curr_attribute))
                # else:
                #   raise ValueError(
                #        f"Unknown attribute type: {curr_attribute.get('type')}"
                #    )

    def print_report(self):
        """
        Print a report of the model
        """
        print("Generic Model Template Report")
        print(f"Model Owner: {self.model_owner}")
        print(f"Model Name: {self.model_name}")
        print(f"Model Description: {self.model_description}")
        print(f"Model Version: {self.model_version}")
        print("Attributes:")
        for attribute in self.attributes:
            print(f"  {attribute}")
