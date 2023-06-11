#!/usr/bin/python3
import sqlite3
import os
import json

studentFile = "./data/ugr_23346_13/info"

for file in os.listdir(studentFile):
    print(file)
