#!/usr/bin/python3
import sqlite3
import os
import json

data = json.loads(open("cols.json", "r").read())
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()


for i in list(data['cols'].keys()):
    cols = []
    for j in list(data['cols'][i].keys()):
        if "F-KEY" in j:
            cols.append(f"{data['cols'][i][j]}")
        else:
            cols.append(f"{j} {data['cols'][i][j]}")
    create = f"CREATE TABLE {i}({', '.join([f'{col}' for col in cols])})"
    cursor.execute(create)
    conn.commit()

cursor.close()
conn.close()
