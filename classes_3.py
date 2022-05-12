'''
repetition(start=0, end=math.)
optional
star
plus
seq
regex

nonterminal
terminal - string
'''
from distutils.log import error
import random
from tracemalloc import start, stop
import exrex

def to_simple_list(lst):
    new_lst = []
    for elem in lst:
        if isinstance(elem, Token):
            new_lst.append(elem)
        elif isinstance(elem, Terminal):
            new_lst.append(elem)
        elif isinstance(elem, Regexp):
            new_lst.append(elem)

    # print(f'new_lst: {new_lst}')
    # print(f'lst: {lst}')

    if new_lst:
        return new_lst
    return lst

def list_to_string(lst):
    temp = ""
    for elem in lst:
        if isinstance(elem, Generatable):
            elem = elem.to_string()
        temp += elem + " "
    return temp[:-1]

#####################################################################################

class Generatable():
    pass

#####################################################################################


class Literal_Range(Generatable):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def to_string(self):
        start = self.start
        stop = self.stop
        if isinstance(start, Generatable):
            start = start.to_string()
        if isinstance(stop, Generatable):
            stop = stop.to_string()
        return f'{start} ".." {stop}'
    
    def get_arg(self):
        start = self.start
        stop = self.stop
        if isinstance(start, Generatable):
            start = start.to_string()
        if isinstance(stop, Generatable):
            stop = stop.to_string()
        return start, stop
    
    def generate_shortest(self, transformed_grammar):
        return self.generate() 

    def generate(self):
        temp = f'[{self.start.generate()}-{self.stop.generate()}]'*3
        # print(f'LITERAL RANGE: {temp}')
        return exrex.getone(temp)

    def contains_cycle(self, nonterminal, visited, grammar):
        return False

#####################################################################################

# expr_range
class Repeat(Generatable):
    def __init__(self, args, start=0, stop=random.randint(1,3)):
        self.args = args
        self.start = start
        self.stop = stop

    def to_string(self):
        arg = self.args
        if isinstance(arg, Generatable):
            arg = arg.to_string()
        txt = f'{arg} ~ {self.start} .. {self.stop}'
        return txt
    
    def get_arg(self):
        return self.args, self.start, self.stop

    def generate_shortest(self, transformed_grammar):
        return self.args.generate_shortest(transformed_grammar)

    def generate(self):
        arg = self.args
        start = self.start
        stop = self.stop
        if isinstance(start, Generatable):
            start = start.generate()
        if isinstance(stop, Generatable):
            stop = stop.generate()
        terminal_string = ''
        # print(f's: {start}, e: {end}')
        start, stop = int(start), int(stop)
        for _ in range(start, stop):
            terminal_string += arg.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar )
        return False

#####################################################################################

class Optional(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        arg = self.args.get_arg()
        return f'<{list_to_string(arg)}>?'

    def get_arg(self):
        return self.args
    
    def generate_shortest(self, transformed_grammar):
        return ""

    
    def generate(self):
        # print(f'\n\n\t{self.args}')
        args = self.args
        if isinstance(args, Sequence):
            args = args.get_arg()
        arg = random.choice(args)
        if isinstance(arg, Generatable):
            return arg.generate()
        return arg

    def contains_cycle(self, nonterminal, visited, grammar):
        return False

#####################################################################################

class Star(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        if isinstance(self, Generatable):
            return f'<{self.args.to_string()}>*'
        return f'<{self.args}>*'

    def get_arg(self):
        return self.args
    
    def generate_shortest(self, transformed_grammar):
        return ""
    
    def generate(self):
        arg = self.args
        terminal_string = ''
        for _ in range(0, random.randint(0,3)):
            # print(arg)
            terminal_string += arg.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False

#####################################################################################

class Plus(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        if isinstance(self, Generatable):
            return f'<{self.args.to_string()}>+'
        return f'<{self.args}>+'

    def get_arg(self):
        return self.args
    
    def generate_shortest(self, transformed_grammar):
        return self.args.generate_shortest(transformed_grammar)
    
    def generate(self):
        arg = self.args
        if isinstance(arg, list):
            arg = arg[0]
        terminal_string = ''
        for _ in range(0, random.randint(1,3)):
            terminal_string += arg.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False

#####################################################################################

class Group(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        lst = []
        for elem in self.args:
            # print(f'\t----> elem: {elem}')
            if isinstance(elem, Generatable):
                lst.append(elem.to_string())
            else:
                lst.append(elem)
        # print(f'\t----> lst: {lst}')
        temp = ' | '.join(lst)
        return f'({temp})'
    
    def get_arg(self):
        return self.args
    
    def generate(self):
        arg = random.choice(self.args)
        return arg.generate()
    
    def contains_cycle(self, nonterminal, visited, grammar):
        args = self.args
        for elem in args:
            if isinstance(elem, list):
                elem = elem[0]
            if elem.contains_cycle(nonterminal, visited, grammar):
                return True
        return False

#####################################################################################

class Sequence(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        return list_to_string(self.args)

    def get_arg(self):
        return self.args
    
    def generate_shortest(self, transformed_grammar):
        terminal_string = ''
        for elem in self.args:
            terminal_string += elem.generate_shortest(transformed_grammar)
        return terminal_string
    
    def generate(self):
        terminal_string = ''
        for elem in self.args:
            terminal_string += elem.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        args = self.args
        for elem in args:
            if isinstance(elem, list):
                # print(f'----> SEQUENCE: {elem}')
                elem = elem[0]
            if elem.contains_cycle(nonterminal, visited, grammar):
                return True
        return False

#####################################################################################

class Regexp(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        return self.args
    
    
    def generate_shortest(self, transformed_grammar):
        return self.generate()
    
    def generate(self):
        words = ["apple", "banana", "cherry"]
        return random.choice(words)

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False

#####################################################################################

class Nonterminal(Generatable):
    def __init__(self, nonterminal, grammar):
        self.nonterminal = nonterminal
        self.grammar = grammar
    
    def __hash__(self):
        return hash(self.nonterminal)

    def __eq__(self, other):
        print(f'\n\n{self.nonterminal} == {other}')
        return self.nonterminal == other.nonterminal
    
    def to_string(self):       
        return self.nonterminal
    
    def generate_shortest(self, transformed_grammar):
        lst = to_simple_list(transformed_grammar.get(self))
        arg = random.choice(lst)
        temp = arg.generate_shortest(transformed_grammar)
        return temp

    def generate(self):
        grammar = self.grammar
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, nonterminal, visited, grammar):
        # Why do i need the or?
        # withoute it I get an error when calling contains_cycle in split_grammar
        if self in visited or isinstance(nonterminal, Token):
            return False
        if self == nonterminal:
            return True
        visited.append(self)
        for elem in grammar.get(self):
            if isinstance(elem, list):
                # print(f'----> NONTERMINAL: {elem}')
                elem = elem[0]
            if elem.contains_cycle(nonterminal, visited, grammar):
                return True
        return False

#####################################################################################

class Token(Generatable):
    def __init__(self, token, grammar):
        self.token = token
        self.grammar = grammar
    
    def __hash__(self):
        return hash(self.token)

    def __eq__(self, other):
        return self.token == other.token
    
    def to_string(self):       
        return self.token
    
    def generate_shortest(self, transformed_grammar):
        arg = random.choice(transformed_grammar.get(self))
        temp = arg.generate_shortest(transformed_grammar)
        return temp

    def generate(self):
        grammar = self.grammar
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, token, visited, grammar):
        return False

#####################################################################################

class Terminal(Generatable):
    def __init__(self, terminal):    
        self.terminal = terminal

    def to_string(self):
        return f'"{self.terminal}"'
    
    def generate_shortest(self, transformed_grammar):
        return self.generate()

    def generate(self):
        return self.terminal.replace('\\', '')
    
    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.terminal, Generatable):
            return self.terminal.contains_cycle(nonterminal, visited, grammar)
        return False





