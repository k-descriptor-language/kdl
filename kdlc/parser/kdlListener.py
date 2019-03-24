# Generated from kdl.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .kdlParser import kdlParser
else:
    from kdlParser import kdlParser

# This class defines a complete listener for a parse tree produced by kdlParser.
class kdlListener(ParseTreeListener):

    # Enter a parse tree produced by kdlParser#kdl.
    def enterKdl(self, ctx:kdlParser.KdlContext):
        pass

    # Exit a parse tree produced by kdlParser#kdl.
    def exitKdl(self, ctx:kdlParser.KdlContext):
        pass


    # Enter a parse tree produced by kdlParser#vertex.
    def enterVertex(self, ctx:kdlParser.VertexContext):
        pass

    # Exit a parse tree produced by kdlParser#vertex.
    def exitVertex(self, ctx:kdlParser.VertexContext):
        pass


    # Enter a parse tree produced by kdlParser#edge.
    def enterEdge(self, ctx:kdlParser.EdgeContext):
        pass

    # Exit a parse tree produced by kdlParser#edge.
    def exitEdge(self, ctx:kdlParser.EdgeContext):
        pass


