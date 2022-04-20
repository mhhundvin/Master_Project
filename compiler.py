from random import choice
from lark import Transformer
from collections import defaultdict
from lark_parser import tree
from classes_2 import Generatable, list_to_string, to_simple_list, Nonterminal, Token, Terminal, Regexp, Star, Plus, Optional, Sequence, Expansions, Repeat, Literal_Range

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
            # lst.append( elem[0] )
            if len(elem) == 1 and isinstance(elem[0], Generatable):
                lst.append(elem[0])
            else:
                lst.append(Sequence( elem ))
        return lst
        # return [ Optional( lst ) ]

        # print(f'\tEXPANSIONS: {lst}\n')
        # return [ Expansions( lst ) ]

    
    def alias(self, args):
        # print(f'ALIAS: {args[:-1]}\n')
        return args[:-1]
    
    def expansion(self, args):
        # args is a list
        # print(f'EXPANSION: {args}')
        if len(args) == 1 and isinstance(args[0], Generatable):
            return args[0]
        else:
            return Sequence( args )
        # return Sequence( args )
    
    def opexper(self, args):
        # args = atop OP
        op = args[1]
        arg = args[0]
        if op == "+":
            return Plus( arg )
        elif op == "*":
            return Star( arg )
        elif op == "?":
            return Optional( [arg, ''] )
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
        # print(f'GROUP: {args[0]}')
        return Expansions( args[0] )
        # return args[0][0]

    def maybe(self, args):
        # print(f'MAYBE: {args[0]}')
        arg = args[0]
        if not isinstance(arg, list):
            arg = [arg]
        return Optional( arg )


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


# for k, v in grammar.items():
#     print(f'{k.to_string()}: {v}\n')


def transform_grammar(grammar, transformed_grammar):
    for k,v in grammar.items():

        # if k.to_string() == "DIGIT":
        #     break

        no_cycles = []
        for seq in v:
            temp = seq.contains_cycle(k, [], grammar)
            if not temp:
                no_cycles.append(seq)

        if len(no_cycles) != 0:
            transformed_grammar[k] = no_cycles
        else:
            transformed_grammar[k] = v

    for k, v in transformed_grammar.items():

    # print(f'{k.to_string()}:')
        for seq in v:
            temp = seq.contains_cycle(k, [], transformed_grammar)
            # print(f'\t{temp}')
            if temp:
                transformed_grammar = transform_grammar(transformed_grammar, {})

    
    return transformed_grammar


def transform_grammar_2(grammar, transformed_grammar):
    for k,v in grammar.items():

        # if k.to_string() == "DIGIT":
        #     break

        no_cycles = []
        for seq in v:
            temp = seq.contains_cycle(k, [], grammar)
            if not temp:
                no_cycles.append(seq)

        if len(no_cycles) == 0:
            transformed_grammar[k] = []
        else:
            transformed_grammar[k] = no_cycles
    
    
    return transformed_grammar

def transform_grammar_3(grammar):
    transformed_grammar = {}
    for k,v in grammar.items():
        transformed_grammar[k] = []
        for seq in v:
            if not seq.contains_cycle(k, [], grammar):
                transformed_grammar[k].append(seq)
    return transformed_grammar


transformed_grammar = transform_grammar(grammar, {})   # no cycles in JSON
# transformed_grammar = transform_grammar(transformed_grammar, {})        # 16 -> 13 cycles in python, doing it again changes nothing.
# transformed_grammar = transform_grammar_3(transformed_grammar)        # no cycles in verilog
# transformed_grammar = transform_grammar_2(transformed_grammar, {})        # 16 -> 13 cycles in python, doing it again changes nothing.
# transformed_grammar = transform_grammar(transformed_grammar, {})        # 16 -> 13 cycles in python, doing it again changes nothing.


# for k,v in transformed_grammar.items():
#     if k.to_string() == "DIGIT":
#         break

#     opt = choice(v)
#     print(f'{k.to_string()}:\n\t{opt.generate()}')



# for k,v in grammar.items():

#     if k.to_string() == "DIGIT":
#         break

#     print(f'{k.to_string()}:\n\t{v}')


print("-----------------------------------------------")
print("Non-terminals that have their options changed:")
print("-----------------------------------------------\n")

for g, t in list(zip(grammar, transformed_grammar)):
    if g.to_string() == "DIGIT":
        break
    temp = list_to_string(transformed_grammar[t]).split(" ")
    temp = ""
    for elem in transformed_grammar[t]:
        temp += elem.to_string() + " | "
    temp2 = ""
    for elem in grammar[t]:
        temp2 += elem.to_string() + " | "
    
    if temp == temp2:
        continue

    print(f'new: {t.to_string()}: {temp}')
    print(f'old: {g.to_string()}: {temp2}\n\n')
    # temp = len(grammar[g]) == len(transformed_grammar[t])
    # if not temp:
    #     print(f'\t{g.to_string()}')

print("-----------------------------------------------")
print("nonterminals with cycles")
print("-----------------------------------------------\n")


for k, v in transformed_grammar.items():
    if k.to_string() == "DIGIT":
            break

    # print(f'{k.to_string()}:')
    for seq in v:
        temp = seq.contains_cycle(k, [], transformed_grammar)
        # print(f'\t{temp}')
        if temp:
            print(f'{k.to_string()}: {seq.to_string()}\n')#:\n\t{temp}')


print("-----------------------------------------------")
print("Generated exaples")
print("-----------------------------------------------\n")
# transform_grammar = grammar
for k,v in transformed_grammar.items():
    if k.to_string() == "DIGIT":
        break
    
    if len(v) == 0:
        opt = Terminal( "" )
    else:
        opt = choice(to_simple_list(v))

    print(f'{k.to_string()}:\n\t{opt.generate_shortest(transformed_grammar)}\n\n')

    break
    