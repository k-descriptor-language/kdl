import sys, getopt, os
from shutil import copyfile, rmtree
from helpers import *


def main(argv):

    input_file = ''

    try:
        opts, args = getopt.getopt(argv,'hi:')
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

    workflow_name = unzip_workflow(input_file)
    workflow_path = f'{INPUT_PATH}/{workflow_name}'

    node_list = extract_nodes(f'{workflow_path}/workflow.knime')
    print(node_list)

    connection_list = extract_connections(f'{workflow_path}/workflow.knime')
    print(connection_list)
    # sys.exit()
    
    infile1 = f'{workflow_path}/CSV Reader (#1)/settings.xml'
    node1 = extract_from_input_xml(infile1)
    print(node1)

    infile2 = f'{workflow_path}/Table To JSON (#2)/settings.xml'
    node2 = extract_from_input_xml(infile2)
    print(node2)

    # sys.exit()

    workflow_output_path = f'{OUTPUT_PATH}/{workflow_name}'
    if not os.path.exists(workflow_output_path):
        os.makedirs(workflow_output_path)

    template_tree1 = create_node_xml_from_template(node1)
    save_node_xml(template_tree1, f'{workflow_output_path}/CSV Reader (#1)')

    template_tree2 = create_node_xml_from_template(node2)
    save_node_xml(template_tree2, f'{workflow_output_path}/Table To JSON (#2)')
    # sys.exit()

    copyfile(f'{workflow_path}/workflow.knime',f'{workflow_output_path}/workflow.knime')
    create_output_workflow(workflow_name)
    rmtree(f'{workflow_path}')
    rmtree(f'{OUTPUT_PATH}/{workflow_name}')

if __name__ == "__main__":
    main(sys.argv[1:])