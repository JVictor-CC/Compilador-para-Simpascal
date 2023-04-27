from rply import LexerGenerator

lg = LexerGenerator()

# Define the tokens 

lg.add('BEGIN', r'begin')
lg.add('END',r'end')
lg.add('RECORD',r'record')
lg.add('CONST',r'const')
lg.add('VAR',r'var')
lg.add('TYPE',r'type')
lg.add('INTEGER',r'integer')
lg.add('REAL',r'real')
lg.add('ARRAY',r'array')
lg.add('OF',r'of')
lg.add('FUNCTION',r'function')
lg.add('IF',r'if')
lg.add('THEN',r'then')
lg.add('ELSE',r'else')
lg.add('WHILE',r'while')
lg.add('WRITE',r'write')
lg.add('READ',r'read')
lg.add('FLOATNUMBER', r'[0-9]+\.[0-9]+')
lg.add('NUMBER', r'[0-9]+')
lg.add('STRING', r'\"[a-zA-Z0-9\' \']*\"')
lg.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MULTIPLY', r'\*')
lg.add('DIVIDE', r'/')
lg.add('EQUAL', r'=')
lg.add('GREATERTHAN',r'>')
lg.add('LESSTHAN',r'<')
lg.add('DIFFERENT',r'!')

lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('LSBRACKETS',r'\[')
lg.add('RSBRACKETS',r'\]')
lg.add('ASSIGNMENT', r':=')
lg.add('SEMICOLON', r';')
lg.add('COLON', r':')
lg.add('COMMA', r',')
lg.add('DOT', r'\.')

# Ignore
lg.ignore(r'\s+')
lg.ignore(r'\{(?:.|\n)*?\}')
lg.ignore(r'\(\*(?:.|\n)*?\*\)')
lg.ignore(r'\/\/.*')


lexer = lg.build()

with open('input.txt', 'r') as file:
    tokens = lexer.lex(file.read())

for token in tokens:
    print(f'Token: {token.name.ljust(15)} Valor {token.value.ljust(15)} Linha {str(token.source_pos.lineno).ljust(10)} Coluna {str(token.source_pos.colno).ljust(10)}')