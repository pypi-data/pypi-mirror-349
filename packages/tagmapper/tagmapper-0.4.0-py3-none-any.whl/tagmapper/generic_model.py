from typing import List, Literal, Optional, Union

from tagmapper.generic_model_template import GenericModelTemplate
from tagmapper.mapping import Constant, Timeseries

from tagmapper.connector_api import get_api_url, get_json, post_json


def add_timeseries_mapping(
    object_name: str,
    model_owner: str,
    model_name: str,
    attribute_name: str,
    time_series_tag_no: str,
    timeseries_source: str,
    mode: Optional[str] = "",
    unit_of_measure: Optional[str] = "",
    comment: Optional[str] = "",
):
    """
    Post a timeseries to the API
    """
    timeseries_dict = {
        "unique_object_identifier": object_name,
        "model_source": model_owner,
        "model_name": model_name,
        "mode": mode,
        "UnitOfMeasure": unit_of_measure,
        "TimeseriesSource": timeseries_source,
        "comment": comment,
        "AttributeName": attribute_name,
        "TimeSeriesTagNo": time_series_tag_no,
    }

    return _post_upload(timeseries_dict)


def add_constant_mapping(
    object_name: str,
    model_owner: str,
    model_name: str,
    attribute_name: str,
    value: str,
    mode: Optional[str] = "",
    unit_of_measure: Optional[str] = "",
    comment: Optional[str] = "",
):
    """
    Post a constant to the API
    """

    constant_dict = [
        {
            "unique_object_identifier": object_name,
            "model_source": model_owner,
            "model_name": model_name,
            "mode": mode,
            "UnitOfMeasure": unit_of_measure,
            "comment": comment,
            "AttributeName": attribute_name,
            "ConstantValue": value,
        }
    ]

    return _post_upload(constant_dict)


def _get_mappings(
    model_owner: str = "",
    model_name: str = "",
    object_name: str = "",
    attribute_type: Optional[Literal["constant", "timeseries"]] = None,
) -> List[dict[str, str]]:
    """
    Get generic model mappings from the API
    """

    if attribute_type is None:
        const = _get_mappings(
            model_owner=model_owner,
            model_name=model_name,
            object_name=object_name,
            attribute_type="constant",
        )

        ts = _get_mappings(
            model_owner=model_owner,
            model_name=model_name,
            object_name=object_name,
            attribute_type="timeseries",
        )
        const.extend(ts)
        return const

    model_dict = {
        "Model_Source": model_owner,
        "Attribute_Type": str(attribute_type),
        "Model_Name": model_name,
        "unique_object_identifier": object_name,
    }

    url = get_api_url(use_dev=True) + "get-model"
    response = get_json(url, params=model_dict)

    if isinstance(response, dict):
        if "data" in response.keys():
            if isinstance(response["data"], list):
                return response["data"]
            else:
                return [response["data"]]
        # raise ValueError("Response is not a valid JSON object")

    return []


def _post_upload(data: Union[dict[str, str], List[dict[str, str]]]):
    """
    Post a generic model to the API
    """

    if isinstance(data, dict):
        data = [data]

    upload = {"data": data}

    url = get_api_url(use_dev=True) + "upload-model"
    response = post_json(url, upload)
    return response


class Model(GenericModelTemplate):
    """
    Generic model class including mappings
    """

    def __init__(self, data: dict[str, str]):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dict")

        self.name = ""

        # description is an attribute property, not a mapping property
        self.description = ""
        if "description" in data.keys():
            self.description = data["description"]

        self.comment = ""
        if "comment" in data.keys():
            self.comment = data["comment"]

        self.attributes = []

    def add_attribute(self, attribute: Union[Constant, Timeseries]):
        """
        Add an attribute to the model
        """
        if not isinstance(attribute, (Constant, Timeseries)):
            raise ValueError("Input data must be a Constant or Timeseries")

        self.attributes.append(attribute)

    def add_constant(self, value: str):
        """
        Add a constant to the model
        """

        c = Constant(value)

        self.add_attribute(c)

    def add_timeseries(self, tagNo: str, source: str):
        """
        Add a Timeseries to the model
        """

        ts = Timeseries([])

        self.attributes.append(ts)

    @staticmethod
    def get_model(model_owner: str = "", model_name: str = "", object_name: str = ""):
        """
        Get a model from the API
        """
        mappings = _get_mappings(
            model_owner=model_owner, model_name=model_name, object_name=object_name
        )

        if not mappings or len(mappings) == 0:
            raise ValueError("No mappings found for model")

        data = {}
        data["name"] = mappings[0]["model_name"]
        data["description"] = ""
        data["owner"] = mappings[0]["model_source"]
        data["object_name"] = mappings[0]["unique_object_identifier"]

        mod = Model(data=data)
        for map in mappings:
            if "ConstantValue" in map.keys():
                mod.add_attribute(Constant(map))
            else:
                mod.add_attribute(Timeseries(map))

        return mod
