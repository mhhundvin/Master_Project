from collections import defaultdict
from classes import Group, Nonterminal, Token, Terminal, Regexp, Star, Plus, Optional, Sequence, Repeat, Literal_Range

def split_grammar(grammar):
    no_cycle_grammar = defaultdict(list)
    leftover_grammar = defaultdict(list)
    for nonterminal, alternatives in grammar.items():
        # print(f'{nonterminal.to_string()}\n\t{alternatives}\n\n')
        for alternative in alternatives:

            if False:#alternative.contains_cycle(nonterminal, [], grammar):
                # print(f'\tCYCLE: {alternative.to_string()}\n')
                # leftover_grammar[nonterminal].append(alternative)
                pass
            

            else:
                if not isinstance(alternative, Sequence):
                    # print(f'--isinst... {alternative}')
                    alternative = Sequence( [alternative] )
                
                multiple_options = False
                new_alternative = []
                # print(f'---->{alternative} --> {alternative.get_arg()}')
                for element in alternative.get_arg():
                    # print(f'1: {element}')
                    if isinstance(element, Optional) or isinstance(element, Star):
                        multiple_options = True

                    elif isinstance(element, Plus):
                        multiple_options = True
                        new_alternative.append(element.get_arg())

                    # elif isinstance(element, Group):
                    #     pass
                    
                    else:
                        # print(f'\t\telement: {element.to_string()}')
                        new_alternative.append(element)
                    # print(f'2: {element}')
                    
                # print(f'==>{new_alternative}, {multiple_options}')

                # print(f'\tNO CYCLE')
                # print(f'\talternative: {alternative.to_string()}')
                # print(f'\tnew_alternative: {new_alternative.to_string()}\n\n')

                if multiple_options:
                    if new_alternative:
                        new_alternative = Sequence( new_alternative )
                        if not new_alternative.contains_cycle(nonterminal, [], grammar):
                            no_cycle_grammar[nonterminal].append(new_alternative)
                        else:
                            leftover_grammar[nonterminal].append(new_alternative)
                    leftover_grammar[nonterminal].append(alternative)
                else:
                    # print(f'\n\n{nonterminal.to_string()}: {alternative}\n\n')
                    if alternative.contains_cycle(nonterminal, [], grammar):
                        leftover_grammar[nonterminal].append(alternative)
                    else:
                        no_cycle_grammar[nonterminal].append(alternative)

    return no_cycle_grammar, leftover_grammar


