from myLexer import lexer, handleLexerError
from rply import ParserGenerator

errorCount = []


pg = ParserGenerator(
    # A list of token names, in the order they appear in the grammar
    ['BEGIN', 'END', 'RECORD', 'CONST', 'VAR', 'TYPE', 'INTEGER', 'REAL', 'ARRAY', 'OF', 'FUNCTION', 'IF', 'THEN', 'ELSE', 'WHILE', 'WRITE', 'READ', 'FLOATNUMBER', 'NUMBER', 'STRING', 'IDENTIFIER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUAL', 'GREATERTHAN', 'LESSTHAN', 'DIFFERENT', 'LPAREN', 'RPAREN', 'LSBRACKETS', 'RSBRACKETS', 'ASSIGNMENT', 'SEMICOLON', 'COLON', 'COMMA', 'DOT'],

    # A list of precedence rules with ascending precedence levels
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MULTIPLY', 'DIVIDE']),
    ]
)

@pg.production('program : declarations main')
def program(p):
    pass

@pg.production('declarations :')
def declarations_empty(p):
    pass

@pg.production('declarations : declarations declaration')
def declarations(p):
    pass

@pg.production('declaration : const_declaration')
@pg.production('declaration : type_declaration')
@pg.production('declaration : var_declaration')
@pg.production('declaration : function_declaration')
def declaration(p):
    pass
#__
@pg.production('const_declaration :')
def const_declaration_empty(p):
    pass

@pg.production('const_declaration : const_definitions const_declaration')
def const_declaration(p):
    pass

@pg.production('const_definitions : CONST IDENTIFIER EQUAL constant SEMICOLON')
def const_definitions(p):
    pass

@pg.production('constant : mat_expression')
def constant_number(p):
    pass

@pg.production('constant : STRING')
def constant_floatnumber(p):
    pass
#__

@pg.production('type_declaration :')
def type_declaration_empty(p):
    pass

@pg.production('type_declaration : type_definitions type_declaration')
def type_declaration(p):
    pass

@pg.production('type_definitions : TYPE IDENTIFIER EQUAL type SEMICOLON')
def type_definitions(p):
    pass

@pg.production('type : INTEGER')
@pg.production('type : REAL')
@pg.production('type : ARRAY LSBRACKETS NUMBER RSBRACKETS OF type')
@pg.production('type : RECORD fields END')
@pg.production('type : IDENTIFIER')
def type(p):
    pass

@pg.production('fields : IDENTIFIER COLON type field_list')
def field(p):
    pass

@pg.production('field_list :')
def field_list_empty(p):
    pass

@pg.production('field_list : SEMICOLON fields field_list')
def field_list(p):
    pass
#__

@pg.production('var_declaration :')
def var_declaration_empty(p):
    pass

@pg.production('var_declaration : var_definitions var_declaration')
def var_declaration(p):
    pass

@pg.production('var_definitions : VAR IDENTIFIER id_list COLON type SEMICOLON')
def var_definitions(p):
    pass

@pg.production('id_list : COMMA IDENTIFIER id_list')
def id_list(p):
    pass

@pg.production('id_list :')
def id_list_empty(p):
    pass

#__

@pg.production('function_declaration :')
def function_declaration_empty(p):
    pass

@pg.production('function_declaration : function_definitions function_declaration')
def function_declaration(p):
    pass

@pg.production('function_definitions : FUNCTION function_name function_block')
def function_definitions(p):
    pass

@pg.production('function_name : IDENTIFIER function_params COLON type')
def function_name(p):
    pass

@pg.production('function_params : LPAREN fields RPAREN')
def function_params(p):
    pass

@pg.production('function_params :')
def function_params_empty(p):
    pass

@pg.production('function_block : var_declaration BEGIN commands commands_list END')
def function_block(p):
    pass

#__

@pg.production('main : BEGIN commands commands_list END')
def main(p):
    pass

@pg.production('commands_list :')
def commands_list_empty(p):
    pass

@pg.production('commands_list : SEMICOLON commands commands_list')
def commands_list(p):
    pass

@pg.production('commands : IDENTIFIER name ASSIGNMENT mat_expression')
@pg.production('commands : WHILE logic_expression command_block')
@pg.production('commands : IF logic_expression THEN command_block else_block')
@pg.production('commands : WRITE constant')
@pg.production('commands : READ IDENTIFIER name')
def commands(p):
    pass

@pg.production('else_block : ELSE command_block')
@pg.production('else_block :')
def else_block(p):
    pass

@pg.production('command_block : BEGIN commands commands_list END')
@pg.production('command_block : commands')
def command_block(p):
    pass

@pg.production('logic_expression : mat_expression logic_op logic_expression')
@pg.production('logic_expression : mat_expression')
def logic_expression(p):
    pass

@pg.production('mat_expression : params mat_op mat_expression')
@pg.production('mat_expression : params')
def mat_expression(p):
    pass

@pg.production('params : IDENTIFIER name')
@pg.production('params : number')
def params(p):
    pass

@pg.production('name : DOT IDENTIFIER name')
@pg.production('name : LSBRACKETS params RSBRACKETS')
@pg.production('name : LPAREN params_list RPAREN')
@pg.production('name :')
def name(p):
    pass

@pg.production('params_list : params COMMA params_list')
@pg.production('params_list : params')
@pg.production('params_list :')
def params_list(p):
    pass

@pg.production('mat_op : PLUS')
@pg.production('mat_op : MINUS')
@pg.production('mat_op : MULTIPLY')
@pg.production('mat_op : DIVIDE')
def mat_op(p):
    pass

@pg.production('logic_op : GREATERTHAN')
@pg.production('logic_op : LESSTHAN')
@pg.production('logic_op : DIFFERENT')
@pg.production('logic_op : EQUAL')
def logic_op(p):
    pass

@pg.production('number : FLOATNUMBER')
@pg.production('number : NUMBER')
def number(p):
    pass


parser = pg.build()

with open('input.txt', 'r') as file:
    tokens = lexer.lex(file.read())
    parser.parse(tokens)
    for token in tokens:
        if(token.name == 'ERROR'):
            errorCount.append(handleLexerError(token))
            continue
#        print(f'Token: {token.name.ljust(15)} Valor {token.value.ljust(15)} Linha {str(token.source_pos.lineno).ljust(10)} Coluna {str(token.source_pos.colno).ljust(10)}')
    print(errorCount)
    
    