from Lexer.lexer import Lexer
from Parser.Parser import Parser

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
    

if __name__ == "__main__":
    main()
