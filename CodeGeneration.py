# Input must be in 3 address code form
import re   # Regex for splitting

registers = {}  # Dictionary to keep track of register assignment
output_code = []  # Output lines


def allocateRegister(operand):
    if operand in registers.values():  # Operand already present in one of the registers, use it
        for key, value in registers.items():
            if operand == value:
                return key
    else:
        register_name = "R" + str(len(registers))  # Allocate a new register for the operand
        registers[register_name] = operand  # Assign operand to register
        output_code.append("MOV "+operand+","+register_name)  # Add MOV statement to output
        return register_name


input_code = list(line.strip() for line in open("code_gen_input.txt"))
for line in input_code:
    line = re.split("([\=\+\-\*\/])", line)  # Split the TAG into operands and operator
    LHS, eq, op1, operator, op2 = line
    op1 = allocateRegister(op1)
    op2 = allocateRegister(op2)
    if operator.strip() == "+":
        output_line = "ADD "+str(op1)+","+str(op2)
        registers[op2] = LHS    # Register now hold output i.e. LHS
    elif operator.strip() == "-":
        output_line = "SUB " + str(op1) + "," + str(op2)
        registers[op2] = LHS
    elif operator.strip() == "*":
        output_line = "MUL " + op1 + "," + op2
        registers[op2] = LHS
    elif operator.strip() == "/":
        output_line = "DIV " + op1 + "," + op2
        registers[op2] = LHS
    output_code.append(output_line)
for line in output_code:
    print(line)
    