import click
from pathlib import Path
import kdlc
from loguru import logger
import sys


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
    "--debug",
    "-d",
    "debug_logging",
    required=False,
    help="Print debug logging to stdout",
    is_flag=True,
)

def prompt(input_file: str, output_file: str, debug_logging: bool = False) -> None:
    """
    CLI interface. Uses the click libraries. Offers two functions:
        knwf to kdl
        kdl to knwf
    Determines the action based off of the input and output file paratmeter extensions

    :param input_file: Name of the input file
    :param output_file: Name of the output file
    :param debug_logging: argument to turn on debug mode
    """
    logger.remove()
    if debug_logging:
        logger.add(
            sys.stdout,
            level="DEBUG",
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                "<cyan>{line}</cyan> - <level>{message}</level>"
            ),
        )

    if Path(input_file).suffix == ".kdl" and Path(output_file).suffix == ".knwf":
        kdlc.kdl_to_workflow(input_file, output_file)
    elif Path(input_file).suffix == ".knwf" and Path(output_file).suffix == ".kdl":
        kdlc.workflow_to_kdl(input_file, output_file)
    else:
        raise click.BadParameter(
            "Input/output file type mismatch. Either .kdl --> .knwf or "
            ".knwf --> .kdl"
        )
