import json
from kdlc.parser.KDLListener import KDLListener


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

        node = {
            "id": node_number,
            "filename": f"{node_name} (#{node_number})/settings.xml",
            "settings": node_settings,
        }

        self.nodes.append(node)

    def exitConnection(self, ctx):
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        source_node_port = source_node.port().port_id().NUMBER().getText()

        destination_node = ctx.destination_node().node()
        destination_node_id = destination_node.node_id().getText()
        destination_node_port = destination_node.port().port_id().NUMBER().getText()

        connection = {
            "id": len(self.connections),
            "source_id": source_node_id,
            "dest_id": destination_node_id,
            "source_port": source_node_port,
            "dest_port": destination_node_port,
        }

        self.connections.append(connection)
