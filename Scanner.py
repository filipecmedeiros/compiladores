from utils import BLANK, is_digit, is_letter

class Scanner:

    def __init__(self, file):
        self.file = file
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.last_token = (0, "")

    def print_last_token(self):
        print ('Last Token: ', self.last_token)

    def read(self):
        c = self.file.read(1)
        if not c:
            return None
        else:
            c = str(c)

        if c == '\n':
            self.column = 1
            self.line += 1
        else:
            self.column += 1
        return c

    def print_error(self, message="default"):
        print ("Erro na linha {line}, coluna {column}. Ultimo token lido: {token} \n {message}".format(
            line=self.line, column=self.column, token=self.last_token, message=message))


    def _int(self, char):

        while(is_digit(char)):
            self.buffer = self.buffer + char
            lookahead = self.read()

            if lookahead == None:
                break
            elif lookahead == '.':
                return self._float(lookahead)

            char = lookahead
            
        return (1, self.buffer), lookahead

    def _float(self, char):
        
        self.buffer = self.buffer + char
        lookahead = self.read()

        if not is_digit(lookahead):
            self.print_error('float mal formado')
            return None, None

        char = lookahead

        while(is_digit(char)):
            self.buffer = self.buffer + char
            lookahead = self.read()

            if lookahead == None:
                break
            char = lookahead
            
        return (2, self.buffer), lookahead        

    def get_no_blank(self, char):

        while char in BLANK:
            char = self.read()
        return char



    def get_token(self, char):
        self.buffer = ""
        lookahead = None

        
        char = self.get_no_blank(char)

        if is_digit(char):
            self.last_token, lookahead = self._int(char)

        elif char == '.':
            self.last_token, lookahead = self._float(char)

        return self.last_token, lookahead








