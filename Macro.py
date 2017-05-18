import re   # Regex for splitting macro name line into args
f_input = open("macro_input.txt")
inputcode = list(line.strip() for line in f_input)

# Pass 1 : Building Definitions
MDT = []
MNT = {}
ALA_list = {}
input_for_pass_2 = []
iterator = iter(inputcode)
while True:
    try:
        line = next(iterator)
        if line == "MACRO":
            nameline = next(iterator)
            nameline = re.split('[,\s]',nameline)
            macro_name = ""
            for token in nameline:
                if "&" not in token:
                    macro_name = token
                    break

            label = None
            if nameline.index(macro_name) == 1:
                label = nameline[0]
            MNT[macro_name] = len(MDT)  # Add MNT entry
            ALA = {}  # Init ALA
            if label is not None:
                ALA[label] = "#LABEL"
                nameline[nameline.index(label)] = ALA[label]
            arg_counter = 0
            for token in nameline:
                if token is not "#LABEL" and token is not macro_name:
                    arg_counter += 1
                    ALA[token] = "#"+str(arg_counter)
                    nameline[nameline.index(token)] = ALA[token]
            ALA_list[macro_name] = ALA
            MDT.append(nameline)

            while True:
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
            if line[0] in MNT.keys():
                macroname = line[0]
            else:
                macroname = line[1]
                label = line[0]

        else:
            print(line)
    except StopIteration:
        break
