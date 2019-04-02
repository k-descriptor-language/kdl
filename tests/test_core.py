import os
import kdlc
import xml.etree.ElementTree as ET
import filecmp
import pytest

test_generated_dir = os.path.dirname(__file__) + "/generated"
test_resources_dir = os.path.dirname(__file__) + "/resources"


def test_unzip_workflow(my_setup):
    assert (
        kdlc.unzip_workflow(f"{test_resources_dir}/TestWorkflow.knwf") == "TestWorkflow"
    )
    assert os.path.isdir(f"{kdlc.INPUT_PATH}/TestWorkflow")


def test_extract_from_input_xml_csv(my_setup):
    result = {
        "name": "CSV Reader",
        "factory": "org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        "bundle_name": "KNIME Base Nodes",
        "bundle_symbolic_name": "org.knime.base",
        "bundle_version": "3.7.1.v201901291053",
        "feature_name": "KNIME Core",
        "feature_symbolic_name": "org.knime.features.base.feature.group",
        "feature_version": "3.7.1.v201901291053",
        "port_count": 1,
        "model": [
            {
                "url": (
                    "/Users/jared/knime-workspace/Example Workflows/"
                    "TheData/Misc/Demographics.csv"
                )
            },
            {"colDelimiter": ","},
            {"rowDelimiter": "%%00010"},
            {"quote": '"'},
            {"commentStart": "#"},
            {"hasRowHeader": True},
            {"hasColHeader": True},
            {"supportShortLines": False},
            {"limitRowsCount": -1, "data_type": "xlong"},
            {"skipFirstLinesCount": -1},
            {"characterSetName": "", "isnull": True},
            {"limitAnalysisCount": -1},
        ],
    }
    assert (
        kdlc.extract_from_input_xml(f"{test_resources_dir}/csv_settings.xml") == result
    )


def test_extract_from_input_xml_cf(my_setup):
    result = {
        "name": "Column Filter",
        "factory": (
            "org.knime.base.node.preproc.filter.column.DataColumnSpecFilterNodeFactory"
        ),
        "bundle_name": "KNIME Base Nodes",
        "bundle_symbolic_name": "org.knime.base",
        "bundle_version": "3.7.1.v201901291053",
        "feature_name": "KNIME Core",
        "feature_symbolic_name": "org.knime.features.base.feature.group",
        "feature_version": "3.7.1.v201901291053",
        "port_count": 1,
        "model": [
            {
                "column-filter": [
                    {"filter-type": "STANDARD"},
                    {
                        "included_names": [
                            {"array-size": 11},
                            {"0": "MaritalStatus"},
                            {"1": "Gender"},
                            {"2": "EstimatedYearlyIncome"},
                            {"3": "SentimentRating"},
                            {"4": "WebActivity"},
                            {"5": "Age"},
                            {"6": "Target"},
                            {"7": "Available401K"},
                            {"8": "CustomerValueSegment"},
                            {"9": "ChurnScore"},
                            {"10": "CallActivity"},
                        ]
                    },
                    {"excluded_names": [{"array-size": 1}, {"0": "NumberOfContracts"}]},
                    {"enforce_option": "EnforceExclusion"},
                    {
                        "name_pattern": [
                            {"pattern": ""},
                            {"type": "Wildcard"},
                            {"caseSensitive": True},
                        ]
                    },
                    {
                        "datatype": [
                            {
                                "typelist": [
                                    {"org.knime.core.data.StringValue": False},
                                    {"org.knime.core.data.IntValue": False},
                                    {"org.knime.core.data.DoubleValue": False},
                                    {"org.knime.core.data.BooleanValue": False},
                                    {"org.knime.core.data.LongValue": False},
                                    {
                                        (
                                            "org.knime.core.data."
                                            "date.DateAndTimeValue"
                                        ): False
                                    },
                                ]
                            }
                        ]
                    },
                ]
            }
        ],
    }
    assert (
        kdlc.extract_from_input_xml(f"{test_resources_dir}/cf_settings.xml") == result
    )


def test_extract_from_input_xml_csv_var(my_setup):
    res = {
        "name": "CSV Reader",
        "factory": "org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        "bundle_name": "KNIME Base Nodes",
        "bundle_symbolic_name": "org.knime.base",
        "bundle_version": "3.7.1.v201901291053",
        "feature_name": "KNIME Core",
        "feature_symbolic_name": "org.knime.features.base.feature.group",
        "feature_version": "3.7.1.v201901291053",
        "port_count": 1,
        "model": [
            {
                "url": "/Users/jared/knime-workspace/Example "
                "Workflows/TheData/Misc/Demographics.csv",
                "used_variable": "TEST",
                "exposed_variable": "TEST2",
            },
            {"colDelimiter": ","},
            {"rowDelimiter": "%%00010"},
            {"quote": '"'},
            {"commentStart": "#"},
            {"hasRowHeader": True},
            {"hasColHeader": True},
            {"supportShortLines": False},
            {"limitRowsCount": -1, "data_type": "xlong"},
            {"skipFirstLinesCount": -1},
            {"characterSetName": "", "isnull": True},
            {"limitAnalysisCount": -1},
        ],
    }

    assert (
        kdlc.extract_from_input_xml(f"{test_resources_dir}/csv_settings_var.xml") == res
    )


def test_extract_from_input_xml_ttj_var(my_setup):
    res = {
        "name": "Table to JSON",
        "factory": "org.knime.json.node.fromtable.TableToJsonNodeFactory",
        "bundle_name": "JSON related functionality for KNIME",
        "bundle_symbolic_name": "org.knime.json",
        "bundle_version": "3.7.1.v201901281201",
        "feature_name": "KNIME JSON-Processing",
        "feature_symbolic_name": "org.knime.features.json.feature.group",
        "feature_version": "3.7.1.v201901281201",
        "port_count": 1,
        "model": [
            {
                "selectedColumns": [
                    {"filter-type": "STANDARD"},
                    {
                        "included_names": [
                            {"array-size": 11},
                            {
                                "0": "MaritalStatus",
                                "used_variable": "TEST",
                                "exposed_variable": "TEST2",
                            },
                            {"1": "Gender"},
                            {"2": "EstimatedYearlyIncome"},
                            {"3": "SentimentRating"},
                            {"4": "WebActivity"},
                            {"5": "Age"},
                            {"6": "Target"},
                            {"7": "Available401K"},
                            {"8": "CustomerValueSegment"},
                            {"9": "ChurnScore"},
                            {"10": "CallActivity"},
                        ]
                    },
                    {"excluded_names": [{"array-size": 0}]},
                    {"enforce_option": "EnforceExclusion"},
                    {
                        "name_pattern": [
                            {"pattern": ""},
                            {"type": "Wildcard"},
                            {"caseSensitive": True},
                        ]
                    },
                    {
                        "datatype": [
                            {
                                "typelist": [
                                    {"org.knime.core.data.StringValue": False},
                                    {"org.knime.core.data.IntValue": False},
                                    {"org.knime.core.data.DoubleValue": False},
                                    {"org.knime.core.data.BooleanValue": False},
                                    {"org.knime.core.data.LongValue": False},
                                    {
                                        (
                                            "org.knime.core.data"
                                            ".date.DateAndTimeValue"
                                        ): False
                                    },
                                ]
                            }
                        ]
                    },
                ]
            },
            {"rowkey.key": "key"},
            {"direction": "KeepRows"},
            {"column.name.separator": "."},
            {"output.column.name": "JSON"},
            {"row.key.option": "omit"},
            {"column.names.as.path": False},
            {"remove.source.columns": False},
            {"output.boolean.asNumbers": False},
            {"missing.values.are.omitted": True},
        ],
    }
    assert (
        kdlc.extract_from_input_xml(f"{test_resources_dir}/ttj_settings_var.xml") == res
    )


def test_extract_from_input_xml_fail(my_setup):
    with pytest.raises(Exception):
        kdlc.extract_from_input_xml(f"{test_resources_dir}/fail_settings.xml")


def test_extract_from_input_xml_fail_var(my_setup):
    with pytest.raises(Exception):
        kdlc.extract_from_input_xml(f"{test_resources_dir}/fail_var_settings.xml")


def test_merge_model_and_variables_1var(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD"},
                {
                    "included_names": [
                        {"array-size": 11},
                        {"0": "MaritalStatus"},
                        {"1": "Gender"},
                        {"2": "EstimatedYearlyIncome"},
                        {"3": "SentimentRating"},
                        {"4": "WebActivity"},
                        {"5": "Age"},
                        {"6": "Target"},
                        {"7": "Available401K"},
                        {"8": "CustomerValueSegment"},
                        {"9": "ChurnScore"},
                        {"10": "CallActivity"},
                    ]
                },
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceExclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {"org.knime.core.data.StringValue": False},
                                {"org.knime.core.data.IntValue": False},
                                {"org.knime.core.data.DoubleValue": False},
                                {"org.knime.core.data.BooleanValue": False},
                                {"org.knime.core.data.LongValue": False},
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        },
        {"rowkey.key": "key"},
        {"direction": "KeepRows"},
        {"column.name.separator": "."},
        {"output.column.name": "JSON"},
        {"row.key.option": "omit"},
        {"column.names.as.path": False},
        {"remove.source.columns": False},
        {"output.boolean.asNumbers": False},
        {"missing.values.are.omitted": True},
    ]

    variables = [
        {
            "selectedColumns": [
                {
                    "included_names": [
                        {
                            "0": [
                                {"used_variable": "TEST"},
                                {"exposed_variable": "", "isnull": "true"},
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    result = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD"},
                {
                    "included_names": [
                        {"array-size": 11},
                        {"0": "MaritalStatus", "used_variable": "TEST"},
                        {"1": "Gender"},
                        {"2": "EstimatedYearlyIncome"},
                        {"3": "SentimentRating"},
                        {"4": "WebActivity"},
                        {"5": "Age"},
                        {"6": "Target"},
                        {"7": "Available401K"},
                        {"8": "CustomerValueSegment"},
                        {"9": "ChurnScore"},
                        {"10": "CallActivity"},
                    ]
                },
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceExclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {"org.knime.core.data.StringValue": False},
                                {"org.knime.core.data.IntValue": False},
                                {"org.knime.core.data.DoubleValue": False},
                                {"org.knime.core.data.BooleanValue": False},
                                {"org.knime.core.data.LongValue": False},
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        },
        {"rowkey.key": "key"},
        {"direction": "KeepRows"},
        {"column.name.separator": "."},
        {"output.column.name": "JSON"},
        {"row.key.option": "omit"},
        {"column.names.as.path": False},
        {"remove.source.columns": False},
        {"output.boolean.asNumbers": False},
        {"missing.values.are.omitted": True},
    ]
    kdlc.merge_model_and_variables(model, variables)
    assert result == model


def test_merge_model_and_variables_2var(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD"},
                {
                    "included_names": [
                        {"array-size": 11},
                        {"0": "MaritalStatus"},
                        {"1": "Gender"},
                        {"2": "EstimatedYearlyIncome"},
                        {"3": "SentimentRating"},
                        {"4": "WebActivity"},
                        {"5": "Age"},
                        {"6": "Target"},
                        {"7": "Available401K"},
                        {"8": "CustomerValueSegment"},
                        {"9": "ChurnScore"},
                        {"10": "CallActivity"},
                    ]
                },
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceExclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {"org.knime.core.data.StringValue": False},
                                {"org.knime.core.data.IntValue": False},
                                {"org.knime.core.data.DoubleValue": False},
                                {"org.knime.core.data.BooleanValue": False},
                                {"org.knime.core.data.LongValue": False},
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        },
        {"rowkey.key": "key"},
        {"direction": "KeepRows"},
        {"column.name.separator": "."},
        {"output.column.name": "JSON"},
        {"row.key.option": "omit"},
        {"column.names.as.path": False},
        {"remove.source.columns": False},
        {"output.boolean.asNumbers": False},
        {"missing.values.are.omitted": True},
    ]

    variables = [
        {
            "selectedColumns": [
                {
                    "included_names": [
                        {
                            "0": [
                                {"used_variable": "TEST"},
                                {"exposed_variable": "TEST2"},
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    result = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD"},
                {
                    "included_names": [
                        {"array-size": 11},
                        {
                            "0": "MaritalStatus",
                            "used_variable": "TEST",
                            "exposed_variable": "TEST2",
                        },
                        {"1": "Gender"},
                        {"2": "EstimatedYearlyIncome"},
                        {"3": "SentimentRating"},
                        {"4": "WebActivity"},
                        {"5": "Age"},
                        {"6": "Target"},
                        {"7": "Available401K"},
                        {"8": "CustomerValueSegment"},
                        {"9": "ChurnScore"},
                        {"10": "CallActivity"},
                    ]
                },
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceExclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {"org.knime.core.data.StringValue": False},
                                {"org.knime.core.data.IntValue": False},
                                {"org.knime.core.data.DoubleValue": False},
                                {"org.knime.core.data.BooleanValue": False},
                                {"org.knime.core.data.LongValue": False},
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        },
        {"rowkey.key": "key"},
        {"direction": "KeepRows"},
        {"column.name.separator": "."},
        {"output.column.name": "JSON"},
        {"row.key.option": "omit"},
        {"column.names.as.path": False},
        {"remove.source.columns": False},
        {"output.boolean.asNumbers": False},
        {"missing.values.are.omitted": True},
    ]
    kdlc.merge_model_and_variables(model, variables)
    assert result == model


def test_extract_entry_tag_string(my_setup):
    tree = ET.fromstring('<entry key="node-name" type="xstring" value="CSV Reader"/>')

    result = {"node-name": "CSV Reader"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_password(my_setup):
    tree = ET.fromstring('<entry key="node-name" type="xstring" value="CSV Reader"/>')

    result = {"node-name": "CSV Reader"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_int(my_setup):
    tree = ET.fromstring('<entry key="password" type="xpassword" value="test" />')

    result = {"password": "test", "data_type": "xpassword"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_long(my_setup):
    tree = ET.fromstring('<entry key="limitRowsCount" type="xlong" value="-1" />')

    result = {"limitRowsCount": -1, "data_type": "xlong"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_short(my_setup):
    tree = ET.fromstring('<entry key="limitRowsCount" type="xshort" value="-1" />')

    result = {"limitRowsCount": -1, "data_type": "xshort"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_float(my_setup):
    tree = ET.fromstring('<entry key="someFloat" type="xfloat" value="1.1" />')

    result = {"someFloat": 1.1}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_double(my_setup):
    tree = ET.fromstring('<entry key="someDouble" type="xdouble" value="1.1" />')

    result = {"someDouble": 1.1, "data_type": "xdouble"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_char(my_setup):
    tree = ET.fromstring('<entry key="someChar" type="xchar" value="A" />')

    result = {"someChar": "A", "data_type": "xchar"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_byte(my_setup):
    tree = ET.fromstring('<entry key="someByte" type="xbyte" value="A" />')

    result = {"someByte": "A", "data_type": "xbyte"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_boolean_true(my_setup):
    tree = ET.fromstring('<entry key="hasRowHeader" type="xboolean" value="true" />')

    result = {"hasRowHeader": True}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_boolean_false(my_setup):
    tree = ET.fromstring('<entry key="hasRowHeader" type="xboolean" value="false" />')

    result = {"hasRowHeader": False}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_with_isnull(my_setup):
    tree = ET.fromstring(
        '<entry key="node-name" type="xstring" value="CSV Reader" isnull="true" />'
    )

    result = {"node-name": "CSV Reader", "isnull": True}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_error(my_setup):
    tree = ET.fromstring(
        '<entry key="node-name" type="invalid" value="CSV Reader" isnull="true" />'
    )
    with pytest.raises(Exception):
        kdlc.extract_entry_tag(tree)


def test_extract_config_tag(my_setup):
    tree = ET.fromstring(
        '<config xmlns="http://www.knime.org/2008/09/XMLConfig" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig '
        'http://www.knime.org/XMLConfig_2008_09.xsd" key="settings.xml">'
        '<config key="column-filter"><entry key="filter-type" type="xstring" '
        'value="STANDARD" /></config></config>'
    )

    result = {"settings.xml": [{"column-filter": [{"filter-type": "STANDARD"}]}]}
    assert kdlc.extract_config_tag(tree) == result


def test_extract_config_tag_fail(my_setup):
    tree = ET.fromstring(
        '<config xmlns="http://www.knime.org/2008/09/XMLConfig" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig '
        'http://www.knime.org/XMLConfig_2008_09.xsd" key="settings.xml">'
        '<fail key="column-filter"><entry key="filter-type" type="xstring" '
        'value="STANDARD" /></fail></config>'
    )
    with pytest.raises(Exception):
        kdlc.extract_config_tag(tree)


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


def test_validate_node_from_schema(my_setup):
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
                    )
                },
                {"colDelimiter": ","},
                {"rowDelimiter": "%%00010"},
                {"quote": '"'},
                {"commentStart": "#"},
                {"hasRowHeader": True},
                {"hasColHeader": True},
                {"supportShortLines": False},
                {"limitRowsCount": -1, "data_type": "xlong"},
                {"skipFirstLinesCount": -1},
                {"characterSetName": "", "isnull": True},
                {"limitAnalysisCount": -1},
            ],
        }
    }
    kdlc.validate_node_from_schema(node)


def test_create_node_settings_from_template_csv(my_setup):
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
            "port_count": 1,
            "model": [
                {
                    "url": (
                        "/Users/jared/knime-workspace/Example Workflows/"
                        "TheData/Misc/Demographics.csv"
                    )
                },
                {"colDelimiter": ","},
                {"rowDelimiter": "%%00010"},
                {"quote": '"'},
                {"commentStart": "#"},
                {"hasRowHeader": True},
                {"hasColHeader": True},
                {"supportShortLines": False},
                {"limitRowsCount": -1, "data_type": "xlong"},
                {"skipFirstLinesCount": -1},
                {"characterSetName": "", "isnull": True},
                {"limitAnalysisCount": -1},
            ],
        }
    }
    expected_result = ET.parse(f"{test_resources_dir}/csv_settings.xml")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_node_settings_from_template(node)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_extract_variables_from_model_used_exposed(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {
                            "0": "MaritalStatus",
                            "used_variable": "TEST",
                            "exposed_variable": "TEST2",
                            "data_type": "xstring",
                        },
                        {"1": "Gender", "data_type": "xstring"},
                        {"2": "EstimatedYearlyIncome", "data_type": "xstring"},
                        {"3": "SentimentRating", "data_type": "xstring"},
                        {"4": "WebActivity", "data_type": "xstring"},
                        {"5": "Age", "data_type": "xstring"},
                        {"6": "Target", "data_type": "xstring"},
                        {"7": "Available401K", "data_type": "xstring"},
                        {"8": "CustomerValueSegment", "data_type": "xstring"},
                        {"9": "ChurnScore", "data_type": "xstring"},
                        {"10": "CallActivity", "data_type": "xstring"},
                    ],
                    "data_type": "config",
                },
                {
                    "excluded_names": [{"array-size": "0", "data_type": "xint"}],
                    "data_type": "config",
                },
                {"enforce_option": "EnforceExclusion", "data_type": "xstring"},
                {
                    "name_pattern": [
                        {"pattern": "", "data_type": "xstring"},
                        {"type": "Wildcard", "data_type": "xstring"},
                        {"caseSensitive": "true", "data_type": "xboolean"},
                    ],
                    "data_type": "config",
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {
                                    "org.knime.core.data.StringValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.IntValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.DoubleValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.BooleanValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.LongValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.date."
                                    "DateAndTimeValue": "false",
                                    "data_type": "xboolean",
                                },
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                },
            ],
            "data_type": "config",
        },
        {"rowkey.key": "key", "data_type": "xstring"},
        {"direction": "KeepRows", "data_type": "xstring"},
        {"column.name.separator": ".", "data_type": "xstring"},
        {"output.column.name": "JSON", "data_type": "xstring"},
        {"row.key.option": "omit", "data_type": "xstring"},
        {"column.names.as.path": "false", "data_type": "xboolean"},
        {"remove.source.columns": "false", "data_type": "xboolean"},
        {"output.boolean.asNumbers": "false", "data_type": "xboolean"},
        {"missing.values.are.omitted": "true", "data_type": "xboolean"},
    ]

    res = [
        {
            "selectedColumns": [
                {
                    "included_names": [
                        {
                            "0": [
                                {"used_variable": "TEST", "data_type": "xstring"},
                                {"exposed_variable": "TEST2", "data_type": "xstring"},
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                }
            ],
            "data_type": "config",
        }
    ]

    assert kdlc.extract_variables_from_model(model) == res


def test_extract_variables_from_model_used(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {
                            "0": "MaritalStatus",
                            "used_variable": "TEST",
                            "data_type": "xstring",
                        },
                        {"1": "Gender", "data_type": "xstring"},
                        {"2": "EstimatedYearlyIncome", "data_type": "xstring"},
                        {"3": "SentimentRating", "data_type": "xstring"},
                        {"4": "WebActivity", "data_type": "xstring"},
                        {"5": "Age", "data_type": "xstring"},
                        {"6": "Target", "data_type": "xstring"},
                        {"7": "Available401K", "data_type": "xstring"},
                        {"8": "CustomerValueSegment", "data_type": "xstring"},
                        {"9": "ChurnScore", "data_type": "xstring"},
                        {"10": "CallActivity", "data_type": "xstring"},
                    ],
                    "data_type": "config",
                },
                {
                    "excluded_names": [{"array-size": "0", "data_type": "xint"}],
                    "data_type": "config",
                },
                {"enforce_option": "EnforceExclusion", "data_type": "xstring"},
                {
                    "name_pattern": [
                        {"pattern": "", "data_type": "xstring"},
                        {"type": "Wildcard", "data_type": "xstring"},
                        {"caseSensitive": "true", "data_type": "xboolean"},
                    ],
                    "data_type": "config",
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {
                                    "org.knime.core.data.StringValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.IntValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.DoubleValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.BooleanValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.LongValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.date."
                                    "DateAndTimeValue": "false",
                                    "data_type": "xboolean",
                                },
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                },
            ],
            "data_type": "config",
        },
        {"rowkey.key": "key", "data_type": "xstring"},
        {"direction": "KeepRows", "data_type": "xstring"},
        {"column.name.separator": ".", "data_type": "xstring"},
        {"output.column.name": "JSON", "data_type": "xstring"},
        {"row.key.option": "omit", "data_type": "xstring"},
        {"column.names.as.path": "false", "data_type": "xboolean"},
        {"remove.source.columns": "false", "data_type": "xboolean"},
        {"output.boolean.asNumbers": "false", "data_type": "xboolean"},
        {"missing.values.are.omitted": "true", "data_type": "xboolean"},
    ]

    res = [
        {
            "selectedColumns": [
                {
                    "included_names": [
                        {
                            "0": [
                                {"used_variable": "TEST", "data_type": "xstring"},
                                {
                                    "exposed_variable": "",
                                    "data_type": "xstring",
                                    "isnull": True,
                                },
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                }
            ],
            "data_type": "config",
        }
    ]

    assert kdlc.extract_variables_from_model(model) == res


def test_extract_variables_from_model_exposed(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {
                            "0": "MaritalStatus",
                            "exposed_variable": "TEST2",
                            "data_type": "xstring",
                        },
                        {"1": "Gender", "data_type": "xstring"},
                        {"2": "EstimatedYearlyIncome", "data_type": "xstring"},
                        {"3": "SentimentRating", "data_type": "xstring"},
                        {"4": "WebActivity", "data_type": "xstring"},
                        {"5": "Age", "data_type": "xstring"},
                        {"6": "Target", "data_type": "xstring"},
                        {"7": "Available401K", "data_type": "xstring"},
                        {"8": "CustomerValueSegment", "data_type": "xstring"},
                        {"9": "ChurnScore", "data_type": "xstring"},
                        {"10": "CallActivity", "data_type": "xstring"},
                    ],
                    "data_type": "config",
                },
                {
                    "excluded_names": [{"array-size": "0", "data_type": "xint"}],
                    "data_type": "config",
                },
                {"enforce_option": "EnforceExclusion", "data_type": "xstring"},
                {
                    "name_pattern": [
                        {"pattern": "", "data_type": "xstring"},
                        {"type": "Wildcard", "data_type": "xstring"},
                        {"caseSensitive": "true", "data_type": "xboolean"},
                    ],
                    "data_type": "config",
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {
                                    "org.knime.core.data.StringValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.IntValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.DoubleValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.BooleanValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.LongValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.date."
                                    "DateAndTimeValue": "false",
                                    "data_type": "xboolean",
                                },
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                },
            ],
            "data_type": "config",
        },
        {"rowkey.key": "key", "data_type": "xstring"},
        {"direction": "KeepRows", "data_type": "xstring"},
        {"column.name.separator": ".", "data_type": "xstring"},
        {"output.column.name": "JSON", "data_type": "xstring"},
        {"row.key.option": "omit", "data_type": "xstring"},
        {"column.names.as.path": "false", "data_type": "xboolean"},
        {"remove.source.columns": "false", "data_type": "xboolean"},
        {"output.boolean.asNumbers": "false", "data_type": "xboolean"},
        {"missing.values.are.omitted": "true", "data_type": "xboolean"},
    ]

    res = [
        {
            "selectedColumns": [
                {
                    "included_names": [
                        {
                            "0": [
                                {
                                    "used_variable": "",
                                    "data_type": "xstring",
                                    "isnull": True,
                                },
                                {"exposed_variable": "TEST2", "data_type": "xstring"},
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                }
            ],
            "data_type": "config",
        }
    ]

    assert kdlc.extract_variables_from_model(model) == res


def test_extract_variables_from_model_none(my_setup):
    model = [
        {
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {"0": "MaritalStatus", "data_type": "xstring"},
                        {"1": "Gender", "data_type": "xstring"},
                        {"2": "EstimatedYearlyIncome", "data_type": "xstring"},
                        {"3": "SentimentRating", "data_type": "xstring"},
                        {"4": "WebActivity", "data_type": "xstring"},
                        {"5": "Age", "data_type": "xstring"},
                        {"6": "Target", "data_type": "xstring"},
                        {"7": "Available401K", "data_type": "xstring"},
                        {"8": "CustomerValueSegment", "data_type": "xstring"},
                        {"9": "ChurnScore", "data_type": "xstring"},
                        {"10": "CallActivity", "data_type": "xstring"},
                    ],
                    "data_type": "config",
                },
                {
                    "excluded_names": [{"array-size": "0", "data_type": "xint"}],
                    "data_type": "config",
                },
                {"enforce_option": "EnforceExclusion", "data_type": "xstring"},
                {
                    "name_pattern": [
                        {"pattern": "", "data_type": "xstring"},
                        {"type": "Wildcard", "data_type": "xstring"},
                        {"caseSensitive": "true", "data_type": "xboolean"},
                    ],
                    "data_type": "config",
                },
                {
                    "datatype": [
                        {
                            "typelist": [
                                {
                                    "org.knime.core.data.StringValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.IntValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.DoubleValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.BooleanValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.LongValue": "false",
                                    "data_type": "xboolean",
                                },
                                {
                                    "org.knime.core.data.date."
                                    "DateAndTimeValue": "false",
                                    "data_type": "xboolean",
                                },
                            ],
                            "data_type": "config",
                        }
                    ],
                    "data_type": "config",
                },
            ],
            "data_type": "config",
        },
        {"rowkey.key": "key", "data_type": "xstring"},
        {"direction": "KeepRows", "data_type": "xstring"},
        {"column.name.separator": ".", "data_type": "xstring"},
        {"output.column.name": "JSON", "data_type": "xstring"},
        {"row.key.option": "omit", "data_type": "xstring"},
        {"column.names.as.path": "false", "data_type": "xboolean"},
        {"remove.source.columns": "false", "data_type": "xboolean"},
        {"output.boolean.asNumbers": "false", "data_type": "xboolean"},
        {"missing.values.are.omitted": "true", "data_type": "xboolean"},
    ]

    res = []

    assert kdlc.extract_variables_from_model(model) == res


def test_create_node_settings_from_template_cf(my_setup):
    node = {
        "settings": {
            "name": "Column Filter",
            "factory": (
                "org.knime.base.node.preproc.filter."
                "column.DataColumnSpecFilterNodeFactory"
            ),
            "bundle_name": "KNIME Base Nodes",
            "bundle_symbolic_name": "org.knime.base",
            "bundle_version": "3.7.1.v201901291053",
            "feature_name": "KNIME Core",
            "feature_symbolic_name": "org.knime.features.base.feature.group",
            "feature_version": "3.7.1.v201901291053",
            "port_count": 1,
            "model": [
                {
                    "column-filter": [
                        {"filter-type": "STANDARD"},
                        {
                            "included_names": [
                                {"array-size": 11},
                                {"0": "MaritalStatus"},
                                {"1": "Gender"},
                                {"2": "EstimatedYearlyIncome"},
                                {"3": "SentimentRating"},
                                {"4": "WebActivity"},
                                {"5": "Age"},
                                {"6": "Target"},
                                {"7": "Available401K"},
                                {"8": "CustomerValueSegment"},
                                {"9": "ChurnScore"},
                                {"10": "CallActivity"},
                            ]
                        },
                        {
                            "excluded_names": [
                                {"array-size": 1},
                                {"0": "NumberOfContracts"},
                            ]
                        },
                        {"enforce_option": "EnforceExclusion"},
                        {
                            "name_pattern": [
                                {"pattern": ""},
                                {"type": "Wildcard"},
                                {"caseSensitive": True},
                            ]
                        },
                        {
                            "datatype": [
                                {
                                    "typelist": [
                                        {"org.knime.core.data.StringValue": False},
                                        {"org.knime.core.data.IntValue": False},
                                        {"org.knime.core.data.DoubleValue": False},
                                        {"org.knime.core.data.BooleanValue": False},
                                        {"org.knime.core.data.LongValue": False},
                                        {
                                            "org.knime.core.data."
                                            "date.DateAndTimeValue": False
                                        },
                                    ]
                                }
                            ]
                        },
                    ]
                }
            ],
        }
    }
    expected_result = ET.parse(f"{test_resources_dir}/cf_settings.xml")
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


def test_set_entry_element_type_string(my_setup):
    entry = {"url": "/Path/To/TheData/Demographics.csv"}
    result = {"url": "/Path/To/TheData/Demographics.csv", "data_type": "xstring"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_password(my_setup):
    entry = {"password": "test", "data_type": "xpassword"}
    result = {"password": "test", "data_type": "xpassword"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_int(my_setup):
    entry = {"skipFirstLinesCount": -1}
    result = {"skipFirstLinesCount": "-1", "data_type": "xint"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_long(my_setup):
    entry = {"limitRowsCount": -1, "data_type": "xlong"}
    result = {"limitRowsCount": "-1", "data_type": "xlong"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_short(my_setup):
    entry = {"limitRowsCount": -1, "data_type": "xshort"}
    result = {"limitRowsCount": "-1", "data_type": "xshort"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_float(my_setup):
    entry = {"someFloat": 1.1}
    result = {"someFloat": "1.1", "data_type": "xfloat"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_double(my_setup):
    entry = {"someDouble": 1.1, "data_type": "xdouble"}
    result = {"someDouble": "1.1", "data_type": "xdouble"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_char(my_setup):
    entry = {"someChar": "A", "data_type": "xchar"}
    result = {"someChar": "A", "data_type": "xchar"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_byte(my_setup):
    entry = {"someByte": "A", "data_type": "xbyte"}
    result = {"someByte": "A", "data_type": "xbyte"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_boolean_true(my_setup):
    entry = {"hasRowHeader": True}
    result = {"hasRowHeader": "true", "data_type": "xboolean"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_boolean_false(my_setup):
    entry = {"hasRowHeader": False}
    result = {"hasRowHeader": "false", "data_type": "xboolean"}
    kdlc.set_entry_element_type(entry)
    assert result == entry


def test_set_entry_element_type_fail(my_setup):
    entry = {"test": None}
    with pytest.raises(Exception):
        kdlc.set_entry_element_type(entry)


def test_set_config_element_type(my_setup):
    config = {"included_names": [{"array-size": 12}, {"0": "MaritalStatus"}]}
    result = {
        "included_names": [
            {"array-size": "12", "data_type": "xint"},
            {"0": "MaritalStatus", "data_type": "xstring"},
        ],
        "data_type": "config",
    }
    kdlc.set_config_element_type(config)
    assert result == config


def test_save_node_settings_xml(my_setup):
    tree = ET.parse(f"{test_resources_dir}/csv_settings.xml")
    kdlc.save_node_settings_xml(tree, f"{test_generated_dir}/settings.xml")
    assert filecmp.cmp(
        f"{test_resources_dir}/csv_settings.xml", f"{test_generated_dir}/settings.xml"
    )


def test_save_workflow_knime(my_setup):
    tree = ET.parse(f"{test_resources_dir}/workflow.knime")
    kdlc.save_workflow_knime(tree, test_generated_dir)
    assert filecmp.cmp(
        f"{test_resources_dir}/workflow.knime", f"{test_generated_dir}/workflow.knime"
    )


def test_create_output_workflow(mocker):
    workflow_name = "test"

    make_archive = mocker.MagicMock()
    mocker.patch("shutil.make_archive", new=make_archive)

    rename = mocker.MagicMock()
    mocker.patch("os.rename", new=rename)

    kdlc.create_output_workflow(workflow_name)
    make_archive.assert_called_with(workflow_name, "zip", kdlc.OUTPUT_PATH)
    rename.assert_called_with(f"{workflow_name}.zip", f"{workflow_name}.knwf")


def test_cleanup(my_setup):
    kdlc.cleanup()
    assert os.path.exists(kdlc.TMP_INPUT_DIR.name) is False
    assert os.path.exists(kdlc.TMP_OUTPUT_DIR.name) is False
