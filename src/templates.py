#///////////////////////////////////////////////////////////////////////////////
#/// 'templates' module
#///
#/// Code templates for the code generator module.
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
parser_call = """\
    return %s( input , pos )
"""

lit_call = """\
    return __parse_lit( input , prod_name , pos , "%s" )
"""

std_call = """\
    return __std__parse_%s( input , prod_name , pos )
"""

string_parser = """\
def _parse_%s( input , prod_name , pos ):
    return parse_%s( input , pos )
"""

literal_parser = """\
def _parse_%s( input , prod_name , pos ):
    return __parse_lit( input , prod_name , pos , "%s" )
"""

std_parser = """\
def _parse_%s( input , prod_name , pos ):
    return __std__parse_%s( input , prod_name , pos )
"""

star_parser = """\
def _parse_%s( input , prod_name , pos ):
    parent = parse_node.Node()
    while True:
        ( child , next ) = _parse_%s( input , prod_name , pos )
        if child == None:
            return ( parent , pos )
        __add_child_flattened( parent , child )
        pos = next
"""

star_call = """\
    return _parse_%s( input , prod_name , pos )
"""

plus_parser = """\
def _parse_%s( input , prod_name , pos ):
    parent = parse_node.Node()
    ( first , next ) = _parse_%s( input , prod_name , pos )
    if first == None:
        return ( None , next )
    __add_child_flattened( parent , first )
    pos = next
    while True:
        ( child , next ) = _parse_%s( input , prod_name , pos )
        if child == None:
            return ( parent , pos )
        __add_child_flattened( parent , child )
        pos = next
"""

plus_call = """\
    return _parse_%s( input , prod_name , pos )
"""

sub_parser_def = """\
def _parse_%s( input , prod_name , pos ):
"""

seq_call = """\
    ( child , next ) = _parse_%s( input , prod_name , pos )
    if child == None:
        return ( None , next )
    __add_child_flattened( parent , child )
    pos = next
"""

seq_call_end = """\
    return ( parent , next )
"""

seq_parser = """\
def _parse_%s( input , prod_name , pos ):
    parent = parse_node.Node()
"""

alt_call = """\
    ( child , next ) = _parse_%s( input , prod_name , pos )
    if child != None:
        return ( child , next )
"""

alt_call_end = """\
    return ( None , next )
"""

opt_call = """\
    ( child , next ) = _parse_%s( input , prod_name , pos )
    if child != None:
        return ( child , next )
"""

opt_call_end = """\
    return ( parse_node.Node( prod_name ) , next )
"""

prod_parser = """\
def %s( input , pos=0 ):
    ( child , next ) = _parse_%s( input , "%s" , pos )
    if child == None:
        return ( None , next )
    child.set_name( "%s" )
    return ( child , next )
"""

