from Scanner import Scanner


class Parser:

    def __init__(self, file):
        self.sintax_is_right = True
        self.file = file

    def run(self):
            with open(self.file) as code:
                self.scanner = Scanner(code)
                char = self.scanner.read()

                self.program(char)

                #token, char = self.scanner.get_token(char)

                #print (token)

    def program (self, char):
            token, char = self.scanner.get_token(char)
            print (token)
            if token[0] != 28:
                self.scanner.error('Programa não iniciado por declaração de int.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[0] != 22:
                self.scanner.error('Função main não declarada.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[0] != 15:
                self.scanner.error('Parênteses não abertos.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[0] != 16:
                self.scanner.error('Parênteses não fechados.')

            # bloco