from prettytable import PrettyTable

class Repository:
    ''' class Repository to hold the students, instructors and grades.  
        This class is just a container to store all of the data structures together in a single place. '''

    student_fields = ['CWID', 'Name', 'Completed Courses']
    instructor_fields = ['CWID', 'Name', 'Dept', 'Course', 'Students']
    
    def __init__(self, univ):
        ''' constructor to initialize repository object '''

        self.univ = univ
        self.students = dict() # key:id, value: student obj
        self.instructors = dict() # key:id, value: instructor obj

    def add_student(self, student):
        ''' add a student object to the repo dict of students '''

        self.students[student.id] = student

    def add_instructor(self, instructor):
        ''' add an instructor to the repo dict of instructors '''

        self.instructors[instructor.id] = instructor

    def print_student_summary(self):
        ''' use Pretty Table to print a summary of the students '''

        print('\n\nStudent Summary')
        
        pt = PrettyTable(field_names=Repository.student_fields)

        for student in self.students.values():
            pt.add_row([student.id, student.name, [course for course in sorted(student.courses.keys())]])

        print(pt)

    def print_instructor_summary(self):
        ''' use Pretty Table to print a summary of instructors '''

        print('\n\n Instructor Summary')

        pt = PrettyTable(field_names=Repository.instructor_fields)
        
        for instructor in self.instructors.values():
            for course, student_count in instructor.courses.items():
                pt.add_row([instructor.id, instructor.name, instructor.dept, course, student_count])

        print(pt)
