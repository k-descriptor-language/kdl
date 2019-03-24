# Generated from kdl.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\n")
        buf.write("\32\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\6\2\13\n\2\r\2\16")
        buf.write("\2\f\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\2")
        buf.write("\2\5\2\4\6\2\2\2\27\2\b\3\2\2\2\4\20\3\2\2\2\6\22\3\2")
        buf.write("\2\2\b\n\7\3\2\2\t\13\5\6\4\2\n\t\3\2\2\2\13\f\3\2\2\2")
        buf.write("\f\n\3\2\2\2\f\r\3\2\2\2\r\16\3\2\2\2\16\17\7\4\2\2\17")
        buf.write("\3\3\2\2\2\20\21\7\b\2\2\21\5\3\2\2\2\22\23\5\4\3\2\23")
        buf.write("\24\7\5\2\2\24\25\5\4\3\2\25\26\7\6\2\2\26\27\7\t\2\2")
        buf.write("\27\30\7\7\2\2\30\7\3\2\2\2\3\f")
        return buf.getvalue()


class kdlParser ( Parser ):

    grammarFileName = "kdl.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'Graph {'", "'}'", "'->'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ID", "NUM", "WS" ]

    RULE_kdl = 0
    RULE_vertex = 1
    RULE_edge = 2

    ruleNames =  [ "kdl", "vertex", "edge" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    ID=6
    NUM=7
    WS=8

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class KdlContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def edge(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(kdlParser.EdgeContext)
            else:
                return self.getTypedRuleContext(kdlParser.EdgeContext,i)


        def getRuleIndex(self):
            return kdlParser.RULE_kdl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKdl" ):
                listener.enterKdl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKdl" ):
                listener.exitKdl(self)




    def kdl(self):

        localctx = kdlParser.KdlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_kdl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(kdlParser.T__0)
            self.state = 8 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 7
                self.edge()
                self.state = 10 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==kdlParser.ID):
                    break

            self.state = 12
            self.match(kdlParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VertexContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(kdlParser.ID, 0)

        def getRuleIndex(self):
            return kdlParser.RULE_vertex

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVertex" ):
                listener.enterVertex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVertex" ):
                listener.exitVertex(self)




    def vertex(self):

        localctx = kdlParser.VertexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_vertex)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.match(kdlParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EdgeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def vertex(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(kdlParser.VertexContext)
            else:
                return self.getTypedRuleContext(kdlParser.VertexContext,i)


        def NUM(self):
            return self.getToken(kdlParser.NUM, 0)

        def getRuleIndex(self):
            return kdlParser.RULE_edge

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEdge" ):
                listener.enterEdge(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEdge" ):
                listener.exitEdge(self)




    def edge(self):

        localctx = kdlParser.EdgeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_edge)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.vertex()
            self.state = 17
            self.match(kdlParser.T__2)
            self.state = 18
            self.vertex()
            self.state = 19
            self.match(kdlParser.T__3)
            self.state = 20
            self.match(kdlParser.NUM)
            self.state = 21
            self.match(kdlParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





