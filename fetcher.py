#!/usr/bin/python3

import json
import os
import sqlite3

conn = sqlite3.connect('test.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
colData = json.loads(open("cols.json", "r").read())

def FetchStudent(StudentID, cursor=cursor):
    rows = []
    for row in colData['cols']['Student']:
        rows.append(row)
    
    query = """
    SELECT g.*
    FROM Student g
    JOIN Student s ON g.StudentID = s.StudentID
    WHERE s.StudentID = ?
    """
    cursor.execute(query, (StudentID,))
    results = cursor.fetchall()
    StudentInfo = []

    for row in results:
        Student = {}
        for r in rows:
            Student[r] = row[r]
        StudentInfo.append(Student)
    
    return StudentInfo



def FetchGrade(StudentID, cursor=cursor):
    rows = []
    for row in colData['cols']['GradeReport']:
        if not "F-KEY" in row:
            rows.append(row)

    query = """
    SELECT g.*
    FROM GradeReport g
    JOIN Student s ON g.StudentID = s.StudentID
    WHERE s.StudentID = ?
    """

    cursor.execute(query, (StudentID,))
    results = cursor.fetchall()
    gradeReports = []
    reportNum = 1
    
    for row in results:
        reports = {}
        for r in rows:
            reports[r] = row[r]
        gradeReports.append(reports)

    return gradeReports


# def FetchEvent(StudentID, cursor=cursor):


for rep in FetchGrade(23182):
    print(rep)

for stud in FetchStudent(23182):
    print(stud)



