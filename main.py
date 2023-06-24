from Parser import simpascal_parser
from larkVisitor import SimpascalVisitor

with open('input.txt', 'r') as file:
    try:
        raw_code = file.read()
        tree = simpascal_parser.parse(raw_code)
        #code = SimpascalTransformer().transform(tree)
    except BaseException as e:
            print(e)

    #print(tree)
    visitor = SimpascalVisitor()
    visitor.visit_topdown(tree)
    errors = visitor.errors
    print('___________________________________________________')
    #visitor.print_symbol_table()
    print(errors)

with open('output.txt', 'w') as file:
    file.write(str(tree.pretty()))
    