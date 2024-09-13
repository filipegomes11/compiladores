class ThreeAddressCode:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def nova_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def nova_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate_code(self, symbol_table):
        for entry in symbol_table:
            if isinstance(entry[4], str) and entry[4].strip() == '=':
                var_name = entry[3]
                expression = entry[5]
                if isinstance(expression, list):
                    self.process_expression(var_name, expression)
                else:
                    self.instructions.append(f"{var_name} = {expression}")
            elif entry[2] == 'CALL':
                self.process_call(entry)
            elif entry[2] == 'FUNC':
                self.process_function(entry)
            elif entry[2] == 'PROC':
                self.process_procedure(entry)
            elif entry[2] == 'IF':
                self.process_if(entry)
            elif entry[2] == 'WHILE':
                self.process_while(entry)

    def process_expression(self, var_name, expression):
        if expression[0] == 'CALL':
            return
        if len(expression) == 1:
            self.instructions.append(f"{var_name} = {expression[0]}")
        else:
            temp_var = self.nova_temp()
            self.instructions.append(f"{temp_var} = {expression[0]} {expression[1]} {expression[2]}")
            for i in range(3, len(expression), 2):
                if i + 1 < len(expression):
                    next_temp = self.nova_temp()
                    self.instructions.append(f"{next_temp} = {temp_var} {expression[i]} {expression[i+1]}")
                    temp_var = next_temp
            self.instructions.append(f"{var_name} = {temp_var}")

    def process_call(self, entry):
        if entry[3] == 'FUNC':
            func_name = entry[4]
            params = entry[5]
            for param in params:
                self.instructions.append(f"param {param}")
            temp_var = self.nova_temp()
            self.instructions.append(f"{temp_var} = call {func_name}")
            self.instructions.append(f"{entry[3]} = {temp_var}")
        elif entry[3] == 'PROC':
            proc_name = entry[4]
            params = entry[5]
            for param in params:
                self.instructions.append(f"param {param}")
            self.instructions.append(f"call {proc_name}")

    def process_function(self, entry):
        func_name = entry[4]
        self.instructions.append(f"{func_name}:")
        for sub_entry in entry[6]:
            self.generate_code([sub_entry])

    def process_procedure(self, entry):
        proc_name = entry[3]
        self.instructions.append(f"{proc_name}:")
        for sub_entry in entry[5]:
            self.generate_code([sub_entry])

    def process_if(self, entry):
        condition = entry[3]
        true_label = self.nova_label()
        false_label = self.nova_label()
        end_label = self.nova_label()

        self.instructions.append(f"if {condition[0]} {condition[1]} {condition[2]} goto {true_label}")
        self.instructions.append(f"goto {false_label}")
        self.instructions.append(f"{true_label}:")
        for sub_entry in entry[4]:
            self.generate_code([sub_entry])
        self.instructions.append(f"goto {end_label}")
        self.instructions.append(f"{false_label}:")
        if len(entry) > 5 and isinstance(entry[5], list):
            if entry[5][2] == 'ELSE':
                for sub_entry in entry[5][3]:
                    self.generate_code([sub_entry])
        self.instructions.append(f"{end_label}:")

    def process_while(self, entry):
        condition = entry[3]
        start_label = self.nova_label()
        end_label = self.nova_label()

        self.instructions.append(f"{start_label}:")
        self.instructions.append(f"ifFalse {condition[0]} {condition[1]} {condition[2]} goto {end_label}")
        for sub_entry in entry[4]:
            self.generate_code([sub_entry])
        self.instructions.append(f"goto {start_label}")
        self.instructions.append(f"{end_label}:")

    def print_instructions(self):
        for instr in self.instructions:
            print(instr)