import json
from typing import List, Dict, Any
from kdlc.parser.KDLListener import KDLListener
from kdlc.parser.KDLParser import KDLParser
from kdlc.objects import (
    AbstractNode,
    AbstractConnection,
    Connection,
    Node,
    MetaNode,
    VariableConnection,
    TemplateCatalogue,
    WrappedMetaNode,
)


class KDLLoader(KDLListener):
    def __init__(self, template_catalogue: TemplateCatalogue):
        self.nodes: List[AbstractNode] = list()
        self.connections: List[AbstractConnection] = list()
        self.global_variables: List[Dict[str, Any]] = list()
        self.template_catalogue: TemplateCatalogue = template_catalogue

    def exitNode_settings(
        self: KDLListener, ctx: KDLParser.Node_settingsContext
    ) -> None:
        node_number = ctx.node().node_id().getText()

        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        node_settings = json.loads(json_string)

        # NB: this name is important, it references the template node name
        node_name = node_settings["name"]
        template = self.template_catalogue.find_template(node_name)
        if template is not None:
            node_settings = TemplateCatalogue.merge_settings(template, node_settings)

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
        node.extract_variables_from_model()
        if "factory_settings" in node_settings:
            node.factory_settings += node_settings["factory_settings"]

        self.nodes.append(node)

    def exitMeta_settings(self, ctx: KDLParser.Meta_settingsContext):
        node_number = ctx.node().node_id().getText()
        name = ctx.STRING(1).getText()[1:-1]
        type = ctx.STRING(3).getText()[1:-1]

        json_tokens = [i.getText() for i in ctx.meta_in_ports().json().children]
        json_string = "".join(json_tokens)
        meta_in_ports = json.loads(json_string)

        json_tokens = [i.getText() for i in ctx.meta_out_ports().json().children]
        json_string = "".join(json_tokens)
        meta_out_ports = json.loads(json_string)

        if type == "MetaNode":
            metanode = MetaNode(
                node_id=node_number,
                name=name,
                children=[],
                connections=[],
                meta_in_ports=meta_in_ports,
                meta_out_ports=meta_out_ports,
            )
        elif type == "SubNode":
            metanode = WrappedMetaNode(
                node_id=node_number,
                name=name,
                children=[],
                connections=[],
                meta_in_ports=meta_in_ports,
                meta_out_ports=meta_out_ports,
            )
        for connection in ctx.connection():
            source_node = connection.source_node().node()
            source_node_id = source_node.node_id().getText()
            source_node_port = source_node.port()
            source_node_port_id = source_node_port.port_id().NUMBER().getText()

            dest_node = connection.destination_node().node()
            dest_node_id = dest_node.node_id().getText()
            dest_node_port = dest_node.port()
            dest_node_port_id = dest_node_port.port_id().NUMBER().getText()

            new_connection = Connection(
                connection_id=len(metanode.connections),
                source_id=source_node_id,
                source_port=source_node_port_id,
                dest_id=dest_node_id,
                dest_port=dest_node_port_id,
            )
            metanode.connections.append(new_connection)

        for connection in ctx.var_connection():
            source_node = connection.source_node().node()
            source_node_id = source_node.node_id().getText()
            source_node_port = source_node.port()
            source_node_port_id = (
                source_node_port.port_id().NUMBER().getText()
                if source_node_port
                else "0"
            )

            dest_node = connection.destination_node().node()
            dest_node_id = dest_node.node_id().getText()
            dest_node_port = dest_node.port()
            dest_node_port_id = (
                dest_node_port.port_id().NUMBER().getText() if dest_node_port else "0"
            )

            new_var_connection = VariableConnection(
                connection_id=len(metanode.connections),
                source_id=source_node_id,
                source_port=source_node_port_id,
                dest_id=dest_node_id,
                dest_port=dest_node_port_id,
            )
            metanode.connections.append(new_var_connection)

        for connection in ctx.meta_connection():
            if connection.meta_in_node():
                source_node_id = "-1"
                source_node_port = (
                    connection.meta_in_node().port().port_id().NUMBER().getText()
                )
            elif connection.source_node():
                source_node = connection.source_node().node()
                source_node_id = source_node.node_id().getText()
                source_node_port = source_node.port().port_id().NUMBER().getText()

            if connection.meta_out_node():
                dest_node_id = "-1"
                dest_node_port = (
                    connection.meta_out_node().port().port_id().NUMBER().getText()
                )
            elif connection.destination_node():
                dest_node = connection.destination_node().node()
                dest_node_id = dest_node.node_id().getText()
                dest_node_port = dest_node.port().port_id().NUMBER().getText()

            new_connection = Connection(
                connection_id=len(metanode.connections),
                source_id=source_node_id,
                dest_id=dest_node_id,
                source_port=source_node_port,
                dest_port=dest_node_port,
            )
            metanode.connections.append(new_connection)

        for connection in ctx.meta_var_connection():
            if connection.meta_in_node():
                source_node_id = "-1"
                source_node_port_id = (
                    connection.meta_in_node().port().port_id().NUMBER().getText()
                )
            elif connection.source_node():
                source_node = connection.source_node().node()
                source_node_id = source_node.node_id().getText()
                source_node_port = source_node.port()
                source_node_port_id = (
                    source_node_port.port_id().NUMBER().getText()
                    if source_node_port
                    else "0"
                )

            if connection.meta_out_node():
                dest_node_id = "-1"
                dest_node_port_id = (
                    connection.meta_out_node().port().port_id().NUMBER().getText()
                )
            elif connection.destination_node():
                dest_node = connection.destination_node().node()
                dest_node_id = dest_node.node_id().getText()
                dest_node_port = dest_node.port()
                dest_node_port_id = (
                    dest_node_port.port_id().NUMBER().getText()
                    if dest_node_port
                    else "0"
                )

            new_var_connection = VariableConnection(
                connection_id=len(metanode.connections),
                source_id=source_node_id,
                source_port=source_node_port_id,
                dest_id=dest_node_id,
                dest_port=dest_node_port_id,
            )
            metanode.connections.append(new_var_connection)
        self.nodes.append(metanode)

    def exitConnection(self: KDLListener, ctx: KDLParser.ConnectionContext) -> None:
        # TODO: is there a cleaner way to do this?
        if type(ctx.parentCtx) is KDLParser.Meta_settingsContext:
            return
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        source_node_port = source_node.port()
        source_node_port_id = source_node_port.port_id().NUMBER().getText()

        dest_node = ctx.destination_node().node()
        dest_node_id = dest_node.node_id().getText()
        dest_node_port = dest_node.port()
        dest_node_port_id = dest_node_port.port_id().NUMBER().getText()

        connection = Connection(
            connection_id=len(self.connections),
            source_id=source_node_id,
            source_port=source_node_port_id,
            dest_id=dest_node_id,
            dest_port=dest_node_port_id,
        )

        self.connections.append(connection)

    def exitVar_connection(self, ctx: KDLParser.Var_connectionContext):
        # TODO: is there a cleaner way to do this?
        if type(ctx.parentCtx) is KDLParser.Meta_settingsContext:
            return
        source_node = ctx.source_node().node()
        source_node_id = source_node.node_id().getText()
        source_node_port = source_node.port()
        source_node_port_id = (
            source_node_port.port_id().NUMBER().getText() if source_node_port else "0"
        )

        dest_node = ctx.destination_node().node()
        dest_node_id = dest_node.node_id().getText()
        dest_node_port = dest_node.port()
        dest_node_port_id = (
            dest_node_port.port_id().NUMBER().getText() if dest_node_port else "0"
        )

        connection = VariableConnection(
            connection_id=len(self.connections),
            source_id=source_node_id,
            dest_id=dest_node_id,
            source_port=source_node_port_id,
            dest_port=dest_node_port_id,
        )
        self.connections.append(connection)

    def exitGlobal_variables(self, ctx: KDLParser.Global_variablesContext):
        json_tokens = [i.getText() for i in ctx.json().children]
        json_string = "".join(json_tokens)
        self.global_variables = json.loads(json_string)
