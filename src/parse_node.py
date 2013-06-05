#///////////////////////////////////////////////////////////////////////////////
#/// 'parse_node' module
#///
#/// Parse tree representation.
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
class Node:
    def __init__( self , name = "" , value = None ):
        self.name = name
        self.value = value
        self.children = []

    def get_name( self ):
        return self.name

    def set_name( self , name ):
        self.name = name
    
    def get_value( self ):
        return self.value

    def set_value( self , value ):
        self.value = value

    def add_child( self , child ):
        self.children.append( child )

    def get_children( self ):
        return self.children

    def is_leaf( self ):
        return len( self.children ) == 0

#///////////////////////////////////////////////////////////////////////////////
def to_xml( tree ):
    
    def node_to_xml( node , indent ):
        result = ' '*indent + "<" + node.get_name() + ">\n"
        for child in node.get_children():
            result += node_to_xml( child , indent+4 )
        if node.is_leaf():
            val = str( node.get_value() )
            result += ' '*(indent+4) + "<value>" + val + "</value>\n"
        result += ' '*indent + "</" + node.get_name() + ">\n"
        return result
    
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
        node_to_xml( tree , 0 )
