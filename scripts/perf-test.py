import sys
import os
import subprocess
import timeit
import shutil

if shutil.which("kdlc") is None:
    print("Please install kdlc before running this script.")
    print("Installation instructions can be found at https://kdl.readthedocs.io")
    sys.exit(1)

node_count = 2
if len(sys.argv) > 1:
    node_count = int(sys.argv[1])

print(f"performance testing with {node_count} nodes")

print("preparing test", end="...", flush=True)

f = open("load.kdl", "a")
f.write("Nodes {")

for node in range(node_count):
    id = node + 1
    f.write(
        f"""
    (n{id}): {{"""
    )
    f.write(
        """
        "name": "Column Filter",
        "factory": "org.knime.base.node.preproc.filter.column.DataColumnSpecFilterNodeFactory",
        "bundle_name": "KNIME Base Nodes",
        "bundle_symbolic_name": "org.knime.base",
        "bundle_version": "3.7.1.v201901291053",
        "feature_name": "KNIME Core",
        "feature_symbolic_name": "org.knime.features.base.feature.group",
        "feature_version": "3.7.1.v201901291053",
        "model": [
            {
                "column-filter": [
                    {
                        "filter-type": "STANDARD"
                    },
                    {
                        "included_names": [
                            {
                                "array-size": 11
                            },
                            {
                                "0": "MaritalStatus"
                            },
                            {
                                "1": "Gender"
                            },
                            {
                                "2": "EstimatedYearlyIncome"
                            },
                            {
                                "3": "SentimentRating"
                            },
                            {
                                "4": "WebActivity"
                            },
                            {
                                "5": "Age"
                            },
                            {
                                "6": "Target"
                            },
                            {
                                "7": "Available401K"
                            },
                            {
                                "8": "CustomerValueSegment"
                            },
                            {
                                "9": "ChurnScore"
                            },
                            {
                                "10": "CallActivity"
                            }
                        ]
                    },
                    {
                        "excluded_names": [
                            {
                                "array-size": 1
                            },
                            {
                                "0": "NumberOfContracts"
                            }
                        ]
                    },
                    {
                        "enforce_option": "EnforceExclusion"
                    },
                    {
                        "name_pattern": [
                            {
                                "pattern": ""
                            },
                            {
                                "type": "Wildcard"
                            },
                            {
                                "caseSensitive": true
                            }
                        ]
                    },
                    {
                        "datatype": [
                            {
                                "typelist": [
                                    {
                                        "org.knime.core.data.StringValue": false
                                    },
                                    {
                                        "org.knime.core.data.IntValue": false
                                    },
                                    {
                                        "org.knime.core.data.DoubleValue": false
                                    },
                                    {
                                        "org.knime.core.data.BooleanValue": false
                                    },
                                    {
                                        "org.knime.core.data.LongValue": false
                                    },
                                    {
                                        "org.knime.core.data.date.DateAndTimeValue": false
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "port_count": 1
    }"""
    )
    if id != node_count:
        f.write(",")

f.write(
    """
}

Workflow {
    "connections": {"""
)

for node in range(0, node_count - 1):
    cur_id = node + 1
    next_id = node + 2

    f.write(
        f"""
        (n{cur_id}:1)-->(n{next_id}:1)"""
    )

    if next_id != node_count:
        f.write(",")

f.write(
    """
    }
}
"""
)

f.close()

print("done")

# kdl to knwf timer
print("kdl compilation:", end=" ", flush=True)
start_compilation = timeit.default_timer()

subprocess.call(["kdlc", "-i", "load.kdl", "-o", "load-result.knwf"])

finished_compilation = timeit.default_timer()

compile_time = finished_compilation - start_compilation
print(f"{compile_time} seconds")

# knwf to kdl timer
print("knwf decompilation:", end=" ", flush=True)
start_decompilation = timeit.default_timer()

subprocess.call(["kdlc", "-i", "load-result.knwf", "-o", "load-result.kdl"])

finished_decompilation = timeit.default_timer()

decompile_time = finished_decompilation - start_decompilation
print(f"{decompile_time} seconds")

# clean up
os.remove("load.kdl")
os.remove("load-result.kdl")
os.remove("load-result.knwf")
