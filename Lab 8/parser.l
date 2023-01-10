%{
	/* Definition Section */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char token[256];
    int st_code;
}PIF;

typedef struct{
    char token[256];
    int index;
}ST;

ST SymbolTable[50];
int st_length = 0;

PIF ProgramInternalForm[200];
int pif_length = 0;

int errorFound = 0;
int lineNumber = 1;


int addToST(char* token) {
	for(int i = 0; i < st_length; i++) {
		
		if(strcmp(SymbolTable[i].token, token) == 0) {
		  return SymbolTable[i].index;
		}
	}
	strcpy(SymbolTable[st_length].token, token);
	SymbolTable[st_length].index = st_length;
	st_length++;
	
	return st_length - 1;
}

void addToPIF(char* token, int stCode) {
	strcpy(ProgramInternalForm[pif_length].token, token);
	ProgramInternalForm[pif_length].st_code = stCode;
	
	pif_length++;
}

void showSymbolTable() {
    printf("---- ST ----\n");
    
    for(int i = 0 ; i < st_length; i++) {
        printf(" %s  %d", SymbolTable[i].token, SymbolTable[i].index);
        printf("\n");
    }
    
    printf("------------\n");
    printf("\n");
}

void showProgramInternalForm() {
    printf("---- PIF ----\n");
    
    for(int i = 0; i < pif_length; i++) {
    
        printf(" %s  %d ", ProgramInternalForm[i].token, ProgramInternalForm[i].st_code);
        printf("\n");
    }
    
    printf("-------------\n");
    printf("\n");
}
%}
	
LETTER [a-zA-Z ]
DIGIT [0-9]
IDENTIFIER @[A-Za-z0-9]+
NUMBER_CONST [+-]?(0|[1-9][0-9]*)(\.[0-9]+)?
STRING_CONST <({LETTER}|{DIGIT})+>
RESERVED_WORD "str"|"nr"|"is"|"check"|"cond"|"yes"|"no"|"display"
OPERATOR " > "|">="|" < "|"<="
SEPARATOR "{"|"}"|"("|")"|"["|"]"|";"|":"
EVERYTHING_ELSE {RESERVED_WORD}|{OPERATOR}|{SEPARATOR}

%%
	/* Rules Section*/	

{EVERYTHING_ELSE} {addToPIF(yytext, -1);}
{IDENTIFIER} {int stCode = addToST(yytext); addToPIF(yytext, stCode);}
{NUMBER_CONST} {int stCode = addToST(yytext); addToPIF(yytext, stCode);}
{STRING_CONST} {int stCode = addToST(yytext); addToPIF(yytext, stCode);}
[\n] { ++lineNumber; }
[ \t\n]+ { ; }
. { errorFound = 1; printf("Illegal token %s at line %d !", yytext, lineNumber); printf("\n"); }
%%

int yywrap() {}

int main(int argc, char** argv) {
	FILE *fp;
	fp = fopen(argv[1], "r");
	yyin = fp;
	yylex();
	if (errorFound == 0) {
    		showSymbolTable();
    		showProgramInternalForm();
	}  
	return 0;
}
