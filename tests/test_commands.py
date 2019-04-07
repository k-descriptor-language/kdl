import kdlc


def test_kdl_to_workflow(mocker):
    # mock_file_stream returns mock_input
    mock_file_stream = mocker.MagicMock()
    mocker.patch.object(kdlc.commands, "FileStream", mock_file_stream)
    mock_input = mocker.MagicMock()
    mock_file_stream.return_value = mock_input

    # mock_kdl_lexer returns mock_lexer
    mock_kdl_lexer = mocker.MagicMock()
    mocker.patch.object(kdlc.commands, "KDLLexer", mock_kdl_lexer)
    mock_lexer = mocker.MagicMock()
    mock_kdl_lexer.return_value = mock_lexer

    # mock_cts returns mock_stream
    mock_cts = mocker.MagicMock()
    mocker.patch.object(kdlc.commands, "CommonTokenStream", mock_cts)
    mock_stream = mocker.MagicMock()
    mock_cts.return_value = mock_stream

    # mock_kdl_parser returns mock_parser
    mock_kdl_parser = mocker.MagicMock()
    mocker.patch.object(kdlc.commands, "KDLParser", mock_kdl_parser)
    mock_parser = mocker.MagicMock()
    mock_kdl_parser.return_value = mock_parser

    # mock_parser.nodes() returns nodes_tree
    nodes_tree = mocker.MagicMock()
    mock_parser.nodes.return_value = nodes_tree

    # mock_parser.workflow() returns workflow_tree
    workflow_tree = mocker.MagicMock()
    mock_parser.workflow.return_value = workflow_tree

    # mock KDLLoader returns mock_listener
    mocker.patch.object(kdlc.commands, "KDLLoader")
    mock_listener = mocker.MagicMock()
    kdlc.commands.KDLLoader.return_value = mock_listener

    # mock ParseTreeWalker returns mock_walker
    mocker.patch.object(kdlc.commands, "ParseTreeWalker")
    mock_walker = mocker.MagicMock()
    kdlc.commands.ParseTreeWalker.return_value = mock_walker

    mock_build_knwf = mocker.MagicMock()
    mocker.patch("kdlc.commands.build_knwf", new=mock_build_knwf)

    kdlc.kdl_to_workflow("fake.kdl", "fake.knwf")

    # validate construction of parser
    mock_file_stream.assert_called_with("fake.kdl")
    mock_kdl_lexer.assert_called_with(mock_input)
    mock_cts.assert_called_with(mock_lexer)
    mock_kdl_parser.assert_called_with(mock_stream)

    # validate walking through tree for nodes and workflow
    mock_walker.walk.assert_any_call(mock_listener, nodes_tree)
    mock_walker.walk.assert_any_call(mock_listener, workflow_tree)

    mock_build_knwf.assert_called_with(
        mock_listener.nodes, mock_listener.connections, "fake.knwf"
    )


def test_workflow_to_kdl(mocker):
    input_file = "test.knwf"
    output_file = "test.kdl"

    unzip_workflow = mocker.MagicMock()
    unzip_workflow.return_value = "test"
    mocker.patch("kdlc.unzip_workflow", new=unzip_workflow)

    extract_connections = mocker.MagicMock()
    extract_connections.return_value = []
    mocker.patch("kdlc.extract_connections", new=extract_connections)

    extract_global_wf_variables = mocker.MagicMock()
    extract_global_wf_variables.return_value = []
    mocker.patch("kdlc.extract_global_wf_variables", new=extract_global_wf_variables)

    node_dict = {"node_id": "1", "filename": "test.xml"}
    extract_node_filenames = mocker.MagicMock()
    extract_node_filenames.return_value = [node_dict]
    mocker.patch("kdlc.extract_node_filenames", new=extract_node_filenames)

    node = kdlc.Node(
        node_id="1",
        name="a",
        factory="a",
        bundle_name="a",
        bundle_symbolic_name="a",
        bundle_version="a",
        feature_name="a",
        feature_symbolic_name="a",
        feature_version="a",
    )
    extract_from_input_xml = mocker.MagicMock()
    extract_from_input_xml.return_value = node
    mocker.patch("kdlc.extract_from_input_xml", new=extract_from_input_xml)

    save_output_kdl_workflow = mocker.MagicMock()
    mocker.patch("kdlc.save_output_kdl_workflow", new=save_output_kdl_workflow)

    cleanup = mocker.MagicMock()
    mocker.patch("kdlc.cleanup", new=cleanup)

    kdlc.workflow_to_kdl(input_file, output_file)

    unzip_workflow.assert_called_with(input_file)
    extract_connections.assert_called_with(f"{kdlc.INPUT_PATH}/test/workflow.knime")
    extract_global_wf_variables.assert_called_with(
        f"{kdlc.INPUT_PATH}/test/workflow.knime"
    )
    extract_node_filenames.assert_called_with(f"{kdlc.INPUT_PATH}/test/workflow.knime")
    extract_from_input_xml.assert_called_with(
        node_dict["node_id"], f'{kdlc.INPUT_PATH}/test/{node_dict["filename"]}'
    )
    save_output_kdl_workflow.assert_called_with(output_file, [], [node], [])
    cleanup.assert_called()


def test_build_knwf(mocker):
    # mock create_workflow_knime_from_template
    mock_create_workflow_knime_from_template = mocker.MagicMock()
    output_workflow_knime = mocker.MagicMock()
    mock_create_workflow_knime_from_template.return_value = output_workflow_knime
    mocker.patch(
        "kdlc.create_workflow_knime_from_template",
        new=mock_create_workflow_knime_from_template,
    )

    # mock save_workflow_knime
    mock_save_workflow_knime = mocker.MagicMock()
    mocker.patch("kdlc.save_workflow_knime", new=mock_save_workflow_knime)

    # mock create_node_settings_from_template
    mock_create_node_settings_from_template = mocker.MagicMock()
    mock_tree = mocker.MagicMock()
    mock_create_node_settings_from_template.return_value = mock_tree
    mocker.patch(
        "kdlc.create_node_settings_from_template",
        new=mock_create_node_settings_from_template,
    )

    # mock save_node_settings_xml
    mock_save_node_settings_xml = mocker.MagicMock()
    mocker.patch("kdlc.save_node_settings_xml", new=mock_save_node_settings_xml)

    # mock create_output_workflow
    mock_create_output_workflow = mocker.MagicMock()
    mocker.patch("kdlc.create_output_workflow", new=mock_create_output_workflow)

    # fake inputs
    node_one = kdlc.Node(
        node_id="1",
        name="a",
        factory="a",
        bundle_name="a",
        bundle_symbolic_name="a",
        bundle_version="a",
        feature_name="a",
        feature_symbolic_name="a",
        feature_version="a",
    )
    node_two = kdlc.Node(
        node_id="2",
        name="b",
        factory="b",
        bundle_name="b",
        bundle_symbolic_name="b",
        bundle_version="b",
        feature_name="b",
        feature_symbolic_name="b",
        feature_version="b",
    )
    nodes = [node_one, node_two]
    connections = [mocker.MagicMock()]

    kdlc.build_knwf(nodes, connections, "fake.knwf")

    # validate workflow generation
    mock_create_workflow_knime_from_template.assert_called_with(nodes, connections)
    mock_save_workflow_knime.assert_called_with(
        output_workflow_knime, f"{kdlc.OUTPUT_PATH}/fake"
    )

    # validate xml generation
    mock_create_node_settings_from_template.assert_any_call(node_one)
    mock_save_node_settings_xml.assert_any_call(
        mock_tree, f"{kdlc.OUTPUT_PATH}/fake/{node_one.get_filename()}"
    )
    mock_create_node_settings_from_template.assert_any_call(node_two)
    mock_save_node_settings_xml.assert_any_call(
        mock_tree, f"{kdlc.OUTPUT_PATH}/fake/{node_two.get_filename()}"
    )

    # validate archive creation
    mock_create_output_workflow.assert_called_with("fake")
