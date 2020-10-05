import sys
from Scanner import Scanner

def main():
    with open(sys.argv[1]) as code:
        scanner = Scanner(code)
        c = code.read(1)
        i=0
        while True:
            i +=1
            print('iteration: ', i)
            if not c:
                print ("EOF")
                break
            _, c = scanner.get_token(c)
            scanner.print_last_token()
            
            

if __name__ == "__main__":
    main()

