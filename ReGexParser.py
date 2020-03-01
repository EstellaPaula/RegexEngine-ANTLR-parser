# Generated from ReGex.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\16")
        buf.write("&\4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\5\2\24\n\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\7\2!\n\2\f\2\16\2$\13\2\3\2\2\3\2\3")
        buf.write("\2\2\2\2/\2\23\3\2\2\2\4\5\b\2\1\2\5\24\7\r\2\2\6\24\7")
        buf.write("\13\2\2\7\24\7\f\2\2\b\t\7\3\2\2\t\n\5\2\2\2\n\13\7\4")
        buf.write("\2\2\13\f\5\2\2\13\f\24\3\2\2\2\r\16\7\3\2\2\16\17\5\2")
        buf.write("\2\2\17\20\7\4\2\2\20\24\3\2\2\2\21\24\7\5\2\2\22\24\7")
        buf.write("\6\2\2\23\4\3\2\2\2\23\6\3\2\2\2\23\7\3\2\2\2\23\b\3\2")
        buf.write("\2\2\23\r\3\2\2\2\23\21\3\2\2\2\23\22\3\2\2\2\24\"\3\2")
        buf.write("\2\2\25\26\f\4\2\2\26!\5\2\2\5\27\30\f\3\2\2\30\31\7\n")
        buf.write("\2\2\31!\5\2\2\4\32\33\f\t\2\2\33!\7\7\2\2\34\35\f\b\2")
        buf.write("\2\35!\7\b\2\2\36\37\f\7\2\2\37!\7\t\2\2 \25\3\2\2\2 ")
        buf.write("\27\3\2\2\2 \32\3\2\2\2 \34\3\2\2\2 \36\3\2\2\2!$\3\2")
        buf.write("\2\2\" \3\2\2\2\"#\3\2\2\2#\3\3\2\2\2$\"\3\2\2\2\5\23")
        buf.write(" \"")
        return buf.getvalue()


class ReGexParser ( Parser ):

    grammarFileName = "ReGex.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "<INVALID>", "<INVALID>", 
                     "'*'", "'+'", "'?'", "'|'", "'.'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "SET", "RANGE", 
                      "STAR", "PLUS", "MAYBE", "ALTERNATION", "ANY", "NUMBER", 
                      "CHAR", "WS" ]

    RULE_exp = 0

    ruleNames =  [ "exp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    SET=3
    RANGE=4
    STAR=5
    PLUS=6
    MAYBE=7
    ALTERNATION=8
    ANY=9
    NUMBER=10
    CHAR=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ExpContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHAR(self):
            return self.getToken(ReGexParser.CHAR, 0)

        def ANY(self):
            return self.getToken(ReGexParser.ANY, 0)

        def NUMBER(self):
            return self.getToken(ReGexParser.NUMBER, 0)

        def exp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ReGexParser.ExpContext)
            else:
                return self.getTypedRuleContext(ReGexParser.ExpContext,i)


        def SET(self):
            return self.getToken(ReGexParser.SET, 0)

        def RANGE(self):
            return self.getToken(ReGexParser.RANGE, 0)

        def ALTERNATION(self):
            return self.getToken(ReGexParser.ALTERNATION, 0)

        def STAR(self):
            return self.getToken(ReGexParser.STAR, 0)

        def PLUS(self):
            return self.getToken(ReGexParser.PLUS, 0)

        def MAYBE(self):
            return self.getToken(ReGexParser.MAYBE, 0)

        def getRuleIndex(self):
            return ReGexParser.RULE_exp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExp" ):
                listener.enterExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExp" ):
                listener.exitExp(self)



    def exp(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ReGexParser.ExpContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_exp, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                self.state = 3
                self.match(ReGexParser.CHAR)
                pass

            elif la_ == 2:
                self.state = 4
                self.match(ReGexParser.ANY)
                pass

            elif la_ == 3:
                self.state = 5
                self.match(ReGexParser.NUMBER)
                pass

            elif la_ == 4:
                self.state = 6
                self.match(ReGexParser.T__0)
                self.state = 7
                self.exp(0)
                self.state = 8
                self.match(ReGexParser.T__1)
                self.state = 9
                self.exp(9)
                pass

            elif la_ == 5:
                self.state = 11
                self.match(ReGexParser.T__0)
                self.state = 12
                self.exp(0)
                self.state = 13
                self.match(ReGexParser.T__1)
                pass

            elif la_ == 6:
                self.state = 15
                self.match(ReGexParser.SET)
                pass

            elif la_ == 7:
                self.state = 16
                self.match(ReGexParser.RANGE)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 32
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 30
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = ReGexParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 19
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 20
                        self.exp(3)
                        pass

                    elif la_ == 2:
                        localctx = ReGexParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 21
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 22
                        self.match(ReGexParser.ALTERNATION)
                        self.state = 23
                        self.exp(2)
                        pass

                    elif la_ == 3:
                        localctx = ReGexParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 24
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 25
                        self.match(ReGexParser.STAR)
                        pass

                    elif la_ == 4:
                        localctx = ReGexParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 26
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 27
                        self.match(ReGexParser.PLUS)
                        pass

                    elif la_ == 5:
                        localctx = ReGexParser.ExpContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_exp)
                        self.state = 28
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 29
                        self.match(ReGexParser.MAYBE)
                        pass

             
                self.state = 34
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.exp_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def exp_sempred(self, localctx:ExpContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         




