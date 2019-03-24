# Generated from grammar/KDL.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .KDLParser import KDLParser
else:
    from KDLParser import KDLParser

# This class defines a complete listener for a parse tree produced by KDLParser.
class KDLListener(ParseTreeListener):

    # Enter a parse tree produced by KDLParser#node.
    def enterNode(self, ctx: KDLParser.NodeContext):
        pass

    # Exit a parse tree produced by KDLParser#node.
    def exitNode(self, ctx: KDLParser.NodeContext):
        pass

    # Enter a parse tree produced by KDLParser#json.
    def enterJson(self, ctx: KDLParser.JsonContext):
        pass

    # Exit a parse tree produced by KDLParser#json.
    def exitJson(self, ctx: KDLParser.JsonContext):
        pass

    # Enter a parse tree produced by KDLParser#node_settings.
    def enterNode_settings(self, ctx: KDLParser.Node_settingsContext):
        pass

    # Exit a parse tree produced by KDLParser#node_settings.
    def exitNode_settings(self, ctx: KDLParser.Node_settingsContext):
        pass
