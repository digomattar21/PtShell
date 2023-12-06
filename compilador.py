from abc import abstractmethod
import sys


class SymbolTable():
    
    symbol_table = {}

    def getter(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        else:
            raise TypeError("Error, variavel não declarada")
        
    def setter(self, identifier, value):
        if value[0] == self.symbol_table[identifier][0]:
            if identifier in self.symbol_table:
                self.symbol_table[identifier] = value
            else:
                raise TypeError("Error, variavel não declarada")
        else:
            raise TypeError("Error, tipo do valor não é compativel com o tipo da variavel")
    
    def  create(self, identifier, type):
        if identifier in self.symbol_table:
            raise TypeError("Error, variavel já declarada")
        else:
            # Criando o valor enviado
            self.symbol_table[identifier] = (type, None)

class PrePro():
    def filter(code):
        code = code.split("\n")
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i].split("//")[0]
        code = "\n".join(code)
        return code

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self, st):
        pass

class BinOp(Node):
    def Evaluate(self, st):
        left = self.children[0].Evaluate(st)
        right = self.children[1].Evaluate(st)
        if self.value == '+' and left[0] == right[0] and left[0] == "int":
            return ("int", left[1] + right[1])
        elif self.value == '-' and left[0] == right[0] and left[0] == "int":
            return ("int", left[1] - right[1])
        elif self.value == '*' and left[0] == right[0] and left[0] == "int":
            return ("int", left[1] * right[1])
        elif self.value == '/' and left[0] == right[0] and left[0] == "int":
            return ("int", left[1] // right[1])
        elif self.value == '==' and left[0] == right[0]:
            return ("int", int(left[1] == right[1]))
        elif self.value == '>' and left[0] == right[0]:
            return ("int", int(left[1] > right[1]))
        elif self.value == '<' and left[0] == right[0]:
            return ("int", int(left[1] < right[1]))
        elif self.value == '&&' and left[0] == right[0] and left[0] == "int":
            return ("int", int(left[1] and right[1]))
        elif self.value == '||' and left[0] == right[0] and left[0] == "int":
            return (int, int(left[1] or right[1]))
        elif self.value == '!=' and left[0] == right[0]:
            return ("int", int(left[1] != right[1]))
        elif self.value == '>=' and left[0] == right[0]:
            return ("int", int(left[1] >= right[1]))
        elif self.value == '<=' and left[0] == right[0]:
            return ("int", int(left[1] <= right[1]))

class UnOp(Node):
    def Evaluate(self, st):
        left = self.children[0].Evaluate(st)
        if self.value == "+" and left[0] == "int":
            return ("int", left[1])
        elif self.value == "-" and left[0] == "int":
            return ("int", -left[1])
        elif self.value == "!" and left[0] == "int":
            return ("int", int(not left[1]))
        
class IntVal(Node):
    def Evaluate(self, st):
        return ("int", self.value)
    
class Identifier(Node):
    def Evaluate(self, st):
        return st.getter(self.value)
    
class NoOp(Node):
    def Evaluate(self, st):
        pass

class Print(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st)[1])

class Conditional(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)

class For(Node):
    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[1]:
            self.children[1].Evaluate(st)

class Block(Node):
    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class Assingnment(Node):
    def Evaluate(self, st):
        filho = self.children[1].Evaluate(st)
        st.setter(self.children[0].value, filho)

class VarDec(Node):
    def Evaluate(self, st):
        if len(self.children) == 2:
            st.create(self.children[0].value, self.value)
            st.setter(self.children[0].value, self.children[1].Evaluate(st))
        else:
            st.create(self.children[0].value, self.value)

class StringVal(Node):
    def Evaluate(self, st):
        return ("str", self.value)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:

    RESERVED = ["echo", "se", "entao", "enquanto", "faca", "num", "var", "ltr", "fim"]
    
    def __init__(self, source : str):
        self.source = source
        self.position = 0
        self.next = None
    
    def select_next(self):

            if self.position == len(self.source):
                self.next = Token("EOF", "")

            elif self.source[self.position].isdigit():
                numero = ""
                while  self.position < len(self.source) and self.source[self.position].isdigit():
                    numero += self.source[self.position]
                    self.position += 1

                self.next = Token("INT", int(numero))
            
            elif self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "(":
                self.next = Token("OPEN", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == ")":
                self.next = Token("CLOSE", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("COMPARE", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUAL", self.source[self.position])
                    # Atualiza a ponteiro
                    self.position += 1
            
            elif self.source[self.position] == "\n":
                self.next = Token("NEWLINE", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == ";":
                self.next = Token("SEMICOLON", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "|":
                if self.source[self.position+1] == "|":
                    self.next = Token("OR", "||")
                    self.position += 2
                else:
                    raise ValueError(f"Error")
            
            elif self.source[self.position] == "&":
                if self.source[self.position+1] == "&":
                    self.next = Token("AND", "&&")
                    self.position += 2
                else:
                    raise ValueError(f"Error")
                
            elif self.source[self.position] == "!":
                if self.source[self.position+1] == "=":
                    self.next = Token("NOTEQUAL", "!=")
                    self.position += 2
                else:
                    self.next = Token("NOT", self.source[self.position])
                    self.position += 1

            elif self.source[self.position] == ">":
                if self.source[self.position+1] == "=":
                    self.next = Token("GREATEREQUAL", ">=")
                    self.position += 2
                else:
                    self.next = Token("GREATER", self.source[self.position])
                    self.position += 1

            elif self.source[self.position] == "<":
                if self.source[self.position+1] == "=":
                    self.next = Token("LESSEQUAL", "<=")
                    self.position += 2
                else:
                    self.next = Token("LESS", self.source[self.position])
                    self.position += 1

            elif self.source[self.position] == '"':
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != '"':
                    string += self.source[self.position]
                    self.position += 1
                if self.source[self.position] == '"':
                    self.position += 1
                    self.next = Token("STRING", string)
                else:
                    raise ValueError(f"Error, caractere {self.source[self.position]} não reconhecido na posição {self.position}")
                
            elif self.source[self.position].isalpha():
                identificador = ""
                while  self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    identificador += self.source[self.position]
                    self.position += 1
                
                if identificador in Tokenizer.RESERVED:
                    if(identificador == "echo" ):
                        self.next = Token("ECHO", identificador)
                    elif(identificador == "se"):
                        self.next = Token("SE", identificador)
                    elif(identificador == "entao"):
                        self.next = Token("ENTAO", identificador)
                    elif(identificador == "enquanto"):
                        self.next = Token("ENQUANTO", identificador)
                    elif(identificador == "faca"):
                        self.next = Token("FACA", identificador)
                    elif(identificador == "var"):
                        self.next = Token("VAR", identificador)
                    elif(identificador == "num"):
                        self.next = Token("TYPE", "int")
                    elif(identificador == "ltr"):
                        self.next = Token("TYPE", "str")
                    elif(identificador == "fim"):
                        self.next = Token("FIM", identificador)
                else:
                    self.next = Token("IDENT", identificador)

            elif self.source[self.position].isspace():
                self.position += 1
                self.select_next()

            else:
                raise ValueError(f"Error no caracter")
    
class Parser:
    tokenizer = None

    def parse_program():
        resultado = Block("Block", [])
        while Parser.tokenizer.next.type != "EOF":
            resultado.children.append(Parser.parse_statement())
        return resultado
    
    def parse_statement():

        # \n
        if Parser.tokenizer.next.type == "NEWLINE":
            Parser.tokenizer.select_next()
            return NoOp("NoOp", [])
        
        # Variavel
        elif Parser.tokenizer.next.type == "IDENT":
            identificador = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.select_next()
                resultado = Assingnment("=", [identificador, Parser.parse_bool_expression()])
                if Parser.tokenizer.next.type == "NEWLINE":
                    Parser.tokenizer.select_next()
                    return resultado
                else:
                    raise TypeError("Error")
            else:
                raise TypeError("Error") 
        
        # Print
        elif Parser.tokenizer.next.type == "ECHO":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "OPEN":
                Parser.tokenizer.select_next()
                resultado = Print("Print", [Parser.parse_bool_expression()])
                if Parser.tokenizer.next.type == "CLOSE":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.select_next()
                        return resultado
                    else:
                        raise TypeError("Error")
                else:
                    raise TypeError("Error")
            else:
                raise TypeError("Error")
        
        # Se
        elif Parser.tokenizer.next.type == "SE":
            # Consome o if
            Parser.tokenizer.select_next()
            # Cria nó condicional com o primeiro filho sendo a condicao
            resultado = Conditional("se", [Parser.parse_bool_expression()])
            # Cria segundo filho que é o bloco
            resultado.children.append(Parser.parse_block())
            # Verifica se tem \n
            if Parser.tokenizer.next.type == "NEWLINE":
                # Consome o \n
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Error")
        
        # Enquanto
        elif Parser.tokenizer.next.type == "ENQUANTO":
            Parser.tokenizer.select_next()
            resultado = For("enquanto", [])
            resultado.children.append(Parser.parse_bool_expression())
            resultado.children.append(Parser.parse_block())
            if Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Error")
        
        # Declara variavel
        elif Parser.tokenizer.next.type == "VAR":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "TYPE":
                tipo = Parser.tokenizer.next.value
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "IDENT":
                    identificador = Identifier(Parser.tokenizer.next.value, [])
                    Parser.tokenizer.select_next()
                    resultado = VarDec(tipo, [identificador])
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.select_next()
                        resultado.children.append(Parser.parse_bool_expression())
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.select_next()
                        return resultado
                    else:
                        raise TypeError("Error")
                else:
                    raise TypeError("Error")
            else:
                raise TypeError("Error")
        else:
            raise TypeError("Error")
        
    
    def parse_assingnment():

        if Parser.tokenizer.next.type == "IDENT":
            identificador = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.select_next()
                resultado = Assingnment("=", [identificador, Parser.parse_bool_expression()])
                return resultado
            else:
                raise TypeError("Error")
        else:
            raise TypeError("Error")
   
    def parse_block():
        resultado = Block("Block", [])
        if Parser.tokenizer.next.type == "ENTAO" or Parser.tokenizer.next.type == "FACA":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.select_next()
                while Parser.tokenizer.next.type != "FIM":
                    resultado.children.append(Parser.parse_statement())
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Error")
        else:
            raise TypeError("Error")
        
    def parse_bool_expression():
        resultado = Parser.parse_bool_term()

        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.select_next()
            resultado = BinOp("||", [resultado, Parser.parse_bool_term()])
        return resultado

    def parse_bool_term():
        resultado = Parser.parse_rel_expression()

        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.select_next()
            resultado = BinOp("&&", [resultado, Parser.parse_rel_expression()])
        return resultado


    def parse_rel_expression():
        resultado = Parser.parse_expression()

        while Parser.tokenizer.next.type == "GREATER" or Parser.tokenizer.next.type == "LESS" or Parser.tokenizer.next.type == "COMPARE" or Parser.tokenizer.next.type == "GREATEREQUAL" or Parser.tokenizer.next.type == "LESSEQUAL" or Parser.tokenizer.next.type == "NOTEQUAL":
            if Parser.tokenizer.next.type == "GREATER":
                Parser.tokenizer.select_next()
                resultado = BinOp(">", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "LESS":
                Parser.tokenizer.select_next()
                resultado = BinOp("<", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "COMPARE":
                Parser.tokenizer.select_next()
                resultado = BinOp("==", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "GREATEREQUAL":
                Parser.tokenizer.select_next()
                resultado = BinOp(">=", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "LESSEQUAL":
                Parser.tokenizer.select_next()
                resultado = BinOp("<=", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "NOTEQUAL":
                Parser.tokenizer.select_next()
                resultado = BinOp("!=", [resultado, Parser.parse_expression()])

        return resultado
    
    def parse_expression():
        resultado = Parser.parse_term()

        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "CONCAT":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                resultado = BinOp("+", [resultado, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                resultado = BinOp("-", [resultado, Parser.parse_term()])

        return resultado
    
    def parse_term():
        resultado = Parser.parse_factor()

        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.select_next()
                resultado = BinOp("*", [resultado, Parser.parse_factor()])
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.select_next()
                resultado = BinOp("/", [resultado, Parser.parse_factor()])
            
        return resultado
    
    def parse_factor():

        if Parser.tokenizer.next.type == "INT":
            resultado = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado
        
        elif Parser.tokenizer.next.type == "IDENT":
            resultado = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado
        
        elif Parser.tokenizer.next.type == "STRING":
            resultado = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado
        
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            resultado = UnOp("+", [Parser.parse_factor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            resultado = UnOp("-", [Parser.parse_factor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.select_next()
            resultado = UnOp("!", [Parser.parse_factor()])
            return resultado

        elif Parser.tokenizer.next.type == "OPEN":
            Parser.tokenizer.select_next()
            resultado = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type == "CLOSE":
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Error")
        else:
            raise TypeError("Error")
        
            
    def run(code):

        # Inicializa objeto Tokenizador
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.select_next()

        resultado = Parser.parse_program()

        if Parser.tokenizer.next.type == "EOF":
            return resultado
        else:
            raise TypeError("Error")

          

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        code = file.read() + '\n'
        code = PrePro.filter(code)

    st = SymbolTable()
    root = Parser.run(code)
    root.Evaluate(st)