from distutils.log import error
from random import choice
from lark import Transformer
from collections import defaultdict
from lark_parser import tree
from classes_3 import Generatable, Group, Nonterminal, Token, Terminal, Regexp, Star, Plus, Optional, Sequence, Repeat, Literal_Range
from split_grammar import split_grammar
from generate2 import generate
from extract_groups import extract_groups

grammar = defaultdict(list)
transformed_grammar = defaultdict(list)

class Compiler(Transformer):

    def start(self, args):
        return args

    def rule(self, args):
        grammar[args[0]] = args[-1]
    
    def token(self, args):
        grammar[args[0]] = args[-1]

    def expansions(self, args):
        # print(f'EXPANSIONS: {args}')
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
        # print(f'ALIAS: {args[:-1]}\n')
        return args[:-1]
    
    def expansion(self, args):
        # args is a list
        # print(f'EXPANSION: {args}')
        
        # if isinstance(args, list):
        #     if len(args) > 1:
        #         raise Exception(f'Should not be a list? {args}')
        #     args = args[0]
        # if isinstance(args, Generatable):
        #     return args
        # else:
        #     return Sequence( args )

        return Sequence( args )
    
    def opexper(self, args):
        # args = atop OP
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
        # print(f'expr_range {args}')
        return Repeat(args[0], args[1], args[2])

    def atom(self, args):
        return args
    
    def group(self, args):
        print(f'GROUP: {args[0]}')
        lst = []
        for elem in args[0]:
            # if isinstance(elem, list):
            #     if len(elem) > 1:
            #         raise Exception(f'Should not be a list? {elem}')
            #     elem = elem[0]

            if isinstance(elem, Generatable):
                lst.append(elem)
            else:
                lst.append(Sequence( elem ))
        # if len(lst) == 1:
        #     return lst[0]
        return Group( lst )
        # return lst

    def maybe(self, args):
        # print(f'MAYBE: {args[0]}')
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
        return Terminal( args[1:-1] )     # args[1:-1]

    def REGEXP(self, args):
        return Regexp( args )

Compiler().transform(tree)


print(f'\n\n\n\n\n\n')
print("########################################################################################################################################################")
print("########################################################################################################################################################")

print(f'\n\n\n\n\n\n')

print("########################################################################################################################################################")
print("########################################################################################################################################################")
print(f'\n\n\n\n\n\n')

# generate(grammar, 10)
extract_groups(grammar)

# no_cycle_grammar, leftover_grammar = split_grammar(grammar)

# print(f'\n\ngrammar: {len(grammar)}, no_cycle: {len(no_cycle_grammar)}, leftover: {len(leftover_grammar)}')
# print(len(no_cycle_grammar) + len(leftover_grammar) , '\n\n')

# # for k, v in grammar.items():
#     # if k.to_string() == "DIGIT":
#     #     break
#     # print(f'{k.to_string()}: {len(v)}\n')

# print()




# for k,v in grammar.items():

#     if k.to_string() == "DIGIT":
#         break

#     print(k.to_string())

#     v = "  |or|  ".join([x.to_string() for x in v])
#     print(f'\tG\t{v}')

#     if k in no_cycle_grammar.keys():
#         v1 = no_cycle_grammar[k]
#         v1 = "  |or|  ".join([x.to_string() for x in v1])
#         print(f'\tG\'\t{v1}')

#     if k in leftover_grammar.keys():
#         v2 = leftover_grammar[k]
#         v2 = "  |or|  ".join([x.to_string() for x in v2])
#         print(f'\tG\'\'\t{v2}')
    
#     print('\n\n')