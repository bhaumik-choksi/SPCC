import re   # Regex for splitting macro name line into args
f_input = open("macro_input.txt")  # File Input
inputcode = list(line.strip() for line in f_input)

# Pass 1 : Building Definitions
# Initialize Data Structures
MDT = []    # MDT is a list since we need to iterate over it
MNT = {}    # MNT is a dictionary since we need to query it
ALA_list = {}   # ALA_list stores ALA for each macro, with the macro name as key
input_for_pass_2 = []   # Lines that are not part of the macro def are sent to pass 2
iterator = iter(inputcode)
while True:
    try:
        line = next(iterator)
        if line == "MACRO":  # Macro definition found
            nameline = next(iterator)
            nameline = re.split('[,\s]',nameline)   # Split line into words
            macro_name = ""
            for token in nameline:
                if "&" not in token:    # Macro name is the word with no ampersand
                    macro_name = token
                    break

            MNT[macro_name] = len(MDT)  # Add MNT entry
            ALA = {}  # Init ALA
            arg_counter = 0
            for token in nameline:  # Adding arguments to ALA
                if token is not macro_name:
                    arg_counter += 1
                    ALA[token] = "#"+str(arg_counter)
                    nameline[nameline.index(token)] = ALA[token]    # Replacing args in macro name line
            ALA_list[macro_name] = ALA
            MDT.append(nameline)

            while True:  # Add subsequent lines into macro definition
                macroline = next(iterator)
                for argument in ALA.keys():
                    if argument in macroline:
                        macroline = macroline.replace(argument,ALA[argument])
                MDT.append(macroline)
                if macroline == "MEND":
                    break
        else:
            input_for_pass_2.append(line)
    except StopIteration:
        break
# Pass 1 ends. Print all tables.
print("\nMNT is ")
for line in MNT.items():
    print(line)
print("\nMDT is ")
for line in MDT:
    print(line)
print("\nALAs are ")
for line in ALA_list.items():
    print(line)

# Pass 2 : Replace Macro Calls
iterator = iter(input_for_pass_2)
print("\n Final Output is ")
while True:
    try:
        line = next(iterator)
        line = re.split('[,\s]', line)
        if any(word in line for word in MNT.keys()):  # MACRO NAME FOUND
            macroname = ""
            # Macro name could be on pos 0 or 1 based on the presence of a label
            if line[0] in MNT.keys():
                macroname = line[0]
            else:
                macroname = line[1]
                label = line[0]
            actual_args = []
            # Append everything that is not the macro name into actual arg list
            # Everything in the macro call apart from macro name is an argument
            for token in line:
                if not token == macroname:
                    actual_args.append(token)
            # Hail Bhaumik
            ALA = ALA_list  [macroname]
            ALA = {val: key for key, val in ALA.items()} # Reverse mapping of ALA from B->A to A->B
            formal_args = sorted(list(ALA.keys()))
            for i in range(len(formal_args)):
                ALA[formal_args[i]] = actual_args[i]    # Add actual arguments into ALA
            MDTP = MNT[macroname] + 1
            while "MEND" not in MDT[MDTP]:
                line = MDT[MDTP]
                for formal_arg,actual_arg in ALA.items():
                    line = line.replace(formal_arg,actual_arg)
                print(line) # Print each line in expanded macro
                MDTP += 1
        else:
            print(" ".join(line))   # Print "line" array as string
    except StopIteration:
        break
# https://www.youtube.com/watch?v=dQw4w9WgXcQ
