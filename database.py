#!/usr/bin/python3
import sqlite3
import os
import json


class Database:
    def __init__(self):
        self.dbName = "data.db"
        self.conn = sqlite3.connect(self.dbName)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.colData = json.loads(open("cols.json", "r").read())
        self.StudentID = ""
        self.studDict = {}
        self.studentFile = ""
        self.StudentInfo = []
        self.gradeReports = []
        self.Events = []
        self.Assessments = []
        self.Results = []
        self.CourseIDs = []
    
    def iterate_nested_dict_and_lists(self, nested_dict, keys_to_print=None, result_dict=None):
        result_dict = self.studDict
        if keys_to_print is None:
            keys_to_print = []
        if result_dict is None:
            result_dict = {}
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                self.iterate_nested_dict_and_lists(value, keys_to_print, result_dict)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.iterate_nested_dict_and_lists(item, keys_to_print, result_dict)
                    else:
                        if key in keys_to_print:
                            result_dict[key] = item
            else:
                if key in keys_to_print:
                    result_dict[key] = value

    def merge_dicts_and_lists(self, data_list):
        result_dict = {}
        for data in data_list:
            if isinstance(data, dict):
                result_dict = self.merge_dict_and_list(result_dict, data)
            elif isinstance(data, list):
                result_dict = self.merge_list(result_dict, data)
        return result_dict
    
    def merge_dict_and_list(self, dict1, dict2):
        result_dict = dict1.copy()
        for key, value in dict2.items():
            if key in result_dict:
                if isinstance(result_dict[key], dict) and isinstance(value, dict):
                    result_dict[key] = self.merge_dict_and_list(result_dict[key], value)
                elif isinstance(result_dict[key], list) and isinstance(value, list):
                    result_dict[key].extend(value)
                else:
                    result_dict[key] = value
            else:
                result_dict[key] = value
        return result_dict
    
    def merge_list(self, dict1, list1):
        result_dict = dict1.copy()
        for index, value in enumerate(list1):
            if isinstance(value, dict):
                result_dict = self.merge_dict_and_list(result_dict, value)
            elif isinstance(value, list):
                result_dict = self.merge_list(result_dict, value)
            else:
                result_dict[index] = value
        return result_dict

    def CreateTable(self):
        try:
            for i in list(self.colData['cols'].keys()):
                cols = []
                for j in list(self.colData['cols'][i].keys()):
                    if "F-KEY" in j:
                        cols.append(f"{self.colData['cols'][i][j]}")
                    else:
                        cols.append(f"{j} {self.colData['cols'][i][j]}")
                create = f"CREATE TABLE {i}({', '.join([f'{col}' for col in cols])})"
                self.cursor.execute(create)
                self.conn.commit()

        except:
            pass

    def addStudent(self):
        #Adding Values to Student Table###################################################
        
        region = f"{json.loads(open(f'{self.studentFile}/getPerson.json', 'r').read())['data']['getPerson']['region']['name']}"
        program = f"{json.loads(open(f'{self.studentFile}/headerProfile.json', 'r').read())['data']['headerProfile']['program']['name']}"
        admission = f"{json.loads(open(f'{self.studentFile}/headerProfile.json', 'r').read())['data']['headerProfile']['applicant']['admission']['name']}"
        zone = f"{json.loads(open(f'{self.studentFile}/getContactAddress.json', 'r').read())['data']['getContactAddress']['zone']['name']}"
        try:
            academicYearSemester = f"{json.loads(open(f'{self.studentFile}/studentActiveSemester.json', 'r').read())['data']['studentActiveSemester']['semesterName']}"
        except:
            academicYearSemester = None
        self.StudentID = f"{json.loads(open(f'{self.studentFile}/user.json', 'r').read())['data']['user']['id']}"

        self.studDict.update({
            "region": region,
            "program": program,
            "admission": admission,
            "zone": zone,
            "academicYearSemester": academicYearSemester,
            "StudentID": self.StudentID
        })

        query = "INSERT INTO Student ({}) VALUES ({})".format(
            ', '.join(self.studDict.keys()), ', '.join(['?' for _ in self.studDict]))
        self.cursor.execute(query, tuple(self.studDict.values()))

    

    def addGrade(self):
        #Adding Values to GradeReport Table#######################################################
        gradeList = []

        for report in json.loads(open(f"{self.studentFile}/gradeReport.json", "r").read()):
            ReportID = report['data']['gradeReport']['id']
            if report['data']['gradeReport']['gpa'] is None:
                status = None
                currentSemesterTotalCreditHour = None
                currentSemesterTotalGradePoint = None
                semesterGpa = None
                cumulativeGpa = None
            else:
                status = report['data']['gradeReport']['gpa']['status']
                currentSemesterTotalCreditHour = report['data']['gradeReport']['gpa']['currentSemesterTotalCreditHour']
                currentSemesterTotalGradePoint = report['data']['gradeReport']['gpa']['currentSemesterTotalGradePoint']
                semesterGpa = report['data']['gradeReport']['gpa']['semesterGpa']
                cumulativeGpa = report['data']['gradeReport']['gpa']['cumulativeGpa']
                semesterName = report['data']['gradeReport']['academicYearSemester']['semesterName']
            gradeDict = {
                'status': status,
                'currentSemesterTotalCreditHour': currentSemesterTotalCreditHour,
                'currentSemesterTotalGradePoint': currentSemesterTotalGradePoint,
                'semesterGpa': semesterGpa,
                'cumulativeGpa': cumulativeGpa,
                'ReportID': ReportID,
                'StudentID': self.StudentID,
                'semesterName': semesterName
            }
            gradeList.append(gradeDict)

        for rep in gradeList:
            query = "INSERT INTO GradeReport ({}) VALUES ({})".format(
            ', '.join(rep.keys()), ', '.join(['?' for _ in rep]))
            self.cursor.execute(query, tuple(rep.values()))

    def addEvent(self):
        #Adding Values to Event Table#############################################################
        eventList = []

        for event in json.loads(open(f"{self.studentFile}/latestEvents.json", "r").read())['data']['latestEvents']:
            EventID = event['id']
            title = event['event']['title']
            startDate = event['startDate']
            endDate = event['endDate']
            semesterName = event['academicYearSemester']['semesterName']
            admissionName = event['admissions'][0]['name']
            eventDict = {
                'title': title,
                'startDate': startDate,
                'endDate': endDate,
                'semesterName': semesterName,
                'admissionName': admissionName,
                'EventID': EventID,
                'StudentID': self.StudentID
            }
            eventList.append(eventDict)

        try:
            for eve in eventList:
                query = "INSERT INTO Event ({}) VALUES ({})".format(
                ', '.join(eve.keys()), ', '.join(['?' for _ in eve]))
                self.cursor.execute(query, tuple(eve.values()))
        except:
            pass


    def addAssRes(self):
        #Adding Value to Assessment and Result Table##############################################

        for assess in json.loads(open(f"{self.studentFile}/assessmentResultForEnrollment.json", "r").read()):
            CourseID = assess['data']['assessmentResultForEnrollment']['id']
            instructorName = assess['data']['assessmentResultForEnrollment']['instructorName']
            sumOfMaximumMark = assess['data']['assessmentResultForEnrollment']['sumOfMaximumMark']
            sumOfResults = assess['data']['assessmentResultForEnrollment']['sumOfResults']
            courseTitle = assess['data']['assessmentResultForEnrollment']['course']['courseTitle']
            courseCode = assess['data']['assessmentResultForEnrollment']['course']['courseCode']
            try:
                studentGrade = assess['data']['assessmentResultForEnrollment']['studentGrade']['letterGrade']
            except:
                studentGrade = assess['data']['assessmentResultForEnrollment']['studentGrade']
            for info in json.loads(open(f"{self.studentFile}/studentTranscript.json", "r").read())['data']['studentTranscript']:
                for course in info['courseEnrollments']:
                    if course['id'] == CourseID:
                        creditHour = course['course']['creditHour']
                        ects = course['course']['ects']
                        semesterName = info['academicYearSemester']['semesterName']
                        classYear = info['classYear']['name']
            assessDict = {
                'CourseID' : CourseID,
                'instructorName' : instructorName,
                'sumOfMaximumMark' : sumOfMaximumMark,
                'sumOfResults' : sumOfResults,
                'courseTitle' : courseTitle,
                'courseCode' : courseCode,
                'studentGrade' : studentGrade,
                'creditHour' : creditHour,
                'ects' : ects,
                'semesterName' : semesterName,
                'classYear' : classYear,
                'StudentID': self.StudentID
            }

            query = "INSERT INTO Assessment ({}) VALUES ({})".format(
            ', '.join(assessDict.keys()), ', '.join(['?' for _ in assessDict]))
            self.cursor.execute(query, tuple(assessDict.values()))

            try:
                for result in assess['data']['assessmentResultForEnrollment']['assessmentResults']:
                    ResultID = result['id']
                    assessmentName = result['assessment']['assessmentName']
                    maximumMark = result['assessment']['maximumMark']
                    assessmentType = result['assessment']['assessmentType']
                    result = result['result']
                    resDict = {
                        'ResultID' : ResultID,
                        'assessmentName' : assessmentName,
                        'maximumMark' : maximumMark,
                        'assessmentType' : assessmentType,
                        'result' : result,
                        'StudentID' : self.StudentID,
                        'CourseID' : CourseID
                    }
                    query = "INSERT INTO Result ({}) VALUES ({})".format(
                    ', '.join(resDict.keys()), ', '.join(['?' for _ in resDict]))
                    self.cursor.execute(query, tuple(resDict.values()))
            except:
                ResultID = None
                assessmentName = None
                maximumMark = None
                assessmentType = None
                result = None
                resDict = {
                    'ResultID' : ResultID,
                    'assessmentName' : assessmentName,
                    'maximumMark' : maximumMark,
                    'assessmentType' : assessmentType,
                    'result' : result,
                    'StudentID' : self.StudentID,
                    'CourseID' : CourseID
                }
                query = "INSERT INTO Result ({}) VALUES ({})".format(
                ', '.join(resDict.keys()), ', '.join(['?' for _ in resDict]))
                self.cursor.execute(query, tuple(resDict.values()))

    def FetchStudent(self):
        rows = []
        for row in self.colData['cols']['Student']:
            rows.append(row)
        
        query = """
        SELECT g.*
        FROM Student g
        JOIN Student s ON g.StudentID = s.StudentID
        WHERE s.StudentID = ?
        """
        self.cursor.execute(query, (self.StudentID,))
        results = self.cursor.fetchall()

        for row in results:
            Student = {}
            for r in rows:
                Student[r] = row[r]
            self.StudentInfo.append(Student)
        

    def FetchGrade(self):
        rows = []
        for row in self.colData['cols']['GradeReport']:
            if not "F-KEY" in row:
                rows.append(row)

        query = """
        SELECT g.*
        FROM GradeReport g
        JOIN Student s ON g.StudentID = s.StudentID
        WHERE s.StudentID = ?
        """

        self.cursor.execute(query, (self.StudentID,))
        results = self.cursor.fetchall()
        
        for row in results:
            reports = {}
            for r in rows:
                reports[r] = row[r]
            self.gradeReports.append(reports)


    def FetchEvent(self):
        rows = []
        for row in self.colData['cols']['Event']:
            if not "F-KEY" in row:
                rows.append(row)

        query = """
        SELECT g.*
        FROM Event g
        JOIN Student s ON g.StudentID = s.StudentID
        WHERE s.StudentID = ?
        """

        self.cursor.execute(query, (self.StudentID,))
        results = self.cursor.fetchall()
        
        for row in results:
            Event = {}
            for r in rows:
                Event[r] = row[r]
            self.Events.append(Event)

    
    def FetchAssessment(self):
        rows = []
        for row in self.colData['cols']['Assessment']:
            if not "F-KEY" in row:
                rows.append(row)

        query = """
        SELECT g.*
        FROM Assessment g
        JOIN Student s ON g.StudentID = s.StudentID
        WHERE s.StudentID = ?
        """

        self.cursor.execute(query, (self.StudentID,))
        results = self.cursor.fetchall()
        
        for row in results:
            Assessment = {}
            for r in rows:
                Assessment[r] = row[r]
            self.Assessments.append(Assessment)


    def FetchResult(self, CourseID):
        rows = []
        for row in self.colData['cols']['Result']:
            if not "F-KEY" in row:
                rows.append(row)

        query = """
        SELECT r.*
        FROM Result r
        JOIN Student s ON r.StudentID = s.StudentID
        JOIN Assessment a ON r.CourseID = a.CourseID
        WHERE s.StudentID = ? AND a.CourseID = ?
        """

        self.cursor.execute(query, (self.StudentID, CourseID))
        results = self.cursor.fetchall()
        
        for row in results:
            Result = {}
            for r in rows:
                Result[r] = row[r]
            self.Results.append(Result)




    def main(self, userName):
        self.studentFile = f"./data/{userName}/info"
        validColsStud = []

        for valid in self.colData['cols']['Student']:
            if valid != "StudentID":
                validColsStud.append(valid)
        dicts = []
        for file in os.listdir(self.studentFile):
            if file.split(".")[-1] == "json":
                with open(f"{self.studentFile}/{file}", "r") as f:
                    data = json.loads(f.read())
                    dicts.append(data)

        self.CreateTable()
        resultDict = self.merge_dicts_and_lists(dicts)
        self.studDict = {}
        self.iterate_nested_dict_and_lists(resultDict, validColsStud, self.studDict)

        self.addStudent()
        self.addGrade()
        self.addEvent()
        self.addAssRes()

        self.conn.commit()
        
        self.cursor.close()
        self.conn.close()
        

