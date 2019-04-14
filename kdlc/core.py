import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape
import tempfile
import textwrap
from typing import List, Any, Dict
from kdlc.objects import Node, Connection, MetaNode, AbstractNode, Workflow

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

META_IN = MetaNode(node_id="-1", name="META_IN")
META_OUT = MetaNode(node_id="-1", name="META_OUT")


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

    name_ele = root.find("./knime:entry[@key='name']", NS)
    if name_ele is not None:
        name = name_ele.attrib["value"]

    factory_ele = root.find("./knime:entry[@key='factory']", NS)
    if factory_ele is not None:
        factory = factory_ele.attrib["value"]

    bundle_name_ele = root.find("./knime:entry[@key='node-bundle-name']", NS)
    if bundle_name_ele is not None:
        bundle_name = bundle_name_ele.attrib["value"]

    bundle_symbolic_name_ele = root.find(
        "./knime:entry[@key='node-bundle-symbolic-name']", NS
    )
    if bundle_symbolic_name_ele is not None:
        bundle_symbolic_name = bundle_symbolic_name_ele.attrib["value"]

    bundle_version_ele = root.find("./knime:entry[@key='node-bundle-version']", NS)
    if bundle_version_ele is not None:
        bundle_version = bundle_version_ele.attrib["value"]

    feature_name_ele = root.find("./knime:entry[@key='node-feature-name']", NS)
    if feature_name_ele is not None:
        feature_name = feature_name_ele.attrib["value"]

    feature_symbolic_name_ele = root.find(
        "./knime:entry[@key='node-feature-symbolic-name']", NS
    )
    if feature_symbolic_name_ele is not None:
        feature_symbolic_name = feature_symbolic_name_ele.attrib["value"]

    feature_version_ele = root.find("./knime:entry[@key='node-feature-version']", NS)
    if feature_version_ele is not None:
        feature_version = feature_version_ele.attrib["value"]

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
        node_id_ele = child.find("./knime:entry[@key='id']", NS)
        if node_id_ele is not None:
            node["node_id"] = node_id_ele.attrib["value"]

        settings_file_ele = child.find("./knime:entry[@key='node_settings_file']", NS)
        if settings_file_ele is not None:
            node["filename"] = settings_file_ele.attrib["value"]

        node_type_ele = child.find("./knime:entry[@key='node_type']", NS)
        if node_type_ele is not None:
            node["node_type"] = node_type_ele.attrib["value"]

        if node["node_type"] == "MetaNode":
            base_tree = ET.parse(f"{input_path}/{node['filename']}")
            root = base_tree.getroot()

            name_ele = root.find("./knime:entry[@key='name']", NS)
            if name_ele is not None:
                node["name"] = name_ele.attrib["value"]
            node["children"] = extract_node_filenames(
                f"{input_path}/{node['filename']}"
            )

        node_list.append(node)
    return node_list


def extract_nodes_from_filenames(workflow_path, node_filenames, parent_id=None):
    input_node_list = list()
    for curr in node_filenames:
        infile = f'{workflow_path}/{curr["filename"]}'
        if parent_id is not None:
            curr["node_id"] = f"{parent_id}.{curr['node_id']}"
        if curr["node_type"] == "NativeNode":
            node = extract_node_from_settings_xml(curr["node_id"], infile)
            input_node_list.append(node)
        elif curr["node_type"] == "MetaNode":
            # connections = extract_connections(infile)
            children = extract_nodes_from_filenames(
                workflow_path=os.path.dirname(infile),
                node_filenames=curr["children"],
                parent_id=curr["node_id"],
            )
            connections = extract_connections(infile, children)
            node = MetaNode(
                node_id=curr["node_id"],
                name=curr["name"],
                children=children,
                connections=connections,
            )
            input_node_list.append(node)
            # input_node_list = input_node_list + children

    return input_node_list


def flatten_node_list(node_list):
    flattened_list = list()
    for node in node_list:
        flattened_list.append(node)
        if type(node) is MetaNode:
            flattened_list += flatten_node_list(node.children)
    return flattened_list


def extract_connections(
    input_file: str, node_list: List[AbstractNode]
) -> List[Connection]:
    """
    Extracts a list of connections from the provided KNIME workflow

    Args:
        input_file (str): Name of input workflow.knime file
        node_list (List[AbstractNode]): List of nodes for connections

    Returns:
        list: The list of connections within the KNIME workflow
    """
    node_dict = {i.node_id.rsplit(".", 1)[-1]: i for i in node_list}
    connection_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for i, child in enumerate(
        root.findall("./knime:config[@key='connections']/knime:config", NS)
    ):
        source_id_ele = child.find("./knime:entry[@key='sourceID']", NS)
        if source_id_ele is not None:
            source_id = source_id_ele.attrib["value"]
            source_node = META_IN if source_id == "-1" else node_dict[source_id]

        dest_id_ele = child.find("./knime:entry[@key='destID']", NS)
        if dest_id_ele is not None:
            dest_id = dest_id_ele.attrib["value"]
            dest_node = META_OUT if dest_id == "-1" else node_dict[dest_id]

        source_port_ele = child.find("./knime:entry[@key='sourcePort']", NS)
        if source_port_ele is not None:
            source_port = source_port_ele.attrib["value"]

        dest_port_ele = child.find("./knime:entry[@key='destPort']", NS)
        if dest_port_ele is not None:
            dest_port = dest_port_ele.attrib["value"]

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


def extract_global_wf_variables(input_file):
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
        variable = dict()
        variable_name_ele = child.find("./knime:entry[@key='name']", NS)
        if variable_name_ele is not None:
            variable_name = variable_name_ele.attrib["value"]

        variable_class_ele = child.find("./knime:entry[@key='class']", NS)
        if variable_class_ele is not None:
            variable_class = variable_class_ele.attrib["value"]

        variable_value_ele = child.find("./knime:entry[@key='value']", NS)
        if variable_value_ele is not None and variable_class is not None:
            if variable_class == "STRING":
                variable_value = variable_value_ele.attrib["value"]
            elif variable_class == "DOUBLE":
                variable_value = float(variable_value_ele.attrib["value"])
            elif variable_class == "INTEGER":
                variable_value = int(variable_value_ele.attrib["value"])
        variable[variable_name] = variable_value
        global_variable_list.append(variable)
    return global_variable_list


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

    node.extract_variables_from_model()
    template_root = ET.fromstring(template.render(node=node))
    return ET.ElementTree(template_root)


def create_workflow_knime_from_template(
    node_list: List[Node], connection_list: List[Connection], global_variable_list
) -> ET.ElementTree:
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        node_list (list): List of Node definitions
        connection_list (list): List of Connections amongst nodes
        global_variable_list (list): List of global workflow variables

    Returns:
        ElementTree: ElementTree populated with nodes and their associated
        connections
    """
    set_class_for_global_variables(global_variable_list)
    template = jinja_env.get_template("workflow_template.xml")
    data = {
        "nodes": node_list,
        "connections": connection_list,
        "variables": global_variable_list,
    }
    return ET.ElementTree(ET.fromstring(template.render(data)))


def set_class_for_global_variables(variable_list):
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
    wrapper = textwrap.TextWrapper(
        initial_indent="\t", subsequent_indent="\t", width=120
    )
    with open(output_file, "w") as file:
        file.write("Nodes {\n")
        for i, node in enumerate(flattened_list):
            output_text = node.kdl_str()
            if i < len(flattened_list) - 1:
                output_text += ","
            for line in output_text.splitlines():
                wrapped = wrapper.fill(line)
                file.write(f"{wrapped}\n")
        file.write("}\n\n")
        file.write(workflow.kdl_str())


def cleanup() -> None:
    """
    Cleans up temp directories

    """
    TMP_INPUT_DIR.cleanup()
    TMP_OUTPUT_DIR.cleanup()
