from src.Scanner import Scanner
from src.utils import token_table


class Parser:

    def __init__(self, file):
        self.sintax_is_right = True
        self.file = file
        self.token = None
        self.context = {}

    def run(self):
        with open(self.file) as code:
            self.scanner = Scanner(code)
            self.scanner.lookahead = self.scanner.read()

            while self.scanner.lookahead:
                self.program()
    
    def program (self):
        """
        <programa> ::= int main ( ) <bloco>
        """
        self.token = self.scanner.get_token()
        if self.token[0] != token_table['int']:
            self.scanner.error('Programa não iniciado por declaração de int.')

        self.token = self.scanner.get_token()
        if self.token[0] != token_table['main']:
            self.scanner.error('Função main não declarada.')

        self.token = self.scanner.get_token()
        if self.token[0] != token_table['(']:
            self.scanner.error('Parênteses não abertos.')

        self.token = self.scanner.get_token()
        if self.token[0] != token_table[')']:
            self.scanner.error('Parênteses não fechados.')

        self.token = self.scanner.get_token()
        self.code_block()
        
        self.token = self.scanner.get_token()
        if self.token:
            self.scanner.error('Programa não finalizado com fechamento de bloco de código.')

    def code_block(self):
        """
        <bloco> ::= { <decl_var>* <comando>* }
        """
        previous_context = self.context.copy()

        if self.token[0] != token_table['{']:
            self.scanner.error("Bloco de código não iniciado por '{'")

        
        self.token = self.scanner.get_token()
        while (self.token != None and self.token[0] != token_table['}']):
            
            if self.type():
                self.declaration_of_variable(self.token[1], previous_context)

            else:
                self.command()
            
            self.token = self.scanner.get_token()

        if self.token[0] != token_table['}']:
            self.scanner.error("Bloco de código não finalizado por '}'")

        print ('Context:', self.context)
        self.context = previous_context
        print ('Context', self.context)
        print ('\n\n\n')

    def declaration_of_variable(self, var_type, previous_context):
        """
        <decl_var> ::= <tipo> <id> ;
        """

        # id
        self.token = self.scanner.get_token()
        if (self.token[0] != token_table['id']):
            self.scanner.error("Token esperado: identificador")
        
        if self.token[1] in self.context.keys() and self.token[1] not in previous_context.keys():
            self.scanner.error("Variável já declarada no mesmo escopo")
        self.context[self.token[1]] = var_type

        self.token = self.scanner.get_token()
        while (self.token[0] == token_table[',']):
            self.token = self.scanner.get_token()
            if (self.token[0] != token_table['id']):
                self.scanner.error("Token esperado: identificador")
            
            if self.token[1] in self.context.keys() and self.token[1] not in previous_context.keys():
                self.scanner.error("Variável já declarada no mesmo escopo")
            self.context[self.token[1]] = var_type
            self.token = self.scanner.get_token()

        if (self.token[0] != token_table[';']):
            self.scanner.error("; esperado ao final de declaração de variável")

    def command(self):
        """
        <comando> ::= <comando_básico> | <iteração> | if ( <expr_relacional> ) <comando> else <comando>+
        """
        if (self.token[0] == token_table['id'] or self.token[0] == token_table['{']):
            self.basic_command()
        elif(self.token[0] == token_table['while']):
            self.iteration()
        elif(self.token[0] == token_table['if']):
            self.if_command()
        else:
            self.scanner.error('Bloco de comando mal formado.')


    def basic_command(self):
        """
        <comando_básico> ::= <atribuição> | <bloco>
        """
        if (self.token[0] == token_table['id']):
            if self.token[1] not in self.context:
                self.scanner.error('Uso de variável não declarada')
            self.attr()
        elif(self.token[0] == token_table['{']):
            self.code_block()

    def if_command(self):
        """
        if ( <expr_relacional> ) <comando> else <comando>+
        """
        self.token = self.scanner.get_token()
        if (self.token[0] == token_table['(']):
            self.relational_expression()
            
            if self.token[0] != token_table[')']:
                self.scanner.error('Parênteses desbalanceados no if.')
            
            self.token = self.scanner.get_token()
            self.command()

            self.token = self.scanner.get_token()
            if self.token[0] == token_table['else']:
                self.token = self.scanner.get_token()
                self.command()

        else:
            self.scanner.error('Comando if não seguido por abertura de parênteses.')

    def iteration(self):
        """
        <iteração> ::= while ( <expr_relacional> ) <comando>
        """
        self.token = self.scanner.get_token()
        if self.token[0] != token_table['(']:
            self.scanner.error('Comando while não seguido por abertura de parênteses.')
        
        self.relational_expression()

        if self.token[0] != token_table[')']:
            self.scanner.error('Parênteses desbalanceados no while.')

        self.token = self.scanner.get_token()
        self.command()

    def attr(self):
        """
        <atribuição> ::= <id> = <expr_arit> ;
        """
        self.token = self.scanner.get_token()
        if (self.token[0] == token_table['=']):
            
            self.arithmetic_expression()

            #self.token = self.scanner.get_token()
            if self.token[0] != token_table[';']:
                self.scanner.error('Esperado ; ao final de atribuição.')
        else:
            self.scanner.error('Operador de atribuição esperado.')

    def relational_expression(self):
        """
        <expr_relacional> ::= <expr_arit> <op_relacional> <expr_arit>
        """
        self.arithmetic_expression()

        self.relational_operator()

        self.arithmetic_expression()

    def relational_operator(self):
        """
        <op_relacional> ::= == | != | < | > | <= | >=
        """
        if (self.token[0] == token_table['=='] 
            or self.token[0] == token_table['!='] 
            or self.token[0] == token_table['<'] 
            or self.token[0] == token_table['>'] 
            or self.token[0] == token_table['<='] 
            or self.token[0] == token_table['>=']):
            return True
        else:
            self.scanner.error('Operador relacional esperado.')

    def arithmetic_expression(self):
        """
        <expr_arit> ::= <termo> <expr_arit_derivada>
        """
        self.term()
        self.derived_arithmetic_expression()

    def derived_arithmetic_expression(self):
        """
        <expr_arit_derivada> ::= + <termo> <expr_arit_derivada> | - <termo> <expr_arit_derivada> | null
        """
        if (self.token[0] == token_table['+'] or self.token[0] == token_table['-']):
            self.term()
            self.derived_arithmetic_expression()
        else:
            return None

    def term(self):
        """
        <termo> ::= <fator> <termo_derivado>
        """
        self.factor()
        self.derived_term()

    def derived_term(self):
        """
        <termo_derivado> ::= * <fator> <termo_derivado> | / <fator> <termo_derivado> | null
        """
        self.token = self.scanner.get_token()
        if (self.token[0] == token_table['*'] or self.token[0] == token_table['/']):
            self.factor()
            self.derived_term()
        else:
            return None

    def factor(self):
        """
        <fator> ::= ( <expr_arit> ) | <id> | <float> | <inteiro | <char>
        """
        self.token = self.scanner.get_token()
        if (self.token[0] == token_table['id'] or 
            self.token[0] == token_table['int_value'] or 
            self.token[0] == token_table['float_value'] or 
            self.token[0] == token_table['char_value']):
            return True
        elif(self.token[0] == token_table['(']):
            
            self.arithmetic_expression()

            if (self.token[0] == token_table[')']):
                return True
            else:
                self.scanner.error('Parênteses desbalanceados.')
        else:
            self.scanner.error('Esperado uma expressão aritmética, variável, valor inteiro, float ou char')

    def type(self):
        """
        <tipo> ::= int | float | char
        """
        return self.token[0] == token_table['int'] or self.token[0] == token_table['float'] or self.token[0] == token_table['char']
