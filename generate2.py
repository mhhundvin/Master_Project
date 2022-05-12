import random
from collections import defaultdict
from split_grammar import split_grammar
from classes_3 import Generatable, Literal_Range, Nonterminal, Repeat, Token, Plus, Optional, Star, Terminal, Regexp, Sequence



def generate(grammar, depth):
    no_cycle_grammar, leftover_grammar = split_grammar(grammar)
    print('The grammar is split in two')
    
    terminal_list = defaultdict(list)

    for nonterminal, alternatives in grammar.items():
        # alternative = random.choice(alternatives)
        for alternative in alternatives:
            print(f'{nonterminal.to_string()}:')#\n\t{alternative}\n')
            alternative, x = generate_nonterminal(no_cycle_grammar, leftover_grammar, alternative, depth)
            # print(x)
            print(alternative.get_arg())
            # print(f'\t=====> {alternative}\n\t\t===> {alternative.get_arg()}')
            terminal_list[nonterminal].append(alternative)
        # print(f'TL[n]: {terminal_list[nonterminal].get_arg()}\n\n')
        # x = input('\n\nContinue? ')
        # if (x == "nei"):
        #     break
    
    print('\n\n###################################################################################################################')
    print('\t\tRemoved nonterminals?')
    print('###################################################################################################################\n\n')

    for nonterminal, alternatives in terminal_list.items():
        
        if nonterminal.to_string() == "DIGIT":
            break

        # print(f'\n\n{nonterminal.to_string()}:')#\n\t{alternative}\n')
        for alternative in alternatives:
            print(f'\n\n{nonterminal.to_string()}:')#\n\t{alternative}\n')
            terminalt_string = ""
            for element in alternative.get_arg():
                
                # print(f'\t{element.to_string()}')
                # print(f'\t{element.generate()}')
                
                # print(f'\t{element}\n\t\t==> {element.to_string()}')
                # if isinstance(element, Sequence):
                #     print(f'\t\t{element.get_arg()}')
                terminalt_string += element.generate()
            print(f'\t{terminalt_string}')
            # x = input('\n\nContinue? ')
            # if (x == "nei"):
            #     return
            





def generate_nonterminal(no_cycle_grammar, leftover_grammar, alternative, depth):
    # if not isinstance(alternative, Generatable):
    #         raise Exception(f'This, {alternative}, is supposed to be a Generatable.')
  
    if not isinstance(alternative, Sequence):
        alternative = Sequence( [alternative] )

    halfway = depth / 2
    
    while contains_nonterminal(alternative):
        # print(f'\t{alternative}')
        new_alternative = []
        for element in alternative.get_arg():
            # print(f'\t\t{element}')
            if isinstance(element, Nonterminal) or isinstance(element, Token):
                depth -= 1
                element = do_step_nonterminal(no_cycle_grammar, leftover_grammar, element, depth, halfway)
                # print(f'\n\n\t\tNONTERMINAL: {element}\n\n')
                new_alternative.append(element)

            elif isinstance(element, Star):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, element.get_arg(), depth)
                if element:
                    new_alternative.append(Star( element ) )
            elif isinstance(element, Plus):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, element.get_arg(), depth)
                if element:
                    new_alternative.append(Plus( element ) )
            elif isinstance(element, Optional):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, element.get_arg(), depth)
                if element:
                    new_alternative.append(Optional( element ) )
            elif isinstance(element, Sequence):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, element, depth)
                if element:
                    # print(f'n: {new_alternative}\t\te: {element.get_arg()}')
                    new_alternative += element.get_arg()
                
            elif isinstance(element, Repeat):
                depth -= 1
                arg, start, stop = element.get_arg()
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, arg, depth)
                if element:
                    new_alternative.append(Repeat( element, start, stop ) )
            # elif isinstance(element, Literal_Range):
            #     depth -= 1
            #     start, stop = element.get_arg()
            #     regexp = f'/[{start}-{stop}]/'
            #     new_alternative.append(Regexp( regexp ))
                

            # elif isinstance(element, Terminal) or isinstance(element, Regexp) or isinstance(element, Literal_Range):
            else:
                new_alternative.append(element)

        # print(f'\t\t\t=====> {new_alternative}')
        if new_alternative:
            alternative = Sequence( new_alternative )
        # print(f'\t\t\t\t=====> {alternative.get_arg()}')
    # print(f'\t=====> {alternative.get_arg()}\n')
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
        

    return do_step(grammar, nonterminal)



def do_step(grammar, nonterminal):
    temp = grammar[nonterminal]
    # print(temp)
    if isinstance(temp, list):
        temp = random.choice(temp)
    return temp




def contains_nonterminal(alternative):
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
            if contains_nonterminal(seq):
                return True

    return False