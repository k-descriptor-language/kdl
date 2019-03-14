import os

from .context import kdlc


def test_unzip_workflow(my_setup):
    assert kdlc.unzip_workflow("TestWorkflow.knwf") == "TestWorkflow"
    assert os.path.isdir(f"{kdlc.INPUT_PATH}/TestWorkflow")


def test_extract_connections(my_setup):
    result = [
        {
            "id": 0,
            "source_id": "1",
            "dest_id": "3",
            "source_port": "1",
            "dest_port": "1",
        },
        {
            "id": 1,
            "source_id": "3",
            "dest_id": "2",
            "source_port": "1",
            "dest_port": "1",
        },
    ]
    assert (
        kdlc.extract_connections(f"{kdlc.INPUT_PATH}/TestWorkflow/workflow.knime")
        == result
    )


def test_extract_nodes(my_setup):
    result = [
        {"id": "1", "filename": "CSV Reader (#1)/settings.xml"},
        {"id": "2", "filename": "Table to JSON (#2)/settings.xml"},
        {"id": "3", "filename": "Column Filter (#3)/settings.xml"},
    ]
    assert (
        kdlc.extract_nodes(f"{kdlc.INPUT_PATH}/TestWorkflow/workflow.knime") == result
    )
