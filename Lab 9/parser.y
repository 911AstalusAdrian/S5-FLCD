%{
#include<stdio.h>
#include<stdlib.h>
#define YYDEBUG 1
extern FILE *yyin;
%}

%token INT
%token STR
%token IS
%token CHECK
%token COND
%token YES
%token NO
%token PRINT

%token plus
%token minus
%token mul
%token division
%token mod
%token greaterOrEq
%token lessOrEq
%token greaterThan
%token lessThan

%token openCb
%token closedCb
%token openSb
%token closedSb
%token openRb
%token closedRb
%token colon
%token semicolon
%token comma

%token IDENTIFIER
%token NUMBER_CONST
%token STRING_CONST

%start program

%%
program: statement
statement: decl_stmt semicolon | if_stmt semicolon | print_stmt semicolon
decl_stmt: type IDENTIFIER IS NUMBER_CONST
type: INT | STR
if_stmt: CHECK openCb COND colon condition semicolon YES colon statement semicolon NO colon statement semicolon closedCb
print_stmt: PRINT IDENTIFIER | PRINT NUMBER_CONST | PRINT STRING_CONST semicolon
condition: expression relation expression
relation: greaterOrEq | lessOrEq | greaterThan | lessThan
expression: expression plus term | expression minus term | term
term: term mul factor | term division factor | factor
factor:  openRb expression closedRb | IDENTIFIER | NUMBER_CONST
%%

yyerror(char *s)
{	
	printf("%s\n",s);
}
 
int main(int argc, char** argv) {
	FILE *fp;
	fp = fopen(argv[1], "r");
	yyin = fp;
	yylex();
	return 0;
}
