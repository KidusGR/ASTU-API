#!/usr/bin/python3
import sqlite3
import os
import json

data = json.loads(open("cols.json", "r").read())

print(data['cols'])