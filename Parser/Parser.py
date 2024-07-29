class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index_token = 0
        self.token_atual = self.tokens[self.index_token]

    def avancar(self):
        self.index_token += 1 if self.index_token < len(self.tokens) - 1 else 0
        self.token_atual = self.tokens[self.index_token]
    
    def verificar_e_avancar(self, tipo_esperado):
        if self.token_atual.tipo == tipo_esperado:
            self.avancar()
            return True
        return False

    def parse(self):
        return self.programa()

    def programa(self):
        if self.verificar_e_avancar('MAIN'):
            if self.verificar_e_avancar('LBRACE'):
                while self.token_atual.tipo != 'RBRACE':
                    block = self.block()
            if self.verificar_e_avancar('RBRACE'):
                if self.verificar_e_avancar('END'):
                    return block
        raise Exception(f"Erro de sintaxe: '{self.token_atual.tipo}' não esperado na linha {self.token_atual.linha}.")

    def block(self):
        if self.verificar_e_avancar('INT') or self.verificar_e_avancar('BOOL'):
            self.declaration_var()
            return True
            
        if self.verificar_e_avancar('FUNC'):
            self.declaration_func()
            return True
        
        if self.verificar_e_avancar('PROC'):
            self.declaration_proc()
            return True
        
        if self.verificar_e_avancar('CALL'):
            if self.token_atual.tipo == 'PROC':
                self.avancar()
                self.call_proc()
                if self.verificar_e_avancar('SEMICOLON'):
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            
            elif self.token_atual.tipo == 'FUNC':
                self.avancar()
                self.call_func()
                if self.verificar_e_avancar('SEMICOLON'):
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'FUNC' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")

        if self.verificar_e_avancar('PRINT'):
            self.print()
        
        if self.verificar_e_avancar('WHILE'):
            self.while_()
        

        if self.verificar_e_avancar('ID'):
            self.call_var()

        else:
            raise Exception(f"Erro de sintaxe: Não esperado'{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        
    def if_stmt(self):
        if self.verificar_e_avancar('IF'):
            if self.verificar_e_avancar('LPAREN'):
                self.expression()
                if self.verificar_e_avancar('RPAREN'):
                    if self.verificar_e_avancar('LBRACE'):
                        self.block()
                        if self.verificar_e_avancar('RBRACE'):
                            self.else_part()
                            return
        raise Exception(f"Erro de sintaxe no if statement na linha {self.token_atual.linha}.")
            
       
    def declaration_var(self):
        if self.verificar_e_avancar('ID'):
            if self.verificar_e_avancar('ATB'):
                self.end_var()
                if self.verificar_e_avancar('SEMICOLON'):
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '=' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
    
    def declaration_func(self):
        if self.verificar_e_avancar('INT') or self.verificar_e_avancar('BOOL'):
            if self.verificar_e_avancar('ID'):
                if self.verificar_e_avancar('LPAREN'):
                    if self.verificar_e_avancar('INT') or self.verificar_e_avancar('BOOL'):
                        if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                            self.avancar()
                            if self.verificar_e_avancar('COMMA'):
                                self.params()
                                if self.verificar_e_avancar('RPAREN'):
                                    if self.verificar_e_avancar('LBRACE'):
                                        self.block()
                                        if self.verificar_e_avancar('RETURN'):
                                            self.return_()
                                            if self.verificar_e_avancar('RBRACE'):
                                                return True
                                            else:
                                                raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            elif self.token_atual.tipo == 'RPAREN':
                                if self.verificar_e_avancar('RPAREN'):
                                    if self.verificar_e_avancar('LBRACE'):
                                        self.block()
                                        if self.verificar_e_avancar('RETURN'):
                                            self.return_()
                                            if self.verificar_e_avancar('RBRACE'):
                                                return True
                                            else:
                                                raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            else:
                                    raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                    else:
                        if self.verificar_e_avancar('RPAREN'):
                            if self.verificar_e_avancar('LBRACE'):
                                self.block()
                                if self.verificar_e_avancar('RETURN'):
                                    self.return_()
                                    if self.verificar_e_avancar('RBRACE'):
                                        return True
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado 'RETURN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            
                else:
                    raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'INT' ou 'BOOLEAN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")

    def declaration_proc(self):
        if self.verificar_e_avancar('ID'):
                if self.verificar_e_avancar('LPAREN'):
                    if self.verificar_e_avancar('INT') or self.verificar_e_avancar('BOOL'):
                        if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                            self.avancar()
                            if self.verificar_e_avancar('COMMA'):
                                self.params()
                                if self.verificar_e_avancar('RPAREN'):
                                    if self.verificar_e_avancar('LBRACE'):
                                        self.block()
                                        if self.verificar_e_avancar('RBRACE'):
                                            return True
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                    else:
                                        raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            elif self.token_atual.tipo == 'RPAREN':
                                if self.verificar_e_avancar('RPAREN'):
                                    if self.verificar_e_avancar('LBRACE'):
                                        self.block()
                                        if self.verificar_e_avancar('RBRACE'):
                                            return True
                                        else:
                                            raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ""{"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            else:
                                raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                        else:
                                raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                    else:
                        if self.verificar_e_avancar('RPAREN'):
                            if self.verificar_e_avancar('LBRACE'):
                                self.block()
                                if self.verificar_e_avancar('RBRACE'):
                                    return True
                                else:
                                    raise Exception(f"Erro de sintaxe: Esperado ""}"" ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                            else:
                                raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                        else:
                            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")

    def call_var(self):
        if self.verificar_e_avancar('ATB'):
            if self.verificar_e_avancar('NUM') or self.verificar_e_avancar('BOOLEAN') or self.verificar_e_avancar('ID'):
                if self.verificar_e_avancar('SEMICOLON'):
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'NUM', 'BOOLEAN' ou 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado '=' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")

    def return_(self):
        if self.verificar_e_avancar('ID') or self.verificar_e_avancar('NUM') or self.verificar_e_avancar('BOOLEAN'):
            if self.verificar_e_avancar('SEMICOLON'):
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")

    def end_var(self):
        if self.verificar_e_avancar('CALL'):
            if self.verificar_e_avancar('FUNC'):
                self.call_func()
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'FUNC' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")

        if self.token_atual.tipo == 'BOOLEAN':
            if self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                self.avancar()
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'True' ou 'False' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
            

        if self.verificar_e_avancar('NUM'):
            if self.verificar_e_avancar('ADD') or self.verificar_e_avancar('SUB') or self.verificar_e_avancar('MUL') or self.verificar_e_avancar('DIV'):
                self.call_op()
                return True
            else:
                return False
        
        if self.verificar_e_avancar('ID'):
            if self.verificar_e_avancar('ADD') or self.verificar_e_avancar('SUB') or self.verificar_e_avancar('MUL') or self.verificar_e_avancar('DIV'):
                self.call_op()
                return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado número ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID', 'NUM' ou 'BOOLEAN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
    def call_func(self):
        if self.verificar_e_avancar('ID'):
            if self.verificar_e_avancar('LPAREN'):
                if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'TRUE' or self.token_atual.lexema == 'False':
                    self.avancar()
                    if self.verificar_e_avancar('COMMA'):
                        self.params_call_func()
                    elif self.verificar_e_avancar('RPAREN'):
                        return True
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
                else:
                    if self.verificar_e_avancar('RPAREN'):
                        return True
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")

    def call_proc(self):
        if self.verificar_e_avancar('ID'):
            if self.verificar_e_avancar('LPAREN'):
                if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'TRUE' or self.token_atual.lexema == 'False':
                    self.avancar()
                    if self.verificar_e_avancar('COMMA'):
                        self.params_call_func()
                    elif self.verificar_e_avancar('RPAREN'):
                        return True
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
                else:
                    if self.verificar_e_avancar('RPAREN'):
                        return True
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ')' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
            else:
                raise Exception(f"Erro de sintaxe: Esperado '(' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
    def identifier(self):
        self.avancar()
        if self.verificar_e_avancar('ID'):
            return True
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
    
    def expression(self):
        if self.verificar_e_avancar('ID') or self.verificar_e_avancar('NUM'):
            if self.verificar_e_avancar('EQUAL') or self.verificar_e_avancar('DIFF') or self.verificar_e_avancar('LESSEQUAL') or self.verificar_e_avancar('GREATEREQUAL'):
                if self.verificar_e_avancar('ID') or self.verificar_e_avancar('NUM'):
                    return True
                else:
                    raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                raise Exception(f"Erro de sintaxe: Esperado operador booleano ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            
    def call_op(self):
        if self.verificar_e_avancar('ID') or self.verificar_e_avancar('NUM'):
            if self.verificar_e_avancar('ADD') or self.verificar_e_avancar('SUB') or self.verificar_e_avancar('MUL') or self.verificar_e_avancar('DIV'):
                self.call_op()
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ou 'NUM' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.") 
        
    def params_call_func(self):
        if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'TRUE' or self.token_atual.lexema == 'FALSE':
            self.avancar()
            if self.verificar_e_avancar('COMMA'):
                self.params_call_func()
            elif self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
            else:
                self.avancar()
                return True
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID', 'TRUE' ou 'FALSE' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                
    def params(self):
        if self.verificar_e_avancar('INT') or self.verificar_e_avancar('BOOL'):
            if self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                self.avancar()
                if self.verificar_e_avancar('COMMA'):
                    self.params()
                elif self.token_atual.tipo == 'ID' or self.token_atual.lexema == 'True' or self.token_atual.lexema == 'False':
                    raise Exception(f"Erro de sintaxe: Esperado ',' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                else:
                    return True
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'ID', 'TRUE' ou 'FALSE' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'INT' ou 'BOOLEAN' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        
    