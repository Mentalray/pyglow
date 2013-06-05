import sys
sys.path.append( "../src" )

import pyglow 

grammar = """
expr ::= 'a' 'b' 'c' ( ( 'd' ) )
"""

exec( pyglow.compile_bytecode( grammar ) )

print parse_node.to_xml( parse( "abcd" , expr ) )
