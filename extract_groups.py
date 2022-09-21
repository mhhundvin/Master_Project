from collections import defaultdict
from unicodedata import name
from classes import Group, Regexp, Nonterminal, Token, Sequence, Plus, Star, Optional, Literal_Range, Repeat

def extract_groups(grammar):
    new_grammar = defaultdict(list)
    for nonterminal, alternatives in grammar.items():
        # if nonterminal.to_string() == "DIGIT":
        #     break

        for alternative in alternatives:
            # print(f'{nonterminal.to_string()}:\t{alternative}')
            # temp = extract_group(new_grammar, nonterminal, alternative, 0)
            # print(f'\t{temp.to_string()}')
            # print(f'\t\t{new_grammar[temp][0].to_string()}')
            temp, _ = extract_group(new_grammar, nonterminal, alternative, 0)
            new_grammar[nonterminal].append(temp)

            # print(new_grammar.keys())
        # break

    print('\n##############################\n')
    for k, v in new_grammar.items():
        print(f'\n{k.to_string()}:')#\t\t\t{v}')
        for elem in v:
            print(f'\t{elem.to_string()}')
    
    return new_grammar


def extract_group(grammar, nonterminal, alternative, num):
    # print(f'1: {alternative}')

    if isinstance(alternative, list):
        alternative = Sequence( alternative )
    elif not isinstance(alternative, Sequence):
        alternative = Sequence( [alternative] )

    # print(f'2: {alternative} --> {alternative.get_arg()}')
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    
    new_alternative = []
    for element in alternative.get_arg():
        # print(f'\n\tELEMENT ==> {element}\n')
        if isinstance(element, Group):
            # print(f'==>{element}: {element.get_arg()}')
            temp, num = extract_group(grammar, nonterminal, element.get_arg(), num)
            name = f'$$$_{nonterminal.to_string()}_{num}'
            if isinstance(nonterminal, Nonterminal):
                name = Nonterminal( name, grammar )
            else:
                name = Token( name.upper(), grammar )
            # if ("expr_stmt_0_" in name.to_string()):
            #     raise Exception(f'{temp.get_arg()[0].get_arg()}')
            num += 1
            grammar[name] = temp.get_arg()
            new_alternative.append(name)


        
        elif isinstance(element, Plus):
            temp, num = extract_group(grammar, nonterminal, element.get_arg(), num)
            new_alternative.append( Plus( temp ))
        elif isinstance(element, Star):
            temp, num = extract_group(grammar, nonterminal, element.get_arg(), num)
            new_alternative.append( Star( temp ))
        elif isinstance(element, Optional):
            temp, num = extract_group(grammar, nonterminal, element.get_arg(), num)
            new_alternative.append( Optional( temp ))
        elif isinstance(element, Repeat):
            arg, start, stop = element.get_arg()
            temp, num = extract_group(grammar, nonterminal, arg, num)
            new_alternative.append( Repeat( temp, start, stop ))

        elif isinstance(element, Sequence):
            temp, num = extract_group(grammar, nonterminal, element.get_arg(), num)
            new_alternative.append( temp )
            

        else:
            new_alternative.append(element)

        if isinstance(element, Regexp):
            element.set_name(nonterminal)
            
    # grammar[nonterminal].append(Sequence( new_alternative ))
    # return "no Group"
    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    return Sequence( new_alternative ), num