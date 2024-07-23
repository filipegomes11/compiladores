from Lexer.lexer import Lexer
from Parser.Parser import Parser

def main():
    codigo_fonte = """"
    main {
        int oi = 10;
    } end
    """

    lexer = Lexer(codigo_fonte)
    tokens = lexer.analisar()

    print(tokens)

    parser = Parser(tokens).parse()

    print(parser)

if __name__ == "__main__":
    main()
