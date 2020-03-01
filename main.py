#!/usr/bin/env python
import sys
import pickle

from antlr4 import *
from ReGexLexer import ReGexLexer
from ReGexParser import ReGexParser
from ReGexListener import ReGexListener
from regular_expression import RegularExpression
from regex import RegEx
from nfa import NFA
from dfa import DFA

EMPTY_SET = 0
EMPTY_STRING = 1
SYMBOL = 2
STAR = 3
CONCATENATION = 4
ALTERNATION = 5

_SIMPLE_TYPES = {EMPTY_SET, EMPTY_STRING, SYMBOL}


def alphabet():

	#create ER equivalent to "."
	pool = "bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	e = RegularExpression(SYMBOL, "a")
	for c in pool:
		e = RegularExpression(ALTERNATION, e, RegularExpression(SYMBOL, c))
	return e

def rangeAlphabet(expression, tuple):

	#create ER equivalent to apparition of exp "tuple" of times
	e = expression
	rez = RegularExpression(EMPTY_STRING)

	#exact interval : minlimit_interval == maxlimit_interval
	if tuple[0] == tuple[1]:
		rez = expression
		for i in range (1, tuple[0]):
			e = RegularExpression(CONCATENATION, e, expression)
		return e

	#min interval : minlimit_interval == -1
	elif tuple[0] == -1:
		rez = RegularExpression(ALTERNATION, rez, e)

		#create concatenation of exp by maxlim_interval times, starting from  minlim_interval
		for i in range (1, tuple[1]):
			e = RegularExpression(CONCATENATION, e, expression)
			rez = RegularExpression(ALTERNATION, rez, e)

	#max interval : max_limit interval == -1
	elif tuple[1] == -1:

		#create concatenation of exp by maxlim_interval times, starting from  minlim_interval
		for i in range (1, tuple[0]):
			e = RegularExpression(CONCATENATION, e, expression)
		rez = RegularExpression(CONCATENATION, e, RegularExpression(STAR,expression))

	#normal interval 
	else:

		#create concatenation of exp by maxlim_interval times, starting from  minlim_interval
		for i in range (1, tuple[0]):
			e = RegularExpression(CONCATENATION, e, expression)
		rez = e

		#add concatenation cases to reunion
		for i in range (tuple[0], tuple[1]):
			e = RegularExpression(CONCATENATION, e, expression)
			rez = RegularExpression(ALTERNATION, rez, e)
	return rez
	
	

def setAlph(interval):

	#create ER equivalent to reunion of chars in set, or in the range sugested by tuples of chars
	pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	fst = 0
	for elem in interval:

		#first elem of range case
		if fst == 0:
			fst = fst + 1

			#elem in range of chars
			if type(elem) is tuple:
				e = RegularExpression(SYMBOL, elem[0])
				for c in range(pool.find(elem[0]) + 1, pool.find(elem[1]) + 1):
					e = RegularExpression(ALTERNATION, e, RegularExpression(SYMBOL, pool[c]))

			#elem is one char
			else:
				e = RegularExpression(SYMBOL, elem)

		else:
			#elem in range of chars
			if type(elem) is tuple:
				for c in range(pool.find(elem[0]), pool.find(elem[1]) + 1):
					e = RegularExpression(ALTERNATION, e, RegularExpression(SYMBOL, pool[c]))

			#elem is one char
			else:
					e = RegularExpression(ALTERNATION, e, RegularExpression(SYMBOL, elem))			
	return e

def converRegToEr(expression):

	#EMPTY_STRING
	if expression.type == 0:
		return RegularExpression(EMPTY_STRING)

	#SYMBOL_SIMPLE
	if expression.type == 1:
		return RegularExpression(SYMBOL, expression.symbol)

	#SYMBOL_ANY
	if expression.type == 2:
		return alphabet()

	#SYMBOL_SET
	if expression.type == 3:
		return setAlph(expression.symbol_set)

	#MAYBE
	if expression.type == 4:
		return RegularExpression(ALTERNATION,RegularExpression(EMPTY_STRING), converRegToEr(expression.lhs))

	#STAR
	if expression.type == 5:
		return RegularExpression(STAR, converRegToEr(expression.lhs))

	#PLUS
	if expression.type == 6:
		return RegularExpression(CONCATENATION,converRegToEr(expression.lhs), RegularExpression(STAR, converRegToEr(expression.lhs)))

	#RANGE
	if expression.type == 7:
		return rangeAlphabet(converRegToEr(expression.lhs), expression.range)

	#CONCATENATION
	if expression.type == 8:
		return RegularExpression(CONCATENATION, converRegToEr(expression.lhs), converRegToEr(expression.rhs))

	#ALTERNATION
	elif expression.type == 9:
		return RegularExpression(ALTERNATION, converRegToEr(expression.lhs), converRegToEr(expression.rhs))

def rename_states(target, reference):
    off = max(reference.states) + 1
    target.start_state += off
    target.states = set(map(lambda s: s + off, target.states))
    target.final_states = set(map(lambda s: s + off, target.final_states))
    new_delta = {}
    for (state, symbol), next_states in target.delta.items():
        new_next_states = set(map(lambda s: s + off, next_states))
        new_delta[(state + off, symbol)] = new_next_states

    target.delta = new_delta


def new_states(*nfas):
    state = 0
    for nfa in nfas:
        m = max(nfa.states)
        if m >= state:
            state = m + 1

    return state, state + 1

def reToNfa(expression):

	#build nfa from expression
	alfabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	#base case : empty set
	if expression.type == EMPTY_SET:
		return NFA(alfabet, {0, 1}, 0, {1}, {})

	#base case : empty string
	elif expression.type == EMPTY_STRING:
		return NFA(alfabet, {0, 1}, 0, {1}, {(0, "ε"): {1}})

	#base case : one char
	elif expression.type == SYMBOL:
		return NFA(alfabet, {0, 1}, 0, {1}, {(0, expression.symbol ): {1}})

	#case concatenate
	elif expression.type == CONCATENATION:
		lhs_nfa = reToNfa(expression.lhs)
		rhs_nfa = reToNfa(expression.rhs)
		rename_states(lhs_nfa, rhs_nfa)
		st1, st2 = new_states(lhs_nfa, rhs_nfa)
		automata = {(st1, "ε"): {lhs_nfa.start_state},
					(list(rhs_nfa.final_states)[0], "ε"): {st2},
					(list(lhs_nfa.final_states)[0], "ε"): {rhs_nfa.start_state}}
		automata.update(lhs_nfa.delta)
		automata.update(rhs_nfa.delta)
		return NFA(alfabet, {st1, st2} | lhs_nfa.states | rhs_nfa.states, st1, {st2}, automata)

	#case alternate
	elif expression.type == ALTERNATION:
		lhs_nfa = reToNfa(expression.lhs)
		rhs_nfa = reToNfa(expression.rhs)
		rename_states(lhs_nfa, rhs_nfa)
		st1, st2 = new_states(lhs_nfa, rhs_nfa)
		automata = {(st1, "ε"): {lhs_nfa.start_state, rhs_nfa.start_state},
					(list(rhs_nfa.final_states)[0], "ε"): {st2},
					(list(lhs_nfa.final_states)[0], "ε"): {st2}}
		automata.update(lhs_nfa.delta)
		automata.update(rhs_nfa.delta)
		return NFA(alfabet, {st1, st2} | lhs_nfa.states | rhs_nfa.states, st1, {st2}, automata)

	#case Kleene Star
	elif expression.type == STAR:
		lhs_nfa = reToNfa(expression.lhs)
		st1, st2 = new_states(lhs_nfa)
		automata = {(st1, "ε"): {lhs_nfa.start_state, st2},
					(list(lhs_nfa.final_states)[0], "ε"): {lhs_nfa.start_state, st2}}
		automata.update(lhs_nfa.delta)
		return NFA(alfabet, {st1, st2} | lhs_nfa.states, st1, {st2}, automata)

def getEpsilonClosuresState(s, nfa):

	#return ε-Closures for state "s"
	statesEpsilon = set()
	#create visited vector to avoid getting stuck in loops
	visited = [False for i in range(0, len(nfa.states) + 1)]
	stack = []
	stack.append(s)

	while(len(stack)):
		s = stack[-1]
		stack.pop()

		#check to see if state was already visited
		if(not visited[s]):
			visited[s] = True
			statesEpsilon.add(s)

		#check states reachable through "ε" transitions from new state
		for elem in nfa.delta.keys():
			if elem[0] == s:
				if elem[1] == "ε":
					nodes = nfa.delta.get(elem)
					for node in  nodes:
						if(not visited[node]):
							stack.append(node)
	return statesEpsilon

def getEpsilonClosuresStates(setStates, nfa):

	#return union of ε-Closures for states that are in set 
	statesEpsilon = set()
	for s in setStates:
		temp = getEpsilonClosuresState(s, nfa)
		statesEpsilon.update(temp)
	return tuple(list(statesEpsilon))

def move(delta, T, char):

	#create tuple of states reachable from T by c transitions
	statesReachable = set()
	for state in T:
		for elem in delta.keys():
			if elem[0] == state:
				if elem[1] == char:
					nodes = delta.get(elem)
					for node in  nodes:
						statesReachable.add(node)
	return tuple(list(statesReachable))

def check(word, dfa):

	#check if word is acceped by dfa
	state = dfa.start_state

	#check to find transitions from current state by current char
	for j in range(0, len(word) - 1):
		c = word[j]
		found = 0
		for elem in dfa.delta.keys():
			if elem[0] == state:
				if elem[1] == c:
					found = 1
					temp = dfa.delta.get((state, c))
		if found == 0:
			return False
		else:
			state = temp

	#check to see if we've ended on a final state or not
	if state in dfa.final_states:
		return True
	else:
		return False


def nfaToDfa(nfa):
	statesDfa = set()
	unmarked = set()
	neWDelta = {}
	newFinalStates = set()

	#get ε closures for start_state
	eS = getEpsilonClosuresState(nfa.start_state, nfa)
	#set eS as the start state for the DFA
	newStartState = tuple(list(eS))
	#add eS to states of DFA
	statesDfa.add(tuple(list(eS)))
	#set eS as unmarked by adding it to the set
	unmarked.add(tuple(list(eS)))
	#append state to stack
	stack = []
	stack.append(tuple(list(eS)))

	while(len(stack)):
		T = stack[-1]
		stack.pop()

		#check to see if state is visited
		if T in unmarked:
			unmarked.remove(T)
		for char in nfa.alphabet:

			#get "ε"-Closure for each state of set
			S = getEpsilonClosuresStates(move(nfa.delta, T, char), nfa)
			if len(S) != 0 :
				if S not in statesDfa:
					statesDfa.add(tuple(list(S)))
					unmarked.add(tuple(list(S)))
					stack.append(tuple(list(S)))
				neWDelta[(T, char)] = S

	#create final states for dfa
	for S in statesDfa:
		for st in S:
			if st in nfa.final_states:
				newFinalStates.add(S)
				break

	return DFA(nfa.alphabet, statesDfa, newStartState, newFinalStates, neWDelta)


if __name__ == "__main__":
    valid = (len(sys.argv) == 4 and sys.argv[1] in ["RAW", "TDA"]) or \
            (len(sys.argv) == 3 and sys.argv[1] == "PARSE")
    if not valid:
        sys.stderr.write(
            "Usage:\n"
            "\tpython3 main.py RAW <regex-str> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py TDA <tda-file> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py PARSE <regex-str>\n"
        )
        sys.exit(1)

    if sys.argv[1] == "TDA":
        tda_file = sys.argv[2]
        with open(tda_file, "rb") as fin:
            parsed_regex = pickle.loads(fin.read())
    else:
        regex_string = sys.argv[2]

        tree = ReGexParser(CommonTokenStream(ReGexLexer(InputStream(regex_string)))).exp()
        parsed_regex = (ReGexListener()).exitExp(tree)

        if sys.argv[1] == "PARSE":
            print(str(parsed_regex))
            sys.exit(0)

    #convert to ER
    regularExpression = converRegToEr(parsed_regex)
    #construct NFA fro ER
    nfaFromEr = reToNfa(regularExpression)
    #convert NFA to DFA
    dfaFromEr = nfaToDfa(nfaFromEr)

    with open(sys.argv[3], "r") as fin:
        content = fin.readlines()

    for word in content:

    	#check each word from file
        print(check(word, dfaFromEr))
        pass
