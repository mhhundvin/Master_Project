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
import random

class Generatable():
    pass


class Repeat(Generatable):
    def __init__(self, args, start=0, end=random.randint(1,3)):
        self.args = args
        self.start = start
        self.end = end
    
    def generate(self):
        arg = self.args
        terminal_string = ''
        for _ in range(self.start, self.end+1):
            terminal_string += arg.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited)
        return False


class Optional(Generatable):
    def __init__(self, args):
        self.args = args
    
    def generate(self):
        arg = random.choice(self.args)
        if isinstance(arg, Generatable):
            return arg.generate()
        return arg

    def contains_cycle(self, nonterminal, visited):
        for elem in self.args:
            if isinstance(elem, Generatable):
                return elem.contains_cycle(nonterminal, visited)
        return False


class Star(Generatable):
    def __init__(self, args):
        self.args = args
    
    def generate(self):
        terminal_string = ''
        for _ in range(0, random.randint(0,3)):
            terminal_string += self.args.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited)
        return False


class Plus(Generatable):
    def __init__(self, args):
        self.args = args
    
    def generate(self):
        terminal_string = ''
        for _ in range(0, random.randint(1,3)):
            terminal_string += self.args.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited)
        return False


class Sequence(Generatable):
    def __init__(self, args):
        self.args = args
    
    def generate(self):
        terminal_string = ''
        for elem in self.args:
            # print(f'Seq elem: {elem}\n-->  {elem.generate()}')
            # print(f'Seq str: {terminal_string}')
            terminal_string += elem.generate()
        return terminal_string

    def contains_cycle(self, nonterminal, visited):
        for elem in self.args:
            if elem.contains_cycle(nonterminal, visited):
                return True
        return False

# class Expansions(Generatable):
#     def __init__(self, args):
#         self.args = args
    
#     def generate(self):
#         x = random.choice(self.args)
#         return x[0].generate()

class Regexp(Generatable):
    def __init__(self, args):
        self.args = args
    
    def generate(self):
        words = ["apple", "banana", "cherry"]
        return random.choice(words)
        # return "-regexp-"  # self.args

    def contains_cycle(self, nonterminal, visited):
        if isinstance(self.args, Generatable):
            return self.args.contains_cycle(nonterminal, visited)
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

    def generate(self):
        grammar = self.grammar
        # print(f'GRAMMAR: {random.choice(grammar.get(self))}')
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, nonterminal, visited):
        # print(f'NON: self: {self.nonterminal}, nont: {nonterminal.to_string()}, visi: {[x.to_string() for x in visited]}')
        if self in visited:
            return False
        if self == nonterminal:
            # print("NON: TRUE")
            return True
        visited.append(self)
        # print(f'\t--> NON self: {self} --> {self.nonterminal} --> {self in self.grammar.keys()}')
        for elem in self.grammar.get(self):
            # print(f'NON2: {elem}')
            if elem.contains_cycle(nonterminal, visited):
                # print(f'\tNON: TRUE')
                return True
        return False
        # if isinstance(self.nonterminal, Nonterminal):
        #     return self.nonterminal == nonterminal
        # return self.nonterminal.contains_cycle(nonterminal)

class Terminal(Generatable):
    def __init__(self, terminal):    
        self.terminal = terminal

    def generate(self):
        return self.terminal.replace('\\', '')
    
    def contains_cycle(self, nonterminal, visited):
        if isinstance(self.terminal, Generatable):
            return self.terminal.contains_cycle(nonterminal, visited)
        return False





