from abc import ABC


class Mapping(ABC):
    """
    Abstract mapping class.

    A mapping refers to a single row in generic model table. It is an instantiation
    of a generic model attribute. In the table there is also

    Currently two types of mappings are supported:
    - Timeseries: a timeseries attribute
    - Constant: a constant attribute
    """

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict")

        # attribute name / mapping name
        self.name = ""
        if "attribute_name" in data.keys():
            self.name = data["attribute_name"]
        elif "AttributeName" in data.keys():
            self.name = data["AttributeName"]
        elif "Attribute_Name" in data.keys():
            self.name = data["Attribute_Name"]
        elif "attribute_identifier" in data.keys():
            # Well
            self.name = data["attribute_identifier"]
        elif "mapping_name" in data.keys():
            self.name = data["mapping_name"]
        elif "Mapping_Name" in data.keys():
            self.name = data["Mapping_Name"]
        elif "mapping_identifier" in data.keys():
            self.name = data["mapping_identifier"]
        elif "identifier" in data.keys():
            self.name = data["identifier"]
        else:
            pass

        # description is an attribute property, not a mapping property
        self.description = ""
        if "description" in data.keys():
            self.description = data["description"]
        else:
            pass

        # comment is a mapping property
        self.comment = ""
        if "comment" in data.keys():
            self.comment = data["comment"]
        elif "mapped_comment" in data.keys():
            self.comment = data["mapped_comment"]

        self.mode = ""
        if "mode" in data.keys():
            self.mode = data["mode"]
        else:
            pass

        self.unit_of_measure = ""
        if "unit_of_measure" in data.keys():
            self.unit_of_measure = data["unit_of_measure"]
        elif "UnitOfMeasure" in data.keys():
            self.unit_of_measure = data["UnitOfMeasure"]
        else:
            # Well data does not contain unit of measure
            pass


class Timeseries(Mapping):
    """
    Timeseries mapping class
    """

    def __init__(self, data):
        super().__init__(data)
        self.tag = ""
        self.source = ""

        # populate tag
        if "TAG_ID" in data.keys():
            self.tag = data["TAG_ID"]
        elif "Tag_Id" in data.keys():
            self.tag = data["Tag_Id"]
        elif "timeseries_name" in data.keys():
            # well
            self.tag = data["timeseries_name"]
        elif "TimeSeriesTagNo" in data.keys():
            self.tag = data["TimeSeriesTagNo"]
        else:
            pass

        # populate source
        if "ims_collective" in data.keys():
            # well
            self.source = data["ims_collective"]
        elif "TimeseriesSource" in data.keys():
            self.source = data["TimeseriesSource"]
        else:
            pass

    def __str__(self):
        return f"Timeseries: {self.name} - ({self.tag}) @ {self.source}"


class Constant(Mapping):
    """
    Constant mapping class
    """

    def __init__(self, data):
        super().__init__(data)
        self.value = ""

        # populate value
        if "value" in data.keys():
            self.value = data["value"]
        elif "ConstantValue" in data.keys():
            self.value = data["ConstantValue"]
        else:
            pass

    def __str__(self):
        return f"Constant: {self.name} - ({self.value}) [{self.unit_of_measure}] - {self.comment}"
