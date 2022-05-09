import random
from split_grammar import split_grammar
from classes_3 import Terminal, Regexp, Sequence

def generate(grammar, depth):
    no_cycle_grammar, leftover_grammar = split_grammar(grammar)

    for nonterminal, alternatives in grammar.items():
        alternative = random.choice(alternatives)
        print(f'{nonterminal.to_string()}:\n\t{alternative}')
        generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth)


def generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth):
    halfway = depth / 2
    while depth > 0:
        new_nonterminal = []
        for element in alternative:
            if isinstance(element, Terminal):
                new_nonterminal.append(element)
            elif isinstance(element, Regexp):
                new_nonterminal.append(element)
            elif isinstance(element, list):
                alternative = random.choice(element)
                element, depth = generate_nonterminal(no_cycle_grammar, leftover_grammar, nonterminal, alternative, depth)
            

            else:
                if depth > halfway:
                    depth -= 1
                    if element in leftover_grammar.keys():
                        element = do_step(leftover_grammar, element)
                    elif element in no_cycle_grammar.keys():
                        element = do_step(no_cycle_grammar, element)
                    else:
                        raise Exception(f'What happend? {element}')
                # Choose randomly between the two grammars so that there is a possebility of reaching every nonterminal.
                else:
                    choices = []
                    if element in leftover_grammar.keys():
                        choices.append(element)
                    elif element in no_cycle_grammar.keys():
                        choices.append(element)
                    else:
                        raise Exception(f'What happend now? {element}')
                    choice = random.choose(choices)
                    element = do_step(choice, element)
                    



    pass


def do_step(grammar, nonterminal):
    return random.choice(grammar[nonterminal])