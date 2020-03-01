# Generated from ReGex.g4 by ANTLR 4.7.2
from antlr4 import *
from regex import RegEx
if __name__ is not None and "." in __name__:
    from .ReGexParser import ReGexParser
else:
    from ReGexParser import ReGexParser

EMPTY_STRING = 0
SYMBOL_SIMPLE = 1
SYMBOL_ANY = 2
SYMBOL_SET = 3
MAYBE = 4
STAR = 5
PLUS = 6
RANGE = 7
CONCATENATION = 8
ALTERNATION = 9

# This class defines a complete listener for a parse tree produced by ReGexParser.
class ReGexListener(ParseTreeListener):

    # Enter a parse tree produced by ReGexParser#exp.
    def enterExp(self, ctx:ReGexParser.ExpContext):
        pass

    # Exit a parse tree produced by ReGexParser#exp.
    def exitExp(self, ctx:ReGexParser.ExpContext):

        #compute case for each input
        #regex symbol_simple char
        if ctx.CHAR():
        	return RegEx(SYMBOL_SIMPLE, ctx.getText())

        #regex symbol_simple number
        if ctx.NUMBER():
        	return RegEx(SYMBOL_SIMPLE, ctx.getText())

        #regex symbol_any
        if ctx.ANY():
        	return RegEx(SYMBOL_ANY)

        #regex maybe for lhs
        if ctx.MAYBE():
        	expression = self.exitExp(ctx.getChild(0))
        	return RegEx(MAYBE, expression)

        #regex star for lhs
        if ctx.STAR():
        	expression = self.exitExp(ctx.getChild(0))
        	return RegEx(STAR, expression)

        ##regex plus for lhs
        if ctx.PLUS():
        	expression = self.exitExp(ctx.getChild(0))
        	return RegEx(PLUS, expression)

        #cross expression and add char or tuple of chars in set
        if ctx.SET():

            #cross expression and add char or tuple of chars in set
        	text = ctx.getText()
        	set_symbols = set()
        	j = 1

            #cross expression
        	for i in range(1, len(text) - 1):
        		if text[j] != '-':

                    #found tuple of chars
        			if text[j + 1] == '-':
        				set_symbols.add((text[j], text[j + 2]))
        				j = j + 3
        				if j >= (len(text) - 1):
        					break;

                    #found char
        			else:
        				set_symbols.add(text[j])
        				j = j + 1
        				if j >= (len(text) - 1):
        					break
                            
        	return RegEx(SYMBOL_SET, set_symbols)

        if ctx.RANGE():

            #check tuple to identify input case
        	text = ctx.getText()
        	symbol = text[0]

            #min interval = max interval
        	if text.find(",") == -1:
        		number = ord(text[2]) - 48;
        		return RegEx(RANGE, RegEx(SYMBOL_SIMPLE, symbol), (number, number))
        	if text[2] == ',':
        		number = ord(text[3]) - 48;
        		return RegEx(RANGE, RegEx(SYMBOL_SIMPLE, symbol), (-1, number))
        	else:
        		acolada = text.find('}')

                #min interval
        		if text[acolada - 1] == ',':
        			number = ord(text[2]) - 48
        			return RegEx(RANGE, RegEx(SYMBOL_SIMPLE, symbol), (number, -1))

                #normal interval
        		else:
        			acolada1 = text.find('{')
        			acolada2 = text.find('}')
        			virgula = text.find(',')
        			nr1 = 0
        			nr2 = 0

                    #compute min limit
        			for i in range(acolada1 + 1, virgula):
        				temp = ord(text[i]) - 48
        				nr1 = nr1 * 10 + temp

                    #compute max limit
        			for i in range(virgula + 1, acolada2):
        				temp = ord(text[i]) - 48
        				nr2 = nr2 * 10 + temp
        			return RegEx(RANGE, RegEx(SYMBOL_SIMPLE, symbol), (nr1, nr2))

        #alternate lhs and rhs
        if ctx.ALTERNATION():
        	e1 = self.exitExp(ctx.getChild(0))
        	e2 = self.exitExp(ctx.getChild(2))
        	return RegEx(ALTERNATION, e1, e2)

        else:
        	text = ctx.getText()

            #no priority needed before concatenation
        	if text[0] == '(':
        		if text[len(text) - 1] == ')' :
        			return self.exitExp(ctx.getChild(1))
        		else:
        			e1 = self.exitExp(ctx.getChild(1))
        			e2 = self.exitExp(ctx.getChild(3))
        			return RegEx(CONCATENATION, e1, e2)

            #concatenate lhs and rhs
        	e1 = self.exitExp(ctx.getChild(0))
        	e2 = self.exitExp(ctx.getChild(1))
        	return RegEx(CONCATENATION, e1, e2)