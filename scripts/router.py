"""
    Repository application page router
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/instructor_courses')
def instructor_courses():
    ''' display a summary of each Instructor with her/his 
        CWID, Name, Department, Course, and the number of students in the course '''

    return "yeah baby!"
    
app.run(debug=True)