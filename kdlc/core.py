import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape
import tempfile
from typing import List, Any, Dict, cast
from kdlc.objects import (
    AbstractNode,
    AbstractConnection,
    Node,
    Connection,
    VariableConnection,
    MetaNode,
    WrappedMetaNode,
    Workflow,
)

jinja_env = Environment(
    loader=PackageLoader("kdlc", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
    extensions=["jinja2.ext.do"],
)

TMP_INPUT_DIR = tempfile.TemporaryDirectory()
INPUT_PATH = TMP_INPUT_DIR.name
TMP_OUTPUT_DIR = tempfile.TemporaryDirectory()
OUTPUT_PATH = TMP_OUTPUT_DIR.name

NS = {"knime": "http://www.knime.org/2008/09/XMLConfig"}
ENTRY_TAG = f'{{{NS["knime"]}}}entry'
CONFIG_TAG = f'{{{NS["knime"]}}}config'

META_IN = MetaNode(
    node_id="-1",
    name="META_IN",
    children=[],
    connections=[],
    meta_in_ports=[],
    meta_out_ports=[],
)
META_OUT = MetaNode(
    node_id="-1",
    name="META_OUT",
    children=[],
    connections=[],
    meta_in_ports=[],
    meta_out_ports=[],
)


def unzip_workflow(input_file: str) -> str:
    """
    Unzips the provided workflow archive and returns the folder with
    the workflow definitions

    Args:
        input_file (str): Name of the workflow archive

    Returns:
        str: Name of the workflow folder
    """

    zip_ref = zipfile.ZipFile(input_file, "r")
    zip_ref.extractall(INPUT_PATH)
    zip_ref.close()
    return os.listdir(INPUT_PATH).pop()


def extract_node_from_settings_xml(node_id: str, input_file: str) -> Node:
    """
    Parses the provided input file and returns a populated dict with
    associated values

    Args:
        node_id (str): Node's id from workflow.knime
        input_file (str): XML file containing a node definition

    Returns:
        dict: Dict populated with values extracted from provided input file
    """
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()

    name = extract_entry_value(root, "name")
    factory = extract_entry_value(root, "factory")
    bundle_name = extract_entry_value(root, "node-bundle-name")
    bundle_symbolic_name = extract_entry_value(root, "node-bundle-symbolic-name")
    bundle_version = extract_entry_value(root, "node-bundle-version")
    feature_name = extract_entry_value(root, "node-feature-name")
    feature_symbolic_name = extract_entry_value(root, "node-feature-symbolic-name")
    feature_version = extract_entry_value(root, "node-feature-version")

    node = Node(
        node_id=node_id,
        name=name,
        factory=factory,
        bundle_name=bundle_name,
        bundle_symbolic_name=bundle_symbolic_name,
        bundle_version=bundle_version,
        feature_name=feature_name,
        feature_symbolic_name=feature_symbolic_name,
        feature_version=feature_version,
    )
    for child in root.findall("./knime:config[@key='model']/*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            node.model.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            node.model.append(config)
        else:
            ex = ValueError("Invalid settings tag")
            raise ex

    for child in root.findall("./knime:config[@key='factory_settings']/*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            node.factory_settings.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            node.factory_settings.append(config)
        else:
            ex = ValueError("Invalid settings tag")
            raise ex

    node.port_count = len(root.findall("./knime:config[@key='ports']/*", NS))

    for child in root.findall("./knime:config[@key='variables']/*", NS):
        if child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            node.variables.append(config)
        else:
            ex = ValueError("Invalid settings tag")
            raise ex
    node.merge_variables_into_model()
    return node


def extract_entry_value(tree: ET.Element, element_key: str) -> str:
    """
    Extracts the value attribute from entry matching element_key

    Args:
        tree (Element): The tree to extract entry value from
        element_key (str): The key of the value being extracted

    Returns:
        str: String containing entry value
    """
    element = tree.find(f"./knime:entry[@key='{element_key}']", NS)
    if element is not None:
        value = element.attrib["value"]
    else:
        ex = ValueError(f"Value not found for element_key: {element_key}")
        raise ex
    return value


def extract_entry_tag(tree: ET.Element) -> Dict[str, Any]:
    """
    Extracts the entry tag from the provided tree

    Args:
        tree (Element): The tree to extract entry tag from

    Returns:
        dict: Dict containing the entry tag definition
    """
    entry: Dict[str, Any] = dict()
    if tree.attrib["type"] == "xstring":
        entry[tree.attrib["key"]] = tree.attrib["value"]
    elif tree.attrib["type"] == "xboolean":
        if tree.attrib["value"] == "true":
            entry[tree.attrib["key"]] = True
        else:
            entry[tree.attrib["key"]] = False
    elif tree.attrib["type"] == "xint":
        entry[tree.attrib["key"]] = int(tree.attrib["value"])
    elif tree.attrib["type"] in ["xlong", "xshort"]:
        entry[tree.attrib["key"]] = int(tree.attrib["value"])
        entry["data_type"] = tree.attrib["type"]
    elif tree.attrib["type"] == "xfloat":
        entry[tree.attrib["key"]] = float(tree.attrib["value"])
    elif tree.attrib["type"] == "xdouble":
        if tree.attrib["value"] == "Infinity" or tree.attrib["value"] == "-Infinity":
            entry[tree.attrib["key"]] = tree.attrib["value"]
        else:
            entry[tree.attrib["key"]] = float(tree.attrib["value"])
        entry["data_type"] = tree.attrib["type"]
    elif tree.attrib["type"] in ["xchar", "xbyte", "xpassword"]:
        entry[tree.attrib["key"]] = tree.attrib["value"]
        entry["data_type"] = tree.attrib["type"]
    else:
        ex = ValueError("Invalid entry type")
        raise ex

    if "isnull" in tree.attrib:
        entry["isnull"] = True
    return entry


def extract_config_tag(tree: ET.Element) -> dict:
    """
    Extracts the config tag from the provided tree

    Args:
        tree (Element): The tree to extract the config tag from

    Returns:
        dict: Dict containing the config tag definition
    """
    config_value = list()
    for child in tree.findall("./*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            config_value.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            config_value.append(config)
        else:
            ex = ValueError("Invalid child tag")
            raise ex
    config = {tree.attrib["key"]: config_value}
    return config


def extract_node_filenames(input_file: str) -> List[Dict[str, Any]]:
    """
    Extracts the list of nodes from the provided KNIME workflow

    Args:
        input_file (str): Name of input workflow.knime file

    Returns:
        list: The list of node file names within the KNIME workflow
    """
    input_path = os.path.dirname(input_file)
    node_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for child in root.findall("./knime:config[@key='nodes']/knime:config", NS):
        node: Dict[str, Any] = dict()

        node["node_id"] = extract_entry_value(child, "id")
        node["filename"] = extract_entry_value(child, "node_settings_file")
        node["node_type"] = extract_entry_value(child, "node_type")

        if node["node_type"] == "MetaNode":
            base_tree = ET.parse(f"{input_path}/{node['filename']}")
            root = base_tree.getroot()
            node["name"] = extract_entry_value(root, "name")
            node["children"] = extract_node_filenames(
                f"{input_path}/{node['filename']}"
            )

            meta_in_ports = list()
            for port in root.findall(
                "./knime:config[@key='meta_in_ports']"
                "/knime:config[@key='port_enum']/knime:config",
                NS,
            ):
                index = str(int(extract_entry_value(port, "index")) + 1)
                port_type = port.find("./knime:config[@key='type']", NS)
                if port_type is not None:
                    object_class = extract_entry_value(port_type, "object_class")

                if index and object_class:
                    meta_in_ports.append({index: object_class})
            node["meta_in_ports"] = meta_in_ports

            meta_out_ports = list()
            for port in root.findall(
                "./knime:config[@key='meta_out_ports']"
                "/knime:config[@key='port_enum']/knime:config",
                NS,
            ):
                index = str(int(extract_entry_value(port, "index")) + 1)
                port_type = port.find("./knime:config[@key='type']", NS)
                if port_type is not None:
                    object_class = extract_entry_value(port_type, "object_class")

                if index and object_class:
                    meta_out_ports.append({index: object_class})
            node["meta_out_ports"] = meta_out_ports
        elif node["node_type"] == "SubNode":

            base_tree = ET.parse(f"{input_path}/{node['filename']}")
            root = base_tree.getroot()

            # Extract inports from settings.xml
            meta_in_ports = list()
            for port in root.findall("./knime:config[@key='inports']/knime:config", NS):
                index = str(int(extract_entry_value(port, "index")) + 1)
                port_type = port.find("./knime:config[@key='type']", NS)
                if port_type is not None:
                    object_class = extract_entry_value(port_type, "object_class")

                if index and object_class:
                    meta_in_ports.append({index: object_class})
            node["meta_in_ports"] = meta_in_ports

            # Extract outports from settings.xml
            meta_out_ports = list()
            for port in root.findall(
                "./knime:config[@key='outports']/knime:config", NS
            ):
                index = str(int(extract_entry_value(port, "index")) + 1)
                port_type = port.find("./knime:config[@key='type']", NS)
                if port_type is not None:
                    object_class = extract_entry_value(port_type, "object_class")

                if index and object_class:
                    meta_out_ports.append({index: object_class})
            node["meta_out_ports"] = meta_out_ports

            # Extract name and children from workflow.knime
            workflow_file_path = (
                f"{input_path}/{os.path.dirname(node['filename'])}/workflow.knime"
            )

            wf_tree = ET.parse(workflow_file_path)
            root = wf_tree.getroot()

            name_ele = root.find("./knime:entry[@key='name']", NS)
            if name_ele is not None:
                node["name"] = name_ele.attrib["value"]
            node["children"] = extract_node_filenames(workflow_file_path)

        node_list.append(node)
    return node_list


def extract_nodes_from_filenames(
    workflow_path: str, node_filenames: List[Dict[str, Any]], parent_id: str = None
) -> List[AbstractNode]:
    """
    Extracts nodes from filename dict, including Metanodes

    Args:
        workflow_path (str): Path to input workflow
        node_filenames (dict): Dictionary of input node filenames
        parent_id (str): id of parent metanode when adding child to metanode

    Returns:
        List[AbstractNode]: The list of nodes extracted from workflow
    """
    input_node_list: List[AbstractNode] = list()
    for curr in node_filenames:
        infile = f'{workflow_path}/{curr["filename"]}'
        if parent_id is not None:
            curr["node_id"] = f"{parent_id}.{curr['node_id']}"
        if curr["node_type"] == "NativeNode":
            node = extract_node_from_settings_xml(curr["node_id"], infile)
            input_node_list.append(node)
        elif curr["node_type"] == "MetaNode":
            children = extract_nodes_from_filenames(
                workflow_path=os.path.dirname(infile),
                node_filenames=curr["children"],
                parent_id=curr["node_id"],
            )
            connections = extract_connections(infile, children)
            metanode = MetaNode(
                node_id=curr["node_id"],
                name=curr["name"],
                children=children,
                connections=connections,
                meta_in_ports=curr["meta_in_ports"],
                meta_out_ports=curr["meta_out_ports"],
            )
            input_node_list.append(metanode)
        elif curr["node_type"] == "SubNode":
            children = extract_nodes_from_filenames(
                workflow_path=os.path.dirname(infile),
                node_filenames=curr["children"],
                parent_id=curr["node_id"],
            )
            infile = f"{os.path.dirname(infile)}/workflow.knime"
            connections = extract_connections(infile, children)
            wrapped_metanode = WrappedMetaNode(
                node_id=curr["node_id"],
                name=curr["name"],
                children=children,
                connections=connections,
                meta_in_ports=curr["meta_in_ports"],
                meta_out_ports=curr["meta_out_ports"],
            )
            input_node_list.append(wrapped_metanode)

    return input_node_list


def flatten_node_list(node_list: List[AbstractNode]) -> List[AbstractNode]:
    """
    Flattens Node list, returning list with all embedded nodes within
    Metanodes

    Args:
        node_list (List[AbstractNode]): input list of Nodes

    Returns:
        List[AbstractNode]: flattened list of Nodes
    """
    flattened_list = list()
    for node in node_list:
        flattened_list.append(node)
        if isinstance(node, MetaNode) or isinstance(node, WrappedMetaNode):
            flattened_list += flatten_node_list(cast(MetaNode, node).children)
    return flattened_list


def unflatten_node_list(node_list: List[AbstractNode]) -> List[AbstractNode]:
    """
    Unflattens node list, adding children to Metanodes

    Args:
        node_list (List[AbstractNode]): input list of Nodes
    Returns:
        List[AbstractNode]: unflattened list of Nodes
    """
    metanode_list = [
        node
        for node in node_list
        if type(node) is MetaNode or type(node) is WrappedMetaNode
    ]

    for metanode in metanode_list:
        dot_count = metanode.node_id.count(".")
        child_list = [
            node
            for node in node_list
            if node.node_id.startswith(f"{metanode.node_id}.")
            and node.node_id.count(".") == dot_count + 1
        ]
        cast(MetaNode, metanode).children += child_list
    return [node for node in node_list if node.node_id.count(".") == 0]


def normalize_connections(
    node_list: List[AbstractNode], connection_list: List[AbstractConnection]
) -> None:
    """
    Updates connections with correct nodes and decrement port ids
    for metanode source/dest nodes

    Args:
        node_list (List[AbstractNode]): List of input nodes
        connection_list (List[AbstractConnection]): List of input
            connections
    """
    node_dict = {node.get_base_id(): node for node in node_list}

    for connection in connection_list:
        connection = cast(Connection, connection)
        if connection.source_id == "-1":
            connection.source_node = META_IN
        else:
            connection.source_node = node_dict[connection.source_id]
        if connection.dest_id == "-1":
            connection.dest_node = META_OUT
        else:
            connection.dest_node = node_dict[connection.dest_id]

        if isinstance(connection.source_node, MetaNode):
            connection.source_port = str(int(connection.source_port) - 1)
        if isinstance(connection.dest_node, MetaNode):
            connection.dest_port = str(int(connection.dest_port) - 1)

    metanodes = [
        node
        for node in node_list
        if type(node) is MetaNode or type(node) is WrappedMetaNode
    ]
    for metanode in metanodes:
        metanode = cast(MetaNode, metanode)
        meta_in_ports = list()
        for port in metanode.meta_in_ports:
            key = list(port.keys())[0]
            new_key = str(int(key) - 1)
            meta_in_ports.append({new_key: port[key]})
        metanode.meta_in_ports = meta_in_ports
        meta_out_ports = list()
        for port in metanode.meta_out_ports:
            key = list(port.keys())[0]
            new_key = str(int(key) - 1)
            meta_out_ports.append({new_key: port[key]})
        metanode.meta_out_ports = meta_out_ports
        normalize_connections(metanode.children, metanode.connections)


def extract_connections(
    input_file: str, node_list: List[AbstractNode]
) -> List[AbstractConnection]:
    """
    Extracts a list of connections from the provided KNIME workflow

    Args:
        input_file (str): Name of input workflow.knime file
        node_list (List[AbstractNode]): List of nodes for connections

    Returns:
        list: The list of connections within the KNIME workflow
    """
    node_dict = {node.get_base_id(): node for node in node_list}
    connection_list: List[AbstractConnection] = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for i, child in enumerate(
        root.findall("./knime:config[@key='connections']/knime:config", NS)
    ):
        source_id = extract_entry_value(child, "sourceID")
        source_node = META_IN if source_id == "-1" else node_dict[source_id]

        dest_id = extract_entry_value(child, "destID")
        dest_node = META_OUT if dest_id == "-1" else node_dict[dest_id]

        source_port = extract_entry_value(child, "sourcePort")
        dest_port = extract_entry_value(child, "destPort")

        is_var_connection = False

        if (isinstance(source_node, Node) and source_port == "0") or (
            isinstance(dest_node, Node) and dest_port == "0"
        ):
            is_var_connection = True
        elif (
            isinstance(source_node, MetaNode)
            and source_node is not META_IN
            and isinstance(dest_node, MetaNode)
            and dest_node is not META_OUT
        ):
            source_out_connections = [
                c
                for c in cast(MetaNode, source_node).connections
                if c.dest_node is META_OUT and c.dest_port == source_port
            ]
            if source_out_connections:
                source_out_connection = source_out_connections.pop()
            dest_in_connections = [
                c
                for c in cast(MetaNode, dest_node).connections
                if c.source_node is META_IN and c.source_port == dest_port
            ]
            if dest_in_connections:
                dest_in_connection = dest_in_connections.pop()
            if isinstance(source_out_connection, VariableConnection) and isinstance(
                dest_in_connection, VariableConnection
            ):
                is_var_connection = True

        if is_var_connection:
            var_connection = VariableConnection(
                connection_id=i,
                source_id=source_id,
                source_node=source_node,
                dest_id=dest_id,
                dest_node=dest_node,
                source_port=source_port,
                dest_port=dest_port,
            )
            connection_list.append(var_connection)
        else:
            connection = Connection(
                connection_id=i,
                source_id=source_id,
                source_node=source_node,
                dest_id=dest_id,
                dest_node=dest_node,
                source_port=source_port,
                dest_port=dest_port,
            )
            connection_list.append(connection)
    return connection_list


def extract_global_wf_variables(input_file: str) -> List[Dict[str, Any]]:
    """
    Extracts global workflow variables from input workflow.knime file

    Args:
        input_file (str): Name of input workflow.knime file

    Returns:
        list: The list of global workflow variable dicts within the KNIME workflow
    """
    global_variable_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for child in root.findall(
        "./knime:config[@key='workflow_variables']/knime:config", NS
    ):
        variable: Dict[str, Any] = dict()
        variable_name = extract_entry_value(child, "name")
        variable_class = extract_entry_value(child, "class")
        variable_value = extract_entry_value(child, "value")

        if variable_value is not None and variable_class is not None:
            if variable_class == "STRING":
                variable[variable_name] = variable_value
            elif variable_class == "DOUBLE":
                variable[variable_name] = float(variable_value)
            elif variable_class == "INTEGER":
                variable[variable_name] = int(variable_value)
        global_variable_list.append(variable)
    return global_variable_list


def create_node_files(output_workflow_path: str, nodes: List[AbstractNode]) -> None:
    """
    Create's output node files for nodes

    Args:
        output_workflow_path (str): Output workflow path for nodes
        nodes (List[AbstractNode]): List of input notes to be written
    """
    for node in nodes:
        if type(node) is Node:
            # TODO: uncomment lines 63-72 and add tests
            # try:
            #     node.validate_node_from_schema()
            # except jsonschema.ValidationError as e:
            #     print(e.message)
            #     kdlc.cleanup()
            #     sys.exit(1)
            # except jsonschema.SchemaError as e:
            #     print(e.message)
            #     kdlc.cleanup()
            #     sys.exit(1)
            tree = create_node_settings_from_template(cast(Node, node))
            save_node_settings_xml(
                tree, f"{output_workflow_path}/{node.get_filename()}"
            )
        elif type(node) is MetaNode:
            node = cast(MetaNode, node)
            tree = create_metanode_workflow_knime_from_template(node)
            metanode_path = (
                f"{output_workflow_path}/{os.path.dirname(node.get_filename())}"
            )
            save_workflow_knime(tree, metanode_path)
            create_node_files(metanode_path, node.children)
        elif type(node) is WrappedMetaNode:
            node = cast(WrappedMetaNode, node)
            wf_tree = create_wrapped_metanode_workflow_knime_from_template(node)
            settings_tree = create_wrapped_metanode_settings_from_template(node)
            metanode_path = (
                f"{output_workflow_path}/{os.path.dirname(node.get_filename())}"
            )
            save_workflow_knime(wf_tree, metanode_path)
            save_node_settings_xml(
                settings_tree, f"{output_workflow_path}/{node.get_filename()}"
            )
            create_node_files(metanode_path, node.children)


def create_node_settings_from_template(node: Node) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node definition

    Args:
        node (Node): Node definition

    Returns:
        ElementTree: ElementTree populated with the provided node definition
    """
    template = jinja_env.get_template("settings_template.xml")
    for value in node.model:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)

    for value in node.factory_settings:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)

    template_root = ET.fromstring(template.render(node=node))
    return ET.ElementTree(template_root)


def create_workflow_knime_from_template(
    node_list: List[AbstractNode], workflow: Workflow
) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        node_list (list): List of Node definitions
        workflow (Workflow): Input workflow

    Returns:
        ElementTree: ElementTree populated with nodes and their associated
        connections
    """
    template = jinja_env.get_template("workflow_template.xml")
    if workflow.variables:
        set_class_for_global_variables(workflow.variables)
    nodes = [node for node in node_list if type(node) is Node]
    metanodes = [
        node
        for node in node_list
        if type(node) is MetaNode or type(node) is WrappedMetaNode
    ]
    data = {
        "nodes": nodes,
        "metanodes": metanodes,
        "connections": workflow.connections,
        "variables": workflow.variables,
    }
    return ET.ElementTree(ET.fromstring(template.render(data)))


def create_metanode_workflow_knime_from_template(metanode: MetaNode) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        metanode (MetaNode): metanode definition

    Returns:
        ElementTree: ElementTree populated with metanode and  associated
        connections
    """

    template = jinja_env.get_template("workflow_template.xml")
    nodes = [node for node in metanode.children if type(node) is Node]
    metanodes = [
        node
        for node in metanode.children
        if type(node) is MetaNode or type(node) is WrappedMetaNode
    ]

    data = {
        "name": metanode.name,
        "nodes": nodes,
        "metanodes": metanodes,
        "connections": metanode.connections,
        "meta_in_ports": metanode.meta_in_ports,
        "meta_out_ports": metanode.meta_out_ports,
    }

    return ET.ElementTree(ET.fromstring(template.render(data)))


def create_wrapped_metanode_workflow_knime_from_template(
    metanode: WrappedMetaNode
) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        metanode (WrappedMetaNode): Wrapped Metanode definition

    Returns:
        ElementTree: ElementTree populated with Wrapped Metanode and associated
        connections
    """

    template = jinja_env.get_template("workflow_template.xml")
    nodes = [node for node in metanode.children if type(node) is Node]
    metanodes = [
        node
        for node in metanode.children
        if type(node) is MetaNode or type(node) is WrappedMetaNode
    ]

    data = {
        "name": metanode.name,
        "nodes": nodes,
        "metanodes": metanodes,
        "connections": metanode.connections,
    }

    return ET.ElementTree(ET.fromstring(template.render(data)))


def create_wrapped_metanode_settings_from_template(
    metanode: WrappedMetaNode
) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        metanode (WrappedMetaNode): Wrapped Metanode definition

    Returns:
        ElementTree: ElementTree populated with Wrapped Metanode ports
    """

    template = jinja_env.get_template("wrapped_settings_template.xml")
    virtual_in = [
        node for node in metanode.children if node.name == "WrappedNode Input"
    ].pop()
    virtual_out = [
        node for node in metanode.children if node.name == "WrappedNode Output"
    ].pop()
    data = {
        "virtual_in_id": virtual_in.get_base_id(),
        "meta_in_ports": metanode.meta_in_ports,
        "virtual_out_id": virtual_out.get_base_id(),
        "meta_out_ports": metanode.meta_out_ports,
    }

    return ET.ElementTree(ET.fromstring(template.render(data)))


def set_class_for_global_variables(variable_list: list) -> None:
    """
    Sets var_class property for each dict in variable_list
    for generating XML template

    Args:
        variable_list (list): List of global variable dicts
    """
    for variable in variable_list:
        name = list(variable.keys())[0]
        value = variable[name]
        if type(value) == int:
            variable["var_class"] = "INTEGER"
        elif type(value) == float:
            variable["var_class"] = "DOUBLE"
        else:
            variable["var_class"] = "STRING"


def set_entry_element_type(entry: dict) -> None:
    """
    Sets an entry Element's type and value based on the provided entry definition

    Args:
        entry (dict): Entry definition

    """
    entry_key = list(entry.keys())[0]
    entry_type = type(entry[entry_key])
    entry_value = str(entry[entry_key])
    if "data_type" in entry:
        data_type = entry["data_type"]
    elif entry_type is int:
        data_type = "xint"
    elif entry_type is float:
        data_type = "xfloat"
    elif entry_type is bool:
        entry_value = entry_value.lower()
        data_type = "xboolean"
    elif entry_type is str:
        data_type = "xstring"
    else:
        ex = ValueError("Cannot set element type")
        raise ex
    entry["data_type"] = data_type
    entry[entry_key] = entry_value


def set_config_element_type(config: dict) -> None:
    """
    Sets a config Element's type based on the provided config definition

    Args:
        config (dict): Config definition

    """
    config_key = list(config.keys())[0]
    config_values = config[config_key]
    config["data_type"] = "config"
    for value in config_values:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)


def save_node_settings_xml(tree: ET.ElementTree, output_path: str) -> None:
    """Writes the provided tree to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree
        output_path (str): Location to write the tree to
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ET.register_namespace("", NS["knime"])
    tree.write(output_path, xml_declaration=True, encoding="UTF-8")


def save_workflow_knime(tree: ET.ElementTree, output_path: str) -> None:
    """
    Writes the provided tree containing a KNIME workflow to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree containing a KNIME workflow
        output_path (str): Location to write tree to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ET.register_namespace("", NS["knime"])
    tree.write(f"{output_path}/workflow.knime", xml_declaration=True, encoding="UTF-8")


def create_output_workflow(workflow_name: str) -> None:
    """
    Bundles the provided workflow into a knwf archive

    Args:
        workflow_name (str): Workflow directory to archive
    """
    shutil.make_archive(workflow_name, "zip", OUTPUT_PATH)
    os.rename(f"{workflow_name}.zip", f"{workflow_name}.knwf")
    cleanup()


def save_output_kdl_workflow(
    output_file: str, workflow: Workflow, node_list: List[AbstractNode]
) -> None:
    """
    Outputs node connections and node JSON as .kdl file

    Args:
        output_file (str): Name of output kdl file
        workflow (Workflow): Workflow to be written
        node_list (List[AbstractNode]): list of Nodes to be written
    """

    flattened_list = flatten_node_list(node_list)
    with open(output_file, "w") as file:
        indent = "    "
        file.write("Nodes {\n")
        for i, node in enumerate(flattened_list):
            output_text = node.kdl_str()
            if i < len(flattened_list) - 1:
                output_text += ","
            for line in output_text.splitlines():
                file.write(f"{indent}{line}\n")
        file.write("}\n\n")
        file.write(workflow.kdl_str())


def cleanup() -> None:
    """
    Cleans up temp directories

    """
    TMP_INPUT_DIR.cleanup()
    TMP_OUTPUT_DIR.cleanup()
