from lark import Lark

json_grammar = open('grammars/jsonGrammar.lark', 'r').read()
hedy_grammar = open('grammars/hedy/level1.lark', 'r').read()
verilog_grammar = open('grammars/verilog.lark').read()
python_grammar = open('grammars/python3.lark').read()
test_grammar = open('grammars/testGrammar.lark').read()
test_grammar2 = open('grammars/testGrammar2.lark').read()

parser = Lark(test_grammar2)

output = "program h { const _ ; const _ ; N = 323745 ; _ = 91 ; _ = 014 ; _ = 76 ; _ = 9431444 ; _ = 53 ; }"
output = "[ false ]"
output = "print You are my best child"

output = "if ( 38 ) { print 5843; print 134433; print 9556064; print 3607207; print 20; print 3357629; print 017357182; print 6; print 9173;  }"

# output = output.replace(' ', '')


tree = parser.parse(output)

print(tree.pretty())