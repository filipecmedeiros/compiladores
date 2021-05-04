import sys
from src.Parser import Parser

def main():
    parser = Parser(sys.argv[1])
    parser.run()
            
if __name__ == "__main__":
    main()

