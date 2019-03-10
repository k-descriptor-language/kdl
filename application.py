import sys
import os
import getopt
from shutil import rmtree

import kdlc


def main(argv):
    input_file = ''

    try:
        opts, args = getopt.getopt(argv, 'hi:')
    except getopt.GetoptError:
        print('application.py -i <input_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('application.py -i <input_file>')
            sys.exit()
        elif opt == '-i' and arg:
            input_file = arg
        else:
            print('application.py -i <input_file>')
            sys.exit()

    # Extract workflow
    workflow_name = kdlc.unzip_workflow(input_file)
    workflow_path = f'{kdlc.INPUT_PATH}/{workflow_name}'

    # Parse connections from workflow.knime
    input_connection_list = kdlc.extract_connections(f'{workflow_path}/workflow.knime')
    # print(input_connection_list)

    # Parse nodes from workflow.knime
    input_node_list = kdlc.extract_nodes(f'{workflow_path}/workflow.knime')
    # print(input_node_list)

    # Parse settings.xml for each node in workflow.knime and add to node
    for node in input_node_list:
        infile = f'{workflow_path}/{node["filename"]}'
        node['settings'] = kdlc.extract_from_input_xml(infile)
    # print(input_node_list)

    # Generate and save workflow.knime in output directory
    workflow_output_path = f'{kdlc.OUTPUT_PATH}/{workflow_name}_new'
    new_workflow_knime = kdlc.create_workflow_knime_from_template(input_node_list, input_connection_list)
    kdlc.save_workflow_knime(new_workflow_knime, workflow_output_path)

    # Generate and save XML for nodes in output directory
    for node in input_node_list:
        tree = kdlc.create_node_xml_from_template(node)
        kdlc.save_node_xml(tree, f'{workflow_output_path}/{node["filename"]}')

    # Zip output workflow into .knwf archive
    kdlc.create_output_workflow(f'{workflow_name}_new')


if __name__ == "__main__":
    main(sys.argv[1:])
