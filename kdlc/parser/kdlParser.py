# Generated from grammar/KDL.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22")
        buf.write("]\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\3\3\3\3")
        buf.write("\3\4\3\4\3\4\3\5\3\5\3\5\3\5\5\5$\n\5\3\5\3\5\3\6\3\6")
        buf.write("\3\6\3\6\3\7\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\t\7\t\66")
        buf.write("\n\t\f\t\16\t9\13\t\3\t\3\t\3\t\3\t\5\t?\n\t\3\n\3\n\3")
        buf.write("\n\3\n\3\13\3\13\3\13\3\13\7\13I\n\13\f\13\16\13L\13\13")
        buf.write("\3\13\3\13\3\13\3\13\5\13R\n\13\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\5\f[\n\f\3\f\2\2\r\2\4\6\b\n\f\16\20\22\24\26\2")
        buf.write("\2\2\\\2\30\3\2\2\2\4\32\3\2\2\2\6\34\3\2\2\2\b\37\3\2")
        buf.write("\2\2\n\'\3\2\2\2\f+\3\2\2\2\16/\3\2\2\2\20>\3\2\2\2\22")
        buf.write("@\3\2\2\2\24Q\3\2\2\2\26Z\3\2\2\2\30\31\7\22\2\2\31\3")
        buf.write("\3\2\2\2\32\33\7\22\2\2\33\5\3\2\2\2\34\35\7\20\2\2\35")
        buf.write("\36\5\4\3\2\36\7\3\2\2\2\37 \7\3\2\2 !\7\17\2\2!#\5\2")
        buf.write("\2\2\"$\5\6\4\2#\"\3\2\2\2#$\3\2\2\2$%\3\2\2\2%&\7\4\2")
        buf.write("\2&\t\3\2\2\2\'(\5\b\5\2()\7\16\2\2)*\5\b\5\2*\13\3\2")
        buf.write("\2\2+,\5\b\5\2,-\7\20\2\2-.\5\16\b\2.\r\3\2\2\2/\60\5")
        buf.write("\26\f\2\60\17\3\2\2\2\61\62\7\5\2\2\62\67\5\22\n\2\63")
        buf.write("\64\7\6\2\2\64\66\5\22\n\2\65\63\3\2\2\2\669\3\2\2\2\67")
        buf.write("\65\3\2\2\2\678\3\2\2\28:\3\2\2\29\67\3\2\2\2:;\7\7\2")
        buf.write("\2;?\3\2\2\2<=\7\5\2\2=?\7\7\2\2>\61\3\2\2\2><\3\2\2\2")
        buf.write("?\21\3\2\2\2@A\7\21\2\2AB\7\20\2\2BC\5\26\f\2C\23\3\2")
        buf.write("\2\2DE\7\b\2\2EJ\5\26\f\2FG\7\6\2\2GI\5\26\f\2HF\3\2\2")
        buf.write("\2IL\3\2\2\2JH\3\2\2\2JK\3\2\2\2KM\3\2\2\2LJ\3\2\2\2M")
        buf.write("N\7\t\2\2NR\3\2\2\2OP\7\b\2\2PR\7\t\2\2QD\3\2\2\2QO\3")
        buf.write("\2\2\2R\25\3\2\2\2S[\7\21\2\2T[\7\22\2\2U[\5\20\t\2V[")
        buf.write("\5\24\13\2W[\7\n\2\2X[\7\13\2\2Y[\7\f\2\2ZS\3\2\2\2ZT")
        buf.write("\3\2\2\2ZU\3\2\2\2ZV\3\2\2\2ZW\3\2\2\2ZX\3\2\2\2ZY\3\2")
        buf.write("\2\2[\27\3\2\2\2\b#\67>JQZ")
        return buf.getvalue()


class KDLParser ( Parser ):

    grammarFileName = "KDL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'{'", "','", "'}'", "'['", 
                     "']'", "'true'", "'false'", "'null'", "<INVALID>", 
                     "'-->'", "'n'", "':'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "WS", "ARROW", 
                      "NODEPREFIX", "COLON", "STRING", "NUMBER" ]

    RULE_node_id = 0
    RULE_port_id = 1
    RULE_port = 2
    RULE_node = 3
    RULE_connection = 4
    RULE_node_settings = 5
    RULE_json = 6
    RULE_obj = 7
    RULE_pair = 8
    RULE_array = 9
    RULE_value = 10

    ruleNames =  [ "node_id", "port_id", "port", "node", "connection", "node_settings", 
                   "json", "obj", "pair", "array", "value" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    WS=11
    ARROW=12
    NODEPREFIX=13
    COLON=14
    STRING=15
    NUMBER=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Node_idContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(KDLParser.NUMBER, 0)

        def getRuleIndex(self):
            return KDLParser.RULE_node_id

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNode_id" ):
                listener.enterNode_id(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNode_id" ):
                listener.exitNode_id(self)




    def node_id(self):

        localctx = KDLParser.Node_idContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_node_id)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.match(KDLParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Port_idContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(KDLParser.NUMBER, 0)

        def getRuleIndex(self):
            return KDLParser.RULE_port_id

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPort_id" ):
                listener.enterPort_id(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPort_id" ):
                listener.exitPort_id(self)




    def port_id(self):

        localctx = KDLParser.Port_idContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_port_id)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(KDLParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PortContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(KDLParser.COLON, 0)

        def port_id(self):
            return self.getTypedRuleContext(KDLParser.Port_idContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_port

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPort" ):
                listener.enterPort(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPort" ):
                listener.exitPort(self)




    def port(self):

        localctx = KDLParser.PortContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_port)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self.match(KDLParser.COLON)
            self.state = 27
            self.port_id()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NodeContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NODEPREFIX(self):
            return self.getToken(KDLParser.NODEPREFIX, 0)

        def node_id(self):
            return self.getTypedRuleContext(KDLParser.Node_idContext,0)


        def port(self):
            return self.getTypedRuleContext(KDLParser.PortContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_node

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNode" ):
                listener.enterNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNode" ):
                listener.exitNode(self)




    def node(self):

        localctx = KDLParser.NodeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_node)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self.match(KDLParser.T__0)
            self.state = 30
            self.match(KDLParser.NODEPREFIX)
            self.state = 31
            self.node_id()
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==KDLParser.COLON:
                self.state = 32
                self.port()


            self.state = 35
            self.match(KDLParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConnectionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def node(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KDLParser.NodeContext)
            else:
                return self.getTypedRuleContext(KDLParser.NodeContext,i)


        def ARROW(self):
            return self.getToken(KDLParser.ARROW, 0)

        def getRuleIndex(self):
            return KDLParser.RULE_connection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConnection" ):
                listener.enterConnection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConnection" ):
                listener.exitConnection(self)




    def connection(self):

        localctx = KDLParser.ConnectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_connection)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.node()
            self.state = 38
            self.match(KDLParser.ARROW)
            self.state = 39
            self.node()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Node_settingsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def node(self):
            return self.getTypedRuleContext(KDLParser.NodeContext,0)


        def COLON(self):
            return self.getToken(KDLParser.COLON, 0)

        def json(self):
            return self.getTypedRuleContext(KDLParser.JsonContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_node_settings

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNode_settings" ):
                listener.enterNode_settings(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNode_settings" ):
                listener.exitNode_settings(self)




    def node_settings(self):

        localctx = KDLParser.Node_settingsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_node_settings)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.node()
            self.state = 42
            self.match(KDLParser.COLON)
            self.state = 43
            self.json()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(KDLParser.ValueContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_json

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJson" ):
                listener.enterJson(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJson" ):
                listener.exitJson(self)




    def json(self):

        localctx = KDLParser.JsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_json)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KDLParser.PairContext)
            else:
                return self.getTypedRuleContext(KDLParser.PairContext,i)


        def getRuleIndex(self):
            return KDLParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)




    def obj(self):

        localctx = KDLParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 47
                self.match(KDLParser.T__2)
                self.state = 48
                self.pair()
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==KDLParser.T__3:
                    self.state = 49
                    self.match(KDLParser.T__3)
                    self.state = 50
                    self.pair()
                    self.state = 55
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 56
                self.match(KDLParser.T__4)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.match(KDLParser.T__2)
                self.state = 59
                self.match(KDLParser.T__4)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(KDLParser.STRING, 0)

        def COLON(self):
            return self.getToken(KDLParser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(KDLParser.ValueContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPair" ):
                listener.enterPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPair" ):
                listener.exitPair(self)




    def pair(self):

        localctx = KDLParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(KDLParser.STRING)
            self.state = 63
            self.match(KDLParser.COLON)
            self.state = 64
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(KDLParser.ValueContext)
            else:
                return self.getTypedRuleContext(KDLParser.ValueContext,i)


        def getRuleIndex(self):
            return KDLParser.RULE_array

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArray" ):
                listener.enterArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArray" ):
                listener.exitArray(self)




    def array(self):

        localctx = KDLParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.match(KDLParser.T__5)
                self.state = 67
                self.value()
                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==KDLParser.T__3:
                    self.state = 68
                    self.match(KDLParser.T__3)
                    self.state = 69
                    self.value()
                    self.state = 74
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 75
                self.match(KDLParser.T__6)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.match(KDLParser.T__5)
                self.state = 78
                self.match(KDLParser.T__6)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(KDLParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(KDLParser.NUMBER, 0)

        def obj(self):
            return self.getTypedRuleContext(KDLParser.ObjContext,0)


        def array(self):
            return self.getTypedRuleContext(KDLParser.ArrayContext,0)


        def getRuleIndex(self):
            return KDLParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = KDLParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_value)
        try:
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [KDLParser.STRING]:
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.match(KDLParser.STRING)
                pass
            elif token in [KDLParser.NUMBER]:
                self.enterOuterAlt(localctx, 2)
                self.state = 82
                self.match(KDLParser.NUMBER)
                pass
            elif token in [KDLParser.T__2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 83
                self.obj()
                pass
            elif token in [KDLParser.T__5]:
                self.enterOuterAlt(localctx, 4)
                self.state = 84
                self.array()
                pass
            elif token in [KDLParser.T__7]:
                self.enterOuterAlt(localctx, 5)
                self.state = 85
                self.match(KDLParser.T__7)
                pass
            elif token in [KDLParser.T__8]:
                self.enterOuterAlt(localctx, 6)
                self.state = 86
                self.match(KDLParser.T__8)
                pass
            elif token in [KDLParser.T__9]:
                self.enterOuterAlt(localctx, 7)
                self.state = 87
                self.match(KDLParser.T__9)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





