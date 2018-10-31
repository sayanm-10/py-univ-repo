class Repository:
    ''' class Repository to hold the students, instructors and grades.  
        This class is just a container to store all of the data structures together in a single place. '''

    
    def __init__(self, student, instructor, grades):
        ''' constructor to initialize repository object '''

        self.student = student
        self.instructor = instructor
        self.grades = grades
