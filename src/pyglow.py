#///////////////////////////////////////////////////////////////////////////////
#/// 'parsepy' module
#///
#/// Simple wrapper over the code generator module (codegen).
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
import lexer, parse, codegen, sys

# Save native 'compile' function
_compile = compile

#///////////////////////////////////////////////////////////////////////////////
def compile( grammar ):
    grammar = grammar.replace( '\r\n' , '\n' )
    grammar += '\n'
    prods = grammar.split( '\n' )
    prods_tokens = []
    for prod in prods:
        prod = prod.strip()
        if len( prod ) == 0:
            continue
        tokens = lexer.lexer( prod )
        if len( tokens ) > 0:
            prods_tokens.append( list( tokens ) )
    tree = parse.parse( prods_tokens )
    code = codegen.codegen( tree )
    return code

def compile_bytecode( grammar ):
    code = compile( grammar )
    return _compile( code , '<string>' , 'exec' )

#///////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    if len( sys.argv ) != 3:
        print "Usage: python pyglow.py <input_grammar.txt> <output_module.py>"
        sys.exit( 1 )
    
    file = open( sys.argv[1], 'r' )
    grammar = file.read()
    file.close()

    code = compile( grammar )
    file = open( sys.argv[2], 'w' )
    file.write( code )
    file.close()

