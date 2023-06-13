#!/usr/bin/python3
import sqlite3
import os
import json


conn = sqlite3.connect("test.db")
cursor = conn.cursor()

studentFile = "./data/ugr_23346_13/info"

try:
    cursor.execute('''CREATE TABLE Student(
    StudentID INTEGER PRIMARY KEY,
    firstName TEXT,
    fatherName TEXT,
    grandFatherName TEXT,
    amharicFirstName,
    amharicFatherName,
    amharicGrandFatherName,
    gender TEXT,
    region TEXT,
    maritalStatus TEXT,
    nationality TEXT,
    disability TEXT,
    dateOfBirth DATE,
    placeOfBirth TEXT,
    photoUrl TEXT,
    userName TEXT,
    classYear TEXT,
    program TEXT,
    email TEXT,
    dormitoryView TEXT,
    section TEXT,
    admission TEXT,
    country TEXT,
    homeTelephone INTEGER,
    mobile INTEGER,
    zone TEXT,
    woreda TEXT,
    kebele INTEGER,
    admissionYear TEXT,
    cafeStatus TEXT,
    academicYearSemester TEXT
    )''')

    cursor.execute('''CREATE TABLE GradeReport(
    ReportID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    status TEXT,
    totalCreditHour REAL,
    totalGradePoint REAL,
    semesterGpa REAL,
    cumulativeGpa REAL,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
    )''')
except:
    pass

res = cursor.execute("SELECT name FROM sqlite_master")
print(res.fetchall())

# for file in os.listdir(studentFile):
#     print(file)
