from Scanner import Scanner


class Parser:

    def __init__(self, file):
        self.sintax_is_right = True
        self.file = file

    def run(self):
            with open(self.file) as code:
                self.scanner = Scanner(code)
                self.scanner.lookahead = self.scanner.read()

                while self.scanner.lookahead:
                    #self.program()
                    token = self.scanner.get_token()
                    self.scanner.print_last_token()

    def program (self):
            token, char = self.scanner.get_token()
            print (token)
            if token[1] != 'int':
                self.scanner.error('Programa não iniciado por declaração de int.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[1] != 'main':
                self.scanner.error('Função main não declarada.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[1] != '(':
                self.scanner.error('Parênteses não abertos.')

            token, char = self.scanner.get_token(char)
            print (token)
            if token[1] != ')':
                self.scanner.error('Parênteses não fechados.')

            self.code_block(char)

    def code_block(self, char):
        token, char = self.scanner.get_token(char)
        print (token)
        if token[1] != '{':
            self.scanner.error("Bloco de código não iniciado por '{'")

        # declaração de variavel
        

        # comando

        token, char = self.scanner.get_token(char)
        print (token)
        if token[1] != '{':
            self.scanner.error("Bloco de código não finalizado por '}'")
