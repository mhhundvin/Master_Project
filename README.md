## Master Project:
# Implementing a tool for browsing syntax of programming languages     


### File overview:
- *\grammars* folder contains all the lark grammars, including the *lark.lark* grammar that is being used to create the lark parser.     

- *classes.py* and *classes_2.py* contains the different classes I have created to represent the grammar
  1. Generatable
  2. Literal_Range
  3. Repeat 
  4. Optional
  5. Star
  6. Plus
  7. Sequence
  8. Expansions
  9. Regex
  10. Nonterminal
  11. Terminal
     
  All the classes except for Generatable have the same functionalities. Generatable is an empty class that can be use in the other classes to see if the element that is being looked at have a generate function.

  The other classes have functions *to_string()*, *contains_cycle()*, *generate_shortest()* and *generate()*, the Nonterminal class also have functionality for comparison.
   - *to_string()* returns the original string from the grammar.
   - *contains_cycle()* takes the parameters nonterminal, visited and grammar, where nonterminal is the rule we are looking at, visited is a list for the nonterminal we have already checked and grammar is tha grammer we are looking through.

- *compiler.py* contains the class **Compiler**, the function **transform_grammar()** and a at the moment a for-loop for generating the shortest terminal string for the different nonterminals.
  - **Compiler** uses Transformer from the Lark library to traverse the tree creating the new representation, a python dictionary, using the classes from *classes_p.py*
  - **transform_grammar()** loops through the new representation removing cycles if possible.       
  
- *lark_parser.py* reads in the lark.lark grammar and using the Lark library creates a parser for lark grammars. It then uses this parser to parse one of the grammars in the */grammars* folder creating the tree *compiler.py* imports.
