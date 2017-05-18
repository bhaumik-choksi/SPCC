table = [["e",">",">",">"],["<",">","<",">"],["<",">",">",">"],["<","<","<","a"]]
indices = {"i":0,"+":1,"*":2,"$":3}
stack = ["$"]   # Not an actual stack. List is used as a stack.
# Picture of parse table used :  https://snag.gy/T3lzt0.jpg
# Only 3 operator for simplicity
input_string = input("Enter expression to parse").strip()
input_string += "$" # Append $ at the end of the input string
input_string = list(input_string)
iterator = iter(input_string)
character = next(iterator)
while True:
        try:
            if character == " ":    # Ignore spaces
                character = next(iterator)
                continue
            if character.isdigit() == False and character.isalpha() == False and character not in indices.keys():
                print("Parse Error. Bad Symbol.")
                print(character)
                break
            else:
                if character not in indices.keys():
                    op = "i"    # Convert all numbers/letters to i
                else:
                    op = character
                print("Stack is ",stack," char is ",op)
                row = indices[stack[-1]]
                col = indices[op]
                if table[row][col] == "<":
                    stack.append(op)    # Push
                    character = next(iterator)
                elif table[row][col] == ">":
                    del stack[-1]       # Pop
                elif table[row][col] == "a":
                    print("Accepted")
                    break
                else:
                    print("Parsing failed")
                    break
        except StopIteration:
            break