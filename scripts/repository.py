from prettytable import PrettyTable

class Repository:
    ''' class Repository to hold the students, instructors and grades.  
        This class is just a container to store all of the data structures together in a single place. '''

    student_fields = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']
    instructor_fields = ['CWID', 'Name', 'Dept', 'Course', 'Students']
    major_fields = ['Dept', 'Required', 'Electives']
    pass_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
    
    def __init__(self, univ):
        ''' constructor to initialize repository object '''

        self.univ = univ
        self.students = dict() # key:id, value: student obj
        self.instructors = dict() # key:id, value: instructor obj
        self.majors = dict() # key: dept, value: dict(flag, [courses])

    def add_student(self, student):
        ''' add a student object to the repo dict of students '''

        self.students[student.id] = student

    def add_instructor(self, instructor):
        ''' add an instructor to the repo dict of instructors '''

        self.instructors[instructor.id] = instructor

    def add_major(self, major):
        ''' add a major to the repo dict of majors '''

        # if dept exists in majors dict
        if major.dept in self.majors:
            # if current flag exists as a key for the values of the dept
            if major.flag in self.majors[major.dept]:
                self.majors[major.dept][major.flag].append(major.course)
            else:
                self.majors[major.dept][major.flag] = [major.course]
        else:
            self.majors[major.dept] = dict()
            self.majors[major.dept][major.flag] = [major.course]


    def print_student_summary(self):
        ''' use Pretty Table to print a summary of the students '''

        print('\n\nStudent Summary')
        
        pt = PrettyTable(field_names=Repository.student_fields)

        for student in self.students.values():
            pt.add_row([
                student.id,
                student.name,
                student.major,
                [course for course in sorted(student.courses.keys()) if student.courses[course] in Repository.pass_grades],
                set(self.majors[student.major]['R']).difference(set([course for course in sorted(student.courses.keys()) \
                    if student.courses[course] in Repository.pass_grades])) if student.major in self.majors else None,
                None if student.major not in self.majors or set(self.majors[student.major]['E']) & set([course for course in sorted(student.courses.keys()) \
                    if student.courses[course] in Repository.pass_grades]) else self.majors[student.major]['E']
            ])

        print(pt)

    def print_instructor_summary(self):
        ''' use Pretty Table to print a summary of instructors '''

        print('\n\n Instructor Summary')

        pt = PrettyTable(field_names=Repository.instructor_fields)
        
        for instructor in self.instructors.values():
            for course, student_count in instructor.courses.items():
                pt.add_row([instructor.id, instructor.name, instructor.dept, course, student_count])

        print(pt)

    def print_major_summary(self):
        ''' use Pretty Table to print a summary of majors '''

        print('\n\n Majors Summary')

        pt = PrettyTable(field_names=Repository.major_fields)

        for dept, major in self.majors.items():
            pt.add_row([
                dept,
                [sorted(course) for flag, course in major.items() if flag.lower() == 'r'][0],
                [sorted(course) for flag, course in major.items() if flag.lower() == 'e'][0]
            ])

        print (pt)

    def get_student(self, id):
        ''' get student object by id '''

        return self.students[id]

    def get_instructor(self, id):
        ''' get instructor by id '''

        return self.instructors[id]
