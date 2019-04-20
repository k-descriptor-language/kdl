import os
from click.testing import CliRunner
import kdlc


"""
def test_kdl_to_knwf(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")

        result = runner.invoke(kdlc.prompt, "-i input.kdl -o output.knwf")

        assert result.exit_code == 0
"""


"""
def test_knwf_to_kdl(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.knwf", "w")

        result = runner.invoke(kdlc.prompt, "-i input.knwf -o output.kdl")

        assert result.exit_code == 0
"""


def test_improper_input_output_files(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.txt", "w")
        os.mkdir("resources")

        result = runner.invoke(kdlc.prompt, "-i input.txt -o output.txt")

        error_message = (
            "Input/output file type mismatch. Either .kdl --> .knwf or "
            ".knwf --> .kdl"
        )
        assert error_message in result.output
