PyGlow 
======

PyGlow is a python parser generator.  Given a language grammar definition and an
input string, it will generate a parse tree for that string that matches the
grammar.

PyGlow is under the MIT license.

For the Impatient
-----------------

To have a quick feel of PyGlow, run the test calculator:

    % cd tests
    % python calc.py

The calculator supports basic mathematical expressions with parenthesis, such as `(1+2)*3`.

Overview
--------

PyGlow takes a grammar in a format very similar to the EBNF form and generates a parser from it.
For example, here is a classic calculator grammar which is understood by PyGlow:

    group  ::= '(' expr ')'
    factor ::= <real> | <integer> | group
    term   ::= factor ( ( '*' | '/' ) factor )*
    expr   ::= term ( ( '+' | '-' ) term )*

You can generate the parser of that grammar with the following command:

    % python pyglow.py calc_grammar.txt calc_parser.py

`calc_grammar.txt` contains the grammar definition and PyGlow will generate the
`calc_parser.py` file which should be a valid python program.  The generated
parser contains many functions, most of which you will never need to use.
However, PyGlow will also generate one parser function per 'production' in your
grammar (a production corresponds to the definition of a non-terminal in your
grammar definition).  For the calculator example, you will have the parser
functions `group()`, `factor()`, `term()` and `expr()`.

Every parser function has the same signature, for example:

    def expr( input , pos=0 ):
        ...
        return ( parse_tree , next_pos )

The `expr()` parser will parse as much of `input` as possible from `pos` and will
return a 2-tuple which contains the parse tree generated and the next position
in the input.

A generic `parse()` function is also available.  This
function takes an input string, a parser and (optionally) a list of whitespace
characters and returns the parse tree of the input.

    def parse( input , parser , whitepsaces = __spaces ):
        ...
        return parse_tree

Using this function is straightforward:

    # 'expr' is the generated parse function
    parse_tree = parse( input , expr )

This approach is recommended since the `parse()` function will throw an
exception if the input does not fully match, unlike the other parse functions
which only return the next position in the input.

Predefined parsers
------------------
The following parsers are predefined and can be used in grammar definitions.
The predefined parsers should be specified between angle brackets ( < > ).

     - <integer>
     - <real>
     - <alpha>
     - <lower>
     - <upper>
     - <digit>
     - <alnum>

PyGlow interface
----------------

The `pyglow` module provides two functions:

  - `compile( grammar )`
    Compiles the grammar (a string) and returns the generated Python code.

  - `compile_bytecode( grammar )`
    Compile the grammar (a string) and return the Python bytecode.

The latter function can be use to use the parsers on-the-spot by executing the
generated code right away.  For example:

    grammar = "a grammar definition here"
    exec( pyglow.compile_bytecode( grammar ) )
    # parse() is now available

This approach is dangerous though, as the 'exec()' call will pollute your
environment with various parsing functions that you may not be aware of.  Use
at your own risk.

You can see the 'tests/calc.py' program for an example of this technique.

Known bugs
----------

TODO


Future work
-----------

TODO

Copyright
---------

&copy; 2013 Martin Côté
