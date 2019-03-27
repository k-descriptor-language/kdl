import kdlc

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from kdlc.parser.KDLLexer import KDLLexer
from kdlc.parser.KDLParser import KDLParser
from kdlc.KDLLoader import KDLLoader


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

    # print("======= nodes =======")
    # print(listener.nodes)
    # print("")
    #
    # print("==== connections ====")
    # print(listener.connections)

    build_knwf(listener.nodes, listener.connections, output_file)


def build_knwf(nodes, connections, output_filename):
    # TODO: revisit this name logic
    output_wf_name = output_filename.replace(".knwf", "")

    # Generate and save workflow.knime in output directory
    output_workflow_path = f"{kdlc.OUTPUT_PATH}/{output_wf_name}"

    output_workflow_knime = kdlc.create_workflow_knime_from_template(nodes, connections)
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
        #     kdlc.validate_node_from_schema(node)
        # except jsonschema.ValidationError as e:
        #     print(e.message)
        #     kdlc.cleanup()
        #     sys.exit(1)
        # except jsonschema.SchemaError as e:
        #     print(e.message)
        #     kdlc.cleanup()
        #     sys.exit(1)
        tree = kdlc.create_node_settings_from_template(node)
        kdlc.save_node_settings_xml(tree, f'{output_workflow_path}/{node["filename"]}')

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_wf_name)
