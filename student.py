from collections import defaultdict

class Student:
    ''' class Student to hold all of the details of a student, 
        including a defaultdict(str) to store the classes taken and 
        the grade where the course is the key and the grade is the value. '''


    def __init__(self, id, name, major):
        ''' constructor to initialize student object '''

        self.id = id
        self.name = name
        self.major = major
        self.courses = defaultdict(str) # key: course, value: letter grade
