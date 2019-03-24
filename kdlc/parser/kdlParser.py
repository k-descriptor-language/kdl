# Generated from grammar/KDL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\n")
        buf.write("\32\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\3\2\3\3\3\3\7")
        buf.write("\3\17\n\3\f\3\16\3\22\13\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\20\2\5\2\4\6\2\2\2\27\2\b\3\2\2\2\4\f\3\2\2\2\6\25")
        buf.write("\3\2\2\2\b\t\7\3\2\2\t\n\7\t\2\2\n\13\7\4\2\2\13\3\3\2")
        buf.write("\2\2\f\20\7\5\2\2\r\17\13\2\2\2\16\r\3\2\2\2\17\22\3\2")
        buf.write("\2\2\20\21\3\2\2\2\20\16\3\2\2\2\21\23\3\2\2\2\22\20\3")
        buf.write("\2\2\2\23\24\7\6\2\2\24\5\3\2\2\2\25\26\5\2\2\2\26\27")
        buf.write("\7\7\2\2\27\30\5\4\3\2\30\7\3\2\2\2\3\20")
        return buf.getvalue()


class KDLParser(Parser):

    grammarFileName = "KDL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'(n'", "')'", "'{'", "'}'", "':'"]

    symbolicNames = [
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "WS",
        "NUMBER",
        "ANY",
    ]

    RULE_node = 0
    RULE_json = 1
    RULE_node_settings = 2

    ruleNames = ["node", "json", "node_settings"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    WS = 6
    NUMBER = 7
    ANY = 8

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(
            self, self.atn, self.decisionsToDFA, self.sharedContextCache
        )
        self._predicates = None

    class NodeContext(ParserRuleContext):
        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(KDLParser.NUMBER, 0)

        def getRuleIndex(self):
            return KDLParser.RULE_node

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNode"):
                listener.enterNode(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNode"):
                listener.exitNode(self)

    def node(self):

        localctx = KDLParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_node)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(KDLParser.T__0)
            self.state = 7
            self.match(KDLParser.NUMBER)
            self.state = 8
            self.match(KDLParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class JsonContext(ParserRuleContext):
        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return KDLParser.RULE_json

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterJson"):
                listener.enterJson(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitJson"):
                listener.exitJson(self)

    def json(self):

        localctx = KDLParser.JsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_json)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.match(KDLParser.T__2)
            self.state = 14
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 0, self._ctx)
            while _alt != 1 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1 + 1:
                    self.state = 11
                    self.matchWildcard()
                self.state = 16
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 0, self._ctx)

            self.state = 17
            self.match(KDLParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Node_settingsContext(ParserRuleContext):
        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def node(self):
            return self.getTypedRuleContext(KDLParser.NodeContext, 0)

        def json(self):
            return self.getTypedRuleContext(KDLParser.JsonContext, 0)

        def getRuleIndex(self):
            return KDLParser.RULE_node_settings

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNode_settings"):
                listener.enterNode_settings(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNode_settings"):
                listener.exitNode_settings(self)

    def node_settings(self):

        localctx = KDLParser.Node_settingsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_node_settings)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.node()
            self.state = 20
            self.match(KDLParser.T__4)
            self.state = 21
            self.json()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
