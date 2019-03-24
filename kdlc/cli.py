import sys
import click
from pathlib import Path
import kdlc
import logging
import jsonschema

from antlr4 import *
from kdlc.parser.KDLLexer import KDLLexer
from kdlc.parser.KDLParser import KDLParser
from kdlc.parser.KDLListener import KDLListener
import json


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


class KDLLoader(KDLListener):
    def __init__(self):
        self.nodes = {}
        self.connections = []

    def exitNode_settings(self, ctx):
        node_number = ctx.node().node_id().NUMBER().getText()
        # print(f"nodeNumber: {node_number}")

        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        node_settings = json.loads(json_string)
        # print(node_settings)

        self.nodes[node_number] = node_settings

    def exitConnection(self, ctx):
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        source_node_port = source_node.port().getText()

        destination_node = ctx.destination_node().node()
        destination_node_id = destination_node.node_id().getText()
        destination_node_port = destination_node.port().getText()

        connection = {
            "source_id": source_node_id,
            "dest_id": destination_node_id,
            "source_port": source_node_port,
            "dest_port": destination_node_port,
        }

        self.connections.append(connection)


def kdl_to_workflow(input_file, output_file):
    input = FileStream(input_file)
    lexer = KDLLexer(input)
    stream = CommonTokenStream(lexer)
    parser = KDLParser(stream)

    listener = KDLLoader()
    walker = ParseTreeWalker()

    nodes_tree = parser.nodes()
    walker.walk(listener, nodes_tree)

    workflow_tree = parser.workflow()
    walker.walk(listener, workflow_tree)

    print("======= nodes =======")
    print(listener.nodes)
    print("")

    print("==== connections ====")
    print(listener.connections)


def workflow_to_kdl(input_file, output_file):
    pass


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
