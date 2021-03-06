
grammar cGrammar;

program
	: program functiondecl
	| program function
	| program global_declaration ';'
	| program include_file  
	|
	;

include_file : INCLUDE_FILE;

function : returntype ID '(' initialfunctionargument ')' '{' function_body '}';

functiondecl : returntype ID '(' initialfunctionargument ')' ';';

initialfunctionargument
	: type_argument type_arguments
	| ;
type_arguments
	: ',' type_argument type_arguments
	| ;
type_argument : dec_type OPERATOR_ADDROF? ID;


function_body : statements;


statements 
	: statement statements
	| ;
statement
	: expression ';'
	| declaration ';'
	| assignment ';'
	| ifelse
	| while_loop
	| for_loop
	| break_stmt ';'
	| continue_stmt ';'
	| return_stmt ';'
	| scanf ';'
	| printf ';'
	;


break_stmt : 'break';
continue_stmt : 'continue';
return_stmt : RETURN expression?;

expression
	: add_sub
	| condition
	| rvalue
	;


add_sub
	: add_sub OPERATOR_PLUS add_sub
	| add_sub OPERATOR_MINUS add_sub
	| rvalue_identifier
	| rvalue
	| mul_div
	;

mul_div
	: mul_div OPERATOR_MUL mul_div
	| mul_div OPERATOR_DIV mul_div
	| rvalue_identifier
	| rvalue
	| minus_expr
	;

minus_expr
	: OPERATOR_MINUS minus_expr
	| dereference_expr
	;

dereference_expr
	: OPERATOR_MUL+ dereference_expr
	| OPERATOR_MUL+ rvalue
	| bracket_expression
	;

bracket_expression : LBRACKET expression RBRACKET;


//////////////////////////////////////////////////////////
// If-else stuff and boolean conditions					//
//////////////////////////////////////////////////////////


lvalue_identifier : ID;
rvalue_identifier : ID;

ifelse
	: 'if' '(' condition ')' '{' first_true_statements '}'
	| 'if' '(' condition ')' first_true_statement else_statement
	| 'if' '(' condition ')' '{' first_true_statements '}' else_statement
	| 'if' '(' condition ')' '{' first_true_statements '}' else_statement
	| 'if' '(' condition ')' first_true_statement else_statement
	;

else_statement
	: 'else' first_false_statement
	| 'else' '{' first_false_statements '}'
	| ;

// Hacks to build the AST
firstcondition : condition;
first_true_statements : statements;
first_true_statement : statement;
first_false_statement : statement;
first_false_statements : statements;

condition : condition_or;

condition_or
	: condition_or OPERATOR_OR condition_or
	| condition_and
	| rvalue
	| comparison
	;

condition_and
	: condition_and OPERATOR_AND condition_and
	| condition_not
	| comparison
	| rvalue
	;

condition_not
	: OPERATOR_NOT comparison
	| OPERATOR_NOT rvalue
	| bracket_condition
	;

bracket_condition
	: LBRACKET condition_or RBRACKET
	| OPERATOR_NOT LBRACKET condition_or RBRACKET
	;

comparison : add_sub comparator add_sub;

comparator
	: OPERATOR_EQ
	| OPERATOR_NE
	| OPERATOR_GT
	| OPERATOR_GE
	| OPERATOR_LT
	| OPERATOR_LE
	;

//////////////////////////////////////////////////////////
// While loop stuff 									//
//////////////////////////////////////////////////////////

while_loop
	: 'while' '(' first_while_condition ')' '{' first_while_statements '}'
	| 'while' '(' first_while_condition ')' first_while_statement
	;

// Hacks to build the AST
first_while_statements : statements;
first_while_statement  : statement;
first_while_condition  : condition;


//////////////////////////////////////////////////////////
// For loop stuff 										//
//////////////////////////////////////////////////////////

for_loop
	: 'for' '(' first_stmt_for ';' second_stmt_for ';' third_stmt_for ')' '{' first_for_statements '}'
	| 'for' '(' first_stmt_for ';' second_stmt_for ';' third_stmt_for ')' first_for_statement
	;

// Hacks to build the AST
first_for_statements : statements;
first_for_statement  : statement;
first_stmt_for
	: expression
	| declaration
	| ;

second_stmt_for
	: expression
	| ;

third_stmt_for
	: assignment
	| ;

//////////////////////////////////////////////////////////
// Scanf and Printf										//
//////////////////////////////////////////////////////////

scanf : 'scanf' '(' format_string scanf_call_arguments ')';
printf : 'printf' '(' format_string call_arguments ')';

format_string : STRING;

scanf_call_arguments
	: ',' lvalue scanf_call_arguments 
	| ;

//////////////////////////////////////////////////////////
// Function calls 										//
//////////////////////////////////////////////////////////
functioncall : ID '(' call_argument_initial ')';

call_argument_initial
	: expression call_arguments
	| ;

call_arguments
	: ',' call_argument call_arguments
	| ;

call_argument : expression;



//////////////////////////////////////////////////////////
// Declarations and assignments							//
//////////////////////////////////////////////////////////

declaration 
	: normal_declaration
	| array_declaration
	;

normal_declaration
	: dec_type ID initialization
	| dec_type ID
	;
array_declaration : dec_type ID LSQUAREBRACKET digits RSQUAREBRACKET;

assignment : lvalue OPERATOR_AS expression; // lack of better words

initialization : OPERATOR_AS expression;

global_declaration : declaration;




//////////////////////////////////////////////////////////
// LValues and RValues									//
//////////////////////////////////////////////////////////

lvalue 
	: lvalue_identifier
	| arrayelement_lvalue
	| lvalue_brackets
	| pointer_dereference
	;

lvalue_brackets : LBRACKET lvalue RBRACKET;

rvalue 
	: charvalue
	| numericalvalue 		// NOTE: no differentiation between int value and pointer value, would match the same anyways
	| functioncall
	| arrayelement_rvalue
	| address_value
	| rvalue_identifier
	| true
	| false
	| OPERATOR_MINUS rvalue // Here in order to give priority to rvalue with a minus operator, instead of whole expressions
	;


arrayelement_rvalue : arrayelement;
arrayelement_lvalue : arrayelement;

arrayelement : ID LSQUAREBRACKET expression RSQUAREBRACKET;


charvalue : CHARVALUE;
numericalvalue : floatvalue | intvalue;

intvalue : DIGIT DIGIT*;
floatvalue : digits? '.' digits;


//////////////////////////////////////////////////////////
// Pointers and addresses								//
//////////////////////////////////////////////////////////

address_value : OPERATOR_ADDROF lvalue;

pointer_dereference
	: dereference_bracket
	| OPERATOR_MUL+ expression
	;


dereference_bracket : LBRACKET pointer_dereference RBRACKET;

ptr : '*' ptr | ;


//////////////////////////////////////////////////////////
// Miscellaneous										//
//////////////////////////////////////////////////////////

digits : DIGIT+;
returntype : dec_type | VOID;

dec_type 
	: CHAR ptr
	| FLOAT ptr
	| INT ptr
	| BOOL ptr
	;

true : TRUE;
false : FALSE;


//////////////////////////////////////////////////////////
// Lexer Rules											//
//////////////////////////////////////////////////////////

INCLUDE_MACRO : '#include';
INCLUDE_FILE 
	: INCLUDE_MACRO OPERATOR_LT .*? OPERATOR_GT
	| INCLUDE_MACRO ' '* OPERATOR_LT .*? OPERATOR_GT
	;


LSQUAREBRACKET : '[';
RSQUAREBRACKET : ']';
LBRACKET : '(';
RBRACKET : ')';
CHARVALUE : '\'' . '\'';
RETURN : 'return';


OPERATOR_AS : '=';
OPERATOR_PLUS : '+';
OPERATOR_MINUS : '-';
OPERATOR_DIV : '/';
OPERATOR_MUL : '*';

OPERATOR_EQ : '==';
OPERATOR_NE : '!=';
OPERATOR_GT : '>';
OPERATOR_GE : '>=' | '=>';
OPERATOR_LT : '<';
OPERATOR_LE : '<=' | '=<';

OPERATOR_ADDROF : '&';

OPERATOR_OR : '||' | 'or';
OPERATOR_AND: '&&' | 'and';
OPERATOR_NOT: '!'  | 'not';

VOID : 'void';
CHAR : 'char';
FLOAT : 'float';
INT : 'int';
BOOL: 'bool';

TRUE : 'true';
FALSE : 'false';

DIGIT : [0-9];
NOTZERODIGIT : [1-9];
ID : ([a-zA-Z] | '_') ([a-zA-Z] | [0-9] | '_')*;
POINT : '.';
STRING : '"' .*? '"';

WS : [ \r\t\n]+ -> skip ;

SL_COMMENT : '//' .*? '\n' -> skip;
ML_COMMENT : '/*' (. | '\n')*? '*/' ->skip;
