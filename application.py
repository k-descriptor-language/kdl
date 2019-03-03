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
  
    infile1 = f'{workflowPath}/CSV Reader (#1)/settings.xml'
    node1 = extractFromInputXML(infile1)
    #print(node1)

    infile2 = f'{workflowPath}/Table To JSON (#2)/settings.xml'
    node2 = extractFromInputXML(infile2)
    #print(node2)

    #sys.exit()

    workflowOutputPath = f'{outputpath}/{workflowName}'
    if not os.path.exists(workflowOutputPath):
        os.makedirs(workflowOutputPath)
    
    templateTree1 = createNodeXMLFromTemplate(node1)
    saveNodeXML(templateTree1, f'{workflowOutputPath}/CSV Reader (#1)')

    templateTree2 = createNodeXMLFromTemplate(node2)
    saveNodeXML(templateTree2, f'{workflowOutputPath}/Table To JSON (#2)')
    #sys.exit()

    copyfile(f'{workflowPath}/workflow.knime',f'{workflowOutputPath}/workflow.knime')
    createOutputWorkflow(workflowName)
    rmtree(f'{workflowPath}')
    rmtree(f'{outputpath}/{workflowName}')

if __name__ == "__main__":
    main(sys.argv[1:])