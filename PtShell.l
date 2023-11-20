%option noyywrap
%{
#include "PtShell.tab.h"
%}

%x STRING_STATE

%%

"se"                     { return SE; }
"entao"                  { return ENTAO; }
"fim"                    { return FIM; }
"enquanto"               { return ENQUANTO; }
"faca"                   { return FACA; }
"echo"                   { return T_ECHO; }
"="                      { return IGUAL; }
"-"                      { return MENOS; }
">"                      { return MAIOR; }
"<"                      { return MENOR; }
[0-9]+                   { yylval.num = atoi(yytext); return NUMERO; }
[a-zA-Z_][a-zA-Z_0-9]*   { yylval.str = strdup(yytext); return IDENTIFICADOR; }
"\""                     { BEGIN(STRING_STATE); }
<STRING_STATE>{
    \\\"                { /* captura uma aspa dupla escapada */ }
    \\\\                { /* captura uma barra invertida escapada */ }
    [^"\\]+             { /* captura o conteúdo da string */ }
    \"                  { BEGIN(INITIAL); yylval.str = strdup(yytext); return STRING; }
}
<INITIAL>{
    [ \t]+              { /* ignorar espaços em branco */ }
    \n                  { /* ignorar nova linha */ }
    .                   { /* caracteres não reconhecidos */ }
}

%%
