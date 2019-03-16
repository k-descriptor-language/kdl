import os
import kdlc
import xml.etree.ElementTree as ET

test_resources_dir = os.path.dirname(__file__) + "/resources/"


def test_unzip_workflow(my_setup):
    assert (
        kdlc.unzip_workflow(f"{test_resources_dir}/TestWorkflow.knwf") == "TestWorkflow"
    )
    assert os.path.isdir(f"{kdlc.INPUT_PATH}/TestWorkflow")


def test_extract_from_input_xml(my_setup):
    result = {
        "name": "CSV Reader",
        "factory": "org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        "bundle_name": "KNIME Base Nodes",
        "bundle_symbolic_name": "org.knime.base",
        "bundle_version": "3.7.1.v201901291053",
        "feature_name": "KNIME Core",
        "feature_symbolic_name": "org.knime.features.base.feature.group",
        "feature_version": "3.7.1.v201901291053",
        "model": [
            {
                "url": (
                    "/Users/jared/knime-workspace/Example Workflows/"
                    "TheData/Misc/Demographics.csv"
                ),
                "type": "xstring",
            },
            {"colDelimiter": ",", "type": "xstring"},
            {"rowDelimiter": "%%00010", "type": "xstring"},
            {"quote": '"', "type": "xstring"},
            {"commentStart": "#", "type": "xstring"},
            {"hasRowHeader": "true", "type": "xboolean"},
            {"hasColHeader": "true", "type": "xboolean"},
            {"supportShortLines": "false", "type": "xboolean"},
            {"limitRowsCount": "-1", "type": "xlong"},
            {"skipFirstLinesCount": "-1", "type": "xint"},
            {"characterSetName": "", "isnull": True, "type": "xstring"},
            {"limitAnalysisCount": "-1", "type": "xint"},
        ],
    }
    assert kdlc.extract_from_input_xml(f"{test_resources_dir}/settings.xml") == result


def test_extract_entry_tag(my_setup):
    tree = ET.fromstring('<entry key="node-name" type="xstring" value="CSV Reader"/>')

    result = {"node-name": "CSV Reader", "type": "xstring"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_with_isnull(my_setup):
    tree = ET.fromstring(
        '<entry key="node-name" type="xstring" value="CSV Reader" isnull="true" />'
    )

    result = {"node-name": "CSV Reader", "type": "xstring", "isnull": True}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_config_tag(my_setup):
    tree = ET.fromstring(
        '<config key="excluded_names"><entry key="array-size" type="xint" value="0" />'
        "</config>"
    )

    result = {"excluded_names": [{"array-size": "0", "type": "xint"}], "type": "config"}
    assert kdlc.extract_config_tag(tree) == result


def test_extract_nodes(my_setup):
    result = [
        {"id": "1", "filename": "CSV Reader (#1)/settings.xml"},
        {"id": "2", "filename": "Table to JSON (#2)/settings.xml"},
        {"id": "3", "filename": "Column Filter (#3)/settings.xml"},
    ]
    assert kdlc.extract_nodes(f"{test_resources_dir}/workflow.knime") == result


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
    assert kdlc.extract_connections(f"{test_resources_dir}/workflow.knime") == result


def test_create_node_settings_from_template(my_setup):
    node = {
        "settings": {
            "name": "CSV Reader",
            "factory": "org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
            "bundle_name": "KNIME Base Nodes",
            "bundle_symbolic_name": "org.knime.base",
            "bundle_version": "3.7.1.v201901291053",
            "feature_name": "KNIME Core",
            "feature_symbolic_name": "org.knime.features.base.feature.group",
            "feature_version": "3.7.1.v201901291053",
            "model": [
                {
                    "url": (
                        "/Users/jared/knime-workspace/Example Workflows/"
                        "TheData/Misc/Demographics.csv"
                    ),
                    "type": "xstring",
                },
                {"colDelimiter": ",", "type": "xstring"},
                {"rowDelimiter": "%%00010", "type": "xstring"},
                {"quote": '"', "type": "xstring"},
                {"commentStart": "#", "type": "xstring"},
                {"hasRowHeader": "true", "type": "xboolean"},
                {"hasColHeader": "true", "type": "xboolean"},
                {"supportShortLines": "false", "type": "xboolean"},
                {"limitRowsCount": "-1", "type": "xlong"},
                {"skipFirstLinesCount": "-1", "type": "xint"},
                {"characterSetName": "", "isnull": True, "type": "xstring"},
                {"limitAnalysisCount": "-1", "type": "xint"},
            ],
        }
    }
    expected_result = ET.parse(f"{test_resources_dir}/settings.xml")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_node_settings_from_template(node)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_workflow_knime_from_template(my_setup):
    node_list = [
        {"id": "1", "filename": "CSV Reader (#1)/settings.xml"},
        {"id": "2", "filename": "Table to JSON (#2)/settings.xml"},
        {"id": "3", "filename": "Column Filter (#3)/settings.xml"},
    ]
    connection_list = [
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

    expected_result = ET.parse(f"{test_resources_dir}/workflow.knime")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_workflow_knime_from_template(node_list, connection_list)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened
