import click
from pathlib import Path
import kdlc
from loguru import logger


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
    "--debug", "-d", "debug_logging", help="Print debug logging to stdout", is_flag=True
)
def prompt(input_file: str, output_file: str, modify_file: str, nodes: str) -> None:
    if debug_logging:
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.add(sys.stderr, level="ERROR")


def prompt(input_file: str, output_file: str) -> None:
    if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
        kdlc.kdl_to_workflow(input_file, output_file)
    elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
        kdlc.workflow_to_kdl(input_file, output_file)
    else:
        raise click.BadParameter(
            "Input/output file type mismatch. Either .kdl --> .knwf or "
            ".knwf --> .kdl"
        )
