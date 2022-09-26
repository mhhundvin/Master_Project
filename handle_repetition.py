from collections import defaultdict
import random
from classes import Generatable, Group, Regexp, Nonterminal, Token, Sequence, Plus, Star, Optional, Literal_Range, Repeat

def handle_repetition(grammar):
    new_grammar = defaultdict(list)
    for nonterminal, alternatives in grammar.items():
        for alternative in alternatives:
            new_alternative = extract_repetetor(new_grammar, nonterminal, alternative)
            new_grammar[nonterminal].append(new_alternative)
    return new_grammar

def extract_repetetor(grammar, nonterminal, alternative):
    if isinstance(alternative, list):
        alternative = Sequence( alternative )
    elif not isinstance(alternative, Sequence):
        alternative = Sequence( [alternative] )

    new_alternative = []
    for element in alternative.get_arg():
        if isinstance(element, Plus):
            alt = extract_repetetor(grammar, nonterminal, element.get_arg())
            alt = alt.get_arg()
            temp = alt
            for _ in range(0, random.randint(1,9)):
                alt += temp
            new_alternative.append(Sequence( alt ))
        
        elif isinstance(element, Star):
            alt = extract_repetetor(grammar, nonterminal, element.get_arg())
            alt = alt.get_arg()
            temp = alt
            x = random.randint(1,9)
            for _ in range(0, x):
                alt += temp
            if x % 2 == 0:
                new_alternative.append(Sequence( alt ))
        
        elif isinstance(element, Optional):
            temp = extract_repetetor(grammar, nonterminal, element.get_arg())
            x = random.randint(0,9)
            if x % 2 == 0:
                new_alternative.append( temp )
            # new_alternative.append( Optional( temp ))
        
        elif isinstance(element, Repeat):
            arg, start, stop = element.get_arg()
            alt = extract_repetetor(grammar, nonterminal, arg)
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
            temp = extract_repetetor(grammar, nonterminal, element.get_arg())
            new_alternative.append( temp )
            

        else:
            new_alternative.append(element)

        if isinstance(element, Regexp):
            element.set_name(nonterminal)
    
    return Sequence( new_alternative )