import os
import json
import jsonschema
from typing import Any, List, Dict
from abc import ABC, abstractmethod
from loguru import logger


class AbstractNode(ABC):
    def __init__(self, node_id, name):
        self.node_id = node_id
        self.name = name
        super(AbstractNode, self).__init__()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    @abstractmethod
    def kdl_str(self) -> str:
        pass

    def get_base_id(self) -> str:
        return self.node_id.rsplit(".", 1)[-1]

    @abstractmethod
    def get_filename(self) -> str:
        pass

    def __str__(self):
        return "NodeID: " + self.node_id + " NodeName: " + self.name


class AbstractConnection(ABC):
    def __init__(
        self,
        connection_id: int,
        source_id: str,
        source_port: str,
        dest_id: str,
        dest_port: str,
        source_node: AbstractNode = None,
        dest_node: AbstractNode = None,
    ):
        self.connection_id = connection_id
        self.source_id = source_id
        self.source_port = source_port
        self.source_node = source_node
        self.dest_id = dest_id
        self.dest_port = dest_port
        self.dest_node = dest_node

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    @abstractmethod
    def kdl_str(self) -> str:
        pass

    def __str__(self):
        return (
            "ConnectionID: "
            + str(self.connection_id)
            + " Source:"
            + self.source_id
            + "."
            + self.source_port
            + " Dest:"
            + self.dest_id
            + ":"
            + self.dest_port
        )


class Node(AbstractNode):
    def __init__(
        self,
        node_id: str,
        name: str,
        factory: str,
        bundle_name: str,
        bundle_symbolic_name: str,
        bundle_version: str,
        feature_name: str,
        feature_symbolic_name: str,
        feature_version: str,
    ):
        super().__init__(node_id=node_id, name=name)
        self.factory = factory
        self.bundle_name = bundle_name
        self.bundle_symbolic_name = bundle_symbolic_name
        self.bundle_version = bundle_version
        self.feature_name = feature_name
        self.feature_symbolic_name = feature_symbolic_name
        self.feature_version = feature_version
        self.factory_settings: list = list()
        self.model: list = list()
        self.variables: list = list()
        self.port_count: int = 0

    def merge_variables_into_model(self) -> None:
        """
        Merges workflow variables into Node's model

        """
        if self.model and self.variables:
            self.__merge_variables_helper(self.model, self.variables)

    def __merge_variables_helper(self, model_list: list, var_list: list) -> None:
        """
        Helper function for merging var

        Args:
            model_list (list): List of model configurations
            var_list (list): List of variables
        """
        for curr_variable in var_list:
            model_iter = iter(model_list)
            curr_model = next(model_iter)
            curr_model_key = list(curr_model.keys())[0]
            curr_model_val = curr_model[curr_model_key]

            curr_variable_key = list(curr_variable.keys())[0]
            curr_variable_val = curr_variable[curr_variable_key]

            while curr_model_key != curr_variable_key:
                curr_model = next(model_iter)
                curr_model_key = list(curr_model.keys())[0]
                curr_model_val = curr_model[curr_model_key]

            if (
                isinstance(curr_model_val, list)
                and curr_model_val
                and isinstance(curr_variable_val, list)
                and curr_variable_val
            ):
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
            if isinstance(curr_model_val, list):
                new_var = self.__extract_variables_from_model_helper(curr_model_val)
                if new_var:
                    variables.append({curr_model_key: new_var, "data_type": "config"})
            elif "used_variable" in curr.keys() or "exposed_variable" in curr.keys():
                temp_list = list()
                if "used_variable" in curr.keys():
                    temp_list.append(
                        {"used_variable": curr["used_variable"], "data_type": "xstring"}
                    )
                else:
                    temp_list.append(
                        {"isnull": True, "used_variable": "", "data_type": "xstring"}
                    )
                if "exposed_variable" in curr.keys():
                    temp_list.append(
                        {
                            "exposed_variable": curr["exposed_variable"],
                            "data_type": "xstring",
                        }
                    )
                else:
                    temp_list.append(
                        {"isnull": True, "exposed_variable": "", "data_type": "xstring"}
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
        folder_name = self.name.replace("(", "_").replace(")", "_")
        return f"{folder_name} (#{self.get_base_id()})/settings.xml"

    def kdl_str(self) -> str:
        settings = self.__dict__.copy()
        settings.pop("node_id")
        settings.pop("variables")
        if not self.factory_settings:
            settings.pop("factory_settings")
        return f"(n{self.node_id}): {json.dumps(settings, indent=4)}"

    def verify_urls_and_warn(self) -> None:
        """
        Reviews all model settings in a Node and warns user of any relative paths

        """
        settings = self.__dict__.copy()
        try:
            model_settings = [model_dict for model_dict in settings["model"]]
            urls = [
                setting_dict
                for setting_dict in model_settings
                for value in setting_dict.values()
                if "knime://" in str(value)
            ]
        except KeyError:
            return
        if len(urls) > 0:
            logger.warning("====== WARNING =======")
            logger.warning(
                "Node " + self.name + " contains relative paths: NodeID:" + self.node_id
            )
            logger.warning(
                "The following settings have relative workflow paths and "
                + "must be manually adjusted in KNIME:"
            )
            for url in urls:
                logger.warning(url)


class MetaNode(AbstractNode):
    def __init__(
        self,
        node_id: str,
        name: str,
        children: List[AbstractNode],
        connections: List[AbstractConnection],
        meta_in_ports: List[Dict[str, Any]],
        meta_out_ports: List[Dict[str, Any]],
    ):
        super().__init__(node_id=node_id, name=name)
        self.children = children
        self.connections = connections
        self.meta_in_ports = meta_in_ports
        self.meta_out_ports = meta_out_ports
        self.type = "MetaNode"

    def kdl_str(self) -> str:
        indent = "    "
        output_connections = ""
        for i, connection in enumerate(self.connections):
            output_text = f"{indent}{indent}{connection.kdl_str()}"
            if i < len(self.connections) - 1:
                output_text += ",\n"
            output_connections += output_text

        in_ports_text = ""
        in_ports = f'"meta_in_ports": {json.dumps(self.meta_in_ports, indent=4)},'
        for line in in_ports.splitlines():
            in_ports_text += f"{indent}{line}\n"

        out_ports_text = ""
        out_ports = f'"meta_out_ports": {json.dumps(self.meta_out_ports, indent=4)}'
        for line in out_ports.splitlines():
            out_ports_text += f"{indent}{line}\n"

        return (
            f"(n{self.node_id}): "
            "{\n"
            f'{indent}"name": "{self.name}",\n'
            f'{indent}"type": "{self.type}",\n'
            f'{indent}"connections": {{\n'
            f"{output_connections}\n"
            f"{indent}}},\n"
            f"{in_ports_text}"
            f"{out_ports_text}"
            "}"
        )

    def get_filename(self) -> str:
        return f"{self.name} (#{self.get_base_id()})/workflow.knime"


class WrappedMetaNode(MetaNode):
    def __init__(
        self,
        node_id: str,
        name: str,
        children: List[AbstractNode],
        connections: List[AbstractConnection],
        meta_in_ports: List[Dict[str, Any]],
        meta_out_ports: List[Dict[str, Any]],
    ):
        super().__init__(
            node_id=node_id,
            name=name,
            children=children,
            connections=connections,
            meta_in_ports=meta_in_ports,
            meta_out_ports=meta_out_ports,
        )
        self.type = "SubNode"

    def get_filename(self) -> str:
        return f"{self.name} (#{self.get_base_id()})/settings.xml"


class Connection(AbstractConnection):
    def __init__(
        self,
        connection_id: int,
        source_id: str,
        source_port: str,
        dest_id: str,
        dest_port: str,
        source_node: AbstractNode = None,
        dest_node: AbstractNode = None,
    ):
        super().__init__(
            connection_id=connection_id,
            source_id=source_id,
            source_port=source_port,
            source_node=source_node,
            dest_id=dest_id,
            dest_port=dest_port,
            dest_node=dest_node,
        )

    def kdl_str(self) -> str:
        if (
            self.source_node
            and isinstance(self.source_node, MetaNode)
            and not isinstance(self.source_node, WrappedMetaNode)
        ):
            if self.source_node.node_id == "-1":
                source_str = f"(META_IN:{int(self.source_port) + 1})"
            else:
                source_str = f"(n{self.source_id}:{int(self.source_port) + 1})"
        else:
            source_str = f"(n{self.source_id}:{self.source_port})"

        if (
            self.dest_node
            and isinstance(self.dest_node, MetaNode)
            and not isinstance(self.dest_node, WrappedMetaNode)
        ):
            if self.dest_node.node_id == "-1":
                dest_str = f"(META_OUT:{int(self.dest_port) + 1})"
            else:
                dest_str = f"(n{self.dest_id}:{int(self.dest_port) + 1})"
        else:
            dest_str = f"(n{self.dest_id}:{self.dest_port})"

        connection_str = "-->"
        return source_str + connection_str + dest_str


class VariableConnection(AbstractConnection):
    def __init__(
        self,
        connection_id: int,
        source_id: str,
        dest_id: str,
        source_port: str,
        dest_port: str,
        source_node: AbstractNode = None,
        dest_node: AbstractNode = None,
    ):
        super().__init__(
            connection_id=connection_id,
            source_id=source_id,
            source_port=source_port,
            source_node=source_node,
            dest_id=dest_id,
            dest_port=dest_port,
            dest_node=dest_node,
        )

    def kdl_str(self) -> str:
        if (
            self.source_node
            and isinstance(self.source_node, MetaNode)
            and not isinstance(self.source_node, WrappedMetaNode)
        ):
            if self.source_node.node_id == "-1":
                source_str = f"(META_IN:{int(self.source_port) + 1})"
            else:
                source_str = f"(n{self.source_id}:{int(self.source_port) + 1})"
        elif self.source_port == "0":
            source_str = f"(n{self.source_id})"
        else:
            source_str = f"(n{self.source_id}:{self.source_port})"

        if (
            self.dest_node
            and isinstance(self.dest_node, MetaNode)
            and not isinstance(self.dest_node, WrappedMetaNode)
        ):
            if self.dest_node.node_id == "-1":
                dest_str = f"(META_OUT:{int(self.dest_port) + 1})"
            else:
                dest_str = f"(n{self.dest_id}:{int(self.dest_port) + 1})"
        elif self.dest_port == "0":
            dest_str = f"(n{self.dest_id})"
        else:
            dest_str = f"(n{self.dest_id}:{self.dest_port})"

        connection_str = "~~>"

        return source_str + connection_str + dest_str


class AbstractWorkflow(ABC):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    @abstractmethod
    def kdl_str(self) -> str:
        pass


class Workflow(AbstractWorkflow):
    def __init__(self, connections: List[AbstractConnection], variables: list = None):
        self.connections = connections
        self.variables = variables

    def kdl_str(self) -> str:
        indent = "    "
        output_text = "Workflow {\n"
        if self.variables:
            var_text = f'"variables": {json.dumps(self.variables, indent=4)}'
            if self.connections:
                var_text += ","
            for line in var_text.splitlines():
                output_text += f"{indent}{line}\n"
        if self.connections:
            output_connections = '"connections": {\n'
            for i, connection in enumerate(self.connections):
                output_connection = connection.kdl_str()
                if i < len(self.connections) - 1:
                    output_connection += ","
                output_connections += f"{indent}{output_connection}\n"
            output_connections += "}\n"
            for line in output_connections.splitlines():
                output_text += f"{indent}{line}\n"

        output_text += "}\n"
        return output_text
