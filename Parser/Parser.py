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
            
        if self.token_atual.tipo == 'INT' or self.token_atual.tipo == 'BOOL':
            self.declaration_var()
            return True

    def declaration_var(self):
        self.avancar()
        if self.verificar_e_avancar('ID'):
                if self.verificar_e_avancar('ATB'):
                    self.end_var()
                    if self.verificar_e_avancar('SEMICOLON'):
                        return
                    else:
                        raise Exception(f"Erro de sintaxe: Esperado ';' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
                else:
                    raise Exception(f"Erro de sintaxe: Esperado '=' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
    
    def end_var(self):
        self.avancar()
        if self.verificar_e_avancar('CALL'):
            if self.verificar_e_avancar('FUNC'):
                self.call_func()

            if self.verificar_e_avancar('PROC'):
                self.call_proc()

        if self.verificar_e_avancar('BOOLEAN'):
            if self.verificar_e_avancar('True') or self.verificar_e_avancar('False'):
                return
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'True' ou 'False' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
        if self.verificar_e_avancar('NUM'):
            if self.token_atual.lexema >= '0' and self.token_atual.lexema <= '9':
                self.avancar()
                return
            else:
                raise Exception(f"Erro de sintaxe: Esperado número ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
        if self.verificar_e_avancar('ID'):
           self.identifier()

    def call_func(self):
        self.avancar()
        if self.verificar_e_avancar('CALL'):
            if self.verificar_e_avancar('FUNC'):
                return
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'FUNC' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'CALL' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
    def call_proc(self):
        self.avancar()
        if self.verificar_e_avancar('CALL'):
            if self.verificar_e_avancar('PROC'):
                return
            else:
                raise Exception(f"Erro de sintaxe: Esperado 'PROC' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'CALL' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}.")
        
    def identifier(self):
        self.avancar()
        if self.verificar_e_avancar('ID'):
            return
        else:
            raise Exception(f"Erro de sintaxe: Esperado 'ID' ao invés de '{self.token_atual.lexema}' na linha {self.token_atual.linha}..")
        
    