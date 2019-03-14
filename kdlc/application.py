import sys
import os
import getopt

import kdlc


def main():
    argv = sys.argv[1:]
    if len(argv) == 0:
        print("kdlc -i <input_file>")
        sys.exit(2)

    input_file = ""

    try:
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print("kdlc -i <input_file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("kdlc -i <input_file>")
            sys.exit()
        elif opt == "-i" and arg:
            input_file = os.path.abspath(arg)
        else:
            print("kdlc -i <input_file>")
            sys.exit()

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
        tree = kdlc.create_node_settings_from_template(node)
        kdlc.save_node_settings_xml(tree, f'{output_workflow_path}/{node["filename"]}')

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(output_workflow_name)


if __name__ == "__main__":
    main()
