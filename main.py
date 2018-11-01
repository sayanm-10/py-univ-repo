#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Sayan Mukherjee"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import unittest
from prettytable import PrettyTable
from repository import Repository
from student import Student
from instructor import Instructor

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

def create_repo(repo_name, directory):
    ''' given univ repo name and the directory for all text files 
        creates a repository of students, instructors and associated grades'''

    repo = Repository(repo_name)
    students_path = os.path.join(directory, "students.txt")
    instructors_path = os.path.join(directory, "instructors.txt")
    grades_path = os.path.join(directory, "grades.txt")

    try:
        for student in file_reader(students_path, 3, '\t'):
            new_student = Student(student[0], student[1], student[2])
            repo.students[new_student.id] = new_student
    except FileNotFoundError:
        print('File not found on', students_path)
    except PermissionError:
        print("Permission denied to open file on destination", students_path)
    except ValueError:
        print("Missing field in students.txt")
    else:
        
        try:
            for instructor in file_reader(instructors_path, 3, '\t'):
                new_instructor = Instructor(instructor[0], instructor[1], instructor[2])
                repo.instructors[new_instructor.id] = new_instructor
        except FileNotFoundError:
            print('File not found on', instructors_path)
        except PermissionError:
            print("Permission denied to open file on destination", instructors_path)
        except ValueError:
            print("Missing field in instructors.txt")
        else:

            try:    
                for grade in file_reader(grades_path, 4, '\t'):
                    student_id = grade[0]
                    course = grade[1]
                    letter_grade = grade[2]
                    inst_id = grade[3]
                    
                    repo.students[student_id].courses[course] = letter_grade
                    repo.instructors[inst_id].courses[course] += 1
            except FileNotFoundError:
                print('File not found on', grades_path)
            except PermissionError:
                print("Permission denied to open file on destination", grades_path)
            except ValueError:
                print("Missing field in grades.txt")
            else:
                return repo

def print_student_summary(students):
    ''' use Pretty Table to print a summary of the students '''

    print('\n\nStudent Summary')
    
    pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
    for student in students.values():
        pt.add_row([student.id, student.name, [course for course in sorted(student.courses.keys())]])

    print(pt)

def print_instructor_summary(instructors):
    ''' use Pretty Table to print a summary of instructors '''

    print('\n\n Instructor Summary')

    pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
    for instructor in instructors.values():
        for course, student_count in instructor.courses.items():
            pt.add_row([instructor.id, instructor.name, instructor.dept, course, student_count])

    print(pt)

def main():
    ''' Entry point of the app '''
    
    repo_name = input("\nEnter university name for repo: ")
    directory = input("\nEnter full directory path for repo: ")
    
    repo = create_repo(repo_name, directory)
    if repo:
        print_student_summary(repo.students)
        print_instructor_summary(repo.instructors)

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

if __name__ == "__main__":
    ''' This is executed when run from the command line '''

    main()
    
    print('\n\n**************** Unit Tests *********************')
    unittest.main(exit=False, verbosity=2)
