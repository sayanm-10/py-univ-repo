from collections import defaultdict

class Instructor:
    ''' class Instructor to hold all of the details of an instructor, 
        including a defaultdict(int) to store the names of the courses taught along with the number of students '''

    
    def __init__(self, id, name, dept):
        ''' constructor to initialize an instructor object '''

        self.id = id
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int) # key course, value number of students

    def increment_student_count(self, course):
        ''' increment the student count for the course by 1 '''

        self.courses[course] += 1

