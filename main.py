from Lexer.lexer import Lexer
from Parser.Parser import Parser
from Parser.ThreeAddressCode import ThreeAddressCode

def main():     
   
    with open('codigo.rf', 'r') as file:
        codigo_fonte = file.read()

    lexer = Lexer(codigo_fonte)
    tokens = lexer.analisar()

    parser = Parser(tokens)
    print(parser.tokens)
    parser.parse()
    parser.Semantica()
    
    print('\n')
    print(parser.tabelaDeSimbolos)
    print('\n')

    tac = ThreeAddressCode()
    tac.generate_code(parser.tabelaDeSimbolos)
    tac.print_instructions()
    

if __name__ == "__main__":
    main()
