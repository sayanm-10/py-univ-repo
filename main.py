#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Sayan Mukherjee"
__version__ = "0.1.0"
__license__ = "MIT"

import os
from prettytable import PrettyTable
from repository import Repository
from student import Student
from instructor import Instructor

def file_reader(path, field_num, sep, header=False):
    ''' a generator function to read text files and return all of the values on a single line on each call to next() '''

    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        print("\n\nError while opening {} for reading".format(os.path.basename(path)))
    else:
        with fp:
            # skip the first line if header is true
            if header: 
                next(fp)
            for line_num, line  in enumerate(fp):
                fields = line.strip().split(sep)
                if (len(fields) < field_num):
                    raise ValueError('\n\n {} has {} fields on line {} but expected {}'.format(os.path.basename(path), len(fields), line_num + 1, field_num))
                else:
                    # return fields from 0:field_num as tuple
                    yield tuple(fields[:field_num])

def create_repo():
    ''' get univ repo name and the directory for all text files '''

    repo_name = input("\nEnter university name for repo: ")
    directory = input("\nEnter directory path for repo: ")

    repo = Repository(repo_name)
    students_path = os.path.join(directory, "students.txt")
    instructors_path = os.path.join(directory, "instructors.txt")
    grades_path = os.path.join(directory, "grades.txt")

    for student in file_reader(students_path, 3, '\t'):
        new_student = Student(student[0], student[1], student[2])
        repo.students[new_student.id] = new_student

    for instructor in file_reader(instructors_path, 3, '\t'):
        new_instructor = Instructor(instructor[0], instructor[1], instructor[2])
        repo.instructors[new_instructor.id] = new_instructor

    for grade in file_reader(grades_path, 4, '\t'):
        student_id = grade[0]
        course = grade[1]
        letter_grade = grade[2]
        inst_id = grade[3]

        repo.students[student_id].courses[course] = letter_grade
        repo.instructors[inst_id].courses[course] += 1

    return repo

def print_student_summary(students):
    ''' use Pretty Table to print a summary of the students '''

    print('\n\nStudent Summary\n')
    
    pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
    for student in students.values():
        pt.add_row([student.id, student.name, [course for course in student.courses.keys()]])

    print(pt)

def main():
    ''' Entry point of the app '''
    
    repo = create_repo()
    print_student_summary(repo.students)
    # print_instructor_summary(repo.instructors)

if __name__ == "__main__":
    ''' This is executed when run from the command line '''

    main()
