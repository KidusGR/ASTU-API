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
    
    for row in results:
        reports = {}
        for r in rows:
            reports[r] = row[r]
        gradeReports.append(reports)

    return gradeReports


def FetchEvent(StudentID, cursor=cursor):
    rows = []
    for row in colData['cols']['Event']:
        if not "F-KEY" in row:
            rows.append(row)

    query = """
    SELECT g.*
    FROM Event g
    JOIN Student s ON g.StudentID = s.StudentID
    WHERE s.StudentID = ?
    """

    cursor.execute(query, (StudentID,))
    results = cursor.fetchall()
    Events = []
    
    for row in results:
        Event = {}
        for r in rows:
            Event[r] = row[r]
        Events.append(Event)

    return Events


def FetchAssessment(StudentID, cursor=cursor):
    rows = []
    for row in colData['cols']['Assessment']:
        if not "F-KEY" in row:
            rows.append(row)

    query = """
    SELECT g.*
    FROM Assessment g
    JOIN Student s ON g.StudentID = s.StudentID
    WHERE s.StudentID = ?
    """

    cursor.execute(query, (StudentID,))
    results = cursor.fetchall()
    Assessments = []
    
    for row in results:
        Assessment = {}
        for r in rows:
            Assessment[r] = row[r]
        Assessments.append(Assessment)

    return Assessments


def FetchResult(StudentID, CourseID, cursor=cursor):
    rows = []
    for row in colData['cols']['Result']:
        if not "F-KEY" in row:
            rows.append(row)

    query = """
    SELECT r.*
    FROM Result r
    JOIN Student s ON r.StudentID = s.StudentID
    JOIN Assessment a ON r.CourseID = a.CourseID
    WHERE s.StudentID = ? AND a.CourseID = ?
    """

    cursor.execute(query, (StudentID, CourseID))
    results = cursor.fetchall()
    Results = []
    
    for row in results:
        Result = {}
        for r in rows:
            Result[r] = row[r]
        Results.append(Result)

    return Results




