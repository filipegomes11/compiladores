class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index_token = 0
        self.tabelaDeSimbolos = []
        self.indexEscopoAtual = -1

    def token_atual(self):
        return self.tokens[self.index_token]


    def parse(self):
        self.indexEscopoAtual += 1
        return self.programa()

    def programa(self):
        if self.token_atual().tipo == 'MAIN':
            self.index_token += 1
            if self.token_atual().tipo == 'LBRACE':
                self.index_token += 1
                while self.token_atual().tipo != 'RBRACE':
                    self.block()
                if self.token_atual().tipo == 'RBRACE':
                    self.index_token += 1
                    if self.token_atual().tipo == 'END':
                        print("Compilado com sucesso!")
                        return
        raise Exception(f"Erro de sintaxe: '{self.token_atual().tipo}' não esperado na linha {self.token_atual().linha}.")

    def block(self):
        if self.token_atual().tipo == 'INT' or self.token_atual().tipo == 'BOOL':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.declaration_var(temp)
            return temp
            
        if self.token_atual().tipo == 'FUNC':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.declaration_func(temp)
            return temp

        if self.token_atual().tipo == 'PROC':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            temp = self.declaration_proc(temp)
            self.tabelaDeSimbolos.append(temp)
            return True

        if self.token_atual().tipo == 'CALL':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.index_token += 1
            if self.token_atual().tipo == 'PROC':
                temp.append(self.token_atual().tipo)
                temp = self.call_proc(temp)
                if self.token_atual().tipo == 'SEMICOLON':
                    self.index_token += 1
                    self.tabelaDeSimbolos.append(temp)
                    return temp
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            
            elif self.token_atual().tipo == 'FUNC':
                temp.append(self.token_atual().tipo)
                temp = self.call_func(temp)
                if self.token_atual().tipo == 'SEMICOLON':
                    self.index_token += 1
                    self.tabelaDeSimbolos.append(temp)
                    return temp
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'FUNC' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

        if self.token_atual().tipo == 'PRINT':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.print_statement(temp)
            return temp

        if self.token_atual().tipo == 'IF':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.if_stmt(temp)
            return temp
        
        if self.token_atual().tipo == 'WHILE':
            self.while_()
            return True
        
        if self.token_atual().tipo == 'ID':
            self.call_var()
            return True
        
        if self.token_atual().tipo == 'BREAK' or self.token_atual().tipo == 'CONTINUE':
            self.unconditional()
            return True

        else:
            raise Exception(f"Erro de sintaxe: Não esperado'{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        
    def if_stmt(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'LPAREN':
            tempExpression = []
            tempExpression = self.expression(tempExpression)
            temp.append(tempExpression)
            if self.token_atual().tipo == 'RPAREN':
                self.index_token += 1
                if self.token_atual().tipo == 'LBRACE':
                    self.index_token += 1
                    tempBlock = []
                    self.indexEscopoAtual += 1
                    while self.token_atual().tipo != 'RBRACE':
                        tempBlock.append(self.block())
                    temp.append(tempBlock)
                    if self.token_atual().tipo == 'RBRACE':
                        self.indexEscopoAtual -= 1
                        self.index_token += 1
                        if self.token_atual().tipo == 'ELSE':
                            self.indexEscopoAtual += 1
                            tempElse = []
                            tempElse.append(self.indexEscopoAtual)
                            tempElse.append(self.token_atual().linha)
                            tempElse.append(self.token_atual().tipo)
                            tempElse = self.else_part(tempElse)
                            temp.append(tempElse)
                            self.tabelaDeSimbolos.append(temp)
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def else_part(self, tempElse):
        self.index_token += 1
        if self.token_atual().tipo == 'LBRACE':
            self.index_token += 1
            tempBlock = []
            while self.token_atual().tipo != 'RBRACE':
                tempBlock.append(self.block())
            tempElse.append(tempBlock)
            if self.token_atual().tipo == 'RBRACE':
                self.index_token += 1
                self.indexEscopoAtual -= 1
                return tempElse
            else:
                raise Exception(f"Erro de sintaxe: Esperado '}}' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '{{' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            
    def while_(self):
        self.index_token += 1
        if self.token_atual().tipo == 'LPAREN':
            self.expression()
            if self.token_atual().tipo == 'RPAREN':
                self.index_token += 1
                if self.token_atual().tipo == 'LBRACE':
                    self.index_token += 1
                    while self.token_atual().tipo != 'RBRACE':
                        self.block()
                    if self.token_atual().tipo == 'RBRACE':
                        self.index_token += 1
                        return True
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
    
    def unconditional(self):
        self.index_token += 1
        if self.token_atual().tipo == 'CONTINUE':
            self.index_token += 1
            if self.token_atual().tipo == 'SEMICOLON':
                self.index_token += 1
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        self.index_token += 1
        if self.token_atual().tipo == 'BREAK':
            self.index_token += 1
            if self.token_atual().tipo == 'SEMICOLON':
                self.index_token += 1
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'CONTINUE' ou 'BREAK' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def print_statement(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'LPAREN':
            tempParams = []
            temp.append(self.params_print(tempParams))
            if self.token_atual().tipo == 'RPAREN':
                self.index_token += 1
                if self.token_atual().tipo == 'SEMICOLON':
                    self.tabelaDeSimbolos.append(temp)
                    self.index_token += 1
                    return
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def params_print(self, tempParams):
        self.index_token += 1
        if self.token_atual().tipo == 'ID'or self.token_atual().tipo == 'NUM' or self.token_atual().tipo == 'BOOLEAN':
            tempParams.append(self.token_atual().lexema)
            if self.token_atual().tipo == 'ADD' or self.token_atual().tipo == 'SUB' or self.token_atual().tipo == 'MULT'or self.token_atual().tipo == 'DIV':
                tempParams.append(self.token_atual().lexema)
                self.call_op(tempParams)
                return tempParams
            self.index_token += 1
            if self.token_atual().tipo == 'COMMA':
                self.params_print(tempParams)
                return tempParams
            return tempParams
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID', 'NUM' ou 'BOOLEAN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def declaration_var(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'ID':
            temp.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'ATB':
                temp.append(self.token_atual().lexema)
                self.index_token += 1
                tempEndVar = []
                self.end_var(tempEndVar)
                temp.append(tempEndVar)
                if self.token_atual().tipo == 'SEMICOLON':
                    self.index_token += 1
                    self.tabelaDeSimbolos.append(temp)
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '=' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
    
    def declaration_func(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'INT' or self.token_atual().tipo == 'BOOL':
            temp.append(self.token_atual().tipo)
            self.index_token += 1
            if self.token_atual().tipo == 'ID':
                temp.append(self.token_atual().lexema)
                self.index_token += 1
                if self.token_atual().tipo == 'LPAREN':
                    tempParen = []
                    self.index_token += 1
                    if self.token_atual().tipo == 'INT' or self.token_atual().tipo == 'BOOL':
                        tempParametroAtual = []
                        tempParametroAtual.append(self.token_atual().tipo)
                        self.index_token += 1
                        if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                            tempParametroAtual.append(self.token_atual().lexema)
                            tempParen.append(tempParametroAtual)
                            self.index_token += 1
                            if self.token_atual().tipo == 'COMMA':
                                tempParen.append(self.params(tempParen))
                                tempParen.pop()
                                temp.append(tempParen)
                                if self.token_atual().tipo == 'RPAREN':
                                    self.index_token += 1
                                    if self.token_atual().tipo == 'LBRACE':
                                        self.index_token += 1
                                        self.indexEscopoAtual += 1
                                        tempBlock = []
                                        while self.token_atual().tipo != 'RETURN':
                                            tempBlock.append(self.block())
                                        temp.append(tempBlock)
                                        tempReturn = []
                                        if self.token_atual().tipo == 'RETURN':
                                            tempReturn.append(self.indexEscopoAtual)
                                            tempReturn.append(self.token_atual().tipo)
                                            tempReturnParams = []
                                            tempReturnParams = self.return_(tempReturnParams)
                                            tempReturn.append(tempReturnParams)
                                            temp.append(tempReturn)
                                            if self.token_atual().tipo == 'RBRACE':
                                                self.index_token += 1
                                                self.indexEscopoAtual -= 1
                                                self.tabelaDeSimbolos.append(temp)
                                            else:
                                                raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                            elif self.token_atual().tipo == 'RPAREN':
                                temp.append(tempParen)
                                self.index_token += 1
                                if self.token_atual().tipo == 'LBRACE':
                                    self.index_token += 1
                                    self.indexEscopoAtual += 1
                                    tempBlock = []
                                    while self.token_atual().tipo != 'RETURN':
                                        tempBlock.append(self.block())
                                    temp.append(tempBlock)
                                    tempReturn = []
                                    if self.token_atual().tipo == 'RETURN':
                                        tempReturn.append(self.indexEscopoAtual)
                                        tempReturn.append(self.token_atual().tipo)
                                        tempReturnParams = []
                                        tempReturnParams = self.return_(tempReturnParams)
                                        tempReturn.append(tempReturnParams)
                                        temp.append(tempReturn)
                                        if self.token_atual().tipo == 'RBRACE':
                                            self.indexEscopoAtual -= 1
                                            self.index_token += 1
                                            self.tabelaDeSimbolos.append(temp)
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado {'}'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                            else:
                                    raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                    else:
                        if self.token_atual().tipo == 'RPAREN':
                            temp.append(tempParen)
                            self.index_token += 1
                            if self.token_atual().tipo == 'LBRACE':
                                tempBlock = []
                                self.indexEscopoAtual += 1
                                self.index_token += 1
                                while self.token_atual().tipo != 'RETURN':
                                    tempBlock.append(self.block())
                                temp.append(tempBlock)
                                tempReturn = []
                                if self.token_atual().tipo == 'RETURN':
                                    tempReturn.append(self.indexEscopoAtual)
                                    tempReturn.append(self.token_atual().tipo)
                                    tempReturnParams = []
                                    tempReturnParams = self.return_(tempReturnParams)
                                    tempReturn.append(tempReturnParams)
                                    temp.append(tempReturn)
                                    if self.token_atual().tipo == 'RBRACE':
                                        self.indexEscopoAtual -= 1
                                        self.index_token += 1
                                        self.tabelaDeSimbolos.append(temp) 
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                else:
                    raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'INT' ou 'BOOLEAN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def declaration_proc(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'ID':
            temp.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'LPAREN':
                tempParen = []
                self.index_token += 1
                if self.token_atual().tipo == 'INT' or self.token_atual().tipo == 'BOOL':
                    tempParametroAtual = []
                    tempParametroAtual.append(self.token_atual().tipo)
                    self.index_token += 1
                    if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                        tempParametroAtual.append(self.token_atual().lexema)
                        tempParen.append(tempParametroAtual)
                        self.index_token += 1
                        if self.token_atual().tipo == 'COMMA':
                            tempParen.append(self.params(tempParen))
                            tempParen.pop()
                            temp.append(tempParen)
                            if self.token_atual().tipo == 'RPAREN':
                                self.index_token += 1
                                if self.token_atual().tipo == 'LBRACE':
                                    tempBlock = []
                                    self.indexEscopoAtual += 1
                                    self.index_token += 1
                                    tempBlock.append(self.block())
                                    temp.append(tempBlock)
                                    if self.token_atual().tipo == 'RBRACE':
                                        self.indexEscopoAtual -= 1
                                        self.index_token += 1
                                        return temp
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado {'}'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado {'{'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                            else:
                                raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                        elif self.token_atual().tipo == 'RPAREN':
                            temp.append(tempParen)
                            self.index_token += 1
                            if self.token_atual().tipo == 'LBRACE':
                                tempBlock = []
                                self.index_token += 1
                                self.indexEscopoAtual += 1
                                tempBlock.append(self.block())
                                temp.append(tempBlock)
                                if self.token_atual().tipo == 'RBRACE':
                                    self.index_token += 1
                                    self.indexEscopoAtual -= 1
                                    return temp
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado {'}'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                            else:
                                raise Exception(f"Erro de sintaxe: Esperado {'{'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                        else:
                            raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                    else:
                            raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                else:
                    if self.token_atual().tipo == 'RPAREN':
                        temp.append(tempParen)
                        self.index_token += 1
                        if self.token_atual().tipo == 'LBRACE':
                            tempBlock = []
                            self.index_token += 1
                            self.indexEscopoAtual += 1
                            tempBlock.append(self.block())
                            temp.append(tempBlock)
                            if self.token_atual().tipo == 'RBRACE':
                                self.indexEscopoAtual -= 1
                                self.index_token += 1
                                return temp
                            else:
                                raise Exception(f"Erro de sintaxe: Esperado {'}'} ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                        else:
                            raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def call_var(self):
        self.index_token += 1
        if self.token_atual().tipo == 'ATB':
            self.index_token += 1
            if self.token_atual().tipo == 'NUM'or self.token_atual().tipo == 'BOOLEAN' or self.token_atual().tipo == 'ID':
                self.index_token += 1
                if self.token_atual().tipo == 'SEMICOLON':
                    self.index_token += 1
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'NUM', 'BOOLEAN' ou 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '=' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def return_(self, tempReturnParams):
        self.index_token += 1
        if self.token_atual().tipo == 'ID' or self.token_atual().tipo == 'NUM' or self.token_atual().tipo == 'BOOLEAN':
            tempReturnParams.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'SEMICOLON':
                self.index_token += 1
                return tempReturnParams
            else:
                raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")

    def end_var(self, tempEndVar):
        if self.token_atual().tipo == 'CALL':
            tempEndVar.append(self.token_atual().tipo)
            self.index_token += 1
            if self.token_atual().tipo == 'FUNC':
                tempEndVar.append(self.token_atual().tipo)
                self.call_func(tempEndVar)
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'FUNC' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")

        if self.token_atual().tipo == 'BOOLEAN':
            if self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                tempEndVar.append(self.token_atual().lexema)
                self.index_token += 1
                return
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'True' ou 'False' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
            
        if self.token_atual().tipo == 'NUM':
            tempEndVar.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'ADD' or self.token_atual().tipo == 'SUB' or self.token_atual().tipo == 'MUL'or self.token_atual().tipo == 'DIV':
                tempEndVar.append(self.token_atual().lexema)
                self.call_op(tempEndVar)
                return
            else:
                return
        
        if self.token_atual().tipo == 'ID':
            tempEndVar.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'ADD' or self.token_atual().tipo == 'SUB' or self.token_atual().tipo == 'MUL' or self.token_atual().tipo == 'DIV':
                tempEndVar.append(self.token_atual().lexema)
                self.call_op(tempEndVar)
                return 
            else:
                raise Exception(f"Erro de sintaxe: Esperado número ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID', 'NUM' ou 'BOOLEAN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
        
    def call_func(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'ID':
            temp.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'LPAREN':
                self.index_token += 1
                tempParams = []
                if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'TRUE' or self.token_atual().lexema == 'False':
                    tempParams.append(self.token_atual().lexema)
                    self.index_token += 1
                    if self.token_atual().tipo == 'COMMA':
                        tempParams.append(self.params_call_func(tempParams))
                        tempParams.pop()
                        if self.token_atual().tipo == 'RPAREN':
                            self.index_token += 1
                            temp.append(tempParams)
                            return temp
                        else:
                            raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
                    elif self.token_atual().tipo == 'RPAREN':
                        self.index_token += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
                else:
                    temp.append(tempParams)
                    if self.token_atual().tipo == 'RPAREN':
                        self.index_token += 1
                        return temp
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")

    def call_proc(self,temp):
        self.index_token += 1
        if self.token_atual().tipo == 'ID':
            temp.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'LPAREN':
                tempParams = []
                self.index_token += 1
                if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'TRUE' or self.token_atual().lexema == 'False':
                    tempParams.append(self.token_atual().lexema)
                    self.index_token += 1
                    if self.token_atual().tipo == 'COMMA':
                        tempParams.append(self.params_call_func(tempParams))
                        tempParams.pop()
                        temp.append(tempParams)
                        if self.token_atual().tipo == 'RPAREN':
                            self.index_token += 1
                            temp.append(tempParams)
                            return temp
                        else:
                            raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
                    elif self.token_atual().tipo == 'RPAREN':
                        self.index_token += 1
                        temp.append(tempParams)
                        return temp
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
                else:
                    temp.append(tempParams)
                    if self.token_atual().tipo == 'RPAREN':
                        self.index_token += 1
                        return temp
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
        
    def identifier(self):
        if self.token_atual().tipo == 'ID':
            self.index_token += 1
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}..")
    
    def expression(self, tempExpression):
        self.index_token += 1
        if self.token_atual().tipo == 'ID' or self.token_atual().tipo == 'NUM':
            tempExpression.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'EQUAL' or self.token_atual().tipo == 'DIFF'or self.token_atual().tipo == 'LESSEQUAL' or self.token_atual().tipo == 'GREATEREQUAL':
                tempExpression.append(self.token_atual().lexema)
                self.index_token += 1
                if self.token_atual().tipo == 'ID' or self.token_atual().tipo == 'NUM':
                    tempExpression.append(self.token_atual().lexema)
                    self.index_token += 1
                    return tempExpression
                else:
                    raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado operador booleano ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            
    def call_op(self, tempEndVar):
        self.index_token += 1
        if self.token_atual().tipo == 'ID' or self.token_atual().tipo == 'NUM':
            tempEndVar.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'ADD' or self.token_atual().tipo == 'SUB' or self.token_atual().tipo == 'MULT' or self.token_atual().tipo == 'DIV':
                tempEndVar.append(self.token_atual().lexema)
                self.call_op(tempEndVar)
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.") 
        
    def params_call_func(self, tempParams):
        self.index_token += 1
        if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'TRUE' or self.token_atual().lexema == 'FALSE':
            tempParams.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'COMMA':
                self.params_call_func(tempParams)
            elif self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
            else:
                return tempParams
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID', 'TRUE' ou 'FALSE' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                
    def params(self, tempParen):
        self.index_token += 1
        if self.token_atual().tipo == 'INT' or self.token_atual().tipo == 'BOOL':
            tempParametroAtual = []
            tempParametroAtual.append(self.indexEscopoAtual + 1)
            tempParametroAtual.append(self.token_atual().tipo)
            self.index_token += 1
            if self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                tempParametroAtual.append(self.token_atual().lexema)
                tempParen.append(tempParametroAtual)
                self.index_token += 1
                if self.token_atual().tipo == 'COMMA':
                    self.params(tempParen)
                elif self.token_atual().tipo == 'ID' or self.token_atual().lexema == 'True' or self.token_atual().lexema == 'False':
                    raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
                else:
                    return tempParen
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'ID', 'TRUE' ou 'FALSE' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'INT' ou 'BOOLEAN' ao invés de '{self.token_atual().lexema}' na linha {self.token_atual().linha}.")
        
    