import os
import json
import jsonschema
from typing import Any


class Connection:
    def __init__(
        self, id: int, source_id: str, dest_id: str, source_port: str, dest_port: str
    ):
        self.id = id
        self.source_id = source_id
        self.dest_id = dest_id
        self.source_port = source_port
        self.dest_port = dest_port

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


class Node:
    def __init__(
        self,
        id: str,
        name: str,
        factory: str,
        bundle_name: str,
        bundle_symbolic_name: str,
        bundle_version: str,
        feature_name: str,
        feature_symbolic_name: str,
        feature_version: str,
    ):
        self.id = id
        self.name = name
        self.factory = factory
        self.bundle_name = bundle_name
        self.bundle_symbolic_name = bundle_symbolic_name
        self.bundle_version = bundle_version
        self.feature_name = feature_name
        self.feature_symbolic_name = feature_symbolic_name
        self.feature_version = feature_version
        self.model: list = list()
        self.variables: list = list()
        self.port_count = 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def merge_variables_into_model(self):
        """
        Merges workflow variables into Node's model

        Args:
            variables (list): List containing workflow variables
        """
        self.__merge_variables_helper(self.model, self.variables)

    def __merge_variables_helper(self, model_list: list, var_list: list) -> None:
        """
        Helper function for merging var

        Args:
            model_list (list): List of model configurations
            var_list (list): List of variables
        """
        model_iter = iter(model_list)
        curr_model = next(model_iter)
        for curr_variable in var_list:
            curr_model_key = list(curr_model.keys())[0]
            curr_model_val = curr_model[curr_model_key]

            curr_variable_key = list(curr_variable.keys())[0]
            curr_variable_val = curr_variable[curr_variable_key]

            while curr_model_key != curr_variable_key:
                curr_model = next(model_iter)
                curr_model_key = list(curr_model.keys())[0]
                curr_model_val = curr_model[curr_model_key]

            if type(curr_model_val) is list and type(curr_variable_val) is list:
                self.__merge_variables_helper(curr_model_val, curr_variable_val)
            else:
                for curr in curr_variable_val:
                    if "isnull" not in curr.keys():
                        var_mod_key = list(curr.keys())[0]
                        var_mod_val = curr[var_mod_key]
                        curr_model[var_mod_key] = var_mod_val

    def extract_variables_from_model(self) -> None:
        """
        Helper function for extracting workflow variables from node

        """
        self.variables = self.__extract_variables_from_model_helper(self.model)

    def __extract_variables_from_model_helper(self, model_list: list) -> list:
        """
        Extracts workflow variables from model and returns them in own list

        Args:
            model_list (list): List of node model settings

        Returns:
            List: List containing workflow variables
        """
        variables = list()
        for curr in model_list:
            curr_model_key = list(curr.keys())[0]
            curr_model_val = curr[curr_model_key]
            if type(curr_model_val) is list:
                new_var = self.__extract_variables_from_model_helper(curr_model_val)
                if new_var:
                    variables.append({curr_model_key: new_var, "data_type": "config"})
            elif "used_variable" in curr.keys() or "exposed_variable" in curr.keys():
                temp_list = list()
                if "used_variable" in curr.keys():
                    temp_list.append(
                        {
                            "used_variable": curr["used_variable"],
                            "data_type": curr["data_type"],
                        }
                    )
                else:
                    temp_list.append(
                        {
                            "isnull": True,
                            "used_variable": "",
                            "data_type": curr["data_type"],
                        }
                    )
                if "exposed_variable" in curr.keys():
                    temp_list.append(
                        {
                            "exposed_variable": curr["exposed_variable"],
                            "data_type": curr["data_type"],
                        }
                    )
                else:
                    temp_list.append(
                        {
                            "isnull": True,
                            "exposed_variable": "",
                            "data_type": curr["data_type"],
                        }
                    )
                variables.append({curr_model_key: temp_list, "data_type": "config"})

        return variables

    def validate_node_from_schema(self) -> None:
        """
        Validates node settings against JSON Schema

        Raises:
            jsonschema.ValidationError: if node does not follow defined json schema

            jsonschema.SchemaError: if schema definition is invalid

        """
        schema = open(
            f"{os.path.dirname(__file__)}/json_schemas/{self.name}.json"
        ).read()
        jsonschema.validate(instance=self.__dict__, schema=json.loads(schema))

    def get_filename(self) -> str:
        return f"{self.name} (#{self.id})/settings.xml"
