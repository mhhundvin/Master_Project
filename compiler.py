from lark import Transformer
from collections import defaultdict
from lark_parser import tree
from classes import Generatable, Group, Nonterminal, Token, Terminal, Regexp, Star, Plus, Optional, Sequence, Repeat, Literal_Range
from generate import generate
from extract_groups import extract_groups

grammar = defaultdict(list)
transformed_grammar = defaultdict(list)

class Compiler(Transformer):

    def start(self, args):
        return args

    def rule(self, args):
        grammar[args[0]] += args[-1]
    
    def token(self, args):
        grammar[args[0]] = args[-1]

    def expansions(self, args):
        lst = []
        for elem in args:
            if isinstance(elem, list):
                if len(elem) > 1:
                    raise Exception(f'Should not be a list? {elem}')
                elem = elem[0]

            if isinstance(elem, Generatable):
                lst.append(elem)                
            else:
                lst.append(Sequence( elem ))
        if len(lst) == 1:
            return lst[0]
        return lst

    
    def alias(self, args):
        return args[:-1]
    
    def expansion(self, args):
        return Sequence( args )
    
    def opexper(self, args):
        op = args[1]
        arg = args[0]
        if op == "+":
            return Plus( arg )
        elif op == "*":
            return Star( arg )
        elif op == "?":
            return Optional( Sequence( [arg, ''] ))
        else:
            print(f'OPEXPER: {op}')

    def repeat(self, args):
        return Repeat(args[0], 0, args[1])
    
    def expr_range(self, args):
        return Repeat(args[0], args[1], args[2])

    def atom(self, args):
        return args
    
    def group(self, args):
        lst = []
        for elem in args[0]:

            if isinstance(elem, Generatable):
                lst.append(elem)
            else:
                lst.append(Sequence( elem ))
        return Group( lst )

    def maybe(self, args):
        arg = args[0]
        if not isinstance(arg, list):
            arg = [arg]
        return Optional( Group( arg ))


    def value(self, args):
        return args

    def literal_range(self, args):
        return Literal_Range( args[0], args[-1] )

    def literal(self, args):
        return args[0]

    def name(self, args):
        return args[0]

    def RULE(self, args):
        if args[0] == '!' or args[0] == '_' or args[0] == '?':
            if args[1] == '_' or args[1] == '?':
                return Nonterminal( f'{args[2:]}', grammar )
            return Nonterminal( f'{args[1:]}', grammar )
        return Nonterminal( f'{args}', grammar )
    
    def TOKEN(self, args):
        if args[0] =='_':
            return Token( f'{args[1:]}', grammar )
        return Token( f'{args}', grammar )

    def STRING(self, args):
        return Terminal( args[1:-1] )

    def REGEXP(self, args):
        return Regexp( args )

Compiler().transform(tree)


print('###################################################################################################################')
no_groups_grammar = extract_groups(grammar)
print("Groups have been extracted.")
print('###################################################################################################################')
print(f'\n\n')

generate(no_groups_grammar, 10)
