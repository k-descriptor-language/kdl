import click
from pathlib import Path
import kdlc


@click.command()
@click.option(
    "--output",
    "-o",
    "output_file",
    required=True,
    help="The output file, either .knwf or .kdl",
)
@click.option(
    "--input",
    "-i",
    "input_file",
    required=True,
    help="The input file, either .knwf or .kdl",
    type=click.Path(exists=True),
)
@click.option(
    "--modify",
    "-m",
    "modify_file",
    help="The KNIME workflow file (.knwf) being modified",
    type=click.Path(exists=True),
)
@click.option(
    "--nodes",
    "-n",
    help="The path to the custom node templates",
    type=click.Path(exists=True),
)
def prompt(input_file, output_file, modify_file, nodes):
    if modify_file and nodes:
        raise click.BadParameter(
            "nodes and modify options cannot be used simulatenously"
        )

    if modify_file:
        if Path(modify_file).suffix != ".knwf":
            raise click.BadParameter("modify file must be of file type *.knwf")

        if Path(input_file).suffix != ".kdl":
            raise click.BadParameter("input file must be of fil type *.kdl")

        if Path(output_file).suffix != ".knwf":
            raise click.BadParameter("output file must be of file type *.knwf")

        update_workflow_with_kdl(input_file, output_file, modify_file)

    elif nodes:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdl_to_workflow_custom_template(input_file, output_file, nodes)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            workflow_to_kdl_custom_template(input_file, output_file, nodes)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )

    elif input_file and output_file:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdl_to_workflow(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            workflow_to_kdl(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".knwf":
            # TODO: add logging here
            workflow_to_workflow(input_file, output_file)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )

    else:
        raise click.UsageError(
            "Improper usage of kdlc. Use the --help option for assistance."
        )


def update_workflow_with_kdl(input_file, output_file, modify_file):
    pass


def kdl_to_workflow_custom_template(input_file, output_file, nodes):
    pass


def workflow_to_kdl_custom_template(input_file, output_file, nodes):
    pass


def kdl_to_workflow(input_file, output_file):
    pass


def workflow_to_kdl(input_file, output_file):
    pass


def workflow_to_workflow(input_file, output_file):
    output_wf_name = output_file.replace(".knwf", "")

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
    kdlc.create_output_workflow(output_wf_name)
