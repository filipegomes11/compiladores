from Lexer.lexer import Lexer
from Parser.Parser import Parser

def main():
    codigo_fonte = """"
    main {
        int a = 1 + 2 + 3 * 3 / 1;
        int num1 = 0;
        b = True;
        num1 = num2;
        
        int num3 = call func soma();

        call func func0b();
        call func func1b(a);
        call func func2b(true, b);

        call proc proc0();
        call proc proc1(x);
        call proc proc2(a, b, c);

        func int soma(int a, int b) {
            int soma = a + b;
            return soma;
        }

        if (a == b) {
            int c = 10;
        } else {
            int d = 11;
        }

        print(c);

        while (c == 20) {
            int e = 10;
        }

        proc proc0() {
            int a = 0;
        }

    } end
    """

    lexer = Lexer(codigo_fonte)
    tokens = lexer.analisar()

    print(tokens)

    parser = Parser(tokens).parse()

    print(parser)

if __name__ == "__main__":
    main()
