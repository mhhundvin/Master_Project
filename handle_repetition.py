from collections import defaultdict
import random
from classes import Generatable, Group, Regexp, Nonterminal, Token, Sequence, Plus, Star, Optional, Literal_Range, Repeat

def handle_repetition(grammar, d):
    new_grammar = defaultdict(list)
    for nonterminal, alternatives in grammar.items():
        for alternative in alternatives:
            new_alternative = handle_repeater(new_grammar, nonterminal, alternative, d)
            new_grammar[nonterminal].append(new_alternative)
    return new_grammar

def handle_repeater(grammar, nonterminal, alternative, d):
    if isinstance(alternative, list):
        alternative = Sequence( alternative )
    elif not isinstance(alternative, Sequence):
        alternative = Sequence( [alternative] )

    new_alternative = []
    for element in alternative.get_arg():
        if isinstance(element, Plus):
            alt = handle_repeater(grammar, nonterminal, element.get_arg(), d)
            alt = alt.get_arg()
            temp = alt
            for _ in range(0, random.randint(1,d)):
                alt += temp
            new_alternative.append(Sequence( alt ))
        
        elif isinstance(element, Star):
            alt = handle_repeater(grammar, nonterminal, element.get_arg(), d)
            alt = alt.get_arg()
            temp = alt
            x = random.randint(1,d)
            for _ in range(0, x):
                alt += temp
            if random.randint(0,9) % 3 == 0:
                new_alternative.append(Sequence( alt ))
        
        elif isinstance(element, Optional):
            alt = handle_repeater(grammar, nonterminal, element.get_arg(), d)
            x = random.randint(0,9)
            if x % 3 == 0:
                new_alternative.append( alt )
            # new_alternative.append( Optional( temp ))
        
        elif isinstance(element, Repeat):
            arg, start, stop = element.get_arg()
            alt = handle_repeater(grammar, nonterminal, arg, d)
            alt = alt.get_arg()
            temp = alt
            if isinstance(start, Generatable):
                start = start.generate()
            if isinstance(stop, Generatable):
                stop = stop.generate()
            for _ in range(start, stop):
                alt += temp
            new_alternative.append( Sequence( alt ))

        elif isinstance(element, Sequence):
            alt = handle_repeater(grammar, nonterminal, element.get_arg(), d)
            new_alternative.append( alt )
            

        else:
            new_alternative.append(element)

        # if isinstance(element, Regexp):
        #     element.set_name(nonterminal)
    
    return Sequence( new_alternative )