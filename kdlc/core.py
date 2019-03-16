import os
import zipfile
from shutil import make_archive
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape
import tempfile

jinja_env = Environment(
    loader=PackageLoader('kdlc', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    extensions=['jinja2.ext.do']
    #trim_blocks=True,
    #lstrip_blocks=True
)

TMP_INPUT_DIR = tempfile.TemporaryDirectory()
INPUT_PATH = TMP_INPUT_DIR.name
TMP_OUTPUT_DIR = tempfile.TemporaryDirectory()
OUTPUT_PATH = TMP_OUTPUT_DIR.name

NS = {"knime": "http://www.knime.org/2008/09/XMLConfig"}
ENTRY_TAG = f'{{{NS["knime"]}}}entry'
CONFIG_TAG = f'{{{NS["knime"]}}}config'


def unzip_workflow(input_file):
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


def extract_from_input_xml(input_file):
    """
    Parses the provided input file and returns a populated dict with
    associated values

    Args:
        input_file (str): XML file containing a node definition

    Returns:
        dict: Dict populated with values extracted from provided input file
    """
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    node = dict()
    node["name"] = root.find("./knime:entry[@key='name']", NS).attrib["value"]
    node["factory"] = root.find("./knime:entry[@key='factory']", NS).attrib["value"]
    node["bundle_name"] = root.find(
        "./knime:entry[@key='node-bundle-name']", NS
    ).attrib["value"]
    node["bundle_symbolic_name"] = root.find(
        "./knime:entry[@key='node-bundle-symbolic-name']", NS
    ).attrib["value"]
    node["bundle_version"] = root.find(
        "./knime:entry[@key='node-bundle-version']", NS
    ).attrib["value"]
    node["feature_name"] = root.find(
        "./knime:entry[@key='node-feature-name']", NS
    ).attrib["value"]
    node["feature_symbolic_name"] = root.find(
        "./knime:entry[@key='node-feature-symbolic-name']", NS
    ).attrib["value"]
    node["feature_version"] = root.find(
        "./knime:entry[@key='node-feature-version']", NS
    ).attrib["value"]
    model = list()
    for child in root.findall("./knime:config[@key='model']/*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            model.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            model.append(config)

    node["model"] = model
    return node


def extract_entry_tag(tree):
    """
    Extracts the entry tag from the provided tree

    Args:
        tree (ElementTree): The tree to extract entry tag from

    Returns:
        dict: Dict containing the entry tag definition
    """
    entry = {tree.attrib["key"]: tree.attrib["value"], "type": tree.attrib["type"]}
    if "isnull" in tree.attrib:
        entry["isnull"] = True
    return entry


def extract_config_tag(tree):
    """
    Extracts the config tag from the provided tree

    Args:
        tree (ElementTree): The tree to extract the config tag from

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
    config = {tree.attrib["key"]: config_value, "type": "config"}
    return config


def extract_nodes(input_file):
    """
    Extracts the list of nodes from the provided KNIME workflow

    Args:
        input_file (str): XML file containing a KNIME workflow

    Returns:
        list: The list of nodes within the KNIME workflow
    """
    node_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for child in root.findall("./knime:config[@key='nodes']/knime:config", NS):
        node = dict()
        node_id = child.find("./knime:entry[@key='id']", NS).attrib["value"]
        node["id"] = node_id
        settings_file = child.find(
            "./knime:entry[@key='node_settings_file']", NS
        ).attrib["value"]
        node["filename"] = settings_file
        node_list.append(node)
    return node_list


def extract_connections(input_file):
    """
    Extracts a list of connections from the provided KNIME workflow

    Args:
        input_file (str): XML file containing a KNIME workflow

    Returns:
        list: The list of connections within the KNIME workflow
    """
    connection_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for i, child in enumerate(
        root.findall("./knime:config[@key='connections']/knime:config", NS)
    ):
        connection = dict()
        connection["id"] = i
        source_id = child.find("./knime:entry[@key='sourceID']", NS).attrib["value"]
        connection["source_id"] = source_id
        dest_id = child.find("./knime:entry[@key='destID']", NS).attrib["value"]
        connection["dest_id"] = dest_id
        source_port = child.find("./knime:entry[@key='sourcePort']", NS).attrib["value"]
        connection["source_port"] = source_port
        dest_port = child.find("./knime:entry[@key='destPort']", NS).attrib["value"]
        connection["dest_port"] = dest_port
        connection_list.append(connection)
    return connection_list


def create_node_settings_from_template(node):
    """
    Creates an ElementTree with the provided node definition

    Args:
        node (dict): Node definition

    Returns:
        ElementTree: ElementTree populated with the provided node definition
    """
    template = jinja_env.get_template('settings_template.xml')
    model = node['settings']['model']
    template_root = ET.fromstring(template.render(node=node, model=model))
    return ET.ElementTree(template_root)


def create_workflow_knime_from_template(node_list, connection_list):
    """
    Creates an ElementTree with the provided node list and connection list

    Args:
        node_list (list): List of node definitions
        connection_list (list): List of connections amongst nodes

    Returns:
        ElementTree: ElementTree populated with nodes and their associated
        connections
    """
    template = jinja_env.get_template("workflow_template.xml")
    data = {"nodes": node_list, "connections": connection_list}
    return ET.ElementTree(ET.fromstring(template.render(data)))


def save_node_settings_xml(tree, output_path):
    """Writes the provided tree to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree
        output_path (str): Location to write the tree too
    """
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ET.register_namespace("", NS["knime"])
    tree.write(output_path, xml_declaration=True, encoding="UTF-8")


def save_workflow_knime(tree, output_path):
    """
    Writes the provided tree containing a KNIME workflow to the provided output path

    Args:
        tree (ElementTree): Populated ElementTree containing a KNIME workflow
        output_path (str): Location to write the tree too
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ET.register_namespace("", NS["knime"])
    tree.write(f"{output_path}/workflow.knime", xml_declaration=True, encoding="UTF-8")


def create_output_workflow(workflow_name):
    """
    Bundles the provided workflow into a knwf archive

    Args:
        workflow_name (str): Workflow directory to archive
    """
    make_archive(workflow_name, "zip", OUTPUT_PATH)
    base = os.path.splitext(f"{workflow_name}.zip")[0]
    os.rename(f"{workflow_name}.zip", base + ".knwf")
    TMP_INPUT_DIR.cleanup()
    TMP_OUTPUT_DIR.cleanup()
