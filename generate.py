import random
from collections import defaultdict
from split_grammar import split_grammar
from handle_repetition import handle_repetition
from classes import Generatable, Group, Literal_Range, Nonterminal, Repeat, Token, Plus, Optional, Star, Terminal, Regexp, Sequence



def generate(grammar, depth):
    no_cycle_grammar, leftover_grammar = split_grammar(grammar)
    print('###################################################################################################################')
    print('The grammar is split in two')
    print('###################################################################################################################')
    print(f'\n\n')

    print('###################################################################################################################')
    grammar = handle_repetition(grammar, depth)
    no_cycle_grammar = handle_repetition(no_cycle_grammar, depth)
    leftover_grammar = handle_repetition(leftover_grammar, depth)
    print("Repetitions have been handeld.")
    print('###################################################################################################################')
    print(f'\n\n')


    # input("Continue?")

    terminal_list = defaultdict(list)

    for nonterminal, alternatives in grammar.items():
        for alternative in alternatives:
            alternative, x = inline_nonterminals(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth)
            terminal_list[nonterminal].append(alternative)
    print('###################################################################################################################')
    print('Nonterminals have been inlined')
    print('###################################################################################################################')
    print(f'\n\n')

    input("continue?")
    
    print('\n\n###################################################################################################################')
    print('\t\tGenerating Starts Here')
    print('###################################################################################################################\n\n')

    for nonterminal, alternatives in terminal_list.items():
        # if nonterminal.to_string() != "CNAME" and nonterminal.to_string() != "variable_decl":
        if nonterminal.to_string()[0] == "$":
            continue
        if nonterminal.to_string() == "DIGIT":
            break

        for alternative in alternatives:
            # input("continue?\n")
            print(f'------------------------------\n{nonterminal.to_string()}:\n')

            terminal_string = ""

            for element in alternative.get_arg():
                if isinstance(element, Generatable):
                    terminal_string += element.generate()
                else:
                    terminal_string += element

            print(f'{terminal_string}\n------------------------------')
            




# RENAME to inline_nonterminal?
def inline_nonterminals(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth):
  
    if not isinstance(alternative, Sequence):
        alternative = Sequence( [alternative] )

    halfway = depth / 2

    while contains_nonterminal(alternative):

        new_alternative = []
        for element in alternative.get_arg():

            if isinstance(element, Nonterminal):    # or isinstance(element, Token):
                depth -= 1
                element = do_step_nonterminal(no_cycle_grammar, leftover_grammar, element, depth, halfway)
                # new_alternative.append(element)
                new_alternative += element.get_arg()
            elif isinstance(element, Token):
                depth -= 1
                element = do_step_nonterminal(no_cycle_grammar, leftover_grammar, element, depth, halfway)
                new_alternative.append(element)

            elif isinstance(element, Sequence):
                depth -= 1
                element, depth = inline_nonterminals(no_cycle_grammar, leftover_grammar, nonterminal, element, depth)
                if element:
                    new_alternative += element.get_arg()                

            else:
                new_alternative.append(element)

        if True:
            alternative = Sequence( new_alternative )


    return alternative, depth






def do_step_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, depth, halfway):
    if depth > halfway:
        if nonterminal in leftover_grammar.keys():
            grammar = leftover_grammar
        elif nonterminal in no_cycle_grammar.keys():
            grammar = no_cycle_grammar
        else:
            raise Exception(f'Halfway\tWhat happend? "{nonterminal}"')
    
    elif depth > 0:
        grammars = []
        if nonterminal in no_cycle_grammar.keys():
            grammars.append(no_cycle_grammar)
        elif nonterminal in leftover_grammar.keys():
            grammars.append(leftover_grammar)
        else:
            raise Exception(f'Else\tWhat happend? "{nonterminal}"')
        grammar = random.choice(grammars)

    else:
        if nonterminal in no_cycle_grammar.keys():
            grammar = no_cycle_grammar
        elif nonterminal in leftover_grammar.keys():
            grammar = leftover_grammar
        else:
            raise Exception(f'Depth\tWhat happend? "{nonterminal.to_string()}"')
        

    return do_step(grammar, nonterminal, depth)



def do_step(grammar, nonterminal, depth):
    alternatives = grammar[nonterminal]
    if depth < 0:
        alternatives = remove_direct_recursion(alternatives, nonterminal)
    
    alternative = random.choice(alternatives)

    return alternative


def remove_direct_recursion(alternatives, nonterminal):
    new_alternatives = []
    for alternative in alternatives:
        contains_recursion = False

        for element in alternative.get_arg():
            if isinstance(element, type(nonterminal)) and element == nonterminal:
                contains_recursion = True

        if not contains_recursion:
            new_alternatives.append(alternative)

    return new_alternatives


def contains_nonterminal(alternative):
    if isinstance(alternative, list):
        alternative = Sequence( alternative )

    if not isinstance(alternative, Sequence):
        raise Exception(f'This, {alternative}, is supposed to be a Sequence.')

    for element in alternative.get_arg():
        if isinstance(element, Nonterminal):
            return True
        elif isinstance(element, Token):
            return True
        
        elif isinstance(element, Sequence):
            if contains_nonterminal(element):
                return True

    return False