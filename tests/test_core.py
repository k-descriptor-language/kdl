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


def test_extract_node_from_settings_xml_csv(my_setup):
    r = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    r.port_count = 1
    r.model = [
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
    ]

    assert r == kdlc.extract_node_from_settings_xml(
        "1", f"{test_resources_dir}/csv_settings.xml"
    )


def test_extract_node_from_settings_xml_cf(my_setup):
    res = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    res.port_count = 1
    res.model = [
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
                                        "org.knime.core.data." "date.DateAndTimeValue"
                                    ): False
                                },
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    assert res == kdlc.extract_node_from_settings_xml(
        "1", f"{test_resources_dir}/cf_settings.xml"
    )


def test_extract_node_from_settings_xml_csv_var(my_setup):
    res = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    res.port_count = 1
    res.model = [
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
    ]
    res.variables = [
        {"url": [{"used_variable": "TEST"}, {"exposed_variable": "TEST2"}]}
    ]

    assert res == kdlc.extract_node_from_settings_xml(
        "1", f"{test_resources_dir}/csv_var.xml"
    )


def test_extract_node_from_settings_xml_ttj_var(my_setup):
    res = kdlc.Node(
        node_id="1",
        name="Table to JSON",
        factory="org.knime.json.node.fromtable.TableToJsonNodeFactory",
        bundle_name="JSON related functionality for KNIME",
        bundle_symbolic_name="org.knime.json",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JSON-Processing",
        feature_symbolic_name="org.knime.features.json.feature.group",
        feature_version="3.7.1.v201901281201",
    )
    res.port_count = 1
    res.model = [
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
                                        "org.knime.core.data" ".date.DateAndTimeValue"
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
    ]
    res.variables = [
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
    assert res == kdlc.extract_node_from_settings_xml(
        "1", f"{test_resources_dir}/ttj_var.xml"
    )


def test_extract_node_from_settings_xml_factory_settings(my_setup):
    res = kdlc.Node(
        node_id="1",
        name="Bar Chart (JavaScript)",
        factory="org.knime.dynamic.js.v30.DynamicJSNodeFactory",
        bundle_name="KNIME Dynamically Created JavaScript Nodes",
        bundle_symbolic_name="org.knime.dynamic.js",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JavaScript Views",
        feature_symbolic_name="org.knime.features.js.views.feature.group",
        feature_version="3.7.2.v201904170930",
    )
    res.port_count = 1
    res.model = [
        {
            "displayFullscreenButton_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"displayFullscreenButton": True},
        {
            "legend_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"legend": True},
        {
            "enableHorizontalToggle_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableHorizontalToggle": True},
        {
            "freq_Internals": [
                {"SettingsModelID": "SMID_columnfilter"},
                {"EnabledStatus": True},
            ]
        },
        {
            "freq": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 1}, {"0": "Accuracy"}]},
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
                        {"typelist": [{"org.knime.core.data.DoubleValue": False}]}
                    ]
                },
            ]
        },
        {
            "tooltip_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"tooltip": True},
        {
            "title_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"title": "Bar Chart"},
        {
            "enableSwitchMissValCat_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSwitchMissValCat": True},
        {
            "includeMissValCat_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"includeMissValCat": True},
        {
            "processInMemory_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"processInMemory": True},
        {
            "freqLabel_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"freqLabel": ""},
        {
            "cat_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"cat": "model"},
        {
            "showWarnings_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"showWarnings": True},
        {
            "enableSubtitleEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSubtitleEdit": True},
        {
            "publishSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"publishSelection": True},
        {
            "showMaximum_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"showMaximum": True},
        {
            "catLabel_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"catLabel": ""},
        {
            "orientation_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"orientation": False},
        {
            "displayClearSelectionButton_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"displayClearSelectionButton": True},
        {"svg_Internals": [{"SettingsModelID": "SMID_svg"}, {"EnabledStatus": True}]},
        {
            "svg": [
                {"width": 600},
                {"height": 400},
                {"fullscreen": True},
                {"showFullscreen": True},
            ]
        },
        {
            "staggerLabels_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"staggerLabels": False},
        {
            "enableTitleEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableTitleEdit": True},
        {
            "enableSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSelection": True},
        {
            "sort_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"sort": False},
        {
            "enableStackedEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableStackedEdit": True},
        {
            "enableAxisEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableAxisEdit": True},
        {
            "reportOnMissingValues_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"reportOnMissingValues": True},
        {
            "subtitle_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"subtitle": ""},
        {
            "chartType_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"chartType": "Grouped"},
        {
            "enableStaggerToggle_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableStaggerToggle": True},
        {
            "enableViewControls_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableViewControls": True},
        {
            "aggr_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"aggr": "Sum"},
        {
            "subscribeToSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"subscribeToSelection": True},
        {
            "enableMaximumValue_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableMaximumValue": True},
        {"hideInWizard": False},
        {"maxRows": 2500},
        {"generateImage": True},
        {"customCSS": ""},
    ]
    res.variables = []
    res.factory_settings = [{"nodeDir": "org.knime.dynamic.js.base:nodes/:barChart"}]
    assert res == kdlc.extract_node_from_settings_xml(
        "1", f"{test_resources_dir}/js_factory_settings.xml"
    )


def test_extract_node_from_settings_xml_fail(my_setup):
    with pytest.raises(ValueError):
        kdlc.extract_node_from_settings_xml(
            "1", f"{test_resources_dir}/fail_settings.xml"
        )


def test_extract_node_from_settings_xml_fail_var(my_setup):
    with pytest.raises(ValueError):
        kdlc.extract_node_from_settings_xml(
            "1", f"{test_resources_dir}/fail_var_settings.xml"
        )


def test_extract_entry_value(my_setup):
    tree = ET.fromstring(
        '<config xmlns="http://www.knime.org/2008/09/XMLConfig" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig '
        'http://www.knime.org/XMLConfig_2008_09.xsd" key="settings.xml">'
        '<entry key="node-name" type="xstring" value="CSV Reader"/></config>'
    )
    result = "CSV Reader"
    assert kdlc.extract_entry_value(tree, "node-name") == result


def test_extract_entry_value_none(my_setup):
    tree = ET.fromstring(
        '<config xmlns="http://www.knime.org/2008/09/XMLConfig" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.knime.org/2008/09/XMLConfig '
        'http://www.knime.org/XMLConfig_2008_09.xsd" key="settings.xml">'
        '<entry key="node-name" type="xstring" value="CSV Reader"/></config>'
    )
    with pytest.raises(Exception):
        kdlc.extract_entry_value(tree, "test")


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


def test_extract_entry_tag_infinity(my_setup):
    tree = ET.fromstring('<entry key="someDouble" type="xdouble" value="Infinity" />')

    result = {"someDouble": "Infinity", "data_type": "xdouble"}
    assert kdlc.extract_entry_tag(tree) == result


def test_extract_entry_tag_ninfinity(my_setup):
    tree = ET.fromstring('<entry key="someDouble" type="xdouble" value="-Infinity" />')

    result = {"someDouble": "-Infinity", "data_type": "xdouble"}
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


def test_extract_node_filenames(my_setup):
    result = [
        {
            "node_id": "1",
            "filename": "CSV Reader (#1)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "2",
            "filename": "Table to JSON (#2)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "3",
            "filename": "Column Filter (#3)/settings.xml",
            "node_type": "NativeNode",
        },
    ]
    assert kdlc.extract_node_filenames(f"{test_resources_dir}/workflow.knime") == result


def test_extract_node_filenames_meta(my_setup):
    result = [
        {
            "node_id": "1",
            "filename": "File Reader (#1)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "7",
            "filename": "CSV Writer (#7)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "8",
            "filename": "workflow_meta_2.knime",
            "node_type": "MetaNode",
            "name": "Metanode",
            "children": [
                {
                    "node_id": "2",
                    "filename": "Row Filter (#2)/settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "3",
                    "filename": "Row Filter (#3)/settings.xml",
                    "node_type": "NativeNode",
                },
            ],
            "meta_in_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "meta_out_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
        },
    ]

    assert (
        kdlc.extract_node_filenames(f"{test_resources_dir}/workflow_meta.knime")
        == result
    )


def test_extract_node_filenames_wrapped(my_setup):
    result = [
        {
            "node_id": "1",
            "filename": "File Reader (#1)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "7",
            "filename": "CSV Writer (#7)/settings.xml",
            "node_type": "NativeNode",
        },
        {
            "node_id": "10",
            "filename": "wrapped/settings_wrapped.xml",
            "node_type": "SubNode",
            "meta_in_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "meta_out_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "name": "WrappedMetanode",
            "children": [
                {
                    "node_id": "2",
                    "filename": "rf_settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "4",
                    "filename": "input_settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "5",
                    "filename": "output_settings.xml",
                    "node_type": "NativeNode",
                },
            ],
        },
    ]
    assert (
        kdlc.extract_node_filenames(f"{test_resources_dir}/workflow_wrapped.knime")
        == result
    )


def test_extract_nodes_from_filenames(my_setup):

    node_filename_list = [
        {"node_id": "1", "filename": "cf_settings.xml", "node_type": "NativeNode"},
        {
            "node_id": "8",
            "filename": "workflow_meta_4.knime",
            "node_type": "MetaNode",
            "name": "Metanode8",
            "children": [
                {
                    "node_id": "4",
                    "filename": "cf_settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "6",
                    "filename": "workflow_meta_3.knime",
                    "node_type": "MetaNode",
                    "name": "Metanode6",
                    "children": [
                        {
                            "node_id": "4",
                            "filename": "cf_settings.xml",
                            "node_type": "NativeNode",
                        }
                    ],
                    "meta_in_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
                    "meta_out_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
                },
            ],
            "meta_in_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "meta_out_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
        },
    ]

    cf_model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    node1 = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.model = cf_model
    node1.port_count = 1

    node84 = kdlc.Node(
        node_id="8.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node84.model = cf_model
    node84.port_count = 1

    node864 = kdlc.Node(
        node_id="8.6.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node864.model = cf_model
    node864.port_count = 1

    connection0 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_port="1",
        dest_node=node864,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection1 = kdlc.Connection(
        connection_id=1,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node864,
    )
    metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[connection0, connection1],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    connection0 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_node=node84,
        dest_port="1",
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection1 = kdlc.Connection(
        connection_id=1,
        dest_id="6",
        dest_node=metanode86,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node84,
    )
    connection2 = kdlc.Connection(
        connection_id=2,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="6",
        source_port="0",
        source_node=metanode86,
    )
    metanode8 = kdlc.MetaNode(
        node_id="8",
        name="Metanode8",
        children=[node84, metanode86],
        connections=[connection0, connection1, connection2],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    result = [node1, metanode8]
    assert result == kdlc.extract_nodes_from_filenames(
        test_resources_dir, node_filename_list
    )


def test_extract_nodes_from_filenames_wrapped(my_setup):
    node_filename_list = [
        {"node_id": "1", "filename": "csv_settings.xml", "node_type": "NativeNode"},
        {
            "node_id": "10",
            "filename": "wrapped/settings_wrapped.xml",
            "node_type": "SubNode",
            "meta_in_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "meta_out_ports": [{"1": "org.knime.core.node.BufferedDataTable"}],
            "name": "WrappedMetanode",
            "children": [
                {
                    "node_id": "2",
                    "filename": "rf_settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "4",
                    "filename": "input_settings.xml",
                    "node_type": "NativeNode",
                },
                {
                    "node_id": "5",
                    "filename": "output_settings.xml",
                    "node_type": "NativeNode",
                },
            ],
        },
    ]
    node1 = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory=("org.knime.base.node.io.csvreader.CSVReaderNodeFactory"),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.port_count = 1
    node1.model = [
        {
            "url": "/Users/jared/knime-workspace/Example "
            "Workflows/TheData/Misc/Demographics.csv"
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
    ]

    node10_2 = kdlc.Node(
        node_id="10.2",
        name="Row Filter",
        factory="org.knime.base.node.preproc.filter.row.RowFilterNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_2.port_count = 1
    node10_2.model = [
        {
            "rowFilter": [
                {"RowFilter_TypeID": "RangeVal_RowFilter"},
                {"ColumnName": "age"},
                {"include": True},
                {"deepFiltering": False},
                {
                    "lowerBound": [
                        {"datacell": "org.knime.core.data.def.IntCell"},
                        {"org.knime.core.data.def.IntCell": [{"IntCell": 20}]},
                    ]
                },
                {
                    "upperBound": [
                        {"datacell": "org.knime.core.data.def.IntCell"},
                        {"org.knime.core.data.def.IntCell": [{"IntCell": 40}]},
                    ]
                },
            ]
        }
    ]

    node10_4 = kdlc.Node(
        node_id="10.4",
        name="WrappedNode Input",
        factory="org.knime.core.node.workflow.virtual."
        "subnode.VirtualSubNodeInputNodeFactory",
        bundle_name="KNIME Core API",
        bundle_symbolic_name="org.knime.core",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_4.port_count = 1
    node10_4.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        }
    ]
    node10_4.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"sub-node-description": ""},
        {"port-names": [{"array-size": 1}, {"0": "Port 1"}]},
        {"port-descriptions": [{"array-size": 1}, {"0": ""}]},
    ]

    node10_5 = kdlc.Node(
        node_id="10.5",
        name="WrappedNode Output",
        factory="org.knime.core.node.workflow.virtual.subnode"
        ".VirtualSubNodeOutputNodeFactory",
        bundle_name="KNIME Core API",
        bundle_symbolic_name="org.knime.core",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_5.port_count = 0
    node10_5.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        }
    ]
    node10_5.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"port-names": [{"array-size": 1}, {"0": "Port 1"}]},
        {"port-descriptions": [{"array-size": 1}, {"0": ""}]},
    ]
    connection2_5 = kdlc.Connection(
        connection_id=0,
        source_id="2",
        source_port="1",
        source_node=node10_2,
        dest_id="5",
        dest_port="1",
        dest_node=node10_5,
    )

    connection4_2 = kdlc.Connection(
        connection_id=1,
        source_id="4",
        source_port="1",
        source_node=node10_4,
        dest_id="2",
        dest_port="1",
        dest_node=node10_2,
    )

    metanode = kdlc.WrappedMetaNode(
        node_id="10",
        name="WrappedMetanode",
        children=[node10_2, node10_4, node10_5],
        connections=[connection2_5, connection4_2],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    result = [node1, metanode]

    assert result == kdlc.extract_nodes_from_filenames(
        test_resources_dir, node_filename_list
    )


def test_flatten_node_list(my_setup):
    cf_model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    node1 = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.model = cf_model
    node1.port_count = 1

    node84 = kdlc.Node(
        node_id="8.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node84.model = cf_model
    node84.port_count = 1

    node864 = kdlc.Node(
        node_id="8.6.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node864.model = cf_model
    node864.port_count = 1

    connection0 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_port="1",
        dest_node=node864,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection1 = kdlc.Connection(
        connection_id=1,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node864,
    )
    metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[connection0, connection1],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    connection0 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_node=node84,
        dest_port="1",
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection1 = kdlc.Connection(
        connection_id=1,
        dest_id="6",
        dest_node=metanode86,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node84,
    )
    connection2 = kdlc.Connection(
        connection_id=2,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="6",
        source_port="0",
        source_node=metanode86,
    )
    metanode8 = kdlc.MetaNode(
        node_id="8",
        name="Metanode8",
        children=[node84, metanode86],
        connections=[connection0, connection1, connection2],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    input = [node1, metanode8]

    result = [node1, metanode8, node84, metanode86, node864]
    assert result == kdlc.flatten_node_list(input)


def test_unflatten_node_list(my_setup):
    cf_model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    node1 = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.model = cf_model
    node1.port_count = 1

    node84 = kdlc.Node(
        node_id="8.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node84.model = cf_model
    node84.port_count = 1

    node864 = kdlc.Node(
        node_id="8.6.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node864.model = cf_model
    node864.port_count = 1

    connection0 = kdlc.Connection(
        connection_id=0, dest_id="4", dest_port="1", source_id="-1", source_port="1"
    )
    connection1 = kdlc.Connection(
        connection_id=1, dest_id="-1", dest_port="1", source_id="4", source_port="1"
    )
    metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[connection0, connection1],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    connection0 = kdlc.Connection(
        connection_id=0, dest_id="4", dest_port="1", source_id="-1", source_port="1"
    )
    connection1 = kdlc.Connection(
        connection_id=1, dest_id="6", dest_port="1", source_id="4", source_port="1"
    )
    connection2 = kdlc.Connection(
        connection_id=2, dest_id="-1", dest_port="1", source_id="6", source_port="1"
    )
    metanode8 = kdlc.MetaNode(
        node_id="8",
        name="Metanode8",
        children=[node84, metanode86],
        connections=[connection0, connection1, connection2],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    input = [node1, metanode8, node84, metanode86, node864]

    result = [node1, metanode8]
    assert result == kdlc.unflatten_node_list(input)


def test_normalize_connections(my_setup):
    cf_model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    node1 = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.model = cf_model
    node1.port_count = 1

    node84 = kdlc.Node(
        node_id="8.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node84.model = cf_model
    node84.port_count = 1

    node864 = kdlc.Node(
        node_id="8.6.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node864.model = cf_model
    node864.port_count = 1

    connection_m_in_864 = kdlc.Connection(
        connection_id=0, dest_id="4", dest_port="1", source_id="-1", source_port="1"
    )
    connection_864_m_out = kdlc.Connection(
        connection_id=1, dest_id="-1", dest_port="1", source_id="4", source_port="1"
    )
    metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[connection_m_in_864, connection_864_m_out],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    connection_m_in_84 = kdlc.Connection(
        connection_id=0, dest_id="4", dest_port="1", source_id="-1", source_port="1"
    )
    connection_84_86 = kdlc.Connection(
        connection_id=1, dest_id="6", dest_port="1", source_id="4", source_port="1"
    )
    connection_86_m_out = kdlc.Connection(
        connection_id=2, dest_id="-1", dest_port="1", source_id="6", source_port="1"
    )
    metanode8 = kdlc.MetaNode(
        node_id="8",
        name="Metanode8",
        children=[node84, metanode86],
        connections=[connection_m_in_84, connection_84_86, connection_86_m_out],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    connection_1_8 = kdlc.Connection(
        connection_id=0, dest_id="8", dest_port="1", source_id="1", source_port="1"
    )

    # Result data begins

    res_connection_m_in_864 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_port="1",
        dest_node=node864,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    res_connection_864_m_out = kdlc.Connection(
        connection_id=1,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node864,
    )
    res_metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[res_connection_m_in_864, res_connection_864_m_out],
        meta_in_ports=[{"0": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"0": "org.knime.core.node.BufferedDataTable"}],
    )
    res_connection_m_in_84 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_node=node84,
        dest_port="1",
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    res_connection_84_86 = kdlc.Connection(
        connection_id=1,
        dest_id="6",
        dest_node=res_metanode86,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node84,
    )
    res_connection_86_m_out = kdlc.Connection(
        connection_id=2,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="6",
        source_port="0",
        source_node=res_metanode86,
    )
    res_metanode8 = kdlc.MetaNode(
        node_id="8",
        name="Metanode8",
        children=[node84, metanode86],
        connections=[
            res_connection_m_in_84,
            res_connection_84_86,
            res_connection_86_m_out,
        ],
        meta_in_ports=[{"0": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"0": "org.knime.core.node.BufferedDataTable"}],
    )

    res_connection_1_8 = kdlc.Connection(
        connection_id=0,
        dest_id="8",
        dest_port="0",
        dest_node=res_metanode8,
        source_id="1",
        source_port="1",
        source_node=node1,
    )

    in_nodes = [node1, metanode8]
    in_connections = [connection_1_8]

    res_connections = [res_connection_1_8]
    res_nodes = [node1, res_metanode8]

    kdlc.normalize_connections(in_nodes, in_connections)

    assert res_nodes == in_nodes
    assert res_connections == in_connections


def test_normalize_connections_wrapped(my_setup):

    node1 = kdlc.Node(
        node_id="1",
        name="File Reader",
        factory="org.knime.base.node.io.filereader.FileReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node1.port_count = 1
    node1.model = [
        {"DataURL": "knime://LOCAL/Example%20Workflows/TheData/Basics/adult.csv"},
        {
            "Delimiters": [
                {
                    "Delim0": [
                        {"pattern": "%%00010"},
                        {"combineMultiple": True},
                        {"includeInToken": False},
                        {"returnAsToken": True},
                    ]
                },
                {
                    "Delim1": [
                        {"pattern": "%%00013"},
                        {"combineMultiple": True},
                        {"includeInToken": False},
                        {"returnAsToken": True},
                    ]
                },
                {
                    "Delim2": [
                        {"pattern": ","},
                        {"combineMultiple": False},
                        {"includeInToken": False},
                        {"returnAsToken": False},
                    ]
                },
            ]
        },
        {
            "Quotes": [
                {
                    "Quote0": [
                        {"left": '"'},
                        {"right": '"'},
                        {"EscChar": "\\", "data_type": "xchar"},
                        {"DontRem": False},
                    ]
                },
                {
                    "Quote1": [
                        {"left": "'"},
                        {"right": "'"},
                        {"EscChar": "\\", "data_type": "xchar"},
                        {"DontRem": False},
                    ]
                },
            ]
        },
        {"Comments": []},
        {"WhiteSpaces": [{"WhiteSpace0": " "}, {"WhiteSpace1": "%%00009"}]},
        {"CombineMultDelims": False},
        {"SkipFirstLines": 0, "data_type": "xlong"},
        {"NewLineInQuotes": False},
        {"hasColHdr": True},
        {"hasRowHdr": False},
        {"ignoreEmptyLines": True},
        {"rowPrefix": "Row"},
        {
            "RowDelims": [
                {"RDelim0": "%%00010"},
                {"SkipEmptyLine0": True},
                {"RDelim1": "%%00013"},
                {"SkipEmptyLine1": True},
            ]
        },
        {"MissingPatterns": []},
        {"FormatParameter": []},
        {"globalMissPattern": "", "isnull": True},
        {"DecimalSeparator": ".", "data_type": "xchar"},
        {"ThrousandsSeparator": "%%00000", "data_type": "xchar"},
        {"ignEmtpyTokensAtEOR": False},
        {"acceptShortLines": False},
        {"uniquifyRowID": False},
        {"MaxNumOfRows": -1, "data_type": "xlong"},
        {"ColNumDetermLine": -1},
        {"CharsetName": "", "isnull": True},
        {"ConnectTimeoutInSeconds": 1},
        {"delimsAtEOLuserVal": False},
        {"numOfColumns": 15},
        {
            "ColumnProperties": [
                {
                    "0": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "age"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "1": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "workclass"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "2": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "fnlwgt"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "3": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "education"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "4": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "education-num"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "5": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "marital-status"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "6": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "occupation"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "7": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "relationship"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "8": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "race"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "9": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "sex"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "10": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "capital-gain"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "11": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "capital-loss"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "12": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "", "isnull": True},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "hours-per-week"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.IntCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "13": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "native-country"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
                {
                    "14": [
                        {"UserSetValues": False},
                        {"MissValuePattern": "?"},
                        {"FormatParameter": "", "isnull": True},
                        {"ReadPossValsFromFile": False},
                        {"SkipThisColumn": False},
                        {"ColumnName": "income"},
                        {
                            "ColumnClass": [
                                {"cell_class": "org.knime.core.data.def.StringCell"},
                                {"is_null": False},
                            ]
                        },
                    ]
                },
            ]
        },
    ]

    node7 = kdlc.Node(
        node_id="7",
        name="CSV Writer",
        factory="org.knime.base.node.io.csvwriter.CSVWriterNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node7.port_count = 1
    node7.model = [
        {"colSeparator": ","},
        {"missing": ""},
        {"quoteBegin": '"'},
        {"quoteEnd": '"'},
        {"quoteMode": "STRINGS"},
        {"quoteReplacement": ""},
        {"sepReplacePattern": ""},
        {"ReplSepInStrings": False},
        {"writeColHeader": True},
        {"writeRowHeader": False},
        {"decimalSeparator": ".", "data_type": "xchar"},
        {"lineEndingMode": "SYST"},
        {"charSet": "", "isnull": True},
        {"filename": "/Users/jared/repos/k-descriptor-language/kdl/demo_output_2.csv"},
        {"fileOverwritePolicy": "Overwrite"},
        {"skipWriteColHeaderOnAppend": False},
        {"commentBegin": ""},
        {"commentEnd": ""},
        {"addTime": False},
        {"addUser": False},
        {"addTablename": False},
        {"userCommentLine": ""},
        {"gzip": False},
    ]

    node11_6 = kdlc.Node(
        node_id="11.6",
        name="Concatenate",
        factory="org.knime.base.node.preproc.append.row.AppendedRowsNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node11_6.port_count = 1
    node11_6.model = [
        {"fail_on_duplicates": False},
        {"append_suffix": True},
        {"intersection_of_columns": False},
        {"suffix": "_dup"},
        {"enable_hiliting": False},
    ]

    node11_7 = kdlc.Node(
        node_id="11.7",
        name="WrappedNode Input",
        factory="org.knime.core.node.workflow.virtual."
        "subnode.VirtualSubNodeInputNodeFactory",
        bundle_name="KNIME Core API",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node11_7.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        },
        {
            "port_1": [
                {"index": 1},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        },
    ]
    node11_7.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"sub-node-description": ""},
        {"port-names": [{"array-size": 2}, {"0": "Port 1"}, {"1": "Port 2"}]},
        {"port-descriptions": [{"array-size": 2}, {"0": ""}, {"1": ""}]},
    ]
    node11_7.port_count = 2

    node11_8 = kdlc.Node(
        node_id="11.8",
        name="WrappedNode Output",
        factory="org.knime.core.node.workflow.virtual."
        "subnode.VirtualSubNodeOutputNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node11_8.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        }
    ]
    node11_8.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"port-names": [{"array-size": 1}, {"0": "Port 1"}]},
        {"port-descriptions": [{"array-size": 1}, {"0": ""}]},
    ]
    node11_8.port_count = 0

    connection6_8 = kdlc.Connection(
        connection_id=0, source_id="6", source_port="1", dest_id="8", dest_port="1"
    )
    connection7_6_1 = kdlc.Connection(
        connection_id=1, source_id="7", source_port="1", dest_id="6", dest_port="2"
    )
    connection7_6_2 = kdlc.Connection(
        connection_id=2, source_id="7", source_port="2", dest_id="6", dest_port="1"
    )

    node11 = kdlc.WrappedMetaNode(
        node_id="11",
        name="WrappedMetanode",
        children=[node11_6, node11_7, node11_8],
        connections=[connection6_8, connection7_6_1, connection7_6_2],
        meta_in_ports=[
            {"1": "org.knime.core.node.BufferedDataTable"},
            {"2": "org.knime.core.node.BufferedDataTable"},
        ],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    connection1_11_1 = kdlc.Connection(
        connection_id=0, source_id="1", source_port="1", dest_id="11", dest_port="1"
    )

    connection1_11_2 = kdlc.Connection(
        connection_id=1, source_id="1", source_port="1", dest_id="11", dest_port="2"
    )

    connection11_7 = kdlc.Connection(
        connection_id=2, source_id="11", source_port="1", dest_id="7", dest_port="1"
    )

    res_connection6_8 = kdlc.Connection(
        connection_id=0,
        source_id="6",
        source_port="1",
        source_node=node11_6,
        dest_id="8",
        dest_port="1",
        dest_node=node11_8,
    )
    res_connection7_6_1 = kdlc.Connection(
        connection_id=1,
        source_id="7",
        source_port="1",
        source_node=node11_7,
        dest_id="6",
        dest_port="2",
        dest_node=node11_6,
    )
    res_connection7_6_2 = kdlc.Connection(
        connection_id=2,
        source_id="7",
        source_port="2",
        source_node=node11_7,
        dest_id="6",
        dest_port="1",
        dest_node=node11_6,
    )

    res_connection1_11_1 = kdlc.Connection(
        connection_id=0,
        source_id="1",
        source_port="1",
        source_node=node1,
        dest_id="11",
        dest_port="1",
        dest_node=node11,
    )

    res_connection1_11_2 = kdlc.Connection(
        connection_id=1,
        source_id="1",
        source_port="1",
        source_node=node1,
        dest_id="11",
        dest_port="2",
        dest_node=node11,
    )

    res_connection11_7 = kdlc.Connection(
        connection_id=2,
        source_id="11",
        source_port="1",
        source_node=node11,
        dest_id="7",
        dest_port="1",
        dest_node=node7,
    )

    res_node11 = kdlc.WrappedMetaNode(
        node_id="11",
        name="WrappedMetanode",
        children=[node11_6, node11_7, node11_8],
        connections=[res_connection6_8, res_connection7_6_1, res_connection7_6_2],
        meta_in_ports=[
            {"0": "org.knime.core.node.BufferedDataTable"},
            {"1": "org.knime.core.node.BufferedDataTable"},
        ],
        meta_out_ports=[{"0": "org.knime.core.node.BufferedDataTable"}],
    )

    res_nodes = [node1, res_node11, node7]
    res_connections = [res_connection1_11_1, res_connection1_11_2, res_connection11_7]

    input_nodes = [node1, node11, node7]
    input_connections = [connection1_11_1, connection1_11_2, connection11_7]

    kdlc.normalize_connections(input_nodes, input_connections)

    assert res_nodes == input_nodes
    assert res_connections == input_connections


def test_extract_connections(my_setup):
    node1 = kdlc.Node(
        node_id="1",
        name="1",
        factory="1",
        bundle_name="1",
        bundle_symbolic_name="1",
        bundle_version="1",
        feature_name="1",
        feature_symbolic_name="1",
        feature_version="1",
    )
    node2 = kdlc.Node(
        node_id="2",
        name="2",
        factory="2",
        bundle_name="2",
        bundle_symbolic_name="2",
        bundle_version="2",
        feature_name="2",
        feature_symbolic_name="2",
        feature_version="2",
    )
    node3 = kdlc.Node(
        node_id="3",
        name="3",
        factory="3",
        bundle_name="3",
        bundle_symbolic_name="3",
        bundle_version="3",
        feature_name="3",
        feature_symbolic_name="3",
        feature_version="3",
    )
    connection1 = kdlc.Connection(
        connection_id=0,
        source_id="1",
        source_node=node1,
        dest_id="3",
        dest_node=node3,
        source_port="1",
        dest_port="1",
    )
    connection2 = kdlc.Connection(
        connection_id=1,
        source_id="3",
        source_node=node3,
        dest_id="2",
        dest_node=node2,
        source_port="1",
        dest_port="1",
    )
    result = [connection1, connection2]
    assert (
        kdlc.extract_connections(
            f"{test_resources_dir}/workflow.knime", [node1, node2, node3]
        )
        == result
    )


def test_extract_var_connections(my_setup):
    node1 = kdlc.Node(
        node_id="1",
        name="1",
        factory="1",
        bundle_name="1",
        bundle_symbolic_name="1",
        bundle_version="1",
        feature_name="1",
        feature_symbolic_name="1",
        feature_version="1",
    )
    node2 = kdlc.Node(
        node_id="2",
        name="2",
        factory="2",
        bundle_name="2",
        bundle_symbolic_name="2",
        bundle_version="2",
        feature_name="2",
        feature_symbolic_name="2",
        feature_version="2",
    )
    node3 = kdlc.Node(
        node_id="3",
        name="3",
        factory="3",
        bundle_name="3",
        bundle_symbolic_name="3",
        bundle_version="3",
        feature_name="3",
        feature_symbolic_name="3",
        feature_version="3",
    )
    connection1 = kdlc.Connection(
        connection_id=0,
        source_id="1",
        source_node=node1,
        dest_id="3",
        dest_node=node3,
        source_port="1",
        dest_port="1",
    )
    connection2 = kdlc.Connection(
        connection_id=1,
        source_id="3",
        source_node=node3,
        dest_id="2",
        dest_node=node2,
        source_port="1",
        dest_port="1",
    )
    connection3 = kdlc.VariableConnection(
        connection_id=2,
        source_id="3",
        source_node=node3,
        dest_id="2",
        dest_node=node2,
        source_port="0",
        dest_port="0",
    )
    result = [connection1, connection2, connection3]
    assert (
        kdlc.extract_connections(
            f"{test_resources_dir}/workflow_var_connection.knime", [node1, node2, node3]
        )
        == result
    )


def test_extract_var_connections_meta(my_setup):
    out_connection = kdlc.VariableConnection(
        connection_id=0,
        source_id="1",
        source_port="0",
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
    )
    node14 = kdlc.MetaNode(
        node_id="14",
        name="14",
        children=[],
        connections=[out_connection],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    in_connection = kdlc.VariableConnection(
        connection_id=0,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
        dest_id="1",
        dest_port="0",
    )
    node15 = kdlc.MetaNode(
        node_id="15",
        name="15",
        children=[],
        connections=[in_connection],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    connection14_15 = kdlc.VariableConnection(
        connection_id=0,
        source_id="14",
        source_node=node14,
        dest_id="15",
        dest_node=node15,
        source_port="0",
        dest_port="0",
    )
    result = [connection14_15]
    assert (
        kdlc.extract_connections(
            f"{test_resources_dir}/workflow_var_connection_meta.knime", [node14, node15]
        )
        == result
    )


def test_extract_global_wf_variables(my_setup):
    result = [{"test1": "test"}, {"test2": 1}, {"test3": 1.1}]
    assert result == kdlc.extract_global_wf_variables(
        f"{test_resources_dir}/workflow_var.knime"
    )


def test_create_node_settings_from_template_csv(my_setup):
    node = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node.port_count = 1
    node.model = [
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
    ]
    expected_result = ET.parse(f"{test_resources_dir}/csv_settings.xml")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_node_settings_from_template(node)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_node_settings_from_template_cf(my_setup):
    node = kdlc.Node(
        node_id="1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node.port_count = 1
    node.model = [
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
                                        "org.knime.core.data." "date.DateAndTimeValue"
                                    ): False
                                },
                            ]
                        }
                    ]
                },
            ]
        }
    ]

    expected_result = ET.parse(f"{test_resources_dir}/cf_settings.xml")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_node_settings_from_template(node)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_node_settings_from_template_js(my_setup):
    node = kdlc.Node(
        node_id="1",
        name="Bar Chart (JavaScript)",
        factory="org.knime.dynamic.js.v30.DynamicJSNodeFactory",
        bundle_name="KNIME Dynamically Created JavaScript Nodes",
        bundle_symbolic_name="org.knime.dynamic.js",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JavaScript Views",
        feature_symbolic_name="org.knime.features.js.views.feature.group",
        feature_version="3.7.2.v201904170930",
    )
    node.port_count = 1
    node.model = [
        {
            "displayFullscreenButton_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"displayFullscreenButton": True},
        {
            "legend_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"legend": True},
        {
            "enableHorizontalToggle_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableHorizontalToggle": True},
        {
            "freq_Internals": [
                {"SettingsModelID": "SMID_columnfilter"},
                {"EnabledStatus": True},
            ]
        },
        {
            "freq": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 1}, {"0": "Accuracy"}]},
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
                        {"typelist": [{"org.knime.core.data.DoubleValue": False}]}
                    ]
                },
            ]
        },
        {
            "tooltip_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"tooltip": True},
        {
            "title_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"title": "Bar Chart"},
        {
            "enableSwitchMissValCat_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSwitchMissValCat": True},
        {
            "includeMissValCat_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"includeMissValCat": True},
        {
            "processInMemory_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"processInMemory": True},
        {
            "freqLabel_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"freqLabel": ""},
        {
            "cat_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"cat": "model"},
        {
            "showWarnings_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"showWarnings": True},
        {
            "enableSubtitleEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSubtitleEdit": True},
        {
            "publishSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"publishSelection": True},
        {
            "showMaximum_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"showMaximum": True},
        {
            "catLabel_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"catLabel": ""},
        {
            "orientation_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"orientation": False},
        {
            "displayClearSelectionButton_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"displayClearSelectionButton": True},
        {"svg_Internals": [{"SettingsModelID": "SMID_svg"}, {"EnabledStatus": True}]},
        {
            "svg": [
                {"width": 600},
                {"height": 400},
                {"fullscreen": True},
                {"showFullscreen": True},
            ]
        },
        {
            "staggerLabels_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"staggerLabels": False},
        {
            "enableTitleEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableTitleEdit": True},
        {
            "enableSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableSelection": True},
        {
            "sort_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"sort": False},
        {
            "enableStackedEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableStackedEdit": True},
        {
            "enableAxisEdit_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableAxisEdit": True},
        {
            "reportOnMissingValues_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"reportOnMissingValues": True},
        {
            "subtitle_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"subtitle": ""},
        {
            "chartType_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"chartType": "Grouped"},
        {
            "enableStaggerToggle_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableStaggerToggle": True},
        {
            "enableViewControls_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableViewControls": True},
        {
            "aggr_Internals": [
                {"SettingsModelID": "SMID_string"},
                {"EnabledStatus": True},
            ]
        },
        {"aggr": "Sum"},
        {
            "subscribeToSelection_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"subscribeToSelection": True},
        {
            "enableMaximumValue_Internals": [
                {"SettingsModelID": "SMID_boolean"},
                {"EnabledStatus": True},
            ]
        },
        {"enableMaximumValue": True},
        {"hideInWizard": False},
        {"maxRows": 2500},
        {"generateImage": True},
        {"customCSS": ""},
    ]
    node.variables = []
    node.factory_settings = [{"nodeDir": "org.knime.dynamic.js.base:nodes/:barChart"}]

    expected_result = ET.parse(f"{test_resources_dir}/js_factory_settings.xml")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_node_settings_from_template(node)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_workflow_knime_from_template(my_setup):
    node1 = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.port_count = 1
    node1.model = [
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
    ]
    node2 = kdlc.Node(
        node_id="2",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node2.port_count = 1
    node2.model = [
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
                                        "org.knime.core.data." "date.DateAndTimeValue"
                                    ): False
                                },
                            ]
                        }
                    ]
                },
            ]
        }
    ]
    node3 = kdlc.Node(
        node_id="3",
        name="Table to JSON",
        factory="org.knime.json.node.fromtable.TableToJsonNodeFactory",
        bundle_name="JSON related functionality for KNIME",
        bundle_symbolic_name="org.knime.json",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JSON-Processing",
        feature_symbolic_name="org.knime.features.json.feature.group",
        feature_version="3.7.1.v201901281201",
    )
    node3.port_count = 1
    node3.model = [
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
                                {
                                    (
                                        "org.knime.core.data" ".date.DateAndTimeValue"
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
    ]
    node_list = [node1, node2, node3]
    connection_list = [
        kdlc.Connection(
            connection_id=0,
            source_id="1",
            source_port="1",
            source_node=node1,
            dest_id="3",
            dest_port="1",
            dest_node=node3,
        ),
        kdlc.Connection(
            connection_id=1,
            source_id="3",
            source_port="1",
            source_node=node3,
            dest_id="2",
            dest_port="1",
            dest_node=node2,
        ),
    ]
    global_variable_list = []
    workflow = kdlc.Workflow(
        connections=connection_list, variables=global_variable_list
    )
    expected_result = ET.parse(f"{test_resources_dir}/workflow.knime")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_workflow_knime_from_template(node_list, workflow)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_workflow_knime_from_template_global_var(my_setup):
    node1 = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.port_count = 1
    node1.model = [
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
    ]
    node2 = kdlc.Node(
        node_id="2",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node2.port_count = 1
    node2.model = [
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
                                        "org.knime.core.data." "date.DateAndTimeValue"
                                    ): False
                                },
                            ]
                        }
                    ]
                },
            ]
        }
    ]
    node3 = kdlc.Node(
        node_id="3",
        name="Table to JSON",
        factory="org.knime.json.node.fromtable.TableToJsonNodeFactory",
        bundle_name="JSON related functionality for KNIME",
        bundle_symbolic_name="org.knime.json",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JSON-Processing",
        feature_symbolic_name="org.knime.features.json.feature.group",
        feature_version="3.7.1.v201901281201",
    )
    node3.port_count = 1
    node3.model = [
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
                                {
                                    (
                                        "org.knime.core.data" ".date.DateAndTimeValue"
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
    ]
    node_list = [node1, node2, node3]
    connection_list = [
        kdlc.Connection(
            connection_id=0,
            source_id="1",
            source_port="1",
            source_node=node1,
            dest_id="3",
            dest_port="1",
            dest_node=node3,
        ),
        kdlc.Connection(
            connection_id=1,
            source_id="3",
            source_port="1",
            source_node=node3,
            dest_id="2",
            dest_port="1",
            dest_node=node2,
        ),
    ]
    global_variable_list = [{"test1": "test"}, {"test2": 1}, {"test3": 1.1}]
    workflow = kdlc.Workflow(
        connections=connection_list, variables=global_variable_list
    )
    expected_result = ET.parse(f"{test_resources_dir}/workflow_var.knime")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_workflow_knime_from_template(node_list, workflow)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_metanode_workflow_knime_from_template(my_setup):
    node864 = kdlc.Node(
        node_id="8.6.4",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node864.model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]
    node864.port_count = 1

    connection_m_in_864 = kdlc.Connection(
        connection_id=0,
        dest_id="4",
        dest_port="1",
        dest_node=node864,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection_864_m_out = kdlc.Connection(
        connection_id=1,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="4",
        source_port="1",
        source_node=node864,
    )
    metanode86 = kdlc.MetaNode(
        node_id="8.6",
        name="Metanode6",
        children=[node864],
        connections=[connection_m_in_864, connection_864_m_out],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    expected_result = ET.parse(f"{test_resources_dir}/workflow_meta_5.knime")
    expected_result_flattened = [i.tag for i in expected_result.iter()]

    result = kdlc.create_metanode_workflow_knime_from_template(metanode86)
    result_flattened = [i.tag for i in result.iter()]

    assert result_flattened == expected_result_flattened


def test_create_node_files(my_setup):
    node21 = kdlc.Node(
        node_id="2.1",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node21.model = [
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
                                {"org.knime.core.data.date.DateAndTimeValue": False},
                            ]
                        }
                    ]
                },
            ]
        }
    ]
    node21.port_count = 1

    connection_m_in_21 = kdlc.Connection(
        connection_id=0,
        dest_id="1",
        dest_port="1",
        dest_node=node21,
        source_id="-1",
        source_port="0",
        source_node=kdlc.META_IN,
    )
    connection_21_m_out = kdlc.Connection(
        connection_id=1,
        dest_id="-1",
        dest_node=kdlc.META_OUT,
        dest_port="0",
        source_id="2",
        source_port="1",
        source_node=node21,
    )
    metanode2 = kdlc.MetaNode(
        node_id="1",
        name="Metanode2",
        children=[node21],
        connections=[connection_m_in_21, connection_21_m_out],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )
    node1 = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.port_count = 1
    node1.model = [
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
    ]
    node_list = [node1, metanode2]

    kdlc.create_node_files(f"{test_generated_dir}/test", node_list)

    expected_result_1 = ET.parse(f"{test_resources_dir}/csv_settings.xml")
    expected_result_flattened_1 = [i.tag for i in expected_result_1.iter()]
    result_1 = ET.parse(f"{test_generated_dir}/test/CSV Reader (#1)/settings.xml")
    result_flattened_1 = [i.tag for i in result_1.iter()]

    expected_result_2 = ET.parse(f"{test_resources_dir}/cf_settings.xml")
    expected_result_flattened_2 = [i.tag for i in expected_result_2.iter()]
    result_2 = ET.parse(
        f"{test_generated_dir}/test/Metanode2 (#1)/Column Filter (#1)/settings.xml"
    )
    result_flattened_2 = [i.tag for i in result_2.iter()]

    expected_result_3 = ET.parse(f"{test_resources_dir}/workflow_meta_6.knime")
    expected_result_flattened_3 = [i.tag for i in expected_result_3.iter()]
    result_3 = ET.parse(f"{test_generated_dir}/test/Metanode2 (#1)/workflow.knime")
    result_flattened_3 = [i.tag for i in result_3.iter()]
    assert result_flattened_1 == expected_result_flattened_1
    assert result_flattened_2 == expected_result_flattened_2
    assert result_flattened_3 == expected_result_flattened_3


def test_create_node_files_wrapped(my_setup):
    node10_2 = kdlc.Node(
        node_id="10.2",
        name="Row Filter",
        factory="org.knime.base.node.preproc.filter.row.RowFilterNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_2.port_count = 1
    node10_2.model = [
        {
            "rowFilter": [
                {"RowFilter_TypeID": "RangeVal_RowFilter"},
                {"ColumnName": "age"},
                {"include": True},
                {"deepFiltering": False},
                {
                    "lowerBound": [
                        {"datacell": "org.knime.core.data.def.IntCell"},
                        {"org.knime.core.data.def.IntCell": [{"IntCell": 20}]},
                    ]
                },
                {
                    "upperBound": [
                        {"datacell": "org.knime.core.data.def.IntCell"},
                        {"org.knime.core.data.def.IntCell": [{"IntCell": 40}]},
                    ]
                },
            ]
        }
    ]

    node10_4 = kdlc.Node(
        node_id="10.4",
        name="WrappedNode Input",
        factory="org.knime.core.node.workflow.virtual.subnode."
        "VirtualSubNodeInputNodeFactory",
        bundle_name="KNIME Core API",
        bundle_symbolic_name="org.knime.core",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_4.port_count = 1
    node10_4.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        }
    ]
    node10_4.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"sub-node-description": ""},
        {"port-names": [{"array-size": 1}, {"0": "Port 1"}]},
        {"port-descriptions": [{"array-size": 1}, {"0": ""}]},
    ]

    node10_5 = kdlc.Node(
        node_id="10.5",
        name="WrappedNode Output",
        factory="org.knime.core.node.workflow.virtual.subnode."
        "VirtualSubNodeOutputNodeFactory",
        bundle_name="KNIME Core API",
        bundle_symbolic_name="org.knime.core",
        bundle_version="3.7.2.v201904170949",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.2.v201904171038",
    )
    node10_5.port_count = 0
    node10_5.factory_settings = [
        {
            "port_0": [
                {"index": 0},
                {"type": [{"object_class": "org.knime.core.node.BufferedDataTable"}]},
            ]
        }
    ]
    node10_5.model = [
        {
            "variable-filter": [
                {"filter-type": "STANDARD"},
                {"included_names": [{"array-size": 0}]},
                {"excluded_names": [{"array-size": 0}]},
                {"enforce_option": "EnforceInclusion"},
                {
                    "name_pattern": [
                        {"pattern": ""},
                        {"type": "Wildcard"},
                        {"caseSensitive": True},
                    ]
                },
            ]
        },
        {"variable-prefix": "", "isnull": True},
        {"port-names": [{"array-size": 1}, {"0": "Port 1"}]},
        {"port-descriptions": [{"array-size": 1}, {"0": ""}]},
    ]
    connection2_5 = kdlc.Connection(
        connection_id=0,
        source_id="2",
        source_port="1",
        source_node=node10_2,
        dest_id="5",
        dest_port="1",
        dest_node=node10_5,
    )

    connection4_2 = kdlc.Connection(
        connection_id=1,
        source_id="4",
        source_port="1",
        source_node=node10_4,
        dest_id="2",
        dest_port="1",
        dest_node=node10_2,
    )

    metanode = kdlc.WrappedMetaNode(
        node_id="10",
        name="WrappedMetanode",
        children=[node10_2, node10_4, node10_5],
        connections=[connection2_5, connection4_2],
        meta_in_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
        meta_out_ports=[{"1": "org.knime.core.node.BufferedDataTable"}],
    )

    node_list = [metanode]
    kdlc.create_node_files(f"{test_generated_dir}/wrapped", node_list)

    expected_result_1 = ET.parse(f"{test_resources_dir}/wrapped/settings_wrapped.xml")
    expected_result_flattened_1 = [i.tag for i in expected_result_1.iter()]
    result_1 = ET.parse(
        f"{test_generated_dir}/wrapped/WrappedMetanode (#10)/settings.xml"
    )
    result_flattened_1 = [i.tag for i in result_1.iter()]

    expected_result_2 = ET.parse(f"{test_resources_dir}/wrapped/workflow.knime")
    expected_result_flattened_2 = [i.tag for i in expected_result_2.iter()]
    result_2 = ET.parse(
        f"{test_generated_dir}/wrapped/WrappedMetanode (#10)/workflow.knime"
    )
    result_flattened_2 = [i.tag for i in result_2.iter()]

    expected_result_3 = ET.parse(f"{test_resources_dir}/wrapped/input_settings.xml")
    expected_result_flattened_3 = [i.tag for i in expected_result_3.iter()]
    result_3 = ET.parse(
        f"{test_generated_dir}/wrapped/WrappedMetanode (#10)"
        f"/WrappedNode Input (#4)/settings.xml"
    )
    result_flattened_3 = [i.tag for i in result_3.iter()]

    expected_result_4 = ET.parse(f"{test_resources_dir}/wrapped/output_settings.xml")
    expected_result_flattened_4 = [i.tag for i in expected_result_4.iter()]
    result_4 = ET.parse(
        f"{test_generated_dir}/wrapped/WrappedMetanode (#10)"
        f"/WrappedNode Output (#5)/settings.xml"
    )
    result_flattened_4 = [i.tag for i in result_4.iter()]

    expected_result_5 = ET.parse(f"{test_resources_dir}/wrapped/rf_settings.xml")
    expected_result_flattened_5 = [i.tag for i in expected_result_5.iter()]
    result_5 = ET.parse(
        f"{test_generated_dir}/wrapped/WrappedMetanode (#10)"
        f"/Row Filter (#2)/settings.xml"
    )
    result_flattened_5 = [i.tag for i in result_5.iter()]

    assert expected_result_flattened_1 == result_flattened_1
    assert expected_result_flattened_2 == result_flattened_2
    assert expected_result_flattened_3 == result_flattened_3
    assert expected_result_flattened_4 == result_flattened_4
    assert expected_result_flattened_5 == result_flattened_5


def test_set_class_for_global_variables_str(my_setup):
    variables = [{"test1": "test"}, {"test2": 2}, {"test3": 3.0}]
    result = [
        {"test1": "test", "var_class": "STRING"},
        {"test2": 2, "var_class": "INTEGER"},
        {"test3": 3.0, "var_class": "DOUBLE"},
    ]
    kdlc.set_class_for_global_variables(variables)
    assert result == variables


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


def test_save_output_kdl_workflow(my_setup):
    node1 = kdlc.Node(
        node_id="1",
        name="CSV Reader",
        factory="org.knime.base.node.io.csvreader.CSVReaderNodeFactory",
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node1.port_count = 1
    node1.model = [
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
    ]
    node2 = kdlc.Node(
        node_id="2",
        name="Column Filter",
        factory=(
            "org.knime.base.node.preproc.filter."
            "column.DataColumnSpecFilterNodeFactory"
        ),
        bundle_name="KNIME Base Nodes",
        bundle_symbolic_name="org.knime.base",
        bundle_version="3.7.1.v201901291053",
        feature_name="KNIME Core",
        feature_symbolic_name="org.knime.features.base.feature.group",
        feature_version="3.7.1.v201901291053",
    )
    node2.port_count = 1
    node2.model = [
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
                                        "org.knime.core.data." "date.DateAndTimeValue"
                                    ): False
                                },
                            ]
                        }
                    ]
                },
            ]
        }
    ]
    node3 = kdlc.Node(
        node_id="3",
        name="Table to JSON",
        factory="org.knime.json.node.fromtable.TableToJsonNodeFactory",
        bundle_name="JSON related functionality for KNIME",
        bundle_symbolic_name="org.knime.json",
        bundle_version="3.7.1.v201901281201",
        feature_name="KNIME JSON-Processing",
        feature_symbolic_name="org.knime.features.json.feature.group",
        feature_version="3.7.1.v201901281201",
    )
    node3.port_count = 1
    node3.model = [
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
                                {
                                    (
                                        "org.knime.core.data" ".date.DateAndTimeValue"
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
    ]
    node_list = [node1, node2, node3]
    connection_list = [
        kdlc.Connection(
            connection_id=0,
            source_id="1",
            source_port="1",
            source_node=node1,
            dest_id="3",
            dest_port="1",
            dest_node=node3,
        ),
        kdlc.Connection(
            connection_id=1,
            source_id="3",
            source_port="1",
            source_node=node3,
            dest_id="2",
            dest_port="1",
            dest_node=node2,
        ),
    ]
    global_variable_list = []
    workflow = kdlc.Workflow(
        connections=connection_list, variables=global_variable_list
    )
    kdlc.save_output_kdl_workflow(f"{test_generated_dir}/out.kdl", workflow, node_list)
    assert filecmp.cmp(f"{test_resources_dir}/in.kdl", f"{test_generated_dir}/out.kdl")


def test_cleanup(my_setup):
    kdlc.cleanup()
    assert os.path.exists(kdlc.TMP_INPUT_DIR.name) is False
    assert os.path.exists(kdlc.TMP_OUTPUT_DIR.name) is False
