import sys
from Scanner import Scanner
from Parser import Parser

def main():
    parser = Parser(sys.argv[1])
    parser.run()

    """
    with open(sys.argv[1]) as code:
        scanner = Scanner(code)
        char = code.read(1)

        while char: #EOF
            _, char = scanner.get_token(char)
            scanner.print_last_token()
    """            
if __name__ == "__main__":
    main()

