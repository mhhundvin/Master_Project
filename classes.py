import random
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
    def to_string(self):
        """Returnes the original format for the given element."""
        pass

    def get_arg(self):
        """Returnes the arguments of the element."""
        pass

    def generate(self):
        """Generates terminal string from the arguments for the element."""
        pass

    def contains_cycle(self, nonterminal, visited, grammar):
        """Returnes ture or false based on weather or not the arguments contains a path to the given nonterminal."""
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

    def generate(self):
        temp = f'[{self.start.generate()}-{self.stop.generate()}]'
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
            if isinstance(elem, Generatable):
                lst.append(elem.to_string())
            else:
                lst.append(elem)
        temp = ' | '.join(lst)
        return f'(({temp}))'
    
    def get_arg(self):
        return self.args
    
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
    
    def generate(self):
        terminal_string = ''
        for elem in self.args:
            if isinstance(elem, Generatable):
                terminal_string += elem.generate()
            else:
                terminal_string += elem
            # if terminal_string and terminal_string[-1] != " " and not isinstance(elem, Token):
            #     terminal_string += " "
        return terminal_string

    def contains_cycle(self, nonterminal, visited, grammar):
        args = self.args
        for elem in args:
            if isinstance(elem, list):
                elem = elem[0]
            if not isinstance(elem, Generatable):
                continue
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
    
    def generate(self):
        name = self.name.to_string()
        regexp = self.args
        regexp = regexp[1:-1]
    
        if "comment" in name.lower():
            comments = [
                "This is a comment",
                "/* This is a comment */",
                "// This is a comment",
                "# This is a comment",
                "# This is a\n# comment",
                "% This is a\n# comment",
                "-- This is a comment",
                "- - This is a comment",
                "{- This is a comment -}",
                "=begin\nThis is a comment\n=end",
                "<!--  This is a comment -->"
            ]
            for c in comments:
                if re.fullmatch(regexp, c):
                    return c

        elif "name" in name.lower() or "var" in name.lower() or "identifier" in name.lower():
            variables = ['variable_0', 'variable_1', 'variable_2', 'variable_3', 'variable_4', 'variable_5', 'variable_6', 'variable_7', 'variable_8', 'variable_9']
            # var = random.choice(variables)
            # while re.fullmatch(regexp, var) == None:
            #     var = random.choice(variables)
            for var in variables:
                if re.fullmatch(regexp, var):
                    return var

        
        txt = ""
        with open("regexp_text.txt", 'r') as f:
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
        return self.nonterminal == other.nonterminal
    
    def to_string(self):       
        return self.nonterminal

    def generate(self):
        grammar = self.grammar
        return random.choice(grammar.get(self)).generate()

    def contains_cycle(self, nonterminal, visited, grammar):
        if self in visited or isinstance(nonterminal, Token):
            return False
        if self == nonterminal:
            return True
        visited.append(self)
        for elem in grammar.get(self):
            if isinstance(elem, list):
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

    def generate(self):
        return self.terminal.replace("\\n", "\n").replace("\\r", "\r").replace("\\", "")
    
    def contains_cycle(self, nonterminal, visited, grammar):
        if isinstance(self.terminal, Generatable):
            return self.terminal.contains_cycle(nonterminal, visited, grammar)
        return False





