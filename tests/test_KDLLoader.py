import kdlc
import pytest


def test_exitNode_settings(mocker):
    ctx = mocker.MagicMock()
    node_id = mocker.MagicMock()
    ctx.node.return_value.node_id.return_value = node_id
    node_id.NUMBER.return_value.getText.return_value = 42

    token_l_paren = mocker.MagicMock()
    token_l_paren.getText.return_value = "{"
    token_r_paren = mocker.MagicMock()
    token_r_paren.getText.return_value = "}"
    token_d_quote = mocker.MagicMock()
    token_d_quote.getText.return_value = '"'
    token_n = mocker.MagicMock()
    token_n.getText.return_value = "n"
    token_a = mocker.MagicMock()
    token_a.getText.return_value = "a"
    token_m = mocker.MagicMock()
    token_m.getText.return_value = "m"
    token_e = mocker.MagicMock()
    token_e.getText.return_value = "e"
    token_colon = mocker.MagicMock()
    token_colon.getText.return_value = ":"
    token_b = mocker.MagicMock()
    token_b.getText.return_value = "b"

    children = [
        token_l_paren,
        token_d_quote,
        token_n,
        token_a,
        token_m,
        token_e,
        token_d_quote,
        token_colon,
        token_d_quote,
        token_b,
        token_d_quote,
        token_r_paren,
    ]
    ctx.json.return_value.children = children

    listener = kdlc.commands.KDLLoader()

    listener.exitNode_settings(ctx)

    expected_node = {
        "id": 42,
        "filename": "b (#42)/settings.xml",
        "settings": {"name": "b"},
    }

    assert len(listener.nodes) == 1
    assert listener.nodes[0] == expected_node


def test_exitConnection(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    # source_node_port
    source_port_id = mocker.MagicMock()
    source_node.port.return_value.port_id = source_port_id
    source_port_id.return_value.NUMBER.return_value.getText.return_value = "2"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # destination_node_port
    destination_port_id = mocker.MagicMock()
    destination_node.port.return_value.port_id = destination_port_id
    destination_port_id.return_value.NUMBER.return_value.getText.return_value = "4"

    # connection arrow
    ctx.ARROW.return_value.getText.return_value = "-->"

    listener = kdlc.commands.KDLLoader()

    listener.exitConnection(ctx)

    expected_connection = {
        "id": 0,
        "source_id": "1",
        "dest_id": "3",
        "source_port": "2",
        "dest_port": "4",
    }

    assert len(listener.connections) == 1
    assert listener.connections[0] == expected_connection


def test_exitConnection_var(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # connection arrow
    ctx.VARIABLE_ARROW.return_value.getText.return_value = "~~>"

    listener = kdlc.commands.KDLLoader()

    listener.exitConnection(ctx)

    expected_connection = {
        "id": 0,
        "source_id": "1",
        "dest_id": "3",
        "source_port": "0",
        "dest_port": "0",
    }

    assert len(listener.connections) == 1
    assert listener.connections[0] == expected_connection


def test_exitConnection_fail(mocker):
    ctx = mocker.MagicMock()

    source_node = mocker.MagicMock()
    ctx.source_node.return_value.node.return_value = source_node

    # source_node_id
    source_node.node_id.return_value.getText.return_value = "1"

    destination_node = mocker.MagicMock()
    ctx.destination_node.return_value.node.return_value = destination_node

    # destination_node_id
    destination_node.node_id.return_value.getText.return_value = "3"

    # connection arrow
    ctx.VARIABLE_ARROW.return_value.getText.return_value = "FAIL"

    listener = kdlc.commands.KDLLoader()

    with pytest.raises(Exception):
        listener.exitConnection(ctx)
