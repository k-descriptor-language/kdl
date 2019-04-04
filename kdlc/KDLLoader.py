import json
from kdlc.parser.KDLListener import KDLListener
from kdlc.objects import Connection, Node


class KDLLoader(KDLListener):
    def __init__(self):
        self.nodes = []
        self.connections = []

    def exitNode_settings(self, ctx):
        node_number = ctx.node().node_id().NUMBER().getText()
        # print(f"nodeNumber: {node_number}")

        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        node_settings = json.loads(json_string)
        # print(node_settings)

        # TODO: does this name even matter? if it does, we need to be defensive here
        node_name = node_settings["name"]
        node = Node(
            id=node_number,
            name=node_name,
            factory=node_settings["factory"],
            bundle_name=node_settings["bundle_name"],
            bundle_symbolic_name=node_settings["bundle_symbolic_name"],
            bundle_version=node_settings["bundle_version"],
            feature_name=node_settings["feature_name"],
            feature_symbolic_name=node_settings["feature_symbolic_name"],
            feature_version=node_settings["feature_version"],
        )
        node.port_count = node_settings["port_count"]
        node.model = node_settings["model"]

        self.nodes.append(node)

    def exitConnection(self, ctx):
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        destination_node = ctx.destination_node().node()
        destination_node_id = destination_node.node_id().getText()

        if ctx.VARIABLE_ARROW():
            source_node_port = "0"
            destination_node_port = "0"
        elif ctx.ARROW():
            source_node_port = source_node.port().port_id().NUMBER().getText()
            destination_node_port = destination_node.port().port_id().NUMBER().getText()
        else:
            ex = ValueError()
            ex.strerror = "Invalid workflow connection"
            raise ex
        connection = Connection(
            id=len(self.connections),
            source_id=source_node_id,
            dest_id=destination_node_id,
            source_port=source_node_port,
            dest_port=destination_node_port,
        )

        self.connections.append(connection)
