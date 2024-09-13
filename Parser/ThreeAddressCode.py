class ThreeAddressCode:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def nova_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate_code(self, symbol_table):
        for entry in symbol_table:
            if isinstance(entry[4], str) and entry[4].strip() == '=':
                var_name = entry[3]
                expression = entry[5]
                if isinstance(expression, list):
                    print(entry)
                    self.process_expression(var_name, expression)
                else:
                    self.instructions.append(f"{var_name} = {expression}")
            elif entry[0] == 0 and entry[2] == 'CALL':
                self.process_call(entry)

    def process_expression(self, var_name, expression):
        print('EXP', expression)
        if expression[0] == 'CALL':
            return
        if len(expression) == 1:
            self.instructions.append(f"{var_name} = {expression[0]}")
        else:
            temp_var = self.nova_temp()
            self.instructions.append(f"{temp_var} = {expression[0]} {expression[1]} {expression[2]}")
            for i in range(3, len(expression), 2):
                print('AAA', expression[i+1])
                next_temp = self.nova_temp()
                self.instructions.append(f"{next_temp} = {temp_var} {expression[i]} {expression[i+1]}")
                temp_var = next_temp
            self.instructions.append(f"{var_name} = {temp_var}")

    def process_call(self, entry):
        if entry[2] == 'CALL' and entry[3] == 'FUNC':
            func_name = entry[4]
            params = ', '.join(entry[5])
            self.instructions.append(f"{func_name}({params})")
        elif entry[2] == 'CALL' and entry[3] == 'PROC':
            proc_name = entry[4]
            params = ', '.join(entry[5])
            self.instructions.append(f"{proc_name}({params})")

    def print_instructions(self):
        for instr in self.instructions:
            print(instr)