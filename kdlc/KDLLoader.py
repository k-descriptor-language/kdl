import json
from kdlc.parser.KDLListener import KDLListener

class KDLLoader(KDLListener):
    def __init__(self):
        self.nodes = {}
        self.connections = []

    def exitNode_settings(self, ctx):
        node_number = ctx.node().node_id().NUMBER().getText()
        # print(f"nodeNumber: {node_number}")

        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        node_settings = json.loads(json_string)
        # print(node_settings)

        self.nodes[node_number] = node_settings

    def exitConnection(self, ctx):
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        source_node_port = source_node.port().getText()

        destination_node = ctx.destination_node().node()
        destination_node_id = destination_node.node_id().getText()
        destination_node_port = destination_node.port().getText()

        connection = {
            "source_id": source_node_id,
            "dest_id": destination_node_id,
            "source_port": source_node_port,
            "dest_port": destination_node_port,
        }

        self.connections.append(connection)


