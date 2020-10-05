import sys
from Scanner import Scanner

def main():
    with open(sys.argv[1]) as code:
        scanner = Scanner(code)
        char = code.read(1)

        while True:
            if not char: #EOF
                break
            _, char = scanner.get_token(char)
            scanner.print_last_token()
            
            

if __name__ == "__main__":
    main()

