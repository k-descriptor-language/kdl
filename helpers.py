import os, zipfile
from shutil import make_archive
import xml.etree.ElementTree as ET

inputpath = 'input'
outputpath = 'output'
templatepath = 'templates'
ns = {'knime': 'http://www.knime.org/2008/09/XMLConfig'}

# assumes workflow filename == workflow name
def unzipWorkflow(inputfile):
    zip_ref = zipfile.ZipFile(inputfile, 'r')
    zip_ref.extractall(inputpath)
    zip_ref.close()
    return os.path.splitext(inputfile)[0]

def extractFromInputXML(inputfile):
    modelAttribs = {}
    baseTree = ET.parse(inputfile)
    root = baseTree.getroot()
    for child in root.findall("./knime:config[@key='model']/knime:entry", ns):
        modelAttribs[child.attrib['key']] = child.attrib['value']
    return modelAttribs

def updateTemplateModel(template, modelAttribs):
    templateTree = ET.parse(template)
    templateRoot = templateTree.getroot()

    for child in templateRoot.findall("./knime:config[@key='model']/knime:entry", ns):
        child.set('value', modelAttribs[child.attrib['key']])
    return templateTree

def saveNodeXML(tree, outputpath):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    ET.register_namespace('', ns['knime'])
    tree.write(f'{outputpath}/settings.xml', xml_declaration=True, encoding='UTF-8')

def createOutputWorkflow(workflowName):
    make_archive(f'{workflowName}_new', 'zip', outputpath)
    base = os.path.splitext(f'{workflowName}_new.zip')[0]
    os.rename(f'{workflowName}_new.zip', base + '.knwf')