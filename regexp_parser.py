from lark import Lark

regexpGrammar = open('grammars/lark_regexp.lark', 'r').read()

parser = Lark(regexpGrammar)

# id_start =  '/[\\p{Lu}\\p{Ll}\\p{Lt}\\p{Lm}\\p{Lo}\\p{Nl}_]+/'
id_start = '/[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+/'
id_continue = '/[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+/'

multiline_comment = '/\/\*(\*(?!\/)|[^*])*\*\//'

float_number =  '/((\d+\.\d*|\.\d+)(e[-+]?\d+)?|\d+(e[-+]?\d+))/'

letters = '/[A-Za-z]+/'

letter = '/(A|B+)*/'

tree = parser.parse(letter)

# print(tree.pretty())