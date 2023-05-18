from myLexer import lexer, handleLexerError
from rply import ParserGenerator
from myAST import ASTNode

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
    program_node = ASTNode('program')
    program_node.add_child(p[0])
    program_node.add_child(p[1])
    return program_node

@pg.production('declarations :')
def declarations_empty(p):
    return ASTNode('leaf')

@pg.production('declarations : declarations declaration')
def declarations(p):
    declarations_node = ASTNode('declarations')
    declarations_node.add_child(p[0])
    declarations_node.add_child(p[1])
    return declarations_node
    

@pg.production('declaration : const_declaration')
@pg.production('declaration : type_declaration')
@pg.production('declaration : var_declaration')
@pg.production('declaration : function_declaration')
def declaration(p):
    declaration_node = ASTNode('declaration')
    declaration_node.add_child(p[0])
    return declaration_node
#__
@pg.production('const_declaration :')
def const_declaration_empty(p):
    return ASTNode('leaf')

@pg.production('const_declaration : const_definitions const_declaration')
def const_declaration(p):
    const_declaration_node = ASTNode('const_declaration')
    const_declaration_node.add_child(p[0])
    const_declaration_node.add_child(p[1])
    return const_declaration_node

@pg.production('const_definitions : CONST IDENTIFIER EQUAL constant SEMICOLON')
def const_definitions(p):
    const_definitions_node = ASTNode('const_definitions')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    const_definitions_node.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    const_definitions_node.add_child(token)
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    const_definitions_node.add_child(token)
    const_definitions_node.add_child(p[3])
    token = ASTNode(p[4].name, p[4].value, p[4].source_pos)
    const_definitions_node.add_child(token)
    return const_definitions_node

@pg.production('constant : mat_expression')
def constant_number(p):
    constant_number_node = ASTNode('constant_number')
    constant_number_node.add_child(p[0])

@pg.production('constant : STRING')
def constant_string(p):
    constant_string_node = ASTNode(p[0].name, p[0].value, source_pos=p[0].source_pos)
    return constant_string_node
#__

@pg.production('type_declaration :')
def type_declaration_empty(p):
    return ASTNode('leaf')

@pg.production('type_declaration : type_definitions type_declaration')
def type_declaration(p):
    type_declaration = ASTNode('type_declaration')
    type_declaration.add_child(p[0])
    type_declaration.add_child(p[1])
    return type_declaration

@pg.production('type_definitions : TYPE IDENTIFIER EQUAL type SEMICOLON')
def type_definitions(p):
    type_definitions = ASTNode('type_definitions')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    type_definitions.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    type_definitions.add_child(token)
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    type_definitions.add_child(token)
    type_definitions.add_child(p[3])
    token = ASTNode( p[4].name, p[4].value, p[4].source_pos)
    type_definitions.add_child(token)
    return type_definitions

@pg.production('type : INTEGER')
@pg.production('type : REAL')
@pg.production('type : IDENTIFIER')
def type_single(p):
    type = ASTNode('type')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    type.add_child(token)
    return type

@pg.production('type : ARRAY LSBRACKETS NUMBER RSBRACKETS OF type')
def type_array(p):
    type = ASTNode('type')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    type.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    type.add_child(token)
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    type.add_child(token)
    token = ASTNode(p[3].name, p[3].value, p[3].source_pos)
    type.add_child(token)
    token = ASTNode(p[4].name, p[4].value, p[4].source_pos)
    type.add_child(token)
    type.add_child(p[5])
    return type

@pg.production('type : RECORD fields END')
def type_record(p):
    type = ASTNode('type')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    type.add_child(token)
    type.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    type.add_child(token)
    return type

@pg.production('fields : IDENTIFIER COLON type field_list')
def field(p):
    field = ASTNode('field')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    field.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    field.add_child(token)
    field.add_child(p[2])
    field.add_child(p[3])
    return field

@pg.production('field_list :')
def field_list_empty(p):
    return ASTNode('leaf')

@pg.production('field_list : SEMICOLON fields field_list')
def field_list(p):
    field_list = ASTNode('field_list')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    field_list.add_child(token)
    field_list.add_child(p[1])
    field_list.add_child(p[2])
    return field_list
#__

@pg.production('var_declaration :')
def var_declaration_empty(p):
    return ASTNode('leaf')

@pg.production('var_declaration : var_definitions var_declaration')
def var_declaration(p):
    var_declaration = ASTNode('var_declaration')
    var_declaration.add_child(p[0])
    var_declaration.add_child(p[1])
    return var_declaration

@pg.production('var_definitions : VAR IDENTIFIER id_list COLON type SEMICOLON')
def var_definitions(p):
    var_definitions = ASTNode('var_definitions')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    var_definitions.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    var_definitions.add_child(token)
    var_definitions.add_child(p[2])
    token = ASTNode(p[3].name, p[3].value, p[3].source_pos)
    var_definitions.add_child(token)
    var_definitions.add_child(p[4])
    token = ASTNode(p[5].name, p[5].value, p[5].source_pos)
    var_definitions.add_child(token)
    return var_definitions

@pg.production('id_list : COMMA IDENTIFIER id_list')
def id_list(p):
    id_list = ASTNode('id_list')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    id_list.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    id_list.add_child(token)
    id_list.add_child(p[2])
    return id_list

@pg.production('id_list :')
def id_list_empty(p):
    return ASTNode('leaf')

#__

@pg.production('function_declaration :')
def function_declaration_empty(p):
    return ASTNode('leaf')

@pg.production('function_declaration : function_definitions function_declaration')
def function_declaration(p):
    function_declaration = ASTNode('function_declaration')
    function_declaration.add_child(p[0])
    function_declaration.add_child(p[1])
    return function_declaration

@pg.production('function_definitions : FUNCTION function_name function_block')
def function_definitions(p):
    function_definitions = ASTNode('function_definitions')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    function_definitions.add_child(token)
    function_definitions.add_child(p[1])
    function_definitions.add_child(p[2])
    return function_definitions

@pg.production('function_name : IDENTIFIER function_params COLON type')
def function_name(p):
    function_name = ASTNode('function_name')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    function_name.add_child(token)
    function_name.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    function_name.add_child(token)
    function_name.add_child(p[3])
    return function_name

@pg.production('function_params : LPAREN fields RPAREN')
def function_params(p):
    function_params = ASTNode('function_params')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    function_params.add_child(token)
    function_params.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    function_params.add_child(token)
    return function_params

@pg.production('function_params :')
def function_params_empty(p):
    return ASTNode('leaf')

@pg.production('function_block : var_declaration BEGIN commands commands_list END')
def function_block(p):
    function_block = ASTNode('function_block')
    function_block.add_child(p[0])
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    function_block.add_child(token)
    function_block.add_child(p[2])
    function_block.add_child(p[3])
    token = ASTNode(p[4].name, p[4].value, p[4].source_pos)
    function_block.add_child(token)
    return function_block

#__

@pg.production('main : BEGIN commands commands_list END')
def main(p):
    main_node = ASTNode('main')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    main_node.add_child(token)
    main_node.add_child(p[1])
    main_node.add_child(p[2])
    token = ASTNode(p[3].name, p[3].value, p[3].source_pos)
    main_node.add_child(token)
    return main_node

@pg.production('commands_list :')
def commands_list_empty(p):
    return ASTNode('leaf')

@pg.production('commands_list : SEMICOLON commands commands_list')
def commands_list(p):
    commands_list = ASTNode('commands_list')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_list.add_child(token)
    commands_list.add_child(p[1])
    commands_list.add_child(p[2])
    return commands_list

@pg.production('commands : IDENTIFIER name ASSIGNMENT mat_expression')
def commands_assign(p):
    commands_assign = ASTNode('commands_assign')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_assign.add_child(token)
    commands_assign.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    commands_assign.add_child(token)
    commands_assign.add_child(p[3])
    return commands_assign

@pg.production('commands : WHILE logic_expression command_block')
def commands_while(p):
    commands_while = ASTNode('commands_while')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_while.add_child(token)
    commands_while.add_child(p[1])
    commands_while.add_child(p[2])
    return commands_while

@pg.production('commands : IF logic_expression THEN command_block else_block')
def commands_if(p):
    commands_if = ASTNode('commands_if')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_if.add_child(token)
    commands_if.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    commands_if.add_child(token)
    commands_if.add_child(p[3])
    commands_if.add_child(p[4])
    return commands_if

@pg.production('commands : WRITE constant')
def commands_write(p):
    commands_write = ASTNode('commands_write')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_write.add_child(token)
    commands_write.add_child(p[1])
    return commands_write

@pg.production('commands : READ IDENTIFIER name')
def commands_read(p):
    commands_read = ASTNode('commands_read')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    commands_read.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    commands_read.add_child(token)
    commands_read.add_child(p[2])
    return commands_read

@pg.production('else_block : ELSE command_block')
def else_block(p):
    else_block = ASTNode('else_block')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    else_block.add_child(token)
    else_block.add_child(p[1])
    return else_block

@pg.production('else_block :')
def else_block_empty(p):
    return ASTNode('leaf')

@pg.production('command_block : BEGIN commands commands_list END')
def command_block(p):
    command_block = ASTNode('command_block')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    command_block.add_child(token)
    command_block.add_child(p[1])
    command_block.add_child(p[2])
    token = ASTNode(p[3].name, p[3].value, p[3].source_pos)
    command_block.add_child(token)
    return command_block


@pg.production('command_block : commands')
def command_block_single(p):
    command_block = ASTNode('command_block')
    command_block.add_child(p[0])
    return command_block


@pg.production('logic_expression : mat_expression logic_op logic_expression')
def logic_expression(p):
    logic_expression = ASTNode('logic_expression')
    logic_expression.add_child(p[0])
    logic_expression.add_child(p[1])
    logic_expression.add_child(p[2])
    return logic_expression

@pg.production('logic_expression : mat_expression')
def logic_expression_single(p):
    logic_expression = ASTNode('logic_expression')
    logic_expression.add_child(p[0])
    return logic_expression

@pg.production('mat_expression : params mat_op mat_expression')
def mat_expression(p):
    mat_expression = ASTNode('mat_expression')
    mat_expression.add_child(p[0])
    mat_expression.add_child(p[1])
    mat_expression.add_child(p[2])
    return mat_expression

@pg.production('mat_expression : params')
def mat_expression_single(p):
    mat_expression = ASTNode('mat_expression')
    mat_expression.add_child(p[0])
    return mat_expression

@pg.production('params : IDENTIFIER name')
def params(p):
    params = ASTNode('params')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    params.add_child(token)
    params.add_child(p[1])
    return params

@pg.production('params : number')
def params(p):
    params = ASTNode('params')
    params.add_child(p[0])
    return params

@pg.production('name : DOT IDENTIFIER name')
def name(p):
    name = ASTNode('name')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    name.add_child(token)
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    name.add_child(token)
    name.add_child(p[2])
    return name

@pg.production('name : LSBRACKETS params RSBRACKETS')
@pg.production('name : LPAREN params_list RPAREN')
def name_block(p):
    name_block = ASTNode('name')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    name_block.add_child(token)
    name_block.add_child(p[1])
    token = ASTNode(p[2].name, p[2].value, p[2].source_pos)
    name_block.add_child(token)
    return name_block

@pg.production('name :')
def name_empty(p):
    return ASTNode('leaf')

@pg.production('params_list : params COMMA params_list')
def params_list(p):
    params_list = ASTNode('params_list')
    params_list.add_child(p[0])
    token = ASTNode(p[1].name, p[1].value, p[1].source_pos)
    params_list.add_child(token)
    params_list.add_child(p[2])
    return params_list

@pg.production('params_list : params')
def params_list_single(p):
    params_list_single = ASTNode('params_list')
    params_list_single.add_child(p[0])
    return params_list_single

@pg.production('params_list :')
def params_list_empty(p):
    return ASTNode('leaf')

@pg.production('mat_op : PLUS')
@pg.production('mat_op : MINUS')
@pg.production('mat_op : MULTIPLY')
@pg.production('mat_op : DIVIDE')
def mat_op(p):
    mat_op = ASTNode('mat_op')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    mat_op.add_child(token)
    return mat_op

@pg.production('logic_op : GREATERTHAN')
@pg.production('logic_op : LESSTHAN')
@pg.production('logic_op : DIFFERENT')
@pg.production('logic_op : EQUAL')
def logic_op(p):
    logic_op = ASTNode('logic_op')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    logic_op.add_child(token)
    return logic_op

@pg.production('number : FLOATNUMBER')
@pg.production('number : NUMBER')
def number(p):
    number = ASTNode('number')
    token = ASTNode(p[0].name, p[0].value, p[0].source_pos)
    number.add_child(token)
    return number

parser = pg.build()

def print_ast(node, indent=''):
    if node is None:
        return
    print(f'{indent}Type: {node.type}')
    if node.value is not None:
        print(f'{indent}Value: {node.value}')
    if node.source_pos is not None:
        print(f'{indent}Source Position: Line {node.source_pos.lineno}, Column {node.source_pos.colno}')
    if node.children:
        print(f'{indent}Children:')
        for child in node.children:
            print_ast(child, indent + '  ')

with open('input.txt', 'r') as file:
    tokens = lexer.lex(file.read())
    ast = parser.parse(tokens)
    for token in tokens:
        if(token.name == 'ERROR'):
            errorCount.append(handleLexerError(token))
            continue
#        print(f'Token: {token.name.ljust(15)} Valor {token.value.ljust(15)} Linha {str(token.source_pos.lineno).ljust(10)} Coluna {str(token.source_pos.colno).ljust(10)}')
    print(errorCount)
    print_ast(ast)
    
    