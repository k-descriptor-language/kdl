# Generated from grammar/KDL.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\n")
        buf.write("\61\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write("\7\4\b\t\b\4\t\t\t\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5")
        buf.write("\3\6\3\6\3\7\6\7 \n\7\r\7\16\7!\3\7\3\7\3\b\3\b\3\b\7")
        buf.write("\b)\n\b\f\b\16\b,\13\b\5\b.\n\b\3\t\3\t\2\2\n\3\3\5\4")
        buf.write('\7\5\t\6\13\7\r\b\17\t\21\n\3\2\5\4\2\13\f""\3\2\63')
        buf.write(";\3\2\62;\2\63\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t")
        buf.write("\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3")
        buf.write("\2\2\2\3\23\3\2\2\2\5\26\3\2\2\2\7\30\3\2\2\2\t\32\3\2")
        buf.write("\2\2\13\34\3\2\2\2\r\37\3\2\2\2\17-\3\2\2\2\21/\3\2\2")
        buf.write("\2\23\24\7*\2\2\24\25\7p\2\2\25\4\3\2\2\2\26\27\7+\2\2")
        buf.write("\27\6\3\2\2\2\30\31\7}\2\2\31\b\3\2\2\2\32\33\7\177\2")
        buf.write("\2\33\n\3\2\2\2\34\35\7<\2\2\35\f\3\2\2\2\36 \t\2\2\2")
        buf.write('\37\36\3\2\2\2 !\3\2\2\2!\37\3\2\2\2!"\3\2\2\2"#\3\2')
        buf.write("\2\2#$\b\7\2\2$\16\3\2\2\2%.\7\62\2\2&*\t\3\2\2')\t\4")
        buf.write("\2\2('\3\2\2\2),\3\2\2\2*(\3\2\2\2*+\3\2\2\2+.\3\2\2")
        buf.write("\2,*\3\2\2\2-%\3\2\2\2-&\3\2\2\2.\20\3\2\2\2/\60\13\2")
        buf.write("\2\2\60\22\3\2\2\2\6\2!*-\3\b\2\2")
        return buf.getvalue()


class KDLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    WS = 6
    NUMBER = 7
    ANY = 8

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>", "'(n'", "')'", "'{'", "'}'", "':'"]

    symbolicNames = ["<INVALID>", "WS", "NUMBER", "ANY"]

    ruleNames = ["T__0", "T__1", "T__2", "T__3", "T__4", "WS", "NUMBER", "ANY"]

    grammarFileName = "KDL.g4"

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(
            self, self.atn, self.decisionsToDFA, PredictionContextCache()
        )
        self._actions = None
        self._predicates = None
