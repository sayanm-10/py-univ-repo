class Repository:
    ''' class Repository to hold the students, instructors and grades.  
        This class is just a container to store all of the data structures together in a single place. '''

    
    def __init__(self, univ):
        ''' constructor to initialize repository object '''

        self.univ = univ
        self.students = dict() # key:id, value: student obj
        self.instructors = dict() # key:id, value: instructor obj
