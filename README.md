# Master Project    
## Implementing a tool for browsing syntax of programming languages     

---
### File overview:
*\grammars* contains all the lark grammars.     

*classes.py* and *classes_2.py* contains the different classes I have created to represent the grammar
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

*compiler.py* contains the class **Compiler**, the function **transform_grammar()** and a at the moment a for-loop for generating the shortest terminal string for the different nonterminals.
- **Compiler** uses Transformer from the Lark library to travers the tree creating the new representation, a python dictionary, using the classes from *classes_p.py*
- **transform_grammar()** loops throug the new representation removing cycles if possible.

*lark_parser.py* reads in the lark.lark grammar and using the Lark library creates a parser for lark grammars. It then uses this parser to parse one of the grammars in the */grammars* folder creating the tree *compiler.py* imports.
