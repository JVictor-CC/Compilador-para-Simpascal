from lark import Visitor,Tree, Token

class SimpascalVisitor(Visitor):

    def __init__(self):
        self.errors = []
        self.symbol_table = []
        self.current_scope = 'global'

    def print_symbol_table(self):
        for symbol in self.symbol_table:
            for key, value in symbol.items():
                print(f"{key}: {value}")
            print("-" * 40)

    def print_line_by_line(self):
        for i, symbol in enumerate(self.symbol_table, start=1):
            print(f"Line {i}:")
            print(symbol)  # Add a blank line between symbols


    def add_symbol(self, name='', classif='', type='', value='', scope='', quant='', order='', ref=''):
            self.symbol_table.append({
            'nome': name,
            'classif':classif,
            'tipo': type,
            'valor': value,
            'escopo': scope,
            'quantidade': quant,
            'ordem': order,
            'ref': ref
        })

    def add_errors(self, error):
            self.errors.append(error)
    
    def lookup(self, symbol_name, symbol_line, symbol_scope='global'):
        for symbol in self.symbol_table:
            if symbol['nome'] == symbol_name and ((symbol['escopo'] == symbol_scope) or (symbol['escopo'] == 'global')): 
                return symbol
                           
        self.add_errors(f"O Identificador '{symbol_name}' não foi declarado na linha: {symbol_line}")
        return None
    
    def check_field(self, symbol_name, symbol_line, symbol_classif):
        for symbol in self.symbol_table:
            if symbol['nome'] == symbol_name and symbol['classif'] == symbol_classif : 
                return symbol
        self.add_errors(f"O identificador {symbol_name} não é um campo de record, na linha: {symbol_line}")
        return None
###################################################

    def const_definitions(self, node):
        symbol_name = node.children[0].value
        symbol_type_value = eval(self.get_const_types(node.children[1]))
        self.add_symbol(symbol_name, 'const', type(symbol_type_value).__name__, symbol_type_value, 'global')
        
    def get_const_types(self, node, aux=None):
        if aux is None:
            aux = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type in ['INT', 'FLOAT', 'PLUS', 'MINUS', 'MULT', 'DIV']:
                        aux.append(child.value)
                    if child.type == 'IDENTIFIER':
                        value = self.lookup(child.value, child.line, self.current_scope)
                        if value is not None and value['valor'] != None:
                            aux.append(str(value['valor']))
                        else:
                            aux.append('0')
                elif isinstance(child, Tree):
                    self.get_const_types(child, aux)
        return ''.join(aux)
    
    ####################################

    def type_definitions(self, node):
        symbol_name = node.children[0].value
        if node.children[1].children[0].type == 'IDENTIFIER':
            value = self.lookup(node.children[1].children[0].value,node.children[1].children[0].line, self.current_scope)
            if value is not None:
                self.add_symbol(symbol_name, 'var', value['tipo'], value['valor'],'global', ref=value['nome'] )
        symbol_type = self.get_type(node)
        if symbol_type is not None:
            if symbol_type in ['INT', 'FLOAT']:
                self.add_symbol(symbol_name, 'var', symbol_type.swapcase(), None, 'global')
            elif symbol_type.children[0].type == 'RECORD':
                record_info = self.get_record(symbol_type)
                self.add_symbol(symbol_name, 'record', 'record', None, 'global')
                if len(record_info) != 0:
                    for i in range(0,len(record_info),2):
                        type = record_info[i+1]
                        if type == 'real':
                            type = 'float'
                        elif type == 'integer':
                            type = 'int'
                        self.add_symbol(record_info[i], 'field', type, None, symbol_name, order=(i+2)/2)
            elif symbol_type.children[0].type == 'ARRAY':
                array_type = self.get_array(symbol_type)
                if array_type == 'real':
                    array_type = 'float'
                elif array_type == 'integer':
                    array_type = 'int'
                self.add_symbol(symbol_name, 'array', array_type, [], 'global', symbol_type.children[1].value)
        
    def get_array(self, node):
        if isinstance(node, Token):
            if node.type in ['INTEGER', 'REAL']:
                return node.value
            elif node.type == 'IDENTIFIER':
                self.lookup(node.value, node.line, self.current_scope)
                return node.value
        if isinstance(node, Tree):
            for child in node.children:
                found_type = self.get_array(child)
                if found_type is not None:
                    return found_type
        return None

    def get_record(self, node, aux = None):
        if aux is None:
            aux = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type == "IDENTIFIER" and len(aux)%2 == 0:
                        aux.append(child.value)
                    elif child.type in ['INTEGER', 'REAL']:
                        aux.append(child.value)
                    elif child.type == 'IDENTIFIER':
                        aux.append(child.value)
                        self.lookup(child.value, child.line, self.current_scope)
                elif isinstance(child, Tree):
                    self.get_record(child, aux)
        return aux

    def get_type(self, node):
        if isinstance(node, Tree): 
            if node.children[0].type in ['RECORD','ARRAY']:
                return node 
            else: 
                for child in node.children:
                    found_type = self.get_type(child)
                    if found_type is not None:
                        return found_type
        else:
            if node.type == "INTEGER":
                return 'INT'
            elif node.type == 'REAL':
                return 'FLOAT'
        return None

############################################################       


    def var_definitions(self, node):
        symbol_name = self.get_vars(node)
        symbol_type = self.get_definitions_type(node)
        if symbol_type == None:
            value = self.lookup(symbol_name[-1], node.children[0].line, self.current_scope)
            if value is not None:
                for i in range(len(symbol_name)-1) :
                    self.add_symbol(symbol_name[i], value['classif'], value['tipo'], value['valor'], self.current_scope, value['quantidade'], value['ordem'], value['nome'])
        elif symbol_type in ['int', 'float']:
            for i in range(len(symbol_name)) :
                    self.add_symbol(symbol_name[i], 'var', symbol_type, None, self.current_scope)
        elif symbol_type.children[0].type == 'RECORD':
                record_info = self.get_record(symbol_type)
                for i in range(len(symbol_name)) :
                    self.add_symbol(symbol_name[i], 'record', 'record', None, self.current_scope)
                    if len(record_info) != 0:
                        for j in range(0,len(record_info),2):
                            type = record_info[j+1]
                            if type == 'real':
                                type = 'float'
                            elif type == 'integer':
                                type = 'int'
                            self.add_symbol(record_info[j], 'field', type, None, symbol_name[i], order=(j+2)/2)
        elif symbol_type.children[0].type == 'ARRAY':
                array_info = self.get_array(symbol_type)
                if array_info == 'real':
                    array_info = 'float'
                elif array_info == 'integer':
                    array_info = 'int'
                    self.add_symbol(record_info[i], 'array', array_info, [], self.current_scope, symbol_type.children[1].value)

    
    def get_definitions_type(self, node):
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type == 'INTEGER':
                        return 'int'
                    elif child.type == 'REAL':
                        return 'float'
                    elif child.type in ['ARRAY', 'RECORD']:
                        return node
                else:
                    type_found = self.get_definitions_type(child)
                    if type_found is not None:
                        return type_found
        return None


    def get_vars(self, node, id=None):
        if id is None:
            id = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token): 
                    if child.type == 'IDENTIFIER':
                        id.append(child.value)
                self.get_vars(child, id)
        return id
#################################################################
    
    def function_name(self,node):
        self.current_scope = node.children[0].value
        symbol_type = self.get_functions_type(node.children[2])
        symbol_params = self.get_function_params(node.children[1])
        self.add_symbol(node.children[0].value, 'function', symbol_type, None, 'global', int(len(symbol_params)/2))
        self.add_symbol('result', 'result', symbol_type, None, self.current_scope)
        if symbol_params != None:
            for i in range(0,len(symbol_params),2):
                type = symbol_params[i+1] 
                if type == 'real':
                    type = 'float'
                elif type == 'integer':
                    type = 'int'
                self.add_symbol(symbol_params[i], 'param', type, None, node.children[0].value, order=(i+2)/2)
                
    
    def get_function_params(self, node, aux=None):
        if aux is None:
            aux = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type == "IDENTIFIER" and len(aux)%2 == 0:
                        aux.append(child.value)
                    elif child.type in ['INTEGER', 'REAL']:
                        aux.append(child.value)
                    elif child.type == 'IDENTIFIER':
                        value = self.lookup(child.value, child.line, self.current_scope)
                        if value is not None:
                            aux.append(value['tipo'])
                        else:
                            aux.append(child.value)
                elif isinstance(child, Tree):
                    self.get_function_params(child, aux)
        return aux

    def get_functions_type(self,node):
        if node.children[0].type == 'IDENTIFIER':
            value = self.lookup(node.children[0].value, node.children[0].line, self.current_scope)
            if value is not None:
                return value['tipo']
            else:
                return node.children[0].value
        elif node.children[0].type == 'INTEGER':
            return 'int'
        elif node.children[0].type == 'REAL': 
            return 'float'
        else: 
            self.add_errors(f"O tipo '{node.children[0].type}' não pode ser definido para uma função, na linha: {node.children[0].line}")

#####################################################

    def commands(self, node):
        if node.children[0].type == 'IDENTIFIER':
            id = self.lookup(node.children[0].value, node.children[0].line, self.current_scope)
            isValid = self.get_command_types(node.children[2])
            if len(isValid) != 0:
                for name in isValid:
                    value = self.lookup(name, node.children[0].line, self.current_scope)
                    if value is not None and value['tipo'] != id['tipo']:
                        self.add_errors(f"Os tipos não correspondem entre '{id['nome']}' e '{name}' na linha: {node.children[0].line}")
            #print(isValid)

        elif node.children[0].type == 'READ':
            id = self.lookup(node.children[1].value, node.children[1].line, self.current_scope)
            isRecord = self.get_record_attr(node.children[2])
            if len(isRecord) != 0:
                for rec in isRecord:
                    self.check_field(rec, node.children[0].line, 'field')

    def get_record_attr(self,node, aux=None):
        if aux == None:
            aux = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type =='IDENTIFIER':
                        aux.append(child.value)
                else:
                    self.get_record_attr(child,aux)
        return aux
    
    def get_function_calls(self,node, aux=None):
        if aux == None:
            aux = []
        pass

    def get_command_types(self,node, aux=None):
        if aux == None:
            aux = []
        if isinstance(node, Tree):
            for child in node.children:
                if isinstance(child, Token):
                    if child.type =='IDENTIFIER':
                        value = self.lookup(child, child.line, self.current_scope)
                        if value is not None and value['classif'] == 'function':
                            self.get_function_calls(node)
                            aux = []
                            return None
                        else:
                            aux.append(child.value)
                    elif child.type =='INTEGER':
                        aux.append('int')
                    elif child.type =='REAL':
                        aux.append('float')
                else:
                    self.get_command_types(child, aux)
        return aux
    

    #######################################################3
    def main(self,node):
        self.current_scope = 'global'