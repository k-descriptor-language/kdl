# Generated from grammar/KDL.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .KDLParser import KDLParser
else:
    from KDLParser import KDLParser

# This class defines a complete listener for a parse tree produced by KDLParser.
class KDLListener(ParseTreeListener):

    # Enter a parse tree produced by KDLParser#node_id.
    def enterNode_id(self, ctx:KDLParser.Node_idContext):
        pass

    # Exit a parse tree produced by KDLParser#node_id.
    def exitNode_id(self, ctx:KDLParser.Node_idContext):
        pass


    # Enter a parse tree produced by KDLParser#port_id.
    def enterPort_id(self, ctx:KDLParser.Port_idContext):
        pass

    # Exit a parse tree produced by KDLParser#port_id.
    def exitPort_id(self, ctx:KDLParser.Port_idContext):
        pass


    # Enter a parse tree produced by KDLParser#port.
    def enterPort(self, ctx:KDLParser.PortContext):
        pass

    # Exit a parse tree produced by KDLParser#port.
    def exitPort(self, ctx:KDLParser.PortContext):
        pass


    # Enter a parse tree produced by KDLParser#node.
    def enterNode(self, ctx:KDLParser.NodeContext):
        pass

    # Exit a parse tree produced by KDLParser#node.
    def exitNode(self, ctx:KDLParser.NodeContext):
        pass


    # Enter a parse tree produced by KDLParser#node_settings.
    def enterNode_settings(self, ctx:KDLParser.Node_settingsContext):
        pass

    # Exit a parse tree produced by KDLParser#node_settings.
    def exitNode_settings(self, ctx:KDLParser.Node_settingsContext):
        pass


    # Enter a parse tree produced by KDLParser#source_node.
    def enterSource_node(self, ctx:KDLParser.Source_nodeContext):
        pass

    # Exit a parse tree produced by KDLParser#source_node.
    def exitSource_node(self, ctx:KDLParser.Source_nodeContext):
        pass


    # Enter a parse tree produced by KDLParser#destination_node.
    def enterDestination_node(self, ctx:KDLParser.Destination_nodeContext):
        pass

    # Exit a parse tree produced by KDLParser#destination_node.
    def exitDestination_node(self, ctx:KDLParser.Destination_nodeContext):
        pass


    # Enter a parse tree produced by KDLParser#connection.
    def enterConnection(self, ctx:KDLParser.ConnectionContext):
        pass

    # Exit a parse tree produced by KDLParser#connection.
    def exitConnection(self, ctx:KDLParser.ConnectionContext):
        pass


    # Enter a parse tree produced by KDLParser#var_connection.
    def enterVar_connection(self, ctx:KDLParser.Var_connectionContext):
        pass

    # Exit a parse tree produced by KDLParser#var_connection.
    def exitVar_connection(self, ctx:KDLParser.Var_connectionContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_in_node.
    def enterMeta_in_node(self, ctx:KDLParser.Meta_in_nodeContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_in_node.
    def exitMeta_in_node(self, ctx:KDLParser.Meta_in_nodeContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_out_node.
    def enterMeta_out_node(self, ctx:KDLParser.Meta_out_nodeContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_out_node.
    def exitMeta_out_node(self, ctx:KDLParser.Meta_out_nodeContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_connection.
    def enterMeta_connection(self, ctx:KDLParser.Meta_connectionContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_connection.
    def exitMeta_connection(self, ctx:KDLParser.Meta_connectionContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_var_connection.
    def enterMeta_var_connection(self, ctx:KDLParser.Meta_var_connectionContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_var_connection.
    def exitMeta_var_connection(self, ctx:KDLParser.Meta_var_connectionContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_in_ports.
    def enterMeta_in_ports(self, ctx:KDLParser.Meta_in_portsContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_in_ports.
    def exitMeta_in_ports(self, ctx:KDLParser.Meta_in_portsContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_out_ports.
    def enterMeta_out_ports(self, ctx:KDLParser.Meta_out_portsContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_out_ports.
    def exitMeta_out_ports(self, ctx:KDLParser.Meta_out_portsContext):
        pass


    # Enter a parse tree produced by KDLParser#meta_settings.
    def enterMeta_settings(self, ctx:KDLParser.Meta_settingsContext):
        pass

    # Exit a parse tree produced by KDLParser#meta_settings.
    def exitMeta_settings(self, ctx:KDLParser.Meta_settingsContext):
        pass


    # Enter a parse tree produced by KDLParser#node_list.
    def enterNode_list(self, ctx:KDLParser.Node_listContext):
        pass

    # Exit a parse tree produced by KDLParser#node_list.
    def exitNode_list(self, ctx:KDLParser.Node_listContext):
        pass


    # Enter a parse tree produced by KDLParser#nodes.
    def enterNodes(self, ctx:KDLParser.NodesContext):
        pass

    # Exit a parse tree produced by KDLParser#nodes.
    def exitNodes(self, ctx:KDLParser.NodesContext):
        pass


    # Enter a parse tree produced by KDLParser#global_variables.
    def enterGlobal_variables(self, ctx:KDLParser.Global_variablesContext):
        pass

    # Exit a parse tree produced by KDLParser#global_variables.
    def exitGlobal_variables(self, ctx:KDLParser.Global_variablesContext):
        pass


    # Enter a parse tree produced by KDLParser#workflow_connections.
    def enterWorkflow_connections(self, ctx:KDLParser.Workflow_connectionsContext):
        pass

    # Exit a parse tree produced by KDLParser#workflow_connections.
    def exitWorkflow_connections(self, ctx:KDLParser.Workflow_connectionsContext):
        pass


    # Enter a parse tree produced by KDLParser#workflow.
    def enterWorkflow(self, ctx:KDLParser.WorkflowContext):
        pass

    # Exit a parse tree produced by KDLParser#workflow.
    def exitWorkflow(self, ctx:KDLParser.WorkflowContext):
        pass


    # Enter a parse tree produced by KDLParser#json.
    def enterJson(self, ctx:KDLParser.JsonContext):
        pass

    # Exit a parse tree produced by KDLParser#json.
    def exitJson(self, ctx:KDLParser.JsonContext):
        pass


    # Enter a parse tree produced by KDLParser#obj.
    def enterObj(self, ctx:KDLParser.ObjContext):
        pass

    # Exit a parse tree produced by KDLParser#obj.
    def exitObj(self, ctx:KDLParser.ObjContext):
        pass


    # Enter a parse tree produced by KDLParser#pair.
    def enterPair(self, ctx:KDLParser.PairContext):
        pass

    # Exit a parse tree produced by KDLParser#pair.
    def exitPair(self, ctx:KDLParser.PairContext):
        pass


    # Enter a parse tree produced by KDLParser#array.
    def enterArray(self, ctx:KDLParser.ArrayContext):
        pass

    # Exit a parse tree produced by KDLParser#array.
    def exitArray(self, ctx:KDLParser.ArrayContext):
        pass


    # Enter a parse tree produced by KDLParser#value.
    def enterValue(self, ctx:KDLParser.ValueContext):
        pass

    # Exit a parse tree produced by KDLParser#value.
    def exitValue(self, ctx:KDLParser.ValueContext):
        pass


