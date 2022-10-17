from collections import defaultdict
from classes import Star, Plus, Optional, Sequence

def split_grammar(grammar):
    no_cycle_grammar = defaultdict(list)
    leftover_grammar = defaultdict(list)
    for nonterminal, alternatives in grammar.items():
        for alternative in alternatives:
            if not isinstance(alternative, Sequence):
                alternative = Sequence( [alternative] )
            
            multiple_options = False
            new_alternative = []

            for element in alternative.get_arg():
                if isinstance(element, Optional) or isinstance(element, Star):
                    multiple_options = True

                elif isinstance(element, Plus):
                    multiple_options = True
                    new_alternative.append(element.get_arg())
                
                else:
                    new_alternative.append(element)

            if multiple_options:
                if True:
                    new_alternative = Sequence( new_alternative )
                    if not new_alternative.contains_cycle(nonterminal, [], grammar):
                        no_cycle_grammar[nonterminal].append(new_alternative)
                    else:
                        leftover_grammar[nonterminal].append(new_alternative)
                leftover_grammar[nonterminal].append(alternative)
            else:
                if alternative.contains_cycle(nonterminal, [], grammar):
                    leftover_grammar[nonterminal].append(alternative)
                else:
                    no_cycle_grammar[nonterminal].append(alternative)

    return no_cycle_grammar, leftover_grammar


