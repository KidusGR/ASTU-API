#!/usr/bin/python3
import sqlite3
import os
import json


conn = sqlite3.connect("test.db")
cursor = conn.cursor()

studentFile = "./data/ugr_23346_13/info"

try:
    cursor.execute('''CREATE TABLE Student(
    firstName,
    fatherName,
    grandFatherName,
    amharicFirstName,
    amharicFatherName,
    amharicGrandFatherName,
    gender,
    region,
    maritalStatus,
    nationality,
    disability,
    dateOfBirth,
    placeOfBirth,
    photoUrl,
    userName,
    classYear,
    program,
    email,
    dormitoryView,
    section,
    admission,
    country,
    homeTelephone,
    mobile,
    zone,
    woreda,
    kebele,
    admissionYear,
    cafeStatus,
    academicYearSemester
    )''')
except:
    pass

res = cursor.execute("SELECT name FROM sqlite_master")
print(res.fetchall())

# for file in os.listdir(studentFile):
#     print(file)
