import kdlc

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from kdlc.parser.KDLLexer import KDLLexer
from kdlc.parser.KDLParser import KDLParser
from kdlc.KDLLoader import KDLLoader
from kdlc.objects import AbstractNode, Workflow
from typing import List


def kdl_to_workflow(input_file: str, output_file: str) -> None:
    input_stream = FileStream(input_file)
    lexer = KDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = KDLParser(stream)

    listener = KDLLoader()
    walker = ParseTreeWalker()

    nodes_tree = parser.nodes()
    walker.walk(listener, nodes_tree)

    workflow_tree = parser.workflow()
    walker.walk(listener, workflow_tree)

    # print("======= nodes =======")
    # print(listener.nodes)
    # print("")
    #
    # print("==== connections ====")
    # print(listener.connections)

    listener.nodes = kdlc.unflatten_node_list(listener.nodes)
    kdlc.normalize_connections(listener.nodes, listener.connections)

    workflow = Workflow(
        variables=listener.global_variables, connections=listener.connections
    )

    build_knwf(listener.nodes, workflow, output_file)


def update_workflow_with_kdl(
    input_file: str, output_file: str, modify_file: str
) -> None:
    pass


def kdl_to_workflow_custom_template(
    input_file: str, output_file: str, nodes: str
) -> None:
    pass


def workflow_to_kdl_custom_template(
    input_file: str, output_file: str, nodes: str
) -> None:
    pass


def workflow_to_kdl(input_file: str, output_file: str) -> None:
    # Extract workflow
    input_workflow_name = kdlc.unzip_workflow(input_file)

    input_workflow_path = f"{kdlc.INPUT_PATH}/{input_workflow_name}"

    input_workflow_filename = f"{input_workflow_path}/workflow.knime"

    # Parse global variables from workflow.knime
    input_global_variable_list = kdlc.extract_global_wf_variables(
        input_workflow_filename
    )
    # print(input_global_variable_list)

    # Parse nodes filenames from workflow.knime
    node_filename_list = kdlc.extract_node_filenames(input_workflow_filename)
    # print(node_filename_list)

    # Parse settings.xml for each node in workflow.knime
    input_node_list = kdlc.extract_nodes_from_filenames(
        input_workflow_path, node_filename_list
    )
    # print(input_node_list)

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(
        input_workflow_filename, input_node_list
    )
    # print(input_connection_list)

    # Create workflow and save output KDL
    input_workflow = Workflow(input_connection_list, input_global_variable_list)
    kdlc.save_output_kdl_workflow(output_file, input_workflow, input_node_list)

    kdlc.cleanup()


def build_knwf(
    nodes: List[AbstractNode], workflow: Workflow, output_filename: str
) -> None:
    output_wf_name = output_filename.replace(".knwf", "")

    # Generate and save workflow.knime in output directory
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_wf_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(nodes, workflow)
    kdlc.save_workflow_knime(output_workflow_knime, output_workflow_path)

    # Generate and save XML for nodes in output directory
    kdlc.create_node_files(output_workflow_path, nodes)

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_wf_name)
