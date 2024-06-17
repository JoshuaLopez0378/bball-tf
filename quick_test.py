list_of_cols = ['test1', 'test3', 'test5']
list_of_values = ['val1', 'val2', 'val3']
update_set = ",\n".join([f"{col} = {val}" for col,val in zip(list_of_cols,list_of_values)])
table_name = 'toinks'

x = f"""
        UPDATE {table_name}
        SET {update_set}
        WHERE {list_of_cols[0]} = {list_of_values[0]}
"""

print(x)