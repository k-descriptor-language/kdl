import os
from click.testing import CliRunner
import kdlc


def test_bad_param_modify_file(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")
        open("modify.knwf", "w")
        os.mkdir("resources")

        result = runner.invoke(
            kdlc.prompt, "-i input.kdl -o output.knwf -m modify.knwf -n resources"
        )
        error_message = "nodes and modify options cannot be used simultaneously"
        assert error_message in result.output


def test_improper_modify_file(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")
        open("modify.txt", "w")

        result = runner.invoke(kdlc.prompt, "-i input.kdl -o output.knwf -m modify.txt")
        error_message = "modify file must be of file type *.knwf"
        assert error_message in result.output


def test_improper_input_file_for_modify(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.txt", "w")
        open("modify.knwf", "w")

        result = runner.invoke(
            kdlc.prompt, "-i input.txt -o output.knwf -m modify.knwf"
        )
        error_message = "input file must be of file type *.kdl"
        assert error_message in result.output


def test_improper_output_file_for_modify(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")
        open("modify.knwf", "w")

        result = runner.invoke(kdlc.prompt, "-i input.kdl -o output.txt -m modify.knwf")
        error_message = "output file must be of file type *.knwf"
        assert error_message in result.output


def test_update_workflow_with_kdl(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")
        open("modify.knwf", "w")

        result = runner.invoke(
            kdlc.prompt, "-i input.kdl -o output.knwf -m modify.knwf"
        )

        assert result.exit_code == 0


def test_nodes_kdl_to_knwf(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")
        os.mkdir("resources")

        result = runner.invoke(kdlc.prompt, "-i input.kdl -o output.knwf -n resources")

        assert result.exit_code == 0


def test_nodes_knwf_to_kdl(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.knwf", "w")
        os.mkdir("resources")

        result = runner.invoke(kdlc.prompt, "-i input.knwf -o output.kdl -n resources")

        assert result.exit_code == 0


def test_nodes_improper_file_types(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.knwf", "w")
        os.mkdir("resources")

        result = runner.invoke(kdlc.prompt, "-i input.knwf -o output.text -n resources")

        error_message = (
            "Input/output file type mismatch. Either .kdl --> .knwf or "
            ".knwf --> .kdl"
        )
        assert error_message in result.output


def test_kdl_to_knwf(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.kdl", "w")

        result = runner.invoke(kdlc.prompt, "-i input.kdl -o output.knwf")

        assert result.exit_code == 0


def test_knwf_to_kdl(my_setup):
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("input.knwf", "w")

        result = runner.invoke(kdlc.prompt, "-i input.knwf -o output.kdl")

        assert result.exit_code == 0


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
