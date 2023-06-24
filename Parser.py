from lark import Lark

simpascal_grammar = """
    program : declarations main

    declarations : declaration declarations
        |

    declaration : const_declaration
        | type_declaration
        | var_declaration
        | function_declaration

    const_declaration : const_definitions const_declaration
        |
    
    const_definitions : "const" IDENTIFIER "=" constant ";"

    constant : mat_expression
        | STRING
        
    type_declaration : type_definitions type_declaration
        |
    
    type_definitions : "type" IDENTIFIER "=" type ";"

    type : INTEGER
        | REAL
        | IDENTIFIER
        | ARRAY "[" INT "]" "of" type
        | RECORD fields "end"

    fields : IDENTIFIER ":" type field_list

    field_list : ";" fields field_list
        |

    var_declaration : var_definitions var_declaration
        |

    var_definitions : "var" IDENTIFIER id_list ":" type ";"

    id_list : "," IDENTIFIER id_list
        |

    function_declaration : function_definitions function_declaration
        |

    function_definitions : "function" function_name function_block
    
    function_name : IDENTIFIER function_params ":" type

    function_params : "(" fields ")"
        |

    function_block : var_declaration "begin" commands commands_list "end"

    main : "begin" commands commands_list "end"

    commands_list : ";" commands commands_list
        |
    
    commands : IDENTIFIER name ":=" mat_expression
        | WHILE logic_expression command_block
        | IF logic_expression "then" command_block else_block
        | WRITE constant
        | READ IDENTIFIER name

    else_block : "else" command_block
        |

    command_block : "begin" commands commands_list "end"
        | commands
    
    logic_expression : mat_expression LESSTHAN logic_expression
        | mat_expression GREATERTHAN logic_expression
        | mat_expression DIFFERENT logic_expression
        | mat_expression EQUAL logic_expression
        | mat_expression    

    mat_expression : params PLUS mat_expression
        | params MINUS mat_expression
        | params MULT mat_expression
        | params DIV mat_expression
        | params   
    
    params : IDENTIFIER name
        | FLOAT
        | INT
    
    name : DOT IDENTIFIER name
        | LSQBR params RSQBR
        | "(" params_list ")"
        |

    params_list : params "," params_list
        | params
        |

    LESSTHAN: "<"
    GREATERTHAN: ">"
    DIFFERENT: "!"
    EQUAL: "="
        
    DIV: "/"
    MULT: "*"
    MINUS: "-"
    PLUS: "+"
    INT: /[-+]?[0-9]+/
    FLOAT: /[-+]?[0-9]+\.[0-9]+/
    STRING: /"([^"\\\\]|\\\\.)*"/
    INTEGER: "integer"
    REAL: "real"
    ARRAY: "array"
    RECORD: "record"
    READ: "read"
    WRITE: "write"
    IF: "if"
    WHILE: "while"
    DOT: "."
    LSQBR: "["
    RSQBR: "]"
    
    COMMENT: /\/\/.*/
    MULTICOMMENT: /\(\*.*?\*\)/ | /\{.*?\}/

    %import common.CNAME -> IDENTIFIER
    %import common.WS
    %ignore COMMENT
    %ignore MULTICOMMENT
    %ignore WS
"""


simpascal_parser = Lark(simpascal_grammar, parser='earley', lexer='auto', start='program')
