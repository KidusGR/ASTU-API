#!/usr/bin/python3
import sqlite3
import os
import json


conn = sqlite3.connect("test.db")
cursor = conn.cursor()

studentFile = "./data/ugr_22551_13/info"

leftoutStud = ["region", "program", "admission", "zone", "academicYearSemester"]


validColsStud = [
    "firstName",
    "fatherName",
    "grandFatherName",
    "amharicFirstName",
    "amharicFatherName",
    "amharicGrandFatherName",
    "gender",
    "region",
    "maritalStatus",
    "nationality",
    "disability",
    "dateOfBirth",
    "placeOfBirth",
    "photoUrl",
    "userName",
    "classYear",
    "program",
    "email",
    "dormitoryView",
    "section",
    "admission",
    "country",
    "homeTelephone",
    "mobile",
    "zone",
    "woreda",
    "kebele",
    "admissionYear",
    "cafeStatus",
    "academicYearSemester"
    ]

validColsGrade = [
    "status",
    "currentSemesterTotalCreditHour",
    "currentSemesterTotalGradePoint",
    "semesterGpa",
    "cumulativeGpa",
    "semesterName"
]

validColsEvent = [
    "title",
    "startDate",
    "endDate",
    "semesterName",
    "admissionName"
]

validColsAssess = [
    "instructorName",
    "sumOfMaximumMark",
    "sumOfResults",
    "courseTitle",
    "studentGrade",
    "creditHour",
    "ects",
    "semesterName",
    "classYear",
    "courseCode"
]

validColsRes = [
    "assessmentName",
    "maximumMark",
    "assessmentType",
    "result"
]

def iterate_nested_dict_and_lists(nested_dict, keys_to_print=None, result_dict=None):
    if keys_to_print is None:
        keys_to_print = []
    if result_dict is None:
        result_dict = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            iterate_nested_dict_and_lists(value, keys_to_print, result_dict)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    iterate_nested_dict_and_lists(item, keys_to_print, result_dict)
                else:
                    if key in keys_to_print:
                        result_dict[key] = item
        else:
            if key in keys_to_print:
                result_dict[key] = value



#DICTS AND LISTS MERGER FUNCTIONS #####################################################

def merge_dicts_and_lists(data_list):
    result_dict = {}
    for data in data_list:
        if isinstance(data, dict):
            result_dict = merge_dict_and_list(result_dict, data)
        elif isinstance(data, list):
            result_dict = merge_list(result_dict, data)
    return result_dict

def merge_dict_and_list(dict1, dict2):
    result_dict = dict1.copy()
    for key, value in dict2.items():
        if key in result_dict:
            if isinstance(result_dict[key], dict) and isinstance(value, dict):
                result_dict[key] = merge_dict_and_list(result_dict[key], value)
            elif isinstance(result_dict[key], list) and isinstance(value, list):
                result_dict[key].extend(value)
            else:
                result_dict[key] = value
        else:
            result_dict[key] = value
    return result_dict

def merge_list(dict1, list1):
    result_dict = dict1.copy()
    for index, value in enumerate(list1):
        if isinstance(value, dict):
            result_dict = merge_dict_and_list(result_dict, value)
        elif isinstance(value, list):
            result_dict = merge_list(result_dict, value)
        else:
            result_dict[index] = value
    return result_dict

#######################################################################################


try:
    cursor.execute('''CREATE TABLE Student(
    StudentID INTEGER PRIMARY KEY,
    firstName TEXT,
    fatherName TEXT,
    grandFatherName TEXT,
    amharicFirstName TEXT NULL,
    amharicFatherName TEXT NULL,
    amharicGrandFatherName TEXT NULL,
    gender TEXT,
    region TEXT,
    maritalStatus TEXT,
    nationality TEXT,
    disability TEXT NULL,
    dateOfBirth DATE,
    placeOfBirth TEXT,
    photoUrl TEXT,
    userName TEXT,
    classYear TEXT NULL,
    program TEXT NULL,
    email TEXT,
    dormitoryView TEXT NULL,
    section TEXT NULL,
    admission TEXT,
    country TEXT,
    homeTelephone INTEGER NULL,
    mobile INTEGER NULL,
    zone TEXT,
    woreda TEXT,
    kebele INTEGER,
    admissionYear TEXT,
    cafeStatus TEXT,
    academicYearSemester TEXT NULL
    )''')

    cursor.execute('''CREATE TABLE GradeReport(
    ReportID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    status TEXT NULL,
    currentSemesterTotalCreditHour REAL NULL,
    currentSemesterTotalGradePoint REAL NULL,
    semesterGpa REAL NULL,
    cumulativeGpa REAL NULL,
    semesterName TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
    )''')

    cursor.execute('''CREATE TABLE Event(
    EventID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    title TEXT,
    startDate DATE,
    endDate DATE,
    semesterName TEXT,
    admissionName TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
    )''')

    cursor.execute('''CREATE TABLE Assessment(
    CourseID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    instructorName TEXT,
    sumOfMaximumMark REAL,
    sumOfResults REAL,
    courseTitle TEXT,
    studentGrade TEXT NULL,
    creditHour INTEGER,
    ects INTEGER NULL,
    semesterName TEXT,
    classYear TEXT,
    courseCode TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
    )''')

    cursor.execute('''CREATE TABLE Result(
    ResultID INTEGER PRIMARY KEY,
    CourseID INTEGER NULL,
    StudentID INTEGER NULL,
    assessmentName TEXT NULL,
    maximumMark REAL NULL,
    assessmentType TEXT NULL,
    result REAL NULL,
    FOREIGN KEY (CourseID) REFERENCES Assessment(CourseID)
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
    )''')

except:
    pass

dicts = []
for file in os.listdir(studentFile):
    if file.split(".")[-1] == "json":
        with open(f"{studentFile}/{file}", "r") as f:
            data = json.loads(f.read())
            dicts.append(data)



resultDict = merge_dicts_and_lists(dicts)
studDict = {}
iterate_nested_dict_and_lists(resultDict, validColsStud, studDict)

region = f"{json.loads(open(f'{studentFile}/getPerson.json', 'r').read())['data']['getPerson']['region']['name']}"
program = f"{json.loads(open(f'{studentFile}/headerProfile.json', 'r').read())['data']['headerProfile']['program']['name']}"
admission = f"{json.loads(open(f'{studentFile}/headerProfile.json', 'r').read())['data']['headerProfile']['applicant']['admission']['name']}"
zone = f"{json.loads(open(f'{studentFile}/getContactAddress.json', 'r').read())['data']['getContactAddress']['zone']['name']}"
try:
    academicYearSemester = f"{json.loads(open(f'{studentFile}/studentActiveSemester.json', 'r').read())['data']['studentActiveSemester']['semesterName']}"
except:
    academicYearSemester = None
StudentID = f"{json.loads(open(f'{studentFile}/user.json', 'r').read())['data']['user']['id']}"

studDict.update({
    "region": region,
    "program": program,
    "admission": admission,
    "zone": zone,
    "academicYearSemester": academicYearSemester,
    "StudentID": StudentID
})

query = "INSERT INTO Student ({}) VALUES ({})".format(
    ', '.join(studDict.keys()), ', '.join(['?' for _ in studDict]))
cursor.execute(query, tuple(studDict.values()))

# for col in list(studDict.keys()):
#     print(f"{col} : {studDict[col]}")

gradeList = []
for report in json.loads(open(f"{studentFile}/gradeReport.json", "r").read()):
    ReportID = report['data']['gradeReport']['id']
    if report['data']['gradeReport']['gpa'] is None:
        status = None
        totalCreditHour = None
        totalGradePoint = None
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
        'StudentID': StudentID,
        'semesterName': semesterName
    }
    gradeList.append(gradeDict)

for rep in gradeList:
    query = "INSERT INTO GradeReport ({}) VALUES ({})".format(
    ', '.join(rep.keys()), ', '.join(['?' for _ in rep]))
    cursor.execute(query, tuple(rep.values()))

eventList = []
for event in json.loads(open(f"{studentFile}/latestEvents.json", "r").read())['data']['latestEvents']:
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
        'StudentID': StudentID
    }
    eventList.append(eventDict)

try:
    for eve in eventList:
        query = "INSERT INTO Event ({}) VALUES ({})".format(
        ', '.join(eve.keys()), ', '.join(['?' for _ in eve]))
        cursor.execute(query, tuple(eve.values()))
except:
    pass


assessmentList = []
for assess in json.loads(open(f"{studentFile}/assessmentResultForEnrollment.json", "r").read()):
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
    for info in json.loads(open(f"{studentFile}/studentTranscript.json", "r").read())['data']['studentTranscript']:
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
        'StudentID': StudentID
    }

    query = "INSERT INTO Assessment ({}) VALUES ({})".format(
    ', '.join(assessDict.keys()), ', '.join(['?' for _ in assessDict]))
    cursor.execute(query, tuple(assessDict.values()))

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
                'StudentID' : StudentID,
                'CourseID' : CourseID
            }
            query = "INSERT INTO Result ({}) VALUES ({})".format(
            ', '.join(resDict.keys()), ', '.join(['?' for _ in resDict]))
            cursor.execute(query, tuple(resDict.values()))
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
            'StudentID' : StudentID,
            'CourseID' : CourseID
        }
        query = "INSERT INTO Result ({}) VALUES ({})".format(
        ', '.join(resDict.keys()), ', '.join(['?' for _ in resDict]))
        cursor.execute(query, tuple(resDict.values()))
        


conn.commit()


res = cursor.execute("SELECT name FROM sqlite_master").fetchall()
print(res)
for r in res:
    print(r[0])
    cols = cursor.execute(f"SELECT * FROM {r[0]}")
    print(cols.fetchall())



