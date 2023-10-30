# PtShell

### Sobre
PtShell é uma linguagem de programação que é uma versão simplificada do Bash com comandos em português. Esta linguagem é destinada a facilitar a automação de tarefas em sistemas Unix-like para falantes de português.

### EBNF
```
COMANDO = DECLARACAO_VARIAVEL | CONDICIONAL | LOOP | IMPRIMIR;
DECLARACAO_VARIAVEL = "declare", IDENTIFICADOR, "=", EXPRESSAO;
CONDICIONAL = "se", EXPRESSAO, "entao", { COMANDO }, "fim";
LOOP = "enquanto", EXPRESSAO, "faca", { COMANDO }, "fim";
IMPRIMIR = "echo", EXPRESSAO;
EXPRESSAO = STRING | NUMERO | IDENTIFICADOR;
IDENTIFICADOR = LETRA, { LETRA | DIGITO | "_" };
STRING = """", { LETRA | DIGITO | ESPACO | "_" }, """";
NUMERO = DIGITO, { DIGITO };
LETRA = "a" | ... | "z" | "A" | ... | "Z";
DIGITO = "0" | ... | "9";
```

### Exemplo

```
declare x = 10
declare y = 5
se x > y entao
  echo "x é maior que y"
fim
enquanto x > 0 faca
  echo x
  declare x = x - 1
fim
```
