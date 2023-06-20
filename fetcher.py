#!/usr/bin/python3

import json
import os
import sqlite3

conn = sqlite3.connect('test.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def FetchStudent(studentID):
    pass


def FetchGrade(StudentID):
    rows = ['status',
        'currentSemesterTotalCreditHour',
        'currentSemesterTotalGradePoint',
        'semesterGpa',
        'cumulativeGpa',
        'ReportID',
        'StudentID',
        'semesterName'
    ]

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

for rep in FetchGrade(23182):
    print(rep)



