import os
import zipfile
from shutil import make_archive
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape
import tempfile
import json
import jsonschema
import textwrap

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
        else:
            ex = ValueError()
            ex.strerror = "Invalid settings tag"
            raise ex

    variables = list()
    for child in root.findall("./knime:config[@key='variables']/*", NS):
        if child.tag == CONFIG_TAG:
            config = extract_config_tag(child, is_variable=True)
            variables.append(config)
        else:
            ex = ValueError()
            ex.strerror = "Invalid settings tag"
            raise ex
    if variables:
        # print(f"model before merge: {model}")
        # print(f"variables: {variables}")
        merge_model_and_variables(model, variables)
        # print(f"model after merge: {model}")

    node["model"] = model
    return node


def merge_model_and_variables(model, variables):
    """
    Merges workflow variable exposed_variable and used_variable
    into model

    Args:
        model (dict): Dict containing model settings
        variables (dict): Dict containing workflow variables
    """
    model_iter = iter(model)
    curr_model = next(model_iter)
    for curr_variable in variables:
        curr_model_key = list(curr_model.keys())[0]
        curr_model_val = curr_model[curr_model_key]

        curr_variable_key = list(curr_variable.keys())[0]
        curr_variable_val = curr_variable[curr_variable_key]

        while curr_model_key != curr_variable_key:
            curr_model = next(model_iter)
            curr_model_key = list(curr_model.keys())[0]
            curr_model_val = curr_model[curr_model_key]

        if type(curr_model_val) is list and type(curr_variable_val) is list:
            merge_model_and_variables(curr_model_val, curr_variable_val)
        else:
            for curr in curr_variable_val:
                var_mod_key = list(curr.keys())[0]
                var_mod_val = curr[var_mod_key]
                curr_model[var_mod_key] = var_mod_val


def extract_entry_tag(tree):
    """
    Extracts the entry tag from the provided tree

    Args:
        tree (ElementTree): The tree to extract entry tag from

    Returns:
        dict: Dict containing the entry tag definition
    """
    if tree.attrib["type"] == "xstring":
        entry = {tree.attrib["key"]: tree.attrib["value"]}
    elif tree.attrib["type"] == "xboolean":
        if tree.attrib["value"] == "true":
            entry = {tree.attrib["key"]: True}
        else:
            entry = {tree.attrib["key"]: False}
    elif tree.attrib["type"] == "xint":
        entry = {tree.attrib["key"]: int(tree.attrib["value"])}
    elif tree.attrib["type"] in ["xlong", "xshort"]:
        entry = {
            tree.attrib["key"]: int(tree.attrib["value"]),
            "data_type": tree.attrib["type"],
        }
    elif tree.attrib["type"] == "xfloat":
        entry = {tree.attrib["key"]: float(tree.attrib["value"])}
    elif tree.attrib["type"] == "xdouble":
        entry = {
            tree.attrib["key"]: float(tree.attrib["value"]),
            "data_type": tree.attrib["type"],
        }
    elif tree.attrib["type"] in ["xchar", "xbyte"]:
        entry = {
            tree.attrib["key"]: tree.attrib["value"],
            "data_type": tree.attrib["type"],
        }
    else:
        ex = ValueError()
        ex.strerror = "Invalid entry type"
        raise ex

    if "isnull" in tree.attrib:
        entry["isnull"] = True
    return entry


def extract_config_tag(tree, is_variable=False):
    """
    Extracts the config tag from the provided tree

    Args:
        tree (ElementTree): The tree to extract the config tag from
        is_variable (Boolean): If the tree is a workflow variable tree

    Returns:
        dict: Dict containing the config tag definition
    """
    config_value = list()
    for child in tree.findall("./*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            if is_variable:
                if "isnull" not in entry.keys():
                    config_value.append(entry)
            else:
                config_value.append(entry)
        elif child.tag == CONFIG_TAG:
            if is_variable:
                config = extract_config_tag(child, is_variable=True)
            else:
                config = extract_config_tag(child)
            config_value.append(config)
        else:
            ex = ValueError()
            ex.strerror = "Invalid child tag"
            raise ex
    config = {tree.attrib["key"]: config_value}
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


def validate_node_from_schema(node):
    """
    Validates node settings against JSON Schema

    Args:
        node (dict): Node definition

    Raises:
        jsonschema.ValidationError: if node does not follow defined json schema

        jsonschema.SchemaError: if schema definition is invalid

    """
    schema = open(
        f"{os.path.dirname(__file__)}/json_schemas/{node['settings']['name']}.json"
    ).read()
    jsonschema.validate(instance=node["settings"], schema=json.loads(schema))


def create_node_settings_from_template(node):
    """
    Creates an ElementTree with the provided node definition

    Args:
        node (dict): Node definition

    Returns:
        ElementTree: ElementTree populated with the provided node definition
    """
    template = jinja_env.get_template("settings_template.xml")
    model = node["settings"]["model"]
    for value in model:
        k = list(value.keys())[0]
        v = value[k]
        if type(v) is list:
            set_config_element_type(value)
        else:
            set_entry_element_type(value)
    # print(model)
    variables = extract_variables_from_model(model)
    # print(variables)
    template_root = ET.fromstring(
        template.render(node=node, model=model, variables=variables)
    )
    return ET.ElementTree(template_root)


def extract_variables_from_model(model):
    """
    Extracts workflow variables from model and returns them in own list

    Args:
        model (dict): Model node settings

    Returns:
        List: List containing workflow variables
    """
    variables = list()
    for curr in model:
        curr_model_key = list(curr.keys())[0]
        curr_model_val = curr[curr_model_key]
        if type(curr_model_val) is list:
            new_var = extract_variables_from_model(curr_model_val)
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


def set_entry_element_type(entry):
    """
    Sets an entry Element's type and value based on the provided entry definition

    Args:
        entry (dict): Entry definition

    """
    entry_key = list(entry.keys())[0]
    entry_type = type(entry[entry_key])
    entry_value = str(entry[entry_key])
    if "data_type" in entry:
        entry_type = entry["data_type"]
    elif entry_type is int:
        entry_type = "xint"
    elif entry_type is float:
        entry_type = "xfloat"
    elif entry_type is bool:
        entry_value = entry_value.lower()
        entry_type = "xboolean"
    elif entry_type is str:
        entry_type = "xstring"
    else:
        ex = ValueError()
        ex.strerror = "Cannot set element type"
        raise ex
    entry["data_type"] = entry_type
    entry[entry_key] = entry_value


def set_config_element_type(config):
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
    cleanup()


def save_output_kdl_workflow(output_file, connection_list, node_list):
    """
    Outputs node connections and node JSON as .kdl file

    Args:
        output_file (str): Name of output kdl file
        connection_list (list): list of connection dicts to be written
        node_list (list): list of node dicts to be written
    """

    wrapper = textwrap.TextWrapper(
        initial_indent="\t", subsequent_indent="\t", width=120
    )
    with open(output_file, "w") as file:
        file.write("Nodes {\n")
        for node in node_list:
            output_text = f"(n{node['id']}): {json.dumps(node['settings'], indent=4)}"
            for line in output_text.splitlines():
                wrapped = wrapper.fill(line)
                file.write(f"{wrapped}\n")
            file.write("\n")
        file.write("}\n\n")
        file.write("Workflow {\n")
        for connection in connection_list:
            if connection["source_port"] == "0" and connection["dest_port"] == "0":
                wrapped = wrapper.fill(
                    f"(n{connection['source_id']})~~>" f"(n{connection['dest_id']})\n"
                )
            else:
                wrapped = wrapper.fill(
                    f"(n{connection['source_id']}:{connection['source_port']})-->"
                    f"(n{connection['dest_id']}:{connection['dest_port']})\n"
                )
            file.write(f"{wrapped}\n")
        file.write("}\n")


def cleanup():
    """
    Cleans up temp directories

    """
    TMP_INPUT_DIR.cleanup()
    TMP_OUTPUT_DIR.cleanup()
