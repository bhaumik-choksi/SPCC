# Removes direct left recursion
grammar = {}
n = int(input("Enter no. of lines in the grammar"))
print("Grammar should be formatted as N->A|AB|a")
for i in range(n):
    LHS,RHS = input("Enter next line").strip().split("->")
    grammar[LHS.strip()] = RHS.split("|")   # Taking input into dictionary, separating each production

for key,value in grammar.items():
    alpha_terms = []    # Left-Recursive productions
    beta_terms = []     # Non left-recursive productions
    for prods in value: # Loop to separate recursive and non-recursive terms
        if prods[0] == key:
            alpha_terms.append(prods)
        else:
            beta_terms.append(prods)
    grammar[key] = {"recursive_part":alpha_terms,"non-recursive_part":beta_terms}
# print(grammar)
output_grammar = {} # This dictionary will store output productions
for LHS, RHS in grammar.items():
    if len(RHS["recursive_part"]) != 0:
        new_nonterminal = LHS + "'"     # A' will store the new productions of A
        new1 = []   # A -> aA'
        new2 = []   # A' -> bA'
        for production in RHS["non-recursive_part"]:
            new1.append(production+new_nonterminal)
        for production in RHS["recursive_part"]:
            new2.append(production+new_nonterminal)
        new2.append("@") # Append an epsilon
        output_grammar[LHS] = new1
        output_grammar[new_nonterminal] = new2
    else:
        output_grammar[LHS] = RHS["non-recursive_part"]
print("Given grammar without left recursion is : ")
for key,value in output_grammar.items():
    print(key,"->",value)