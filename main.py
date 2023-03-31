from tkinter import *
from tkinter.ttk import *
import re
import itertools
import random


class Case:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, fileName=None):
        self.name = ""
        self.attributes = ""
        self.constraints = ""
        self.penalty = ""
        self.possibility = ""
        self.quality = ""
        if fileName is not None:
            file_addr = '{}/attributes.txt'.format(fileName)
            attr = read_file(file_addr)
            file_addr = '{}/constraints.txt'.format(fileName)
            constraints = read_file(file_addr)

            file_addr = '{}/penaltylogic.txt'.format(fileName)
            penalty = read_file(file_addr)
            file_addr = '{}/possibilisticlogic.txt'.format(fileName)
            possibilistic = read_file(file_addr)
            file_addr = '{}/qualitativechoicelogic.txt'.format(fileName)
            qualitative = read_file(file_addr)

            self.name = fileName
            self.attributes = attr
            self.constraints = constraints
            self.penalty = penalty
            self.possibility = possibilistic
            self.quality = qualitative

    def null(self):
        self.name = ""
        self.attributes = ""
        self.constraints = ""
        self.penalty = ""
        self.possibility = ""
        self.quality = ""

    def manual(self, n, a, c, p, pos, q):
        self.name = n
        self.attributes = a
        self.constraints = c
        self.penalty = p
        self.possibility = pos
        self.quality = q


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

case = Case()

def manual_retrieve_input(self, n, att, con, pen, pos, qual):
    name = n.get("1.0", "end-1c")
    attr = att.get("1.0","end-1c")
    cons = con.get("1.0","end-1c")
    pena = pen.get("1.0","end-1c")
    posi = pos.get("1.0","end-1c")
    quali = qual.get("1.0","end-1c")
    try:
        case.manual(name, attr, cons, pena, posi, quali)
        text_label = Label(self, text="Accepted!", width=40, font=("TkDefaultFont", 8))
        text_label.place(x=1380, y=430)
    except:
        print("Error with Input")
        text_label = Label(self, text="Error! Check file(s) for correct format", width=40, font=("TkDefaultFont", 8))
        text_label.place(x=1380, y=430)


def file_retrieve_input(self, textBox):
    inputValue = textBox.get("1.0","end-1c")
    try:
        print(inputValue)
        case.__init__(inputValue)
        text_label = Label(self, text="Accepted!", width=40, font=("TkDefaultFont", 8))
        text_label.place(x=255, y=50)
    except:
        text_label = Label(self, text="Error with file or could not find file!", width=40, font=("TkDefaultFont", 8))
        text_label.place(x=255, y=50)


class InputPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # File Input
        text_label = Label(self, text="Manual Input", width=20, font=("TkDefaultFont", 14))
        text_label.place(x=5, y=5)
        text_label = Label(self, text="Folder Name:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=10, y=30)
        fileName = Text(self, width=20,height=1)
        fileName.place(x=10, y=52)
        buttonCommit1 = Button(self, width=10, text="Commit",command=lambda: file_retrieve_input(self, fileName))
        buttonCommit1.place(x=180,y=50)

        #Manual Input
        text_label = Label(self, text="Manual Input", width=20, font=("TkDefaultFont", 14))
        text_label.place(x=795, y=5)
        text_label = Label(self, text="Attributes:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=800, y=30)
        AttributeInput = Text(self, width=30, height=8)
        AttributeInput.place(x=800, y=52)
        text_label = Label(self, text="Constraints:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=800, y=190)
        ConstraintsInput = Text(self, width=30, height=6)
        ConstraintsInput.place(x=800, y=212)
        text_label = Label(self, text="Penalty:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=800, y=320)
        PenaltyInput = Text(self, width=30, height=6)
        PenaltyInput.place(x=800, y=342)
        text_label = Label(self, text="Possibilistic:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=800, y=450)
        PossibilisticInput = Text(self, width=30, height=6)
        PossibilisticInput.place(x=800, y=472)
        text_label = Label(self, text="Qualitative:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=800, y=580)
        QualitativeInput = Text(self, width=30, height=6)
        QualitativeInput.place(x=800, y=602)
        newfileName = Text(self, width=20, height=1)
        text_label = Label(self, text="Case Name:", width=20, font=("TkDefaultFont", 12))
        text_label.place(x=1200, y=433)
        newfileName.place(x=1200, y=453)
        buttonCommit = Button(self, width=10, text="Commit", command=lambda: manual_retrieve_input(self, newfileName, AttributeInput, ConstraintsInput, PenaltyInput, PossibilisticInput, QualitativeInput))
        buttonCommit.place(x=1380, y=450)
        SaveButton = Button(self, width=10, text="Save",
                              command=lambda: print("Add save func"))
        SaveButton.place(x=1380, y=480)


def parse_text(text):
    lines = text.strip().split('\n')
    parsed = {}
    for line in lines:
        category, items = line.split(':')
        parsed[category.strip()] = [item.strip() for item in items.split(',')]
    return parsed


def parse_input_string(input_string):
    pattern = r'(NOT )?([\w-]+)(?: OR )?'
    matches = re.findall(pattern, input_string)
    parsed = []
    for match in matches:
        if match[0] == 'NOT ':
            parsed.append(['NOT', match[1]])
        else:
            parsed.append(['+', match[1]])
    return parsed


def parse_penalty(text):
    input_lines = text.strip().split('\n')
    parsed_input = []
    for line in input_lines:
        items = line.split(',', 1)
        if len(items) == 2:
            first, second = items
            first_items = first.split()
            if len(first_items) >= 3 and first_items[1] in ['AND', 'OR']:
                operator = first_items[1]
                parsed_input.append([first_items[0], operator, ' '.join(first_items[2:]), int(second.strip())])
    return parsed_input


def parse_poss(text):
    input_lines = text.strip().split('\n')
    parsed_input = []
    for line in input_lines:
        items = line.split(',', 1)
        if len(items) == 2:
            first, second = items
            first_items = first.split()
            if len(first_items) >= 3 and first_items[1] in ['AND', 'OR']:
                operator = first_items[1]
                try:
                    value = float(second.strip())
                except ValueError:
                    value = int(second.strip())
                parsed_input.append([first_items[0], operator, ' '.join(first_items[2:]), value])
    return parsed_input


def parse_choice(text):
    # Split text into lines and remove empty lines
    lines = filter(lambda x: x.strip(), text.split("\n"))

    # Split each line into tokens
    tokens_list = [line.split() for line in lines]

    # Remove "IF" from the end of lines that end with it
    for tokens in tokens_list:
        if len(tokens) > 1 and tokens[-1] == "IF":
            tokens.pop(-1)

    # Return the list of tokens for each line
    return tokens_list


def constr(items, text):
    sub_expressions = text.split('\n')
    for sub_expr in sub_expressions:
        value = parse_input_string(sub_expr)
        if value[0][0] == 'NOT' and value[1][0] == 'NOT':
            if any(item == value[0][1] for item in items) and any(item == value[1][1] for item in items):
                return True
        elif value[0][0] == '+' and value[1][0] == 'NOT':
            if any(item != value[0][1] for item in items) and any(item == value[1][1] for item in items):
                return True
        elif value[0][0] == 'NOT' and value[1][0] == '+':
            if any(item == value[0][1] for item in items) and any(item != value[1][1] for item in items):
                return True
        elif value[0][0] == '+' and value[1][0] == '+':
            if any(item != value[0][1] for item in items) and any(item != value[1][1] for item in items):
                return True
    return False


def returnOnes(choice_table, index):
    counter = 0
    try:
        values = choice_table.item(choice_table.get_children()[index], "values")
        counter = 0
        for value in values:
            if value == '1':
                counter += 1
    except:
        counter = counter
    return counter


def create_table(parsed_data, table_frame):
    num_columns = len(parsed_data) + 1
    table = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    table.heading('column1', text='Obj')
    table.column('column1', width=10, minwidth=0)
    for i, category in enumerate(parsed_data.keys()):
        column_name = f'column{i + 2}'
        table.heading(column_name, text=category)
        table.column(column_name, width=10, minwidth=0)

    # add rows to the table
    row_idx = 0
    for items in itertools.product(*parsed_data.values()):
        obj_name = f'O. {row_idx}'
        row_idx += 1
        if constr(items, case.constraints):
            continue
        table.insert('', 'end', values=(obj_name,) + items)

    return table


def preference_calc(item, pref):
    if pref[1] == "AND":
        if pref[0] in item and pref[2] in item:
            return True
        else:
            return False
    elif pref[1] == "OR":
        if pref[0] in item or pref[2] in item:
            return True
        else:
            return False
    elif pref[1] == "AND NOT":
        if pref[0] in item and pref[2] not in item:
            return True
        else:
            return False
    elif pref[1] == "OR NOT":
        if pref[0] in item or pref[2] not in item:
            return True
        else:
            return False
    else:
        return False


def create_pen_table(parsed_data, table_frame, table):
    num_pens = len(parsed_data)
    num_columns = num_pens + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=50, minwidth=50)

    for i in range(1, num_pens + 1):
        column_name = f'pref{i}'
        column = f'column{i + 1}'
        newTable.heading(column, text=column_name)
        newTable.column(column, width=50, minwidth=50)

    newTable.heading(f'column{num_columns}', text='Total')
    newTable.column(f'column{num_columns}', width=50, minwidth=50)

    # add rows to the table
    for item in table.get_children():
        obj = table.item(item, "values")[0]
        pen_values = []
        for pref in parsed_data:
            if preference_calc(table.item(item, "values"), pref):
                pref_val = pref[3]
            else:
                pref_val = 0
            pen_values.append(pref_val)
        total = sum(pen_values)
        newTable.insert("", "end", values=[obj] + pen_values + [total])

    return newTable


def create_poss_table(parsed_data, table_frame, table):
    num_pens = len(parsed_data)
    num_columns = num_pens + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=50, minwidth=50)

    for i in range(1, num_pens + 1):
        column_name = f'pref{i}'
        column = f'column{i + 1}'
        newTable.heading(column, text=column_name)
        newTable.column(column, width=50, minwidth=50)

    newTable.heading(f'column{num_columns}', text='Tolerance')
    newTable.column(f'column{num_columns}', width=50, minwidth=50)

    # add rows to the table
    for item in table.get_children():
        obj = table.item(item, "values")[0]
        pen_values = []
        for pref in parsed_data:
            if preference_calc(table.item(item, "values"), pref):
                pref_val = round(1.0 - pref[3], ndigits=1)
            else:
                pref_val = 1
            pen_values.append(pref_val)
        total = min(pen_values)  # change total
        newTable.insert("", "end", values=[obj] + pen_values + [total])

    return newTable


def create_choice_table(parsed_data, table_frame, table):
    num_pens = len(parsed_data)
    num_columns = num_pens + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=50, minwidth=50)

    for i in range(1, num_pens + 1):
        column_name = f'pref{i}'
        column = f'column{i + 1}'
        newTable.heading(column, text=column_name)
        newTable.column(column, width=50, minwidth=50)

    for item in table.get_children():
        obj = table.item(item, "values")[0]
        qual_values = []
        for pref in parsed_data:
            if 'IF' not in pref:
                if pref[0] in table.item(item, "values"):
                    qual_values.append(1)
                else:
                    qual_values.append(2)
            else:
                if pref[pref.index('IF') + 1] not in table.item(item, "values"):
                    qual_values.append('INF')
                else:
                    if pref[0] in table.item(item, "values"):
                        qual_values.append(1)
                    elif pref[2] in table.item(item, "values"):
                        qual_values.append(2)
                    else:
                        qual_values.append('INF')

        newTable.insert("", "end", values=[obj] + qual_values)

    return newTable


def opt_pen_table(parsed_data, table_frame, table, pen_table):
    num_columns = len(parsed_data) + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=10, minwidth=0)
    for i, category in enumerate(parsed_data.keys()):
        column_name = f'column{i + 2}'
        newTable.heading(column_name, text=category)
        newTable.column(column_name, width=10, minwidth=0)

    newTable.heading(f'column{num_columns}', text='Total')
    newTable.column(f'column{num_columns}', width=20, minwidth=0)

    # find item with lowest penalty value
    try:
        min_value = float('inf')
        min_item = None
        for item in pen_table.get_children():
            values = pen_table.item(item, "values")
            penalty = float(values[-1])  # convert to float
            if penalty <= min_value:
                min_value = penalty
                min_item = item
        if min_item:
            obj = pen_table.item(min_item, "values")[0]
            for item in table.get_children():
                if obj in table.item(item, "values"):
                    row_values = list(table.item(item, "values"))
                    row_values.append(int(min_value))
                    newTable.insert("", "end", values=tuple(row_values))
        else:
            obj = ''
    except Exception as e:
        print(f"Error: {e}")

    return newTable


def opt_poss_table(parsed_data, table_frame, table, poss_table):
    num_columns = len(parsed_data) + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=10, minwidth=0)
    for i, category in enumerate(parsed_data.keys()):
        column_name = f'column{i + 2}'
        newTable.heading(column_name, text=category)
        newTable.column(column_name, width=10, minwidth=0)

    newTable.heading(f'column{num_columns}', text='Total')
    newTable.column(f'column{num_columns}', width=20, minwidth=0)

    # find item with highest float value
    try:
        min_value = float('-inf')
        min_item = None
        for item in poss_table.get_children():
            values = poss_table.item(item, "values")
            penalty = float(values[-1])
            if penalty >= min_value:
                min_value = penalty
                min_item = item
        if min_item:
            obj = poss_table.item(min_item, "values")[0]
            for item in table.get_children():
                if obj in table.item(item, "values"):
                    row_values = list(table.item(item, "values"))
                    row_values.append(min_value)
                    newTable.insert("", "end", values=tuple(row_values))
        else:
            obj = ''
    except Exception as e:
        print(f"Error: {e}")

    return newTable


def opt_choice_table(parsed_data, table_frame, table, choice_table):
    num_columns = len(parsed_data) + 2
    newTable = Treeview(table_frame, columns=[f'column{i}' for i in range(1, num_columns + 1)], show='headings')

    # add columns to the table
    newTable.heading('column1', text='Obj')
    newTable.column('column1', width=10, minwidth=0)
    for i, category in enumerate(parsed_data.keys()):
        column_name = f'column{i + 2}'
        newTable.heading(column_name, text=category)
        newTable.column(column_name, width=10, minwidth=0)

    newTable.heading(f'column{num_columns}', text='Total 1s')
    newTable.column(f'column{num_columns}', width=20, minwidth=0)

    # find item with highest float value
    try:
        min_value = float('-inf')
        min_item = []
        for item in choice_table.get_children():
            values = choice_table.item(item, "values")
            counter = 0
            for idx, value in enumerate(values):
                if value == '1':
                    counter += 1
            if counter >= min_value:
                min_value = counter
                min_item.append(values[0])

        for item in table.get_children():
            values = table.item(item, "values")
            if values[0] in min_item:
                row_values = list(table.item(item, "values"))
                row_values.append(min_value)
                newTable.insert("", "end", values=tuple(row_values))

    except Exception as e:
        print(f"Error: {e}")

    return newTable


def exeplemp(table_frame, parsed_data, pen_table, poss_table, choice_table):
    textbox = Text(table_frame, bg="white")
    num_rows = len(pen_table.get_children())
    random_int = random.randint(0, num_rows - 1)
    random_int2 = random.randint(0, num_rows - 1)
    while random_int == random_int2:
        random_int2 = random.randint(0, num_rows - 1)

    #penalty
    row_values = [pen_table.item(pen_table.get_children()[random_int], "values")[0], pen_table.item(pen_table.get_children()[random_int], "values")[-1]]
    row_values2 = [pen_table.item(pen_table.get_children()[random_int2], "values")[0],pen_table.item(pen_table.get_children()[random_int2], "values")[-1]]
    number = '{:.0f}'.format(float(row_values[0].split()[1]))
    number2 = '{:.0f}'.format(float(row_values2[0].split()[1]))
    if(row_values[1] < row_values2[1]):
        textbox.insert("end", f"Obj {number} is preferred to Obj {number2} because it has the penalty value: {row_values[1]} while Obj {number2} has the penalty value: {row_values2[1]}.")
    elif row_values2[1] == row_values[1]:
        textbox.insert("end", f"Obj {number} is equal in preference to Obj {number2} because they both have the penalty value: {row_values[1]}.")
    else:
        textbox.insert("end", f"Obj {number2} is preferred to Obj {number} because it has the penalty value: {row_values2[1]} while Obj {number} has the penalty value: {row_values[1]}.")
    textbox.insert("end", "\n\n")

    #poss table
    row_values = [poss_table.item(poss_table.get_children()[random_int], "values")[0], poss_table.item(poss_table.get_children()[random_int], "values")[-1]]
    row_values2 = [poss_table.item(poss_table.get_children()[random_int2], "values")[0],poss_table.item(poss_table.get_children()[random_int2], "values")[-1]]
    number = '{:.0f}'.format(float(row_values[0].split()[1]))
    number2 = '{:.0f}'.format(float(row_values2[0].split()[1]))
    if(row_values[1] > row_values2[1]):
        textbox.insert("end", f"Obj {number} is preferred to Obj {number2} because it has the tolerance value: {row_values[1]} while Obj {number2} has the tolerance value: {row_values2[1]}.")
    elif row_values2[1] == row_values[1]:
        textbox.insert("end", f"Obj {number} is equal in preference to Obj {number2} because they both have the tolerance value: {row_values[1]}.")
    else:
        textbox.insert("end", f"Obj {number2} is preferred to Obj {number} because it has the tolerance value: {row_values2[1]} while Obj {number} has the tolerance value: {row_values[1]}.")
    textbox.insert("end", "\n\n")

    # choice table
    row_values = [choice_table.item(choice_table.get_children()[random_int], "values")[0], returnOnes(choice_table, random_int)]
    row_values2 = [choice_table.item(choice_table.get_children()[random_int2], "values")[0], returnOnes(choice_table, random_int2)]
    number = '{:.0f}'.format(float(row_values[0].split()[1]))
    number2 = '{:.0f}'.format(float(row_values2[0].split()[1]))

    if (row_values[1] > row_values2[1]):
        textbox.insert("end",f"Obj {number} is preferred to Obj {number2} because it has the qualitative choice value: {row_values[1]} while Obj {number2} has the value: {row_values2[1]}.")
    elif row_values2[1] == row_values[1]:
        textbox.insert("end",f"Obj {number} is equal in preference to Obj {number2} because they both have the qualitative choice value: {row_values[1]}.")
    else:
        textbox.insert("end",f"Obj {number2} is preferred to Obj {number} because it has the qualitative choice value: {row_values2[1]} while Obj {number} has the value: {row_values[1]}.")
    textbox.insert("end", "\n\n")


    return textbox


class OutputPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        OutputPage.update(self)
        buttonCommit = Button(self, width=10, text="Calculate",command=lambda: OutputPage.update(self))
        buttonCommit.place(x=10, y=10)

    def update(self):
        try:

            # Possible Cases
            text_label1 = Label(self, text="Possible Objects:", width=20, font=("TkDefaultFont", 14))
            text_label1.place(x=12, y=40)

            # create a frame to hold the table
            table_frame = Frame(self)

            parsed_data = parse_text(case.attributes)
            table = create_table(parsed_data, table_frame)
            # position the table inside the frame
            table_frame.place(x=10, y=65, width=500, height=200)
            table.place(relwidth=1, relheight=1)

            #penalty table
            text_label2 = Label(self, text="Penalty Logic Table:", width=20, font=("TkDefaultFont", 14))
            text_label2.place(x=522, y=40)
            table_frame2 = Frame(self)
            parsed_pen = parse_penalty(case.penalty)
            table2 = create_pen_table(parsed_pen, table_frame2, table)
            table_frame2.place(x=520, y=65, width=500, height=200)
            table2.place(relwidth=1, relheight=1)

            #Possibilistic Table
            text_label3 = Label(self, text="Possibilitic Logic Table:", width=20, font=("TkDefaultFont", 14))
            text_label3.place(x=1032, y=40)
            table_frame3 = Frame(self)
            parsed_poss = parse_poss(case.possibility)
            table3 = create_poss_table(parsed_poss, table_frame3, table) #parsed penalty needs to be replace
            table_frame3.place(x=1030, y=65, width=500, height=200)
            table3.place(relwidth=1, relheight=1)

            # Optimal Objects (Penalty)
            text_label4 = Label(self, text="Penalty Optimal Object(s):", width=20, font=("TkDefaultFont", 12))
            text_label4.place(x=522, y=270)
            table_frame4 = Frame(self)
            table4 = opt_pen_table(parsed_data, table_frame4, table, table2)
            table_frame4.place(x=520, y=295, width=500, height=150)
            table4.place(relwidth=1, relheight=1)

            # Optimal Objects (Poss)
            text_label5 = Label(self, text="Possibilitic Optimal Object(s):", width=30, font=("TkDefaultFont", 12))
            text_label5.place(x=1032, y=270)
            table_frame5 = Frame(self)
            table5 = opt_poss_table(parsed_data, table_frame5, table, table3)
            table_frame5.place(x=1030, y=295, width=500, height=150)
            table5.place(relwidth=1, relheight=1)

            # Qualilative logic
            text_label6 = Label(self, text="Qualitative Logic:", width=20, font=("TkDefaultFont", 12))
            text_label6.place(x=12, y=270)
            table_frame6 = Frame(self)
            parsed_choice = parse_choice(case.quality)
            table6 = create_choice_table(parsed_choice, table_frame6, table)
            table_frame6.place(x=10, y=295, width=500, height=150)
            table6.place(relwidth=1, relheight=1)

            #Qualilative Optiminal
            text_label7 = Label(self, text="Qualitative Optimal:", width=20, font=("TkDefaultFont", 12))
            text_label7.place(x=12, y=460)
            table_frame7 = Frame(self)
            table7 = opt_choice_table(parsed_data, table_frame7, table, table6)
            table_frame7.place(x=10, y=485, width=500, height=200)
            table7.place(relwidth=1, relheight=1)

            #Exemplification
            text_label8 = Label(self, text="Exemplification:", width=20, font=("TkDefaultFont", 12))
            text_label8.place(x=522, y=460)
            table_frame8 = Frame(self)
            table8 = exeplemp(table_frame8, parsed_data, table2, table3, table6)
            table_frame8.place(x=520, y=485, width=500, height=200)
            table8.place(relwidth=1, relheight=1)

        except Exception as e:

            print(f"Error: {e}")
            #Possible Table
            text_label1 = Label(self, text="Possible Objects:", width=20, font=("TkDefaultFont", 14))
            text_label1.place(x=12, y=40)
            table_frame = Frame(self)
            table = Treeview(table_frame, columns="column1", show='headings')
            table_frame.place(x=10, y=65, width=500, height=200)
            table.place(relwidth=1, relheight=1)

            #Penalty Table
            text_label2 = Label(self, text="Penalty Logic Table:", width=20, font=("TkDefaultFont", 14))
            text_label2.place(x=522, y=40)
            table_frame2 = Frame(self)
            table2 = Treeview(table_frame2, columns="column1", show='headings')
            table_frame2.place(x=520, y=65, width=500, height=200)
            table2.place(relwidth=1, relheight=1)

            #Possibilistic Table
            text_label3 = Label(self, text="Possibilitic Logic Table:", width=20, font=("TkDefaultFont", 14))
            text_label3.place(x=1032, y=40)
            table_frame3 = Frame(self)
            table3 = Treeview(table_frame3, columns="column1", show='headings')
            table_frame3.place(x=1030, y=65, width=500, height=200)
            table3.place(relwidth=1, relheight=1)

            #Optimal Objects (Penatly)
            text_label4 = Label(self, text="Penalty Optimal Object(s):", width=20, font=("TkDefaultFont", 12))
            text_label4.place(x=522, y=270)
            table_frame4 = Frame(self)
            table4 = Treeview(table_frame4, columns="column1", show='headings')
            table_frame4.place(x=520, y=295, width=500, height=150)
            table4.place(relwidth=1, relheight=1)

            # Optimal Objects (Poss)
            text_label5 = Label(self, text="Possibilitic Optimal Object(s):", width=30, font=("TkDefaultFont", 12))
            text_label5.place(x=1032, y=270)
            table_frame5 = Frame(self)
            table5 = Treeview(table_frame5, columns="column1", show='headings')
            table_frame5.place(x=1030, y=295, width=500, height=150)
            table5.place(relwidth=1, relheight=1)

            #Qualilative logic
            text_label6 = Label(self, text="Qualitative Logic:", width=20, font=("TkDefaultFont", 12))
            text_label6.place(x=12, y=270)
            table_frame6 = Frame(self)
            table6 = Treeview(table_frame6, columns="column1", show='headings')
            table_frame6.place(x=10, y=295, width=500, height=150)
            table6.place(relwidth=1, relheight=1)

            #Qualilative Optiminal
            text_label7 = Label(self, text="Qualitative Optimal:", width=20, font=("TkDefaultFont", 12))
            text_label7.place(x=12, y=460)
            table_frame7 = Frame(self)
            table7 = Treeview(table_frame7, columns="column1", show='headings')
            table_frame7.place(x=10, y=485, width=500, height=200)
            table7.place(relwidth=1, relheight=1)

            #Exemplification
            text_label8 = Label(self, text="Exemplification:", width=20, font=("TkDefaultFont", 12))
            text_label8.place(x=522, y=460)
            table_frame8 = Frame(self)
            table8 = Text(table_frame8, bg="white")
            table_frame8.place(x=520, y=485, width=500, height=200)
            table8.place(relwidth=1, relheight=1)







root = Tk()

# Set the window title and size
root.title("Project 3")
root.geometry("400x300")

# Change the background color
root.configure(bg="white")

notebook_style = Style()

notebook = Notebook(root)

input_page = InputPage(notebook)
notebook.add(input_page, text="Input")

output_page = OutputPage(notebook)
notebook.add(output_page, text="Output")

notebook.pack(expand=True, fill=BOTH)


# Run the main event loop to display the window
root.mainloop()
