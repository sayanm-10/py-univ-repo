#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Sayan Mukherjee"
__version__ = "0.2.1"
__license__ = "MIT"

import os
import unittest
from prettytable import PrettyTable
from repository import Repository
from student import Student
from instructor import Instructor
from major import Major

# modify this to run unit tests with different directory
TEST_DIR = os.path.join(os.getcwd(), 'Stevens')

def file_reader(path, field_num, sep, header=False):
    ''' a generator function to read text files and return all of the values on a single line on each call to next() '''

    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError
    except PermissionError:
        raise PermissionError
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

def add_students(repo, directory):
    ''' add students to the repo object '''

    students_path = os.path.join(directory, "students.txt")

    try:
        for student in file_reader(students_path, 3, '\t'):
            repo.add_student(Student(student[0], student[1], student[2]))
    except FileNotFoundError:
        print('File not found on', students_path)
    except PermissionError:
        print("Permission denied to open file on destination", students_path)
    except ValueError:
        print("Missing field in students.txt")
    else:
        return repo

def add_instructors(repo, directory):
    ''' add instructors to the repo object '''

    instructors_path = os.path.join(directory, "instructors.txt")

    try:
        for instructor in file_reader(instructors_path, 3, '\t'):
            repo.add_instructor(Instructor(instructor[0], instructor[1], instructor[2]))
    except FileNotFoundError:
        print('File not found on', instructors_path)
    except PermissionError:
        print("Permission denied to open file on destination", instructors_path)
    except ValueError:
        print("Missing field in instructors.txt")
    else:
        return repo

def add_grades(repo, directory):
    ''' add course/grades to the relevant student and instructor '''
    
    grades_path = os.path.join(directory, "grades.txt")

    try:    
        for grade in file_reader(grades_path, 4, '\t'):
            student_id = grade[0]
            course = grade[1]
            letter_grade = grade[2]
            inst_id = grade[3]

            # assign grade to the student for particular course            
            repo.get_student(student_id).assign_grade(course, letter_grade)
            # increment the student count for that course by 1
            repo.get_instructor(inst_id).increment_student_count(course)
    except FileNotFoundError:
        print('File not found on', grades_path)
    except PermissionError:
        print("Permission denied to open file on destination", grades_path)
    except ValueError:
        print("Missing field in grades.txt")
    else:
        return repo

def add_majors(repo, directory):
    ''' add majors to the repo '''

    majors_path = os.path.join(directory, "majors.txt")

    try:
        for major in file_reader(majors_path, 3, '\t'):
            repo.add_major(Major(major[0], major[1], major[2]))
    except FileNotFoundError:
        print('File not found on', majors_path)
    except PermissionError:
        print("Permission denied to open file on destination", majors_path)
    except ValueError:
        print("Missing field in grades.txt")
    else:
        return repo

def create_repo(repo_name, directory):
    ''' given univ repo name and the directory for all text files 
        creates a repository of students, instructors and associated grades'''

    repo = Repository(repo_name)

    repo = add_students(repo, directory)
    repo = add_instructors(repo, directory)
    repo = add_grades(repo, directory)
    repo = add_majors(repo, directory)

    return repo

def main():
    ''' Entry point of the app '''
    
    repo_name = input("\nEnter university name for repo: ")
    directory = input("\nEnter full directory path for repo: ")
    
    repo = create_repo(repo_name, directory)
    if repo:
        repo.print_student_summary()
        repo.print_instructor_summary()
        repo.print_major_summary()

class RepoTest(unittest.TestCase):
    ''' Unit test the Repo '''

    test_repo = create_repo('test_repo', TEST_DIR)
    
    def test_instructors(self):
        ''' test the instructors in the repo '''

        repo = RepoTest.test_repo
        instructor = repo.instructors['98764'] #  98764 |  Feynman, R | SFEN | SSW 564 |    3

        self.assertIsNotNone(repo)
        self.assertEqual(instructor.courses['SSW 564'], 3)
        self.assertEqual(instructor.name, 'Feynman, R')
        self.assertEqual(instructor.dept, 'SFEN')

    def test_students(self):
        ''' test the students in the repo '''

        repo = RepoTest.test_repo
        student = repo.students['10115'] #  10115 |   Wyatt, X  | ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']

        self.assertEqual(student.name, 'Wyatt, X')
        self.assertEqual(sorted(student.courses.keys()), ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'])

    def test_majors(self):
        ''' test the majors in the repo '''

        repo = RepoTest.test_repo
        major = repo.majors['SYEN'] # {'R' : ['SYS 612', 'SYS 671', 'SYS 800'], 'E' : ['SSW 540', 'SSW 565', 'SSW 810']}

        self.assertEqual(sorted(major['R']), ['SYS 612', 'SYS 671', 'SYS 800'])
        self.assertEqual(sorted(major['E']), ['SSW 540', 'SSW 565', 'SSW 810'])


if __name__ == "__main__":
    ''' This is executed when run from the command line '''

    main()
    
    print('\n\n**************** Unit Tests *********************')
    unittest.main(exit=False, verbosity=2)
