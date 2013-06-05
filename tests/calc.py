import sys
sys.path.append( "../src" )

import pyglow

# Calculator grammar definition
calc_grammar = \
"""
group  ::= '(' expr ')'
factor ::= <real> | <integer> | group
term   ::= factor ( ( '*' | '/' ) factor )*
expr   ::= term ( ( '+' | '-' ) term )*
"""

# Compile and execute the grammar
# This will augment the environment with various functions, including "parse()"
exec( pyglow.compile_bytecode( calc_grammar ) )

# Functions to evaluate the parse tree of the expressions
def eval_expr( tree ):
    children = tree.get_children()
    term = eval_term( children[0] )
    for i in range( 1, len(children)-1, 2 ):
        op = children[i].get_value()
        other_term = eval_term( children[i+1] )
        if op == '+':
            term += other_term
        elif op == '-':
            term -= other_term
    return term

def eval_term( tree ):
    children = tree.get_children()
    term = eval_factor( children[0] )
    for i in range( 1, len(children)-1, 2 ):
        op = children[i].get_value()
        other_factor = eval_factor( children[i+1] )
        if op == '*':
            term *= other_factor
        elif op == '/':
            term /= other_factor
    return term    

def eval_factor( tree ):
    child = tree.get_children()[0]
    child_name = child.get_name()
    if child_name == "real":
        return float( child.get_value() )
    elif child_name == "integer":
        return int( child.get_value() )
    elif child_name == "group":
        return eval_expr( child.get_children()[1] )

# Read-eval-print loop
while True:
    try:
        value = raw_input( "Enter an expression ('q' to quit): " )
    except EOFError:
        break

    if value.lower() == "q":
        break

    try:
        # Call the generated parsing function
        expr_tree = parse( value, expr )
        if expr_tree == None:
            continue

        print "Expression tree:"
        print parse_node.to_xml( expr_tree )
        print "Result: ", eval_expr( expr_tree )
    except Exception, e:
        print e

