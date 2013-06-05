#///////////////////////////////////////////////////////////////////////////////
#/// 'std_parsers' module
#///
#/// Standard parsers.
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
std_parsers = { }

std_parsers[ "eat_spaces" ] = """\
__spaces = string.whitespace

def set_spaces( spaces ):
    global __spaces
    __spaces = spaces

def __eat_spaces( input , pos ):
    global __spaces
    while pos < len(input) and input[pos] in __spaces:
        pos += 1
    return pos
"""

std_parsers[ "add_child_flattened" ] = """\
def __add_child_flattened( tree , node ):
    if node.get_name() == "":
        for child in node.get_children():
            __add_child_flattened( tree , child )
    else:
        tree.add_child( node )
"""

std_parsers[ "parse_lit" ] = """\
def __parse_lit( input , prod_name , pos , lit ):
    pos_backup = pos
    pos = __eat_spaces( input , pos )
    if input[pos:pos+len(lit)] != lit:
        return [ None , pos_backup ]
    pos += len(lit)
    return ( parse_node.Node( prod_name , lit ) , pos )
"""

std_parsers[ "regex" ] = """\
def __std__parse_from_regex( input , prod_name , pos , regex ):
    if pos >= len( input ):
        return ( None , pos )
    pos_backup = pos
    pos = __eat_spaces( input , pos )
    m = regex.search( input[pos:] )
    if m == None or m.start() != 0:
        return ( None , pos_backup )
    return ( parse_node.Node( prod_name , m.group() ) , pos+len( m.group() ) )
"""

std_parsers[ "integer" ] = """\
__integer_regex = re.compile( r"-?\d+" )
def __std__parse_integer( input , prod_name , pos ):
    global __integer_regex
    return __std__parse_from_regex( input , "integer" , pos , __integer_regex )
"""

std_parsers[ "real" ] = """\
__real_regex = re.compile( r"-?((\d*\.\d+)|(\d+\.\d*))" )
def __std__parse_real( input , prod_name , pos ):
    global __real_regex
    return __std__parse_from_regex( input , "real" , pos , __real_regex )
"""

std_parsers[ "alpha" ] = """\
__alpha_regex = re.compile( r"[a-zA-Z]" )
def __std__parse_alpha( input , prod_name , pos ):
    global __alpha_regex
    return __std__parse_from_regex( input , "alpha" , pos , __alpha_regex )
"""

std_parsers[ "lower" ] = """\
__lower_regex = re.compile( r"[a-z]" )
def __std__parse_lower( input , prod_name , pos ):
    global __lower_regex
    return __std__parse_from_regex( input , "lower" , pos , __lower_regex )
"""

std_parsers[ "upper" ] = """\
__upper_regex = re.compile( r"[A-Z]" )
def __std__parse_upper( input , prod_name , pos ):
    global __upper_regex
    return __std__parse_from_regex( input , "upper" , pos , __upper_regex )
"""

std_parsers[ "digit" ] = """\
__digit_regex = re.compile( r"[0-9]" )
def __std__parse_digit( input , prod_name , pos ):
    global __digit_regex
    return __std__parse_from_regex( input , "digit" , pos , __digit_regex )
"""

std_parsers[ "alnum" ] = """\
__alnum_regex = re.compile( r"[a-zA-Z0-9]" )
def __std__parse_alnum( input , prod_name , pos ):
    global __alnum_regex
    return __std__parse_from_regex( input , "alnum" , pos , __alnum_regex )
"""

std_parsers[ "parse" ] = """\
def parse( input , parser , skip_spaces = __spaces ):
    set_spaces( skip_spaces )
    ( child , next ) = parser( input )
    next = __eat_spaces( input , next )
    if next != len(input):
        err = "Parsing failed at position %d near\\n" % next
        err += "'" + input[next:] + "'"
        raise Exception, err
    return child
"""
