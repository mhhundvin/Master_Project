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

class Generatable():
    pass

class Literal_Range(Generatable):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    
    def to_string(self):
        if isinstance(self, Generatable):
            return self.args.to_string()
        return f'{self.start} ".." {self.stop}'
    
    def generate_shortest(self, transformed_grammar):
        return self.generate() 

    def generate(self):
        temp = f'[{self.start.generate()}-{self.stop.generate()}]'*3
        # print(f'LITERAL RANGE: {temp}')
        return exrex.getone(temp)

    def contains_cycle(self, nonterminal, visited, grammar):
        return False

# expr_range
class Repeat(Generatable):
    def __init__(self, args, start=0, end=random.randint(1,3)):
        self.args = args
        self.start = start
        self.end = end

    def to_string(self):
        if isinstance(self, Generatable):
            return self.args.to_string()
        return self.args

    def generate_shortest(self, transformed_grammar):
        return self.args.generate_shortest(transformed_grammar)

    def generate(self):
        arg = self.args
        terminal_string = ''
        for _ in range(self.start, self.end+1):
            terminal_string += arg.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited )
        return False


class Optional(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        return f'[{list_to_string(self.args)}]'
    
    def generate_shortest(self, transformed_grammar):
        return ""
        # arg = random.choice(self.args)
        # if isinstance(arg, Generatable):
        #     return arg.generate_shortest(transformed_grammar)
        # return arg

    
    def generate(self):
        arg = random.choice(self.args)
        if isinstance(arg, Generatable):
            return arg.generate()
        return arg

    def contains_cycle(self, nonterminal, visited, grammar):
        # for elem in self.args:
        #     if isinstance(elem, Generatable):
        #         return elem.contains_cycle(nonterminal, visited, grammar)
        return False


class Star(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        if isinstance(self, Generatable):
            return f'({self.args.to_string()})*'
        return f'({self.args})*'
    
    def generate_shortest(self, transformed_grammar):
        # return random.choice([self.args.generate_shortest(transformed_grammar), ""])
        return ""
    
    def generate(self):
        terminal_string = ''
        for _ in range(0, random.randint(0,3)):
            terminal_string += self.args.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False


class Plus(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        if isinstance(self, Generatable):
            return f'({self.args.to_string()})+'
        return f'({self.args})+'
    
    def generate_shortest(self, transformed_grammar):
        return self.args.generate_shortest(transformed_grammar)
    
    def generate(self):
        terminal_string = ''
        for _ in range(0, random.randint(1,3)):
            terminal_string += self.args.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False


class Sequence(Generatable):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        return list_to_string(self.args)

    
    
    def generate_shortest(self, transformed_grammar):
        terminal_string = ''
        for elem in self.args:
            terminal_string += elem.generate_shortest(transformed_grammar)
        # print(f'GENERATING SEQUENCE: {terminal_string}')
        # input('continue?')
        return terminal_string
    
    def generate(self):
        terminal_string = ''
        for elem in self.args:
            # print(f'Seq elem: {elem}\n-->  {elem.generate()}')
            # print(f'Seq str: {terminal_string}')
            terminal_string += elem.generate()
        # print(f'GENERATING SEQUENCE: {terminal_string}')
        # input('continue?')
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        args = self.args
        # if not isinstance(args, list):
        #     args = [args]
        for elem in args:
            if elem.contains_cycle(nonterminal, visited, grammar):
                # if isinstance(elem, Optional):
                #     return False
                return True
        return False

class Expansions(Generatable):  # ??? Group ???
    def __init__(self, args):
        self.args = args
    
    def to_string(self):
        txt = ''
        for seq in self.args:
            txt += seq.to_string() + " | "
        return txt[:-3]
    
    def generate_shortest(self, transformed_grammar):
        # print(f'Expansions: {self.args}')
        lst = to_simple_list(self.args)
        temp = random.choice(lst)       # self.args)
        return temp.generate_shortest(transformed_grammar)
    
    def generate(self):
        temp = random.choice(self.args)
        return temp.generate()
    
    def contains_cycle(self, nonterminal, visited, grammar):
        args = self.args
        cycles = []
        for elem in args:
            if elem.contains_cycle(nonterminal, visited, grammar):
                cycles.append(elem)
        return len(args) == len(cycles)

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
        # return "-regexp-"  # self.args

    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited, grammar)
        return False


class Nonterminal(Generatable):
    def __init__(self, nonterminal, grammar):
        self.nonterminal = nonterminal
        self.grammar = grammar
    
    def __hash__(self):
        return hash(self.nonterminal)

    def __eq__(self, other):
        return self.nonterminal == other.nonterminal
    
    def to_string(self):       
        return self.nonterminal
    
    def generate_shortest(self, transformed_grammar):
        # print(f'GRAMMAR: {random.choice(grammar.get(self))}')
        lst = to_simple_list(transformed_grammar.get(self))
        arg = random.choice(lst)
        temp = arg.generate_shortest(transformed_grammar)
        return temp

    def generate(self):
        grammar = self.grammar
        # print(f'GRAMMAR: {random.choice(grammar.get(self))}')
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, nonterminal, visited, grammar):
        # print(f'NON: self: {self.nonterminal}, nont: {nonterminal.to_string()}, visi: {[x.to_string() for x in visited]}')
        if self in visited:
            return False
        if self == nonterminal:
            # print("NON: TRUE")
            return True
        visited.append(self)
        # print(f'\t--> NON self: {self} --> {self.nonterminal} --> {self in self.grammar.keys()}')
        for elem in grammar.get(self):
            # print(f'NON2: {elem}')
            if elem.contains_cycle(nonterminal, visited, grammar):
                # print(f'\tNON: TRUE')
                return True
        return False
        # if isinstance(self.nonterminal, Nonterminal):
        #     return self.nonterminal == nonterminal
        # return self.nonterminal.contains_cycle(nonterminal)

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
        # print(f'GRAMMAR: {random.choice(grammar.get(self))}')
        arg = random.choice(transformed_grammar.get(self))
        temp = arg.generate_shortest(transformed_grammar)
        return temp

    def generate(self):
        grammar = self.grammar
        # print(f'GRAMMAR: {random.choice(grammar.get(self))}')
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, token, visited, grammar):
        return False

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





