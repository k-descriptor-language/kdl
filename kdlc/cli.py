import click
from pathlib import Path
import kdlc
import logging

logger = logging.getLogger("kdlc.cli")


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
def prompt(input_file: str, output_file: str, modify_file: str, nodes: str) -> None:
    if modify_file and nodes:
        raise click.UsageError("nodes and modify options cannot be used simultaneously")

    if modify_file:
        if Path(modify_file).suffix != ".knwf":
            raise click.BadParameter("modify file must be of file type *.knwf")

        if Path(input_file).suffix != ".kdl":
            raise click.BadParameter("input file must be of file type *.kdl")

        if Path(output_file).suffix != ".knwf":
            raise click.BadParameter("output file must be of file type *.knwf")

        kdlc.update_workflow_with_kdl(input_file, output_file, modify_file)

    elif nodes:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdlc.kdl_to_workflow_custom_template(input_file, output_file, nodes)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            kdlc.workflow_to_kdl_custom_template(input_file, output_file, nodes)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )

    elif input_file and output_file:
        if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
            kdlc.kdl_to_workflow(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
            kdlc.workflow_to_kdl(input_file, output_file)
        elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".knwf":
            # This functionality is here for development purposes and not part of
            # the final solution
            logger.warning("TEMPORARY! This will be removed before the release.")
            kdlc.workflow_to_workflow(input_file, output_file)
        else:
            raise click.BadParameter(
                "Input/output file type mismatch. Either .kdl --> .knwf or "
                ".knwf --> .kdl"
            )
