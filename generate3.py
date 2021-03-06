import random
from collections import defaultdict
from split_grammar import split_grammar
from classes_3 import Generatable, Group, Literal_Range, Nonterminal, One_word, Repeat, Token, Plus, Optional, Star, Terminal, Regexp, Sequence



def generate(grammar, depth):
    no_cycle_grammar, leftover_grammar = split_grammar(grammar)
    print('The grammar is split in two')
    print('###################################################################################################################\n\n')

    terminal_list = defaultdict(list)

    for nonterminal, alternatives in grammar.items():
        for alternative in alternatives:
            alternative, x = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth)
            terminal_list[nonterminal].append(alternative)
    
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
            print(f'------------------------------\n{nonterminal.to_string()}:\n')

            terminal_string = ""

            for element in alternative.get_arg():
                # print(f'\t=>{element}')
                # if not isinstance(element, Terminal):
                #     print(f'\t\t=>{element.get_arg()}')
                terminal_string += element.generate()
                if terminal_string[-1] != " " and not isinstance(element, Token):
                    terminal_string += " "

            print(f'{terminal_string}\n------------------------------\n\n')
            





def generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth):
  
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
                # new_alternative.append(element)
                new_alternative.append( One_word( element.get_arg() ))

            elif isinstance(element, Star):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_alternative.append(Star( element ) )

            elif isinstance(element, Plus):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_alternative.append( Plus( element ) )

            elif isinstance(element, Optional):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_alternative.append(Optional( element ) )

            elif isinstance(element, Sequence):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element, depth)
                if element:
                    new_alternative += element.get_arg()

            elif isinstance(element, One_word):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element, depth)
                if element:
                    new_alternative.append(element)
                
            elif isinstance(element, Repeat):
                depth -= 1
                arg, start, stop = element.get_arg()
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, arg, depth)
                if element:
                    new_alternative.append(Repeat( element, start, stop ) )
                

            else:
                new_alternative.append(element)

        if new_alternative:
            if isinstance(nonterminal, Token):
                alternative = One_word( new_alternative )
            else:
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
            raise Exception(f'Depth\tWhat happend? "{nonterminal}"')
        

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
    if not isinstance(alternative, Sequence) and not isinstance(alternative, One_word):
        raise Exception(f'This, {alternative}, is supposed to be a Sequence.')

    for element in alternative.get_arg():
        if isinstance(element, Nonterminal):
            return True
        elif isinstance(element, Token):
            return True
        
        elif isinstance(element, Sequence):
            if contains_nonterminal(element):
                return True
            
        elif isinstance(element, Plus) or isinstance(element, Star) or isinstance(element, Optional):
            if isinstance(element.get_arg(), Sequence):
                seq = element.get_arg()
                if contains_nonterminal(seq):
                    return True
            else:
                seq = Sequence( [element.get_arg()] )
                if contains_nonterminal(seq):
                    return True
        elif isinstance(element, Repeat):
            arg, start, stop = element.get_arg()
            if not isinstance(arg, Sequence):
                seq = Sequence( [arg] )
            if contains_nonterminal(arg):
                return True

    return False