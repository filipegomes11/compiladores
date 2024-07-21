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
            char = self.codigo_fonte[self.posicao_atual]

            if char in [' ', '\t']:
                self.posicao_atual += 1
                continue

            elif char == '\n':
                self.linha_atual += 1
                self.posicao_atual += 1
                continue

            elif char == ',':
                self.posicao_atual += 1
                self.tokens.append(Token('COMMA', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif char == ';':
                self.posicao_atual += 1
                self.tokens.append(Token('SEMICOLON', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif char == '=':
                self.posicao_atual += 1
                self.tokens.append(Token('EQUALS', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif char == '+':
                self.posicao_atual += 1
                self.tokens.append(Token('PLUS', self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif char.isdigit():
                while self.lookAhead().isdigit():
                    self.posicao_atual += 1
                self.tokens.append(Token("NUM", self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            elif char.isalpha():
                while self.lookAhead().isalnum():
                    self.posicao_atual += 1
                self.tokens.append(Token("ID", self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual))

            else:
                print(f"Caractere inválido na linha {self.linha_atual}: {char}")
                self.posicao_atual += 1

        return self.tokens
