import kdlc


def test_merge_model_and_variables_1var(my_setup):
    node = kdlc.Node(
        id=1,
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
    node.variables = variables
    result = kdlc.Node(
        id=1,
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
    result.port_count = 1
    result.model = [
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
    result.variables = variables
    node.merge_variables_into_model()
    assert result == node


def test_merge_model_and_variables_2var(my_setup):
    node = kdlc.Node(
        id=1,
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
    node.variables = variables
    result = kdlc.Node(
        id=1,
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
    result.port_count = 1
    result.model = [
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
    result.variables = variables
    node.merge_variables_into_model()
    assert result == node


def test_extract_variables_from_model_used_exposed(my_setup):
    node = kdlc.Node(
        id=1,
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
    res = kdlc.Node(
        id=1,
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
    res.variables = [
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
    node.extract_variables_from_model()
    assert node == res


def test_extract_variables_from_model_used(my_setup):
    node = kdlc.Node(
        id=1,
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
    res = kdlc.Node(
        id=1,
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
    res.variables = [
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
    node.extract_variables_from_model()
    assert node == res


def test_extract_variables_from_model_exposed(my_setup):
    node = kdlc.Node(
        id=1,
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
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {
                            "0": "MaritalStatus",
                            "exposed_variable": "TEST",
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
    res = kdlc.Node(
        id=1,
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
            "selectedColumns": [
                {"filter-type": "STANDARD", "data_type": "xstring"},
                {
                    "included_names": [
                        {"array-size": "11", "data_type": "xint"},
                        {
                            "0": "MaritalStatus",
                            "exposed_variable": "TEST",
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
    res.variables = [
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
                                {"exposed_variable": "TEST", "data_type": "xstring"},
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
    node.extract_variables_from_model()
    assert node == res


def test_extract_variables_from_model_none(my_setup):
    node = kdlc.Node(
        id=1,
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
    res = kdlc.Node(
        id=1,
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

    node.extract_variables_from_model()
    assert node == res


def test_validate_node_from_schema(my_setup):
    node = kdlc.Node(
        id=1,
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
    node.validate_node_from_schema()
