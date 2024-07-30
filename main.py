from Lexer.lexer import Lexer
from Parser.Parser import Parser

def main():
   
    with open('codigo.rf', 'r') as file:
        codigo_fonte = file.read()

    lexer = Lexer(codigo_fonte)
    tokens = lexer.analisar()

    print(tokens)

    parser = Parser(tokens).parse()

    print(parser)

if __name__ == "__main__":
    main()
