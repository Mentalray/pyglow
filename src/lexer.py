#///////////////////////////////////////////////////////////////////////////////
#/// 'lexer' module
#///
#/// The lexer module generates tokens from an input string.
#/// Every tokens has the following form: ( token_type , lexeme ).
#///////////////////////////////////////////////////////////////////////////////

import re , string

#///////////////////////////////////////////////////////////////////////////////
token_types = [
    ( re.compile( r"::=" ) ,        "SEP"    ) ,
    ( re.compile( r"\(" ) ,         "LPAR"   ) ,
    ( re.compile( r"\)" ) ,         "RPAR"   ) ,
    ( re.compile( r"<[^>]+>" ) ,    "STD"    ) ,
    ( re.compile( r'"[^"]+"' ) ,    "LIT"    ) ,
    ( re.compile( r"'[^']+'" ) ,    "LIT"    ) ,
    ( re.compile( r"\*" ) ,         "STAR"   ) ,
    ( re.compile( r"\+" ) ,         "PLUS"   ) ,
    ( re.compile( r"\|" ) ,         "OR"     ) ,
    ( re.compile( r"\?" ) ,         "OPT"    ) ,
    ( re.compile( r"\w+" ) ,        "STR"    ) ,
    ]

#///////////////////////////////////////////////////////////////////////////////
def lexer( input ):
    tokens = []
    pos = 0
    length = len( input )
    while pos < length:
        if input[pos] in string.whitespace:
            pos += 1
            continue
        match = False
        for (r,t) in token_types:
            m = r.search( input , pos )
            if m != None and m.start() == pos:
                match = True
                tokens.append( ( t , m.group(0) ) )
                pos += ( m.end() - m.start() )
                break
        if not match:
            sample = input[pos:pos+10]
            sample = sample.replace( '\n' , ' ' )
            err = "Bad token at position %d\n" % pos
            err += "Near: '%s...'" % sample
            raise Exception, err
    return tokens

#///////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        print "Usage: python lexer.py <input_filename>"
        sys.exit( 1 )
    input = open( sys.argv[1] , 'r' ).read()
    prods = input.split( '\n' )
    for p in prods:
        print lexer( p )
