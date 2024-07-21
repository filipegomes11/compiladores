from Lexer.lexer import Lexer  

def main():
    codigo_fonte = """"
    main {
        x = 42;
        y = 3;
        z = x + y;
        x == y
        x != y
        (x < y)
        {}
    }
    """

    lexer = Lexer(codigo_fonte)
    tokens = lexer.analisar()

    print(tokens)
if __name__ == "__main__":
    main()
