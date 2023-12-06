# PtShell

### Sobre
PtShell é uma linguagem de programação que é uma versão simplificada do Bash com comandos em português. Esta linguagem é destinada a facilitar a automação de tarefas em sistemas Unix-like para falantes de português.

### EBNF
```
COMANDO = DECLARACAO_VARIAVEL | CONDICIONAL | LOOP | IMPRIMIR;
DECLARACAO_VARIAVEL = IDENTIFICADOR, EXPRESSAO;
CONDICIONAL = "se", EXPRESSAO_LOGICA, "entao", { COMANDO }, "fim";
LOOP = "enquanto", EXPRESSAO_LOGICA, "faca", { COMANDO }, "fim";
IMPRIMIR = "echo", EXPRESSAO;
EXPRESSAO = STRING | NUMERO | IDENTIFICADOR | EXPRESSAO_LOGICA;
EXPRESSAO_LOGICA = EXPRESSAO, OPERADOR_LOGICO, EXPRESSAO;
IDENTIFICADOR = LETRA, { LETRA | DIGITO | "_" };
STRING = """", { LETRA | DIGITO | ESPACO | "_" | SIMBOLOS }, """";
NUMERO = DIGITO, { DIGITO };
OPERADOR_LOGICO = ">" | "<" | "==" | "!=" | ">=" | "<=" | "&&" | "||";
LETRA = "a" | ... | "z" | "A" | ... | "Z";
DIGITO = "0" | ... | "9";
ESPACO = " ";
SIMBOLOS = "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")";
```

### Exemplo

```
var num x = 10
var num y = 5
se x > y entao
  echo(x > y)
fim
enquanto x >= 0 faca
  echo(x)
  x = x - 1
fim
```
