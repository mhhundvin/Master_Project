from lark import Lark

larkGrammar = open('grammars/lark.lark', 'r').read()
json_grammar = open('grammars/jsonGrammar.lark', 'r').read()
hedy_grammar = open('grammars/hedy/level_1.lark', 'r').read()
verilog_grammar = open('grammars/verilog.lark').read()
python_grammar = open('grammars/python3.lark').read()
test_grammar = open('grammars/testGrammar.lark').read()
test_grammar2 = open('grammars/testGrammar2.lark').read()

parser = Lark(larkGrammar)

tree = parser.parse(hedy_grammar)