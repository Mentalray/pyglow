#///////////////////////////////////////////////////////////////////////////////
#/// 'parse.py' module
#///
#/// From a grammar (see 'grammar.txt'), generate an abstract syntax tree
#/// that represents the input.
#///
#/// Every parser function returns the (sub-)tree and the next position
#/// to parse from.  If the parsing fails, it returns 'None' and the
#/// farthest point it was able to parse to.
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
import std_parsers

#///////////////////////////////////////////////////////////////////////////////
def _parse_token( tokens , pos , token_type ):
    if pos >= len( tokens ):
        return ( None , pos )
    t,val = tokens[pos]
    if t != token_type:
        return ( None , pos )
    return ( [ t , [ val ] ] , pos+1 )

def _parse_quoted_str( tokens , pos , expected = None ):
    if pos >= len( tokens ):
        return ( None , pos )
    tok = tokens[pos]
    if tok[0] != "LIT":
        return ( None , pos )
    val = tok[1]
    val = val[1:len(val)-1] # remove quotes
    if expected != None and val != expected:
        return ( None , pos )
    return ( [ "LIT" , [ val ] ] , pos+1 )

def _parse_std( tokens , pos ):
    if pos >= len( tokens ):
        return ( None , pos )
    tok = tokens[pos]
    if tok[0] != "STD":
        return ( None , pos )
    val = tok[1]
    val = val[1:len(val)-1] # remove brackets
    if not std_parsers.std_parsers.has_key( val ):
        err = "Unknown parser: %s", val
        raise Exception, err
    return ( [ "STD" , [ val ] ] , pos+1 )

def _parse_str( tokens , pos , expected = None ):
    if pos >= len( tokens ):
        return ( None , pos )
    t,val = tokens[pos]
    if t != "STR":
        return ( None , pos )
    if expected != None and val != expected:
        return ( None , pos )
    return ( [ t , [ val ] ] , pos+1 )

def _parse_term( tokens , pos ):
    return _parse_quoted_str( tokens , pos )

def _parse_nonterm( tokens , pos ):
    return _parse_str( tokens , pos )

def _parse_val( tokens , pos ):
    ( std , next ) = _parse_std( tokens , pos )
    if std != None:
        return ( std , next )
    ( term , next ) = _parse_term( tokens , pos )
    if term != None:
        return ( term , next )
    old_next = next
    ( nonterm , next ) = _parse_nonterm( tokens , pos )
    if nonterm != None:
        return ( nonterm , next )
    return ( None , max( next , old_next ) )

def _parse_group( tokens , pos ):
    ( lit , next ) = _parse_token( tokens , pos , "LPAR" )
    if lit == None:
        return ( None , next )
    pos = next
    ( alt , next ) = _parse_alt( tokens , pos )
    if alt == None:
        return ( None , next )
    pos = next
    ( lit , next ) = _parse_token( tokens , pos , "RPAR" )
    if lit == None:
        return ( None , next )
    return ( alt , next )

def _parse_mul( tokens , pos ):
    ( lit , next ) = _parse_token( tokens , pos , "STAR" )
    if lit != None:
        return ( "STAR" , next )
    ( lit , next ) = _parse_token( tokens , pos , "PLUS" )
    if lit != None:
        return ( "PLUS" , next )
    ( lit , next ) = _parse_token( tokens , pos , "OPT" )
    if lit != None:
        return ( "OPT" , next )
    return ( None , next )
    
def _parse_def( tokens , pos ):
    ( group , next ) = _parse_group( tokens , pos )
    item = None
    if group == None:
        ( val , next ) = _parse_val( tokens , pos )
        if val == None:
            return ( None , next )
        item = val
    else:
        item = group
    pos = next
    ( mul , next ) = _parse_mul( tokens , pos )
    if mul == None:
        return ( [ item ] , next )
    else:
        return ( [ mul , [ item ] ] , next )

def _parse_def_seq( tokens , pos ):
    defs = []
    ( _def , next ) = _parse_def( tokens , pos )
    if _def == None:
        return ( None , next )
    pos = next
    defs.append( _def )
    while True:
        ( _def , next ) = _parse_def( tokens , pos )
        if _def == None:
            next = pos
            break
        pos = next
        defs.append( _def )
    return ( [ "DEF_SEQ" , defs ] , next )

def _parse_alt( tokens , pos ):
    alts = []
    ( def_seq , next ) = _parse_def_seq( tokens , pos )
    if def_seq == None:
        return ( None , next )
    pos = next
    alts.append( def_seq )
    while True:
        ( lit , next ) = _parse_token( tokens , pos , "OR" )
        if lit == None:
            next = pos
            break
        pos = next
        ( def_seq , next ) = _parse_def_seq( tokens , pos )
        if def_seq == None:
            return ( None , next )        
        pos = next
        alts.append( def_seq )
    return ( [ "ALT" , alts ] , next )

def _parse_nonterm( tokens , pos ):
    return _parse_str( tokens , pos )

def _parse_prod( tokens , pos ):
    ( nonterm , next ) = _parse_nonterm( tokens , pos )
    if nonterm == None:
        return ( None , next )
    pos = next
    ( lit , next ) = _parse_token( tokens , pos , "SEP" )
    if lit == None:
        return ( None , next )
    pos = next
    ( result , next ) = _parse_alt( tokens , pos )
    if result == None:
        return ( None , next )
    return ( [ "PROD" , [ nonterm , result ] ] , next )

def _parse_productions( prods ):
    children = []
    for tokens in prods:
        ( tree , next ) = _parse_prod( tokens , 0 )
        if tree == None:
            if next < len( tokens ):
                print "Missing token after %d (%s)" % (next,tokens[next])
            else:
                print "Parsing error near token %d" % next
            return None
        children.append( tree )
        pos = next
    return [ "PRODUCTIONS" , children ]

#///////////////////////////////////////////////////////////////////////////////
def parse( prods ):
    return _parse_productions( prods )

#///////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    import sys , lexer
    if len(sys.argv) <= 1:
        print "Usage: python parse.py <input_filename>"
        sys.exit( 1 )
    input = open( sys.argv[1] , 'r' ).read()
    prods = input.split( '\n' )
    prods_tokens = []
    for p in prods:
        tokens = lexer.lexer( p )
        if len( tokens ) > 0:
            prods_tokens.append( list( tokens ) )
    print parse( prods_tokens )
