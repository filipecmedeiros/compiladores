import sys
from src.Parser import Parser

def main():
    parser = Parser(sys.argv[1])
    parser.run()
    parser.close_code()
    print ("Programa compilado com êxito")
            
if __name__ == "__main__":
    main()

