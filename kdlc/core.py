import os
import zipfile
from shutil import make_archive, rmtree
import xml.etree.ElementTree as ET
from jinja2 import Environment, PackageLoader, select_autoescape

jinja_env = Environment(
    loader=PackageLoader('kdlc', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

INPUT_PATH = 'input'
OUTPUT_PATH = 'output'
NS = {'knime': 'http://www.knime.org/2008/09/XMLConfig'}
ENTRY_TAG = f'{{{NS["knime"]}}}entry'
CONFIG_TAG = f'{{{NS["knime"]}}}config'


def unzip_workflow(input_file):
    if not os.path.exists(INPUT_PATH):
        os.makedirs(INPUT_PATH)
    else:
        rmtree(INPUT_PATH)
        os.makedirs(INPUT_PATH)

    zip_ref = zipfile.ZipFile(input_file, 'r')
    zip_ref.extractall(INPUT_PATH)
    zip_ref.close()
    return os.listdir(INPUT_PATH).pop()


def extract_from_input_xml(input_file):
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    node = dict()
    node['name'] = root.find("./knime:entry[@key='name']", NS).attrib['value']
    node['factory'] = root.find("./knime:entry[@key='factory']", NS).attrib['value']
    node['bundle_name'] = root.find("./knime:entry[@key='node-bundle-name']", NS).attrib['value']
    node['bundle_symbolic_name'] = root.find("./knime:entry[@key='node-bundle-symbolic-name']", NS).attrib['value']
    node['bundle_version'] = root.find("./knime:entry[@key='node-bundle-version']", NS).attrib['value']
    node['feature_name'] = root.find("./knime:entry[@key='node-feature-name']", NS).attrib['value']
    node['feature_symbolic_name'] = root.find("./knime:entry[@key='node-feature-symbolic-name']", NS).attrib['value']
    node['feature_version'] = root.find("./knime:entry[@key='node-feature-version']", NS).attrib['value']
    model = list()
    for child in root.findall("./knime:config[@key='model']/*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            model.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            model.append(config)

    node['model'] = model
    return node


def extract_entry_tag(tree):
    entry = {tree.attrib['key']: tree.attrib['value'],
             'type': tree.attrib['type']}
    if 'isnull' in tree.attrib:
        entry['isnull'] = True
    return entry


def extract_config_tag(tree):
    config_value = list()
    for child in tree.findall("./*", NS):
        if child.tag == ENTRY_TAG:
            entry = extract_entry_tag(child)
            config_value.append(entry)
        elif child.tag == CONFIG_TAG:
            config = extract_config_tag(child)
            config_value.append(config)
    config = {tree.attrib['key']: config_value, 'type': 'config'}
    return config


def extract_nodes(input_file):
    node_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for child in root.findall("./knime:config[@key='nodes']/knime:config", NS):
        node = dict()
        node_id = child.find("./knime:entry[@key='id']", NS).attrib['value']
        node['id'] = node_id
        settings_file = child.find("./knime:entry[@key='node_settings_file']", NS).attrib['value']
        node['filename'] = settings_file
        node_list.append(node)
    return node_list


def extract_connections(input_file):
    connection_list = list()
    base_tree = ET.parse(input_file)
    root = base_tree.getroot()
    for i, child in enumerate(root.findall("./knime:config[@key='connections']/knime:config", NS)):
        connection = dict()
        connection['id'] = i
        source_id = child.find("./knime:entry[@key='sourceID']", NS).attrib['value']
        connection['source_id'] = source_id
        dest_id = child.find("./knime:entry[@key='destID']", NS).attrib['value']
        connection['dest_id'] = dest_id
        source_port = child.find("./knime:entry[@key='sourcePort']", NS).attrib['value']
        connection['source_port'] = source_port
        dest_port = child.find("./knime:entry[@key='destPort']", NS).attrib['value']
        connection['dest_port'] = dest_port
        connection_list.append(connection)
    return connection_list


def create_node_xml_from_template(node):
    template = jinja_env.get_template('settings_template.xml')
    template_root = ET.fromstring(template.render(node=node))
    model = template_root.find("./knime:config[@key='model']", NS)
    for curr in node['settings']['model']:
        if curr['type'] == 'config':
            config = create_config_element(curr)
            model.append(config)
        else:
            entry = create_entry_element(curr)
            model.append(entry)
    return ET.ElementTree(template_root)


def create_workflow_knime_from_template(node_list, connection_list):
    template = jinja_env.get_template('workflow_template.xml')
    data = {'nodes': node_list, 'connections': connection_list}
    template_tree = ET.ElementTree(ET.fromstring(template.render(data)))
    return template_tree


def create_entry_element(entry):
    entry_key = list(entry.keys())[0]
    entry_value = entry[entry_key]
    entry_type = entry['type']
    entry_elt = ET.Element('entry', key=entry_key, type=entry_type, value=entry_value)
    if 'isnull' in entry:
        entry_elt.attrib['isnull'] = 'true'
    return entry_elt


def create_config_element(config):
    config_key = list(config.keys())[0]
    config_values = config[config_key]
    config_elt = ET.Element('config', key=config_key)
    for value in config_values:
        if value['type'] == 'config':
            child_config = create_config_element(value)
            config_elt.append(child_config)
        else:
            child_entry = create_entry_element(value)
            config_elt.append(child_entry)
    return config_elt


def save_node_xml(tree, output_path):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ET.register_namespace('', NS['knime'])
    tree.write(output_path, xml_declaration=True, encoding='UTF-8')


def save_workflow_knime(tree, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ET.register_namespace('', NS['knime'])
    tree.write(f'{output_path}/workflow.knime', xml_declaration=True, encoding='UTF-8')


def create_output_workflow(workflow_name):
    make_archive(workflow_name, 'zip', OUTPUT_PATH)
    base = os.path.splitext(f'{workflow_name}.zip')[0]
    os.rename(f'{workflow_name}.zip', base + '.knwf')
    rmtree(INPUT_PATH)
    rmtree(OUTPUT_PATH)
