grammar ReGex;

exp : CHAR 
	| ANY
	| NUMBER
	| '(' exp ')' exp
	| '(' exp ')'
	| exp STAR 
	| exp PLUS
	| exp MAYBE 
	| SET 
	| RANGE 
	| exp exp 
	| exp ALTERNATION exp ;

SET : '[' CHAR ']'
	| '[' CHAR '-' CHAR ']'
	| '[' CHAR+ ']'
	| '[' (CHAR '-' CHAR)+ ']'
	| '[' (CHAR | (CHAR '-' CHAR))+ ']';

RANGE : CHAR '{' NUMBER '}'
	| CHAR '{' ',' NUMBER '}'
	| CHAR '{' NUMBER ',' '}'
	| CHAR '{' NUMBER ',' NUMBER '}';

STAR : '*' ;
PLUS : '+' ;
MAYBE : '?' ;
ALTERNATION : '|' ;
ANY : '.';
NUMBER : [0-9]+;
CHAR : [a-zA-Z0-9] | [0-9]+ | '0' ;
WS : [ \t\r\n]+ -> skip;