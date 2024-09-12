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
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.while_(temp)
            return temp
        
        if self.token_atual().tipo == 'ID':
            temp = []
            temp.append(self.indexEscopoAtual)
            temp.append(self.token_atual().linha)
            temp.append(self.token_atual().tipo)
            self.call_var(temp)
            return temp
        
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
            
    def while_(self, temp):
        self.index_token += 1
        if self.token_atual().tipo == 'LPAREN':
            tempExpression = []
            tempExpression = self.expression(tempExpression)
            temp.append(tempExpression)
            if self.token_atual().tipo == 'RPAREN':
                self.index_token += 1
                if self.token_atual().tipo == 'LBRACE':
                    self.index_token += 1
                    TempBlock = []
                    self.indexEscopoAtual += 1
                    while self.token_atual().tipo != 'RBRACE':
                        TempBlock.append(self.block())
                    temp.append(TempBlock)
                    if self.token_atual().tipo == 'RBRACE':
                        self.index_token += 1
                        self.indexEscopoAtual -= 1
                        self.tabelaDeSimbolos.append(temp)
                        return temp
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
                                    while self.token_atual().tipo != 'RBRACE':
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
                                while self.token_atual().tipo != 'RBRACE':
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
                            while self.token_atual().tipo != 'RBRACE':
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

    def call_var(self, temp):
        temp.append(self.token_atual().lexema)
        self.index_token += 1
        if self.token_atual().tipo == 'ATB':
            temp.append(self.token_atual().lexema)
            self.index_token += 1
            if self.token_atual().tipo == 'NUM'or self.token_atual().tipo == 'BOOLEAN' or self.token_atual().tipo == 'ID':
                temp.append(self.token_atual().lexema)
                self.index_token += 1
                if self.token_atual().tipo == 'SEMICOLON':
                    self.index_token += 1
                    self.tabelaDeSimbolos.append(temp)
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
                return
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

    def buscarNaTabelaDeSimbolos(self, simbolo, indice):
        for i in range(len(self.tabelaDeSimbolos)):
            if self.tabelaDeSimbolos[i][indice] == simbolo:
                return self.tabelaDeSimbolos[i]

    def Semantica(self):
        for i in range(len(self.tabelaDeSimbolos)):
            token = self.tabelaDeSimbolos[i][2]

            if token == 'FUNC':
                self.func_sem(self.tabelaDeSimbolos[i])
            
            if token == 'PROC':
                self.proc_sem(self.tabelaDeSimbolos[i])

            if token == 'INT' or token == 'BOOL':
                self.declaration_var_sem(self.tabelaDeSimbolos[i])

            if token == 'ID':
                self.call_var_sem(self.tabelaDeSimbolos[i])

            if token == 'IF':
                self.expression_sem(self.tabelaDeSimbolos[i])
            
            if token == 'WHILE':
                self.expression_sem(self.tabelaDeSimbolos[i])
            
            if token == 'CALL':
                if self.tabelaDeSimbolos[i][3] == 'FUNC':
                    self.call_func_sem(self.tabelaDeSimbolos[i])

                if self.tabelaDeSimbolos[i][3] == 'PROC':
                    self.call_proc_sem(self.tabelaDeSimbolos[i])

        print("Análise semântica realizada com sucesso.")

            
    def declaration_var_sem(self, indiceAtual):
        if indiceAtual[2] == 'INT':
            token = indiceAtual[5][0]

            if token.isnumeric():
                return True
            
            if token == 'CALL':
                return
            #     func = self.buscarNaTabelaDeSimbolos(indiceAtual[5][2], 4)
            #     if func != None:
            #         if func[0] <= indiceAtual[0] and func[1] <= indiceAtual[1]:
            #             return True
            #         else:
            #             raise Exception(f"Erro semântico: Função não declarada na linha {indiceAtual[1]}aa.")
            #     else:
            #         raise Exception(f"Erro semântico: Função não declarada na linha {indiceAtual[1]}.bb")
            
            
            if token.isalpha() and token != 'True' and token != 'False':
                var = self.buscarNaTabelaDeSimbolos(indiceAtual[5][0], 3)
                if var != None:
                    if(var[0] <= indiceAtual[0] and var[1] <= indiceAtual[1]):
                        if(var[2] == 'INT'):
                            return True
                        else:
                            raise Exception(f"Erro semântico: Atribuição de tipo diferente na linha {indiceAtual[1]}.")
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
                else:
                    raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
            
            if indiceAtual[2] == 'BOOL':
                token = indiceAtual[5][0]

                if token == 'True' or token == 'False':
                    return True
                
                if token.isnumeric():
                    raise Exception(f"Erro semântico: Atribuição de tipo diferente na linha {indiceAtual[1]}.")
                
                if token.isalpha() and token != 'True' and token != 'False':
                    var = self.buscarNaTabelaDeSimbolos(indiceAtual[5][0], 3)
                    if var != None:
                        if(var[0] <= indiceAtual[0] and var[1] <= indiceAtual[1]):
                            if(var[2] == 'BOOL'):
                                if var[5][0] == 'True' and var[5][0] == 'False':
                                    return True
                                else:
                                    raise Exception(f"Erro semântico: Atribuição de tipo diferente na linha {indiceAtual[1]}.")
                            else:
                                raise Exception(f"Erro semântico: Atribuição de tipo diferente na linha {indiceAtual[1]}.")
                        else:
                            raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
            
            else:
                return 
                # raise Exception(f"Erro semântico: Atribuição de tipo diferente na linha {indiceAtual[1]}.")

    def call_var_sem(self, indiceAtual):
        status = False
        for i in range(len(self.tabelaDeSimbolos)):
            if self.tabelaDeSimbolos[i][2] == 'INT' or self.tabelaDeSimbolos[i][2] == 'BOOL':
                print('1')
                if self.tabelaDeSimbolos[i][3] == indiceAtual[5]:
                    print('1.1',self.tabelaDeSimbolos[i], indiceAtual)
                    if self.tabelaDeSimbolos[i][0] <= indiceAtual[0] and self.tabelaDeSimbolos[i][1] <= indiceAtual[1]:
                        print('1.2')
                        print(self.tabelaDeSimbolos[i])
                        print('BB', indiceAtual)
                        if self.tabelaDeSimbolos[i][2] == 'INT' and indiceAtual[5][2].isnumeric():
                            print('2')
                            status = True
                            break
                        elif self.tabelaDeSimbolos[i][2] == 'BOOL' and (indiceAtual[5][2] == 'True' or indiceAtual[5][2] == 'False'):
                            status = True
                            break
                        else:
                            raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual}.")
                        
            elif self.buscarParamsProc(indiceAtual):
                status = True
                break

            elif self.buscarParamsFunc(indiceAtual):
                status = True
                break
                    
    
        if not status:
            raise Exception(f"Erro Semântico: Variável '{indiceAtual[3]}' não declarada ou tipos incompatíveis na linha {indiceAtual[1]}.")
        
    def buscarParamsProc(self, indiceAtual):
        for simbolo in self.tabelaDeSimbolos:
            if simbolo[2] == 'PROC':
                if simbolo[4][0][1] == indiceAtual[3]:
                    paramsProc = simbolo[4] 
                    for param in paramsProc:
                        if param[0] == 'INT' and indiceAtual[5].isnumeric():
                            return True
                        elif param[0] == 'BOOL' and indiceAtual[5] in ('True', 'False'):
                            return True
                    return False
        return False
                            
    def buscarParamsFunc(self, indiceAtual):
        for simbolo in self.tabelaDeSimbolos:
            if simbolo[2] == 'FUNC':
                if simbolo[4][0][1] == indiceAtual[3]:
                    paramsFunc = simbolo[4]
                    for param in paramsFunc:
                        if param[0] == 'INT' and indiceAtual[5].isnumeric():
                            return True
                        elif param[0] == 'BOOL' and indiceAtual[5] in ('True', 'False'):
                            return True
                    return False
        return False

    def expression_sem(self, indiceAtual):
        param1 = self.buscarNaTabelaDeSimbolos(indiceAtual[3][0], 3)
        param2 = self.buscarNaTabelaDeSimbolos(indiceAtual[3][2], 3)
        if indiceAtual[3][0].isnumeric() and indiceAtual[3][2].isnumeric():
            return True
        
        if indiceAtual[3][0].isalpha() and indiceAtual[3][2].isalpha():
            if param1 != None and param2 != None:
                if param1[2] == 'INT' and param2[2] == 'INT':
                    if param1[0] <= indiceAtual[0] and param1[1] <= indiceAtual[1] and param2[0] <= indiceAtual[0] and param2[1] <= indiceAtual[1]:
                        return True
                elif param1[2] == 'BOOL' and param2[2] == 'BOOL':
                    if param1[0] <= indiceAtual[0] and param1[1] <= indiceAtual[1] and param2[0] <= indiceAtual[0] and param2[1] <= indiceAtual[1]:
                        if indiceAtual[3][1] == '==' or indiceAtual[3][1] == '!=':
                            return True
                elif param1[2] == 'INT' and param2[2] != 'INT':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                elif param1[2] != 'INT' and param2[2] == 'INT':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                elif param1[2] == 'BOOL' and param2[2] != 'BOOL':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                elif param1[2] != 'BOOL' and param2[2] == 'BOOL':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                elif param1[2] == 'INT' and param2[2] == 'BOOL':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                elif param1[2] == 'BOOL' and param2[2] == 'INT':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
            else:
                raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
        
        if indiceAtual[3][0].isnumeric() and indiceAtual[3][2].isalpha():
            if param2 != None:
                if param2[2] != 'INT':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                else:
                    if param1[0] <= indiceAtual[0]:
                        return True
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada no escopo da função.")
            else:
                raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
            
        if indiceAtual[3][0].isalpha() and indiceAtual[3][2].isnumeric():
            if param1 != None:
                if param1[2] != 'INT':
                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                else:
                    if param1[0] <= indiceAtual[0]:
                        return True
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada no escopo da função.")
            else:
                raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")

        else:
            raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                
    def func_sem(self, indiceAtual):
        if indiceAtual[3] == 'INT':
            if indiceAtual[7][2][0].isnumeric():
                return True
            
            if indiceAtual[7][2][0].isalpha():
                return_type = self.buscarNaTabelaDeSimbolos(indiceAtual[7][2][0], 3)
                if return_type[0] == indiceAtual[0] + 1:
                    if return_type != None:
                        if return_type[2] == 'INT':
                            return True
                        else:
                            raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
                else:
                    raise Exception(f"Erro semântico: Variável não declarada no escopo da funçao.")

        if indiceAtual[3] == 'BOOL':
            if indiceAtual[7][2][0] == 'True' or indiceAtual[7][2][0] == 'False':
                return True
            
            if indiceAtual[7][2][0].isnumeric():
                raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
            
            if indiceAtual[7][2][0].isalpha():
                return_type = self.buscarNaTabelaDeSimbolos(indiceAtual[7][2][0], 3)
                if return_type[0] == indiceAtual[0] + 1:
                    if return_type != None:
                        if return_type[2] == 'BOOL':
                            return True
                        else:
                            raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                    else:
                        raise Exception(f"Erro semântico: Variável não declarada na linha {indiceAtual[1]}.")
                else:
                    raise Exception(f"Erro semântico: Variável não declarada no escopo da funçao.")
        
        else:
            raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
        
    def proc_sem(self, indiceAtual):
        for i in range(len(self.tabelaDeSimbolos)):
            for j in range(len(indiceAtual[5])):
                if self.tabelaDeSimbolos[i][2] == 'INT' or self.tabelaDeSimbolos[i][2] == 'BOOL':
                    if indiceAtual[5][j] == self.tabelaDeSimbolos[i]:
                        if indiceAtual[0] <= self.tabelaDeSimbolos[i][0] and indiceAtual[1] <= self.tabelaDeSimbolos[i][1]:
                            if self.tabelaDeSimbolos[i][2] == 'INT':
                                if indiceAtual[5][j][5][0].isnumeric():
                                    return True
                                else:
                                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")
                            elif self.tabelaDeSimbolos[i][2] == 'BOOL':
                                if indiceAtual[5][j][5][0] == 'True' or indiceAtual[5][j][5][0] == 'False':
                                    return True
                                else:
                                    raise Exception(f"Erro semântico: Tipos incompatíveis na linha {indiceAtual[1]}.")


    ##FALTANDO APENAS OS CALL                
    def call_func_sem(self, indiceAtual):
        return
    
    def call_proc_sem(self, indiceAtual):
       return