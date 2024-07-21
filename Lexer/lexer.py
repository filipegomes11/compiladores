from Token.token import Token

class Lexer:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens = []
        self.posicao_atual = 0
        self.inicio = 0
        self.linha_atual = 1

    def lookAhead(self):
        if self.posicao_atual < len(self.codigo_fonte):
            return self.codigo_fonte[self.posicao_atual]
        else:
            return "\0"

    def analisar(self):
        while self.posicao_atual < len(self.codigo_fonte):
            self.inicio = self.posicao_atual

            if self.codigo_fonte[self.posicao_atual] in [' ', '\t']:
                self.posicao_atual += 1
                continue

            elif self.codigo_fonte[self.posicao_atual] == '\n':
                self.linha_atual += 1
                self.posicao_atual += 1
                continue

            elif self.codigo_fonte[self.posicao_atual].isdigit():
                while self.lookAhead().isdigit():
                    self.posicao_atual += 1
                self.tokens.append(Token("NUM", self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual].isalpha():
                while self.lookAhead().isalnum():
                    self.posicao_atual += 1
                self.tokens.append(Token("ID", self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual] == '=' or self.codigo_fonte[self.posicao_atual] == '!' or self.codigo_fonte[self.posicao_atual] == '<' or self.codigo_fonte[self.posicao_atual] == '>':
                token = self.codigo_fonte[self.posicao_atual]
                self.posicao_atual += 1
                self.tokens.append(Token(self.op_boolean(token), self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual] == '+' or self.codigo_fonte[self.posicao_atual] == '-' or self.codigo_fonte[self.posicao_atual] == '*' or self.codigo_fonte[self.posicao_atual] == '/' or self.codigo_fonte[self.posicao_atual] == '%':
                token = self.codigo_fonte[self.posicao_atual]
                self.posicao_atual += 1
                self.tokens.append(Token(self.op_arithmetic(token), self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual] == '(' or self.codigo_fonte[self.posicao_atual] == ')' or self.codigo_fonte[self.posicao_atual] == '{' or self.codigo_fonte[self.posicao_atual] == '}':
                token = self.codigo_fonte[self.posicao_atual]
                self.posicao_atual += 1
                self.tokens.append(Token(self.delimitadores(token), self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual] == ',':
                self.posicao_atual += 1
                self.tokens.append(Token('COMMA', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif self.codigo_fonte[self.posicao_atual] == ';':
                self.posicao_atual += 1
                self.tokens.append(Token('SEMICOLON', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))


            else:
                print(f"Caractere inválido na linha {self.linha_atual}: {self.codigo_fonte[self.posicao_atual]}")
                self.posicao_atual += 1

        return self.tokens


    def op_boolean(self, token):
        if token == '=':
            if self.lookAhead() == '=':
                self.posicao_atual += 1
                return 'EQUAL'
            else:
                return 'ATB'
            
        elif token == '!':
            if self.lookAhead() == '=':
                self.posicao_atual += 1
                return 'DIFF'

        elif token == '<':
            if self.lookAhead() == '=':
                self.posicao_atual += 1
                return 'LESSEQUAL'
            else:
                return 'LESS'
        
        elif token == '>':
            if self.lookAhead() == '=':
                self.posicao_atual += 1
                return 'GREATEREQUAL'
            else:
                return 'GREATER'
    
    def op_arithmetic(self, token):
        if token == '+':
            return 'ADD'
        elif token == '-':
            return 'SUB'
        elif token == '*':
            return 'MULT'
        elif token == '/':
            return 'DIV'
        elif token == '%':
            return 'MOD'
        
    def delimitadores(self, token): 
        if token == '(':
            return 'LPAREN'
        elif token == ')':
            return 'RPAREN'
        elif token == '{':
            return 'LBRACE'
        elif token == '}':
            return 'RBRACE'