import kdlc

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from kdlc.parser.KDLLexer import KDLLexer
from kdlc.parser.KDLParser import KDLParser
from kdlc.KDLLoader import KDLLoader
from kdlc.objects import Node, Connection
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

    build_knwf(
        listener.nodes, listener.connections, listener.global_variables, output_file
    )


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

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(input_workflow_filename)
    # print(input_connection_list)

    # Parse global variables from workflow.knime
    input_global_variable_list = kdlc.extract_global_wf_variables(
        input_workflow_filename
    )
    # print(input_global_variable_list)

    # Parse nodes from workflow.knime
    node_filename_list = kdlc.extract_node_filenames(input_workflow_filename)
    # print(node_filename_list)

    # Parse settings.xml for each node in workflow.knime and add to node
    input_node_list = list()
    for curr in node_filename_list:
        infile = f'{input_workflow_path}/{curr["filename"]}'
        node = kdlc.extract_from_input_xml(curr["node_id"], infile)
        input_node_list.append(node)
    # print(input_node_list)

    kdlc.save_output_kdl_workflow(
        output_file, input_connection_list, input_node_list, input_global_variable_list
    )

    kdlc.cleanup()


def build_knwf(
    nodes: List[Node],
    connections: List[Connection],
    global_variables,
    output_filename: str,
) -> None:
    # TODO: revisit this name logic
    output_wf_name = output_filename.replace(".knwf", "")

    # Generate and save workflow.knime in output directory
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_wf_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(
        nodes, connections, global_variables
    )
    kdlc.save_workflow_knime(output_workflow_knime, output_workflow_path)

    # Generate and save XML for nodes in output directory
    for node in nodes:
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
        tree = kdlc.create_node_settings_from_template(node)
        kdlc.save_node_settings_xml(
            tree, f"{output_workflow_path}/{node.get_filename()}"
        )

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_wf_name)
