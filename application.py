import sys, getopt, os
from shutil import copyfile, rmtree
from helpers import *

def main(argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv,'hi:')
    except getopt.GetoptError:
        print('application.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('application.py -i <inputfile>')
            sys.exit()
        elif opt == '-i' and arg:
            inputfile = arg
        else:
            print('application.py -i <inputfile>')
            sys.exit()

    workflowName = unzipWorkflow(inputfile)
    workflowPath = f'{inputpath}/{workflowName}'

    nodeList = extractNodes(f'{workflowPath}/workflow.knime')
    connectionList = extractConnections(f'{workflowPath}/workflow.knime')
  
    infile = f'{inputpath}/{workflowName}/CSV Reader (#1)/settings.xml'
    node1 = extractFromInputXML(infile)

    template = f'{templatepath}/{node1["name"]}/settings.xml'
    templateTree = updateTemplateModel(template, node1['model'])

    workflowOutputPath = f'{outputpath}/{workflowName}'
    if not os.path.exists(workflowOutputPath):
        os.makedirs(workflowOutputPath)

    saveNodeXML(templateTree, f'{workflowOutputPath}/CSV Reader (#1)')
    copyfile(f'{inputpath}/{workflowName}/workflow.knime',f'{workflowOutputPath}/workflow.knime')
    createOutputWorkflow(workflowName)
    rmtree(f'{inputpath}/{workflowName}')
    rmtree(f'{outputpath}/{workflowName}')

if __name__ == "__main__":
    main(sys.argv[1:])