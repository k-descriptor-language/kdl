import sys
import click
from pathlib import Path
import kdlc
import logging
import jsonschema
import json
from antlr4 import *
from .parse import *


logger = logging.getLogger("kdlc.cli")


@click.command()
@click.option(
    "--output",
    "-o",
    "output_file",
    required=True,
    help="The output file, either .knwf or .kdl",
)
@click.option(
    "--input",
    "-i",
    "input_file",
    required=True,
    help="The input file, either .knwf or .kdl",
    type=click.Path(exists=True),
)
@click.option(
    "--modify",
    "-m",
    "modify_file",
    help="The KNIME workflow file (.knwf) being modified",
    type=click.Path(exists=True),
)
@click.option(
    "--nodes",
    "-n",
    help="The path to the custom node templates",
    type=click.Path(exists=True),
)
def prompt(input_file, output_file, modify_file, nodes):
    if modify_file and nodes:
        raise click.UsageError("nodes and modify options cannot be used simultaneously")

    if modify_file:
        if Path(modify_file).suffix != ".knwf":
            raise click.BadParameter("modify file must be of file type *.knwf")

        if Path(input_file).suffix != ".kdl":
            raise click.BadParameter("input file must be of file type *.kdl")

        if Path(output_file).suffix != ".knwf":
            raise click.BadParameter("output file must be of file type *.knwf")

        update_workflow_with_kdl(input_file, output_file, modify_file)

    elif nodes:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdl_to_workflow_custom_template(input_file, output_file, nodes)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            workflow_to_kdl_custom_template(input_file, output_file, nodes)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )

    elif input_file and output_file:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdl_to_workflow(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            workflow_to_kdl(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".knwf":
            # This functionality is here for development purposes and not part of
            # the final solution
            logger.warning("TEMPORARY! This will be removed before the release.")
            workflow_to_workflow(input_file, output_file)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )


def update_workflow_with_kdl(input_file, output_file, modify_file):
    pass


def kdl_to_workflow_custom_template(input_file, output_file, nodes):
    pass


def workflow_to_kdl_custom_template(input_file, output_file, nodes):
    pass


def kdl_to_workflow(input_file, output_file):
    kdl_input = FileStream(input_file)
    lexer = KDLLexer(kdl_input)
    stream = CommonTokenStream(lexer)
    parser = KDLParser(stream)

    connection_list = []
    node_list = []

    tree = parser.connection()
    source_id = tree.node(0).node_id().getText()
    source_port = tree.node(0).port().port_id().getText()
    dest_id = tree.node(1).node_id().getText()
    dest_port = tree.node(1).port().port_id().getText()
    connection1 = {
        "id": "0",
        "source_id": source_id,
        "source_port": source_port,
        "dest_id": dest_id,
        "dest_port": dest_port,
    }
    connection_list.append(connection1)

    tree2 = parser.connection()
    source_id = tree2.node(0).node_id().getText()
    source_port = tree2.node(0).port().port_id().getText()
    dest_id = tree2.node(1).node_id().getText()
    dest_port = tree2.node(1).port().port_id().getText()
    connection2 = {
        "id": "1",
        "source_id": source_id,
        "source_port": source_port,
        "dest_id": dest_id,
        "dest_port": dest_port,
    }
    connection_list.append(connection2)

    tree3 = parser.node_settings()
    node_id = tree3.node().node_id().getText()
    node_settings = json.loads(tree3.json().getText())
    node1 = {
        "id": node_id,
        "filename": f"{node_settings['name']} (#{node_id})/settings.xml",
        "settings": node_settings,
    }
    node_list.append(node1)

    tree4 = parser.node_settings()
    node_id = tree4.node().node_id().getText()
    node_settings = json.loads(tree4.json().getText())
    node2 = {
        "id": node_id,
        "filename": f"{node_settings['name']} (#{node_id})/settings.xml",
        "settings": node_settings,
    }
    node_list.append(node2)

    tree5 = parser.node_settings()
    node_id = tree5.node().node_id().getText()
    node_settings = json.loads(tree5.json().getText())
    node3 = {
        "id": node_id,
        "filename": f"{node_settings['name']} (#{node_id})/settings.xml",
        "settings": node_settings,
    }
    node_list.append(node3)

    print(node_list)


def workflow_to_kdl(input_file, output_file):
    # Extract workflow
    input_workflow_name = kdlc.unzip_workflow(input_file)
    input_workflow_path = f"{kdlc.INPUT_PATH}/{input_workflow_name}"

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(
        f"{input_workflow_path}/workflow.knime"
    )
    # print(input_connection_list)

    # Parse nodes from workflow.knime
    input_node_list = kdlc.extract_nodes(f"{input_workflow_path}/workflow.knime")
    # print(input_node_list)

    # Parse settings.xml for each node in workflow.knime and add to node
    for node in input_node_list:
        infile = f'{input_workflow_path}/{node["filename"]}'
        node["settings"] = kdlc.extract_from_input_xml(infile)
        # print(node)
    # print(input_node_list)

    kdlc.save_output_kdl_workflow(output_file, input_connection_list, input_node_list)

    kdlc.cleanup()


def workflow_to_workflow(input_file, output_file):
    output_wf_name = output_file.replace(".knwf", "")

    # Extract workflow
    input_workflow_name = kdlc.unzip_workflow(input_file)
    input_workflow_path = f"{kdlc.INPUT_PATH}/{input_workflow_name}"

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(
        f"{input_workflow_path}/workflow.knime"
    )
    # print(input_connection_list)

    # Parse nodes from workflow.knime
    input_node_list = kdlc.extract_nodes(f"{input_workflow_path}/workflow.knime")
    # print(input_node_list)

    # Parse settings.xml for each node in workflow.knime and add to node
    for node in input_node_list:
        infile = f'{input_workflow_path}/{node["filename"]}'
        node["settings"] = kdlc.extract_from_input_xml(infile)
    # print(input_node_list)

    # Generate and save workflow.knime in output directory
    output_workflow_name = f"{input_workflow_name}_new"
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_workflow_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(
        input_node_list, input_connection_list
    )
    kdlc.save_workflow_knime(output_workflow_knime, output_workflow_path)

    # Generate and save XML for nodes in output directory
    for node in input_node_list:
        # POC for JSON validation, uncomment below and indent to test diff scenarios
        # if node["settings"]["name"] == "CSV Reader":
        # empty url
        # node["settings"]["model"][0]["url"] = ""
        # no url entry
        # node["settings"]["model"].pop(0)
        # update url
        # node["settings"]["model"][0]["url"] = "/path/to/other/file.csv"
        # not csv
        # node["settings"]["model"][0]["url"] = "/path/to/other/file.txt"
        try:
            kdlc.validate_node_from_schema(node)
        except jsonschema.ValidationError as e:
            print(e.message)
            kdlc.cleanup()
            sys.exit(1)
        except jsonschema.SchemaError as e:
            print(e.message)
            kdlc.cleanup()
            sys.exit(1)
        tree = kdlc.create_node_settings_from_template(node)
        kdlc.save_node_settings_xml(tree, f'{output_workflow_path}/{node["filename"]}')

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_wf_name)
