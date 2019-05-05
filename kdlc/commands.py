import kdlc

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from kdlc.parser.KDLLexer import KDLLexer
from kdlc.parser.KDLParser import KDLParser
from kdlc.KDLLoader import KDLLoader
from kdlc.objects import AbstractNode, Node, Workflow, TemplateCatalogue
from typing import List, Optional
from loguru import logger
import os


def kdl_to_workflow(input_file: str, output_file: str, custom_path: Optional[str]) -> None:
    """
        Converts a KDL file (.kdl) to a KNIME workflow archive.

    :param input_file: Name of the KDL file
    :param output_file: Name of the KNIME archive
    :param custom_path: Path to the user specified templates catalogue
    """
    logger.debug("======= BEGIN KDL to WORKFLOW =======")

    input_stream = FileStream(input_file)
    lexer = KDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = KDLParser(stream)

    template_catalogue_path = f"{os.path.dirname(__file__)}/node_templates"
    template_catalogue = TemplateCatalogue(template_catalogue_path, custom_path)
    listener = KDLLoader(template_catalogue)
    walker = ParseTreeWalker()

    nodes_tree = parser.nodes()
    walker.walk(listener, nodes_tree)

    workflow_tree = parser.workflow()
    walker.walk(listener, workflow_tree)

    logger.debug("======= Nodes from walker =======")
    logger.debug([str(node) for node in listener.nodes])
    logger.debug("==== Connections from walker ====")
    logger.debug([str(connection) for connection in listener.connections])

    listener.nodes = kdlc.unflatten_node_list(listener.nodes)
    kdlc.normalize_connections(listener.nodes, listener.connections)

    logger.debug("======= Unflattened Nodes =======")
    logger.debug([str(node) for node in listener.nodes])
    logger.debug("==== Normalized Connections ====")
    logger.debug([str(connection) for connection in listener.connections])

    workflow = Workflow(
        variables=listener.global_variables, connections=listener.connections
    )

    build_knwf(listener.nodes, workflow, output_file)


def workflow_to_kdl(input_file: str, output_file: str) -> None:
    """
        Converts a KNIME workflow archive to a kdl file.

    :param input_file:  Name of the KNIME archive
    :param output_file: Name of the KDL file
    """
    logger.debug("======= BEGIN WORKFLOW to KDL =======")

    # Extract workflow
    input_workflow_name = kdlc.unzip_workflow(input_file)

    input_workflow_path = f"{kdlc.INPUT_PATH}/{input_workflow_name}"

    input_workflow_filename = f"{input_workflow_path}/workflow.knime"

    # Parse global variables from workflow.knime
    input_global_variable_list = kdlc.extract_global_wf_variables(
        input_workflow_filename
    )
    logger.debug("======= Global Variables from Workflow =======")
    logger.debug([str(variable) for variable in input_global_variable_list])

    # Parse nodes filenames from workflow.knime
    node_filename_list = kdlc.extract_node_filenames(input_workflow_filename)
    logger.debug("======= Raw Node Data from Workflow =======")
    logger.debug([str(filename) for filename in node_filename_list])

    # Parse settings.xml for each node in workflow.knime
    input_node_list = kdlc.extract_nodes_from_filenames(
        input_workflow_path, node_filename_list
    )
    logger.debug("======= Node Objects from Workflow =======")
    logger.debug([str(node) for node in input_node_list])

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(
        input_workflow_filename, input_node_list
    )
    logger.debug("======= Connections from Workflow =======")
    logger.debug([str(connection) for connection in input_connection_list])

    # Create workflow and save output KDL
    input_workflow = Workflow(input_connection_list, input_global_variable_list)
    kdlc.save_output_kdl_workflow(output_file, input_workflow, input_node_list)

    kdlc.cleanup()


def build_knwf(
    nodes: List[AbstractNode], workflow: Workflow, output_filename: str
) -> None:
    """
        Builds the knwf archive in the file system:
        write workflow.knime
        Write associated sxml
        zip the files into a .knwf archive

    :param nodes: List of Nodes in the workflow
    :param workflow: Represents the workflow being built
    :param output_filename: Name of the output archive file name
    :return:
    """
    logger.debug("======= BEGIN BUILD KNWF =======")

    output_wf_name = output_filename.replace(".knwf", "")

    # Verify urls in Nodes and warn if needed
    for node in nodes:
        if isinstance(node, Node):
            node.verify_urls_and_warn()

    # Generate and save workflow.knime in output directory
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_wf_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(nodes, workflow)
    kdlc.save_workflow_knime(output_workflow_knime, output_workflow_path)

    # Generate and save XML for nodes in output directory
    kdlc.create_node_files(output_workflow_path, nodes)

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_wf_name)
