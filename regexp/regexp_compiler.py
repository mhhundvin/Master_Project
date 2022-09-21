from lark import Transformer
from regexp_compiler.regexp_parser import tree
from regexp_compiler.regexp_classes import P_element, Letter, Symbol, Escaped_symbol, Look, Range_elt, Range, Repetition, Rex, Regex_ere

divided_regexp = []

class Compiler(Transformer):

    def start(self, args):
        if (len(args)>0):
            print(f'start: {args[0]}')
        return args

    def regex(self, args):
        if (len(args)>0):
            print(f'regex: {args[0]}')
        return args

    def regex_ere(self, args):
        temp = []
        for arg in args:
            temp.append(Rex(arg))
        # if (len(args)>0):
        #     print(f'regex_ere: {args[0]}')
        #     temp =  Regex_ere( args[0] )
        #     divided_regexp.append(temp)
        #     return temp
        divided_regexp.append(temp)
        return temp

    def rex(self, args):
        if (len(args)>0):
            print(f'rex: {args[0]}')
            temp =  Rex( args )
        # divided_regexp.append(temp)
            return temp
        return args

    def repetition(self, args):
        if (len(args)>0):
            print(f'repetition: {args[0]}')
            temp =  Repetition( args )
        # divided_regexp.append(temp)
            return temp
        return args

    def range(self, args):
        if (len(args)>0):
            print(f'range: {args[0]}')
            temp =  Range( args )
        # divided_regexp.append(temp)
            return temp
        return args


    def range_elt(self, args):
        if (len(args)>0):
            print(f'range_elt: {args[0]}')
            temp =  Range_elt( args )
        # divided_regexp.append(temp)
            return temp
        return args

    def look(self, args):
        if (len(args)>0):
            print(f'look: {args[0]}')
            temp =  Look( args )
        # divided_regexp.append(temp)
            return temp
        return args

    # def lookahead(self, args):
    #     return args[0]

    # def negative_lookahead(self, args):
    #     return args[0]

    # def positive_lookbehind(self, args):
    #     return args[0]

    # def negative_lookbehind(self, args):
        # return args[0]

    def ESCAPED_SYMBOL(self, args):
        if (len(args)>0):
            print(f'ESCAPED_SYMBOL: {args[0]}')
            temp = Escaped_symbol( args[0] )
        # divided_regexp.append(temp)
            return temp
        return args

    def SYMBOL(self, args):
        if (len(args)>0):
            print(f'SYMBOL: {args[0]}')
            temp =  Symbol( args[0] )
        # divided_regexp.append(temp)
            return temp
        return args

    def LETTER(self, args):
        if (len(args)>0):
            # print(f'LETTER: {args[0]}')
            temp =  Letter( args[0] )
        # divided_regexp.append(temp)
            return temp
        return args

    def P_ELEMENT(self, args):
        if (len(args)>0):
            print(f'P_ELEMENT: {args[0]}')
            temp = P_element( args[0] )
        # divided_regexp.append(temp)
            return temp
        return args


new_tree = Compiler().transform(tree)
# print(new_tree)

txt = ""
for elem in divided_regexp:
    if (isinstance(elem, list)):
        for e in elem:
            txt += e.to_string()
        print(txt)
    else:
        print(f'ELEM: {elem.to_string()}')
    # txt += elem.to_string()
print(txt)