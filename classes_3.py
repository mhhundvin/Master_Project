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
import numpy as np
import re

def draw_random_normal_int(low:int, high:int):

    # generate a random normal number (float)
    normal = np.random.normal(loc=0, scale=1, size=1)

    # clip to -3, 3 (where the bell with mean 0 and std 1 is very close to zero
    # normal = -3 if normal < -3 else normal
    # normal = 3 if normal > 3 else normal

    # scale range of 6 (-3..3) to range of low-high
    # scaling_factor = (high-low) / 6
    # normal_scaled = normal * scaling_factor

    # center around mean of range of low high
    # normal_scaled += low + (high-low)/2

    # then round and return
    # temp = np.round(normal)#_scaled)
    # print(temp)
    # return int(temp[0])
    temp = random.randint(low, high)
    # print(temp)
    return temp

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
        temp = f'[{self.start.generate()}-{self.stop.generate()}]'
        # print(f'LITERAL RANGE: {temp}')
        return exrex.getone(temp)

    def contains_cycle(self, nonterminal, visited, grammar):
        return False

#####################################################################################

# expr_range
class Repeat(Generatable):
    def __init__(self, args, start, stop):
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
        if len(arg) > 1:
            if not isinstance(arg[1], str):
                return f'<{list_to_string(arg)}>?'
        if isinstance(arg[0], Generatable):
            return f'<{arg[0].to_string()}>?'
        return f'<{arg[0]}>?'
        # return f'<{list_to_string(arg)}>?'

    def get_arg(self):
        return self.args
    
    def generate_shortest(self, transformed_grammar):
        return ""

    
    def generate(self):
        # print(f'\n\n\t{self.args}')
        args = self.args
        if isinstance(args, Sequence) or isinstance(args, Group):
            args = args.get_arg()
        if not isinstance(args, list):
            raise Exception(f"What happend now? --> {args} <--")
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
        # print(f'\t==>STAR( {arg} )\n')
        terminal_string = ''
        for _ in range(0, draw_random_normal_int(0,9)):
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
    
    # def generate(self):
    #     arg = self.args
    #     if isinstance(arg, list):
    #         arg = arg[0]
    #     terminal_string = ''
    #     for _ in range(0, draw_random_normal_int(1,9)):
    #         terminal_string += arg.generate()
    #     return terminal_string
    
    def generate(self):
        arg = self.args
        # print(f'\t==>PULS( {arg} )\n')
        terminal_string = ''
        for _ in range(0, draw_random_normal_int(1,9)):
            # print(arg)
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
        return f'(({temp}))'
    
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
            if terminal_string[-1] != " " and not isinstance(elem, Token):
                terminal_string += " "
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

class One_word(Generatable):
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

    def set_name(self, name):
        self.name = name

    def to_string(self):
        return self.args
    
    
    def generate_shortest(self, transformed_grammar):
        return self.generate()
    
    def generate(self):
        name = self.name.to_string()
        regexp = self.args
        # if regexp[-1] == "i":
        #     regexp = regexp[1:-2]
        # else:
        regexp = regexp[1:-1]
    
        # print(f'{self.args} ==> {regexp}')
        if "comment" in name.lower():
            txt = ""
            for e in regexp:
                if e == "\\":
                    continue
                elif e =="[":
                    break
                txt += e
            temp = f'{txt}(?=\[)'
            new_regexp = regexp.replace("\\", '')
            m = re.search(temp, new_regexp)
            if m:
                return f'{txt} This is a comment'
            return "This is a comment"

        elif "name" in name.lower() or "var" in name.lower():
            variables = ['variable_0', 'variable_1', 'variable_2', 'variable_3', 'variable_4', 'variable_5', 'variable_6', 'variable_7', 'variable_8', 'variable_9']
            var = random.choice(variables)
            if re.fullmatch(regexp, var):
                return var

        
        txt = ""
        with open("text.txt", 'r') as f:
            for line in f.readlines():
                txt += line
        m = re.findall(regexp, txt)
        # m = re.search(regexp, txt)
        if m:
            m = random.choice(m)
            if isinstance(m, tuple):
                return f'{m[0]}'
            return f'{m}'

            # return m.group()


        return exrex.getone(regexp)
        # return name


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
        # print(f'\n\n{self.nonterminal} == {other}')
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





