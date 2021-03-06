import random
from split_grammar import split_grammar
from classes_3 import Literal_Range, Nonterminal, Token, Plus, Optional, Star, Terminal, Regexp, Sequence

def generate(grammar, depth):
    no_cycle_grammar, leftover_grammar = split_grammar(grammar)

    terminal_list = {}

    for nonterminal, alternatives in grammar.items():
        alternative = random.choice(alternatives)
        print(f'{nonterminal.to_string()}:\n\t{alternative}\n')
        alternative, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth)
        # print(f'{alternative}\n\n\n')
        terminal_list[nonterminal] = alternative
        # break
    for nontermianl, alternative in terminal_list.items():
        if nontermianl.to_string() == "DIGIT":
            break
        print('\n\n#########################################################################################################################')
        print(f'{nontermianl.to_string()}:')
        for elem in alternative:
            # if isinstance(elem, Sequence):
            #     print(f'\t{elem.get_arg()}')
            # else:
            print(f'{elem}')
            print(f'{elem.generate()}')

def generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth):
    halfway = depth / 2
    # if not isinstance(alternative, list):
    #     if isinstance(alternative, Sequence):
    #         alternative = alternative.get_arg()
    #     else:
    #         print(f'\n\n\t=====> {alternative} <=====\n\n')
    #         alternative = [alternative]
    while depth > 0 and contains_nonterminal(alternative):
        if isinstance(alternative, Sequence):
            alternative = alternative.get_arg()
        elif not isinstance(alternative, list):
            alternative = [alternative]
        print(f'\n\nFIRST WHILE: {depth}\n\t{alternative}\n\n')
        new_nonterminal = []
        for element in alternative:
            print(f'\t==>> {element}')

            if isinstance(element, Terminal):
                new_nonterminal.append(element)
            # elif isinstance(element, Token):
            #     new_nonterminal.append(element)
            elif isinstance(element, Literal_Range):
                new_nonterminal.append(element)
            elif isinstance(element, Regexp):
                new_nonterminal.append(element)

            elif isinstance(element, Star):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_nonterminal.append(Star( element ) )
            elif isinstance(element, Plus):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_nonterminal.append(Plus( element ) )
            elif isinstance(element, Optional):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_nonterminal.append(Optional( element ) )
            elif isinstance(element, Sequence):
                depth -= 1
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element, depth)
                # new_nonterminal.append(element)
                if element:
                    print(f'n: {new_nonterminal}\t\te: {element.get_arg()}')
                    new_nonterminal += element.get_arg()

            

            else:
                depth -= 1
                if depth > halfway:
                    print(f"1:{element}")
                    if element in leftover_grammar.keys():
                        element = do_step(leftover_grammar, element)
                    elif element in no_cycle_grammar.keys():
                        print("2")
                        element = do_step(no_cycle_grammar, element)
                    else:
                        raise Exception(f'What happend? {element}')
                    if element:
                        new_nonterminal.append(element)
                # Choose randomly between the two grammars so that there is a possebility of reaching every nonterminal.
                else:
                    choices = []
                    if element in leftover_grammar.keys():
                        choices.append(leftover_grammar)
                    elif element in no_cycle_grammar.keys():
                        choices.append(no_cycle_grammar)
                    else:
                        raise Exception(f'What happend now? {element}')
                    choice = random.choice(choices)
                    element = do_step(choice, element)
                    if element:
                        new_nonterminal.append(element)
            print(f'\n\n=======================\n{new_nonterminal}\n=======================\n\n')
            
        # if len(new_nonterminal) == 1:
        #     alternative = new_nonterminal
        # else:
        #     alternative = Sequence(new_nonterminal)         
        alternative = new_nonterminal

    while contains_nonterminal(alternative):
        if isinstance(alternative, Sequence):
            alternative = alternative.get_arg()
        elif not isinstance(alternative, list):
            alternative = [alternative]
        new_nonterminal = []
        for element in alternative:
            if isinstance(element, Terminal):
                new_nonterminal.append(element)
            elif isinstance(element, Literal_Range):
                new_nonterminal.append(element)
            elif isinstance(element, Regexp):
                new_nonterminal.append(element)

            elif isinstance(element, Star):
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_nonterminal.append(Star( element ) )
            elif isinstance(element, Plus):
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                if element:
                    new_nonterminal.append(Plus( element ) )
            elif isinstance(element, Optional):
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element.get_arg(), depth)
                print(f'\n\t{element}')
                if element:
                    new_nonterminal.append(Optional( element ) )
            elif isinstance(element, Sequence):
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, element, depth)
                # new_nonterminal.append(element)
                if element:
                    new_nonterminal += element.get_arg()

            else:
                if element in no_cycle_grammar.keys():
                    element = do_step(no_cycle_grammar, element)
                elif element in leftover_grammar.keys():
                    element = do_step(leftover_grammar, element)
                else:
                    print(f'\n\n\t\t##### {alternative} : {element} ##### {alternative[0].to_string()}')
                    raise Exception(f'What happend 2? {element}')
                if element:
                        new_nonterminal.append(element)
        #     new_nonterminal.append(element)
        # if len(new_nonterminal) == 1:
        #     alternative = new_nonterminal
        # else:
        #     alternative = Sequence(new_nonterminal)
        alternative = new_nonterminal

    return Sequence( [alternative] ), depth


def do_step(grammar, nonterminal):
    temp = grammar[nonterminal]
    print(temp)
    if isinstance(temp, list):
        temp = random.choice(temp)
    return temp

def contains_nonterminal(alternative):
    if isinstance(alternative, Sequence):
        alternative = alternative.get_arg()
    elif not isinstance(alternative, list):
        alternative = [alternative]
    print(alternative)
    for element in alternative:
        if isinstance(element, Nonterminal):
            return True
        elif isinstance(element, Token):
            return True
        elif isinstance(element, Plus) or isinstance(element, Star) or isinstance(element, Optional):
            if isinstance(element.get_arg(), Nonterminal):
                return True
        elif isinstance(element, Sequence):
            if contains_nonterminal(element.get_arg()):
                return True
            # temp = element.get_arg()
            # for elem in temp:
            #     if isinstance(elem, Nonterminal):
            #         return True
    return False