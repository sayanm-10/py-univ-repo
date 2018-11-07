class Major:
    ''' class that stores all information about a major 
        including the name of the major, the required courses and electives '''

        
    def __init__(self, dept, flag, course):
        ''' constructor to create a Major object '''
            
        self.dept = dept
        self.flag = flag
        self.course = course
