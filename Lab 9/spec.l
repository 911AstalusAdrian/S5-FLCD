%{
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include "parser.tab.h"
int lineNumber = 1;
%}

%option noyywrap

LETTER [a-zA-z ]
DIGIT[0-9]
IDENTIFIER @[a-zA-Z0-9]+
NUMBER_CONST [+-]?(0|[1-9][0-9]*)(\.[0-9]+)?
STRING_CONST <({LETTER}|{DIGIT})+>

%%
"nr"		{printf("Reserved word: %s\n", yytext); return INT;}
"str"		{printf("Reserved word: %s\n", yytext); return STR;}
"is"		{printf("Reserved word: %s\n", yytext); return IS;}
"check"		{printf("Reserved word: %s\n", yytext); return CHECK;}
"cond"		{printf("Reserved word: %s\n", yytext); return COND;}
"yes"		{printf("Reserved word: %s\n", yytext); return YES;}
"no"		{printf("Reserved word: %s\n", yytext); return NO;}
"display"	{printf("Reserved word: %s\n", yytext); return PRINT;}

"+"			{printf("Operator %s\n", yytext); return plus;}
"-"			{printf("Operator %s\n", yytext); return minus;}
"*"			{printf("Operator %s\n", yytext); return mul;}
"/"			{printf("Operator %s\n", yytext); return division;}
"%"			{printf("Operator %s\n", yytext); return mod;}
">="		{printf("Operator: %s\n", yytext); return greaterOrEq;}
"<="		{printf("Operator: %s\n", yytext); return lessOrEq;}
"/>"		{printf("Operator: %s\n", yytext); return greaterThan;}
"/<"		{printf("Operator: %s\n", yytext); return lessThan;}

"{"			{printf("Separator: %s\n", yytext); return openCb;}
"}"			{printf("Separator: %s\n", yytext); return closedCb;}
"["			{printf("Separator: %s\n", yytext); return openSb;}
"]"			{printf("Separator: %s\n", yytext); return closedSb;}
"("			{printf("Separator: %s\n", yytext); return openRb;}
")"			{printf("Separator: %s\n", yytext); return closedRb;}
":"			{printf("Separator: %s\n", yytext); return colon;}
";"			{printf("Separator: %s\n", yytext); return semicolon;}
","			{printf("Separator: %s\n", yytext); return comma;}


{IDENTIFIER} {printf("Identifier: %s\n", yytext); return IDENTIFIER;}
{NUMBER_CONST} {printf("Number: %s\n", yytext); return NUMBER_CONST;}
{STRING_CONST} {printf("String: %s\n", yytext); return STRING_CONST;}
[\n] { ++lineNumber; }
[ \t\n]+ { ; }
. { printf("Illegal token %s at line %d !", yytext, lineNumber); printf("\n"); }
%%
