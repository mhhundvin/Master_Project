from ast import arg


class Regexp_class():
    pass

class P_element(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt

class Letter(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Symbol(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Escaped_symbol(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Look(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Range_elt(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Range(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return f'[{txt}]'


class Repetition(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        for elem in args:
            print(elem)
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Rex(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        if isinstance(args, Regexp_class):
            return args.to_string()
        for elem in args:
            print(f'\nelem: {elem}\n')
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt


class Regex_ere(Regexp_class):
    def __init__(self, args):
        self.args = args

    def to_string(self):
        args = self.args
        txt = ""
        if isinstance(args, Regexp_class):
            return args.to_string()
        for elem in args:
            if isinstance(elem, Regexp_class):
                elem = elem.to_string()
            txt += elem
        return txt
