%{
#include <stdio.h>
#include <stdlib.h>
#include "PtShell.tab.h" // Este inclui os protótipos de função e definições do Bison

void yyerror(const char *s);
extern int yylex(); // Declaração externa para o yylex
%}

%union {
    int num;
    char *str;
}

%token <num> NUMERO
%token <str> IDENTIFICADOR STRING
%token SE ENTAO FIM ENQUANTO FACA ECHO IGUAL MENOS MAIOR
%token T_ECHO

%type <num> expressao_logica
%type <num> expressao
%type <str> comando

%nonassoc MENOR MAIOR IGUAL DIFERENTE MENOR_IGUAL MAIOR_IGUAL
%left '+' '-'
%left '*' '/'
%left E_LOGICO OU_LOGICO


%%

programa:
    | programa comando
    ;

comando:
      IDENTIFICADOR IGUAL expressao         { /* código para atribuição */ }
    | SE expressao_logica ENTAO comandos FIM { /* código para condicional */ }
    | ENQUANTO expressao_logica FACA comandos FIM { /* código para loop */ }
    | T_ECHO expressao                         { /* código para imprimir */ }
    ;

comandos:
    | comandos comando
    ;

expressao:
      NUMERO                                 { /* código para número */ }
    | STRING                                 { /* código para string */ }
    | IDENTIFICADOR                          { /* código para variável */ }
    | expressao '+' expressao                { /* código para adição */ }
    | expressao '-' expressao                { /* código para subtração */ }
    | expressao '*' expressao                { /* código para multiplicação, se necessário */ }
    | expressao '/' expressao                { /* código para divisão, se necessário */ }
    ;


expressao_logica:
      expressao MAIOR expressao             { /* código para maior que */ }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
}

int main(void) {
    yyparse();
    return 0;
}
