import sqlite3
import pyperclip

#create/open database and set up connection
name = input('Database name: \n')
con = sqlite3.connect(f'{name}.sqlite3')
curs = con.cursor()

#recieves and formats copied table
input('Select and copy the google sheets cells that you want to turn into an SQL table. Do not paste it here; this program will pull the table directly from your clipboard.\nClick return to continue.\n')
complete_stuff = pyperclip.paste()
split_newline = complete_stuff.split('\n')
for line in split_newline:
    oline = line
    if line[0] == '\t':
        line = 'NULL' + line
    i = 1
    while i < len(line):
        if line[i-1]=='\t' and line[i]=='\t':
            line = line[:i] + 'NULL' + line[i:]
            i += 1
        i += 1
    if line[len(line)-1] == '\t':
        line = line + 'NULL'
    split_newline[split_newline.index(oline)] = line
split_tabs = [lin.split('\t') for lin in split_newline]
split_tabs.pop()

#create table and add columns
tab_name = input('Table name: \n')
curs.execute(
    f""" CREATE TABLE {tab_name} (
        blank TEXT
    ); """
)
if input('Flip Table (y/n)?\nMakes the original tables\' rows and columns into columns and rows respectively\n') == 'y':
    #flips the table
    new_split_tabs = []
    for i in range(len(split_tabs[0])):
        col_holder = []
        for row in split_tabs:
            col_holder.append(row[i])
        new_split_tabs.append(col_holder)
    split_tabs = new_split_tabs
def eliminate_special_chars(line):
    for i in range(len(line)):
        num = ord(line[i])
        if num < 65 or (num > 90 and num < 97 and num != 95) or num > 122:
            line = line[:i] + '_' + line[i+1:]
    return line
split_tabs[0] = list(map(eliminate_special_chars,split_tabs[0]))
header = split_tabs[0]
f_row = split_tabs[1]
def get_dtypes():
    #assigns column data types based on the values in the first row of the table
    prefer_real = input('Prefer REAL over INT (y/n)?\nThis will cause all columns with numbers to be assigned the data type REAL, even if they contain only integers. If you have columns that contain both floats and integers, answer y to avoid errors\n') == 'y'
    for val in f_row:
        try:
            if str(float(val))[::-1][0:2] == '0.' and not prefer_real:
                raise ValueError
            yield 'REAL'
            continue
        except ValueError:
            pass
        try:
            int(val)
            yield 'INTEGER'
            continue
        except ValueError:
            pass
        yield 'TEXT'
data_type =  'TEXT'
get_types = input('Get data types for columns (y/n)?\nNote: this uses the values in the first non-header row (second row) to decide the datatypes of each column. If there are varying data types in a given column or a NULL value in the first row, this feature will not work. Data types default to TEXT if you answer n\n') == 'y'
data_types = get_dtypes()
for col in header:
    if get_types:
        data_type = next(data_types)
    print(col,data_type)
    curs.execute(f'''ALTER TABLE {tab_name}
                    ADD COLUMN {col} {data_type};''')
curs.execute(f'''ALTER TABLE {tab_name}
                DROP COLUMN blank;''')

#add rows
q_marks = ','.join(['?' for i in range(len(header))])
curs.executemany(f'''INSERT INTO {tab_name} VALUES ({q_marks});''',split_tabs)

#display table, save it, and close the connection
print('Created table looks like this:')
print(curs.execute(f'''SELECT * FROM {tab_name}''').fetchall())
con.commit()
con.close()
