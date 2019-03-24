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


    # Enter a parse tree produced by KDLParser#connection.
    def enterConnection(self, ctx:KDLParser.ConnectionContext):
        pass

    # Exit a parse tree produced by KDLParser#connection.
    def exitConnection(self, ctx:KDLParser.ConnectionContext):
        pass


    # Enter a parse tree produced by KDLParser#node_settings.
    def enterNode_settings(self, ctx:KDLParser.Node_settingsContext):
        pass

    # Exit a parse tree produced by KDLParser#node_settings.
    def exitNode_settings(self, ctx:KDLParser.Node_settingsContext):
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


