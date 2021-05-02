from utils import BLANK, is_digit, is_letter

class Scanner:

    def __init__(self, file):
        self.file = file
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.last_token = (None, "")
        self.char = None
        self.lookahead = None
        
        self.reserved_words = {
            'main': 22,
            'if': 23,
            'else': 24,
            'while': 25,
            'do': 26,
            'for': 27,
            'int': 28,
            'float': 29,
            'char': 30
        }


    def print_last_token(self):
            print ('Last Token: ' + str(self.last_token))


    def read(self):
        char = self.file.read(1)
        if not char:
            return None
        else:
            char = str(char)

        if char == '\n':
            self.column = 1
            self.line = self.line + 1
        else:
            self.column = self.column + 1
        
        return char        


    def error(self, message="default"):
        print ("Erro na linha {line}, coluna {column}. Ultimo token lido: {token} \n {message}".format(
            line=self.line, column=self.column, token=self.last_token, message=message))
        exit(1)


    def get_no_blank(self):

        while self.char in BLANK:
            self.char = self.read()
        return self.char


    def _int(self):

        while(is_digit(self.char)):
            self.buffer = self.buffer + self.char
            self.lookahead = self.read()

            if self.lookahead == None:
                break
            elif self.lookahead == '.':
                return self._float()

            self.char = self.lookahead
            
        return (1, self.buffer)


    def _float(self):
        
        self.buffer = self.buffer + self.lookahead
        self.lookahead = self.read()

        if not is_digit(self.lookahead):
            self.error('float mal formado')

        self.char = self.lookahead

        while(is_digit(self.char)):
            self.buffer = self.buffer + self.char
            self.lookahead = self.read()

            if self.lookahead == None:
                break
            self.char = self.lookahead
            
        return (2, self.buffer)


    def _char(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if (not is_digit(self.lookahead)) and (not is_letter(self.lookahead)):
            self.error('char mal formado')

        self.char = self.lookahead
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead != "'":
            self.error('char mal formado')

        self.char = self.lookahead
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (3, self.buffer)

    def _add(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()
        return (4, self.buffer)

    def _sub(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()
        return (5, self.buffer)

    def _mul(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()
        return (6, self.buffer)


    def _div(self):
        self.lookahead = self.read()

        if self.lookahead == '/':
            return self._one_line_comment()

        elif self.lookahead == '*':
            return self._multiline_comment()

        self.buffer = self.buffer + self.char
        return (7, self.buffer)

    
    def _one_line_comment(self):
        self.lookahead = self.read()

        while self.char != '\n':
            self.char = self.lookahead
            self.lookahead = self.read()

            if self.char is None:
                return None, None
        return self.get_token()

    
    def _multiline_comment(self):
        self.char = self.read()
        self.lookahead = self.read()
        
        if self.char == None or self.lookahead == None:
            self.error('Comentario de multilinha: fim de arquivo dentro de comentario')
        
        while (self.char+self.lookahead) != '*/':
            self.char = self.lookahead
            self.lookahead = self.read()

            if self.lookahead == None:
                self.error('Comentario de multilinha: fim de arquivo dentro de comentario')

        self.char = self.lookahead
        self.lookahead = self.read()
        return self.get_token()

    
    def _attr(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead == '=':
            return self._equal(self.lookahead)        

        return (8, self.buffer)

    
    def _equal(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (9, self.buffer)


    def _min(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead == '=':
            return self._min_equal(self.lookahead)

        return (10, self.buffer)


    def _min_equal(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (11, self.buffer)


    def _max(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead == '=':
            return self._max_equal(self.lookahead)

        return (12, self.buffer)


    def _max_equal(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (13, self.buffer)


    def _diff(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead != '=':
            self.error("operador invalido: exclamacao nao sucedida por '='")

        self.char = self.lookahead
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (14, self.buffer)

    
    def _open_parenthesis(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (15, self.buffer)

    
    def _close_parenthesis(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (16, self.buffer)


    def _open_brackets(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (17, self.buffer)


    def _close_brackets(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (18, self.buffer)


    def _comma(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (19, self.buffer)


    def _semmicolon(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        return (20, self.buffer)

    
    def _id(self):
        self.buffer = self.buffer + self.char
        self.lookahead = self.read()

        if self.lookahead is None:
            return (21, self.buffer), self.lookahead

        while is_digit(self.lookahead) or is_letter(self.lookahead) or self.lookahead == '_':
            self.char = self.lookahead
            self.buffer = self.buffer + self.char
            self.lookahead = self.read()

            if self.lookahead is None:
                if self.buffer in self.reserved_words:
                    return (self.reserved_words[self.buffer], self.buffer), self.lookahead
                else:
                    return (21, self.buffer), self.lookahead

        if self.buffer in self.reserved_words:
            return (self.reserved_words[self.buffer], self.buffer), self.lookahead
        else:
            return (21, self.buffer)

    
    def get_token(self):
        self.buffer = ""
        self.char = self.lookahead
        self.lookahead = None

        self.char = self.get_no_blank()

        if self.char is None or self.char == '\n': #EOF
            self.last_token = None
            self.lookahead = None
        elif is_digit(self.char):
            self.last_token = self._int()
        elif self.char == "'":
            self.last_token = self._char()
        elif self.char == '+':
            self.last_token = self._add()
        elif self.char == '-':
            self.last_token = self._sub()
        elif self.char == '*':
            self.last_token = self._mul()
        elif self.char == '/':
            self.last_token = self._div()
        elif self.char == '=':
            self.last_token = self._attr()
        elif self.char == '<':
            self.last_token = self._min()
        elif self.char == '>':
            self.last_token = self._max()
        elif self.char == '!':
            self.last_token = self._diff()
        elif self.char == '(':
            self.last_token = self._open_parenthesis()
        elif self.char == ')':
            self.last_token = self._close_parenthesis()
        elif self.char == '{':
            self.last_token = self._open_brackets()
        elif self.char == '}':
            self.last_token = self._close_brackets()
        elif self.char == ',':
            self.last_token = self._comma()
        elif self.char == ';':
            self.last_token = self._semmicolon()
        elif is_letter(self.char) or self.char == '_':
            self.last_token = self._id()
        else:
            self.error('Caractere invalido')

        return self.last_token
