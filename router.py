"""
    Repository application page router
"""

import os
import sqlite3
from flask import Flask, render_template

# modify this to work with a different db file
DB_FILE = os.path.join(os.getcwd(), 'DB', 'ssw810_university.db')

app = Flask(__name__)

@app.route('/instructor_courses')
def instructor_courses():
    ''' display a summary of each Instructor with her/his 
        CWID, Name, Department, Course, and the number of students in the course '''

    query = """ select CWID, Name, Dept, Course, count(*) as Student_Count
                from Instructors I
                join Grades G
                on I.CWID = G.Instructor_CWID
                group by Dept, Course
                order by Student_Count desc """

    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    # create a list of dictionaries for easy unpacking
    data = [{'id': id, 'name': name, 'department': department, 'course': course, 'students': students}
            for id, name, department, course, students in results]

    db.close()

    return render_template('instructor.html',
                            title="University Repo",
                            inst_header=" Number of students by course and instructor",
                            instructors=data)
    
app.run(debug=True)