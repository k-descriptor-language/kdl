import json
from kdlc.parser.KDLListener import KDLListener
from kdlc.parser.KDLParser import KDLParser
from kdlc.objects import Connection, Node, MetaNode
from kdlc.core import META_IN, META_OUT


class KDLLoader(KDLListener):
    def __init__(self):
        self.nodes = []
        self.connections = []
        self.global_variables = []

    def exitNode_settings(
        self: KDLListener, ctx: KDLParser.Node_settingsContext
    ) -> None:
        node_number = ctx.node().node_id().getText()
        # print(f"nodeNumber: {node_number}")

        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        node_settings = json.loads(json_string)
        # print(node_settings)

        # TODO: does this name even matter? if it does, we need to be defensive here
        node_name = node_settings["name"]
        node = Node(
            node_id=node_number,
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

    def exitMeta_settings(self, ctx: KDLParser.Meta_settingsContext):
        node_number = ctx.node().node_id().getText()
        name = ctx.STRING(1)
        metanode = MetaNode(node_id=node_number, name=name, children=[], connections=[])
        for connection in ctx.connection():
            source_node = connection.source_node().node()
            source_node_id = source_node.node_id().getText()
            dest_node = connection.destination_node().node()
            dest_node_id = dest_node.node_id().getText()
            if connection.VARIABLE_ARROW():
                source_node_port = "0"
                dest_node_port = "0"
            elif connection.ARROW():
                source_node_port = source_node.port().port_id().NUMBER().getText()
                dest_node_port = dest_node.port().port_id().NUMBER().getText()

            newConnection = Connection(
                connection_id=len(self.connections),
                source_id=source_node_id,
                dest_id=dest_node_id,
                source_port=source_node_port,
                dest_port=dest_node_port,
            )
            metanode.connections.append(newConnection)

        for connection in ctx.meta_connection():
            if connection.meta_in_node():
                source_node_port = (
                    connection.meta_in_node().port().port_id().NUMBER().getText()
                )
                dest_node = connection.destination_node().node()
                dest_node_id = dest_node.node_id().getText()
                dest_node_port = dest_node.port().port_id().NUMBER().getText()
                newConnection = Connection(
                    connection_id=len(self.connections),
                    source_id="-1",
                    source_node=META_IN,
                    dest_id=dest_node_id,
                    source_port=source_node_port,
                    dest_port=dest_node_port,
                )
            elif connection.meta_out_node():
                source_node = connection.source_node().node()
                source_node_id = source_node.node_id().getText()
                source_node_port = source_node.port().port_id().NUMBER().getText()
                dest_node_port = (
                    connection.meta_out_node().port().port_id().NUMBER().getText()
                )
                newConnection = Connection(
                    connection_id=len(self.connections),
                    source_id=source_node_id,
                    dest_id="-1",
                    dest_node=META_OUT,
                    source_port=source_node_port,
                    dest_port=dest_node_port,
                )
            metanode.connections.append(newConnection)
        self.nodes.append(metanode)

    def exitConnection(self: KDLListener, ctx: KDLParser.ConnectionContext) -> None:
        # TODO: is there a cleaner way to do this?
        if type(ctx.parentCtx) is KDLParser.Meta_settingsContext:
            return
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
            ex = ValueError("Invalid workflow connection")
            raise ex
        connection = Connection(
            connection_id=len(self.connections),
            source_id=source_node_id,
            dest_id=destination_node_id,
            source_port=source_node_port,
            dest_port=destination_node_port,
        )

        self.connections.append(connection)

    def exitGlobal_variables(self, ctx: KDLParser.Global_variablesContext):
        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        self.global_variables = json.loads(json_string)
