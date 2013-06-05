#///////////////////////////////////////////////////////////////////////////////
#/// 'codegen' module
#///
#/// Generates python parser from the grammar in a tree form.
#///////////////////////////////////////////////////////////////////////////////

import templates, std_parsers, string

#///////////////////////////////////////////////////////////////////////////////
def escape_string( s ):
    s = s.replace( '\\' , '\\\\' )
    s = s.replace( '"' , '\\"' )
    return s

class CodeGenerator:

    def __init__( self , tab ):
        self.tab = tab
        self.helper_parsers = []

    def _tab( self ):
        return ' ' * self.tab

    def _generate_parser( self , parser_name , tree ):
        if tree[0] == "STR":
            self._generate_string_parser( parser_name , tree[1][0] )
        elif tree[0] == "LIT":
            self._generate_literal_parser( parser_name , tree[1][0] )
        elif tree[0] == "STD":
            self._generate_std_parser( parser_name , tree[1][0] )
        elif tree[0] == "STAR":
            self._generate_star_parser( parser_name , tree[1][0] )
        elif tree[0] == "PLUS":
            self._generate_plus_parser( parser_name , tree[1][0] )
        elif tree[0] == "DEF_SEQ":
            self._generate_seq_parser( parser_name , tree )
        elif tree[0] == "ALT":
            self._generate_alt_parser( parser_name , tree )
        elif tree[0] == "OPT":
            self._generate_opt_parser( parser_name , tree )
        else:
            err = "Cannot generate parser for tree: %s" % str(tree)
            raise Exception, err

    def _generate_parser_call( self , parser_name ):
        return templates.parser_call % parser_name

    def _generate_lit_call( self , string ):
        return templates.lit_call % escape_string( string )

    def _generate_std_call( self , std ):
        return templates.std_call % std

    def _generate_string_parser( self , parser_name , parser_to_call ):
        code = templates.string_parser % ( parser_name , parser_to_call )
        self.helper_parsers.append( code )

    def _generate_literal_parser( self , parser_name , lit_to_match ):
        code = templates.literal_parser % ( parser_name , lit_to_match )
        self.helper_parsers.append( code )

    def _generate_std_parser( self , parser_name , std ):
        code = templates.std_parser % ( parser_name , std )
        self.helper_parsers.append( code )

    def _generate_star_parser( self , parser_name , tree ):
        name = parser_name + "_star"
        self._generate_parser( name , tree )
        code = templates.star_parser % ( parser_name , name )
        self.helper_parsers.append( code )

    def _generate_star_call( self , parser_name ):
        return templates.star_call % parser_name

    def _generate_plus_parser( self , parser_name , tree ):
        name = parser_name + "_plus"
        self._generate_parser( name , tree )
        code = templates.plus_parser % ( parser_name , name , name )
        self.helper_parsers.append( code )

    def _generate_plus_call( self , parser_name ):
        return templates.plus_call % parser_name

    def _generate_def_parser( self , parser_name , tree ):
        code = templates.sub_parser_def % parser_name
        if len( tree ) == 0: 
            return
        while len( tree ) == 1 and type(tree[0]) == list: # flatten
            tree = tree[0]
        if tree[0] == "STR":
            string = tree[1][0]
            code += self._generate_parser_call( string )
        elif tree[0] == "LIT":
            lit = tree[1][0]
            code += self._generate_lit_call( lit )
        elif tree[0] == "STD":
            std = tree[1][0]
            code += self._generate_std_call( std )
        elif tree[0] == "STAR":
            name = parser_name + "_star"
            self._generate_star_parser( name , tree[1][0] )
            code += self._generate_star_call( name )
        elif tree[0] == "PLUS":
            name = parser_name + "_plus"
            self._generate_plus_parser( name , tree[1][0] )
            code += self._generate_plus_call( name )
        elif tree[0] == "DEF_SEQ":
            name = parser_name + "_seq"
            self._generate_parser( name , tree )
            code += self._generate_seq_call( name )
            code += self._generate_seq_call_end()
        elif tree[0] == "ALT":
            name = parser_name + "_alt"
            self._generate_parser( name , tree )
            code += self._generate_alt_call( name )
            code += self._generate_alt_call_end()
        elif tree[0] == "OPT":
            name = parser_name + "_opt"
            self._generate_parser( name , tree )
            code += self._generate_opt_call( name )
            code += self._generate_opt_call_end()
        else:
            code += "    #Cannot generate tree for: %s\n" % str( tree )
            code += "    pass\n"
        self.helper_parsers.append( code )

    def _generate_seq_call( self , parser_name ):
        return templates.seq_call % parser_name

    def _generate_seq_call_end( self ):
        return templates.seq_call_end

    def _generate_seq_parser( self , parser_name , tree ):
        code = templates.seq_parser % parser_name
        for i,_def in enumerate(tree[1]):
            name = parser_name + "_%d" % i
            self._generate_def_parser( name , _def )
            code += self._generate_seq_call( name )
        code += self._generate_seq_call_end()
        self.helper_parsers.append( code )

    def _generate_alt_call( self , parser_name ):
        return templates.alt_call % parser_name

    def _generate_alt_call_end( self ):
        return templates.alt_call_end

    def _generate_alt_parser( self , parser_name , tree ):
        if tree[0] != "ALT":
            raise Exception, "ALT required"
        code = templates.sub_parser_def % parser_name
        for i,alt in enumerate(tree[1]):
            name = parser_name + "_%d" % i
            self._generate_parser( name , alt )
            code += self._generate_alt_call( name )
        code += self._generate_alt_call_end()
        self.helper_parsers.append( code )

    def _generate_opt_call( self , parser_name ):
        return templates.opt_call % parser_name

    def _generate_opt_call_end( self ):
        return templates.opt_call_end

    def _generate_opt_parser( self , parser_name , tree ):
        if tree[0] != "OPT":
            raise Exception, "OPT required"
        code = templates.sub_parser_def % parser_name
        name = parser_name + "_0"
        self._generate_parser( name , tree[1][0] )
        code += self._generate_opt_call( name )
        code += self._generate_opt_call_end()
        self.helper_parsers.append( code )

    def _generate_prod_parser( self , parser_name , tree ):
        name = parser_name + "_prod"
        self._generate_parser( name , tree )
        code = templates.prod_parser % ( parser_name , name , parser_name , parser_name )
        self.helper_parsers.append( code )
        
    def _generate_prod( self , tree ):
        if tree[0] != "PROD":
            raise Exception, "PROD required"
        children = tree[1]
        name = children[0][1][0]
        tree = children[1]        
        self._generate_prod_parser( name , tree )

    def generate( self , tree ):
        if tree[0] != "PRODUCTIONS":
            raise Exception, "PRODUCTIONS required"

        for prod in tree[1]:
            self._generate_prod( prod )
        code = ""
        for helper in reversed(self.helper_parsers):
            code = helper + '\n' + code

        imports = [ "re" , "string" , "parse_node" ]
        import_code = ""
        for i in imports:
            import_code += "import %s\n" % i

        std_code = ""
        for std_p in std_parsers.std_parsers.itervalues():
            std_code += std_p + '\n'

        return import_code + '\n' + std_code + '\n' + code

#///////////////////////////////////////////////////////////////////////////////
def codegen( tree , tab=4 ):
    code = CodeGenerator( 0 )
    return code.generate( tree )

#///////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    import sys , lexer , parse
    if len(sys.argv) <= 1:
        print "Usage: python codegen.py <input_filename>"
        sys.exit( 1 )
    input = open( sys.argv[1] , 'r' ).read()
    prods = input.split( '\n' )
    prods_tokens = []
    for p in prods:
        tokens = lexer.lexer( p )
        if len( tokens ) > 0:
            prods_tokens.append( list( tokens ) )
    tree = parse.parse( prods_tokens )
    print "#", tree
    print "#", '-'*80
    print
    print codegen( tree )

