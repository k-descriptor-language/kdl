import sys, getopt, os
from shutil import copyfile, rmtree
from helpers import *


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
    workflow_name = unzip_workflow(input_file)
    workflow_path = f'{INPUT_PATH}/{workflow_name}'

    # Parse connections from workflow.knime
    input_connection_list = extract_connections(f'{workflow_path}/workflow.knime')
    # print(input_connection_list)

    # Parse nodes from workflow.knime
    input_node_list = extract_nodes(f'{workflow_path}/workflow.knime')

    # Parse settings.xml for each node in workflow.knime and add to node
    for node in input_node_list:
        infile = f'{workflow_path}/{node["filename"]}'
        node['settings'] = extract_from_input_xml(infile)
    # print(input_node_list)

    # Create output workflow directory
    workflow_output_path = f'{OUTPUT_PATH}/{workflow_name}'
    if not os.path.exists(workflow_output_path):
        os.makedirs(workflow_output_path)

    # Generate and save XML for nodes in output directory
    for node in input_node_list:
        tree = create_node_xml_from_template(node)
        save_node_xml(tree, f'{workflow_output_path}/{node["filename"]}')

    # Generate and save workflow.knime in output directory
    new_workflow_knime = create_workflow_knime_from_template(input_node_list, input_connection_list)
    save_workflow_knime(new_workflow_knime, workflow_output_path)

    # Zip output workflow into .knwf archive
    create_output_workflow(workflow_name)

    # Clean up input and output directories
    rmtree(workflow_path)
    rmtree(workflow_output_path)


if __name__ == "__main__":
    main(sys.argv[1:])
