from Token.token import Token

class Lexer:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.tokens = []
        self.posicao_atual = 0
        self.inicio = 0
        self.linha_atual = 1

        self.palavras_reservadas = {
            'main': 'MAIN',
            'end': 'END',
            'func': 'FUNC',
            'proc': 'PROC',
            'call': 'CALL',
            'int': 'INT',
            'bool': 'BOOL',
            'True': 'BOOLEAN',
            'False': 'BOOLEAN',
            'return': 'RETURN',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'print': 'PRINT',
            'break': 'BREAK',
            'continue': 'CONTINUE'
        }
        
        self.operadores_booleanos = {
            '=': 'ATB',
            '!': 'DIFF',
            '<': 'LESS',
            '>': 'GREATER'
        }
        
        self.operadores_booleanos_completo = {
            '=': 'EQUAL',
            '!': 'DIFF',
            '<': 'LESSEQUAL',
            '>': 'GREATEREQUAL'
        }
        
        self.operadores_aritmeticos = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MULT',
            '/': 'DIV',
            '%': 'MOD'
        }
        
        self.delimitadores = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            ',': 'COMMA',
            ';': 'SEMICOLON'
        }

    def lookAhead(self):
        return self.codigo_fonte[self.posicao_atual] if self.posicao_atual < len(self.codigo_fonte) else "\0"
        
    def adicionar_token(self, tipo, lexema=None, linha=None):
        lexema = lexema if lexema else self.codigo_fonte[self.posicao_atual]
        linha = self.linha_atual if not linha else linha
        self.tokens.append(Token(tipo, lexema, linha))

    def analisar(self):
        while self.posicao_atual < len(self.codigo_fonte):
            self.inicio = self.posicao_atual

            char_atual = self.codigo_fonte[self.posicao_atual]

            if char_atual in [' ', '\t']:
                self.posicao_atual += 1
                continue

            elif char_atual == '\n':
                self.linha_atual += 1
                self.posicao_atual += 1
                continue

            elif char_atual.isdigit():
                self.analisar_numero()

            elif char_atual.isalpha():
                self.analisar_identificador()

            elif char_atual in self.operadores_booleanos:
                self.analisar_op_booleano()

            elif char_atual in self.operadores_aritmeticos:
                self.analisar_op_aritmetico()

            elif char_atual in self.delimitadores:
                self.analisar_delimitador()

            else:
                print(f"Caractere inválido na linha {self.linha_atual}: {char_atual}")
                self.posicao_atual += 1

        return self.tokens

    def analisar_numero(self):
        while self.lookAhead().isdigit():
            self.posicao_atual += 1
        self.adicionar_token("NUM", self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual)
    
    def analisar_identificador(self):
        while self.lookAhead().isalnum():
            self.posicao_atual += 1
        lexema = self.codigo_fonte[self.inicio:self.posicao_atual]
        if lexema in self.palavras_reservadas:
            tipo = self.palavras_reservadas[lexema]
        else:
            tipo = "ID"
        self.adicionar_token(tipo, lexema, self.linha_atual)
    
    def analisar_op_booleano(self):
        token = self.codigo_fonte[self.posicao_atual]
        self.posicao_atual += 1
        if token in self.operadores_booleanos_completo:
            if self.lookAhead() == '=':
                self.posicao_atual += 1
                tipo = self.operadores_booleanos_completo[token]
            else:
                tipo = self.operadores_booleanos[token]
        else:
            tipo = self.operadores_booleanos[token]
        self.posicao_atual += 1
        self.adicionar_token(tipo, self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual)

    def analisar_op_aritmetico(self):
        token = self.codigo_fonte[self.posicao_atual]
        tipo = self.operadores_aritmeticos[token]
        self.posicao_atual += 1
        self.adicionar_token(tipo, self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual)
    
    def analisar_delimitador(self):
        token = self.codigo_fonte[self.posicao_atual]
        tipo = self.delimitadores[token]
        self.posicao_atual += 1
        self.adicionar_token(tipo, self.codigo_fonte[self.inicio:self.posicao_atual], self.linha_atual)
