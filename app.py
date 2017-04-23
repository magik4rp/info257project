
""" Table Name: universities
(0, 'universityID', 'INTEGER', 0, None, 0)
(1, 'name', 'TEXT', 0, None, 0)
(2, 'ug_admissions_rate', 'TEXT', 0, None, 0)
(3, 'size', 'TEXT', 0, None, 0)
(4, 'in_state_tuition', 'TEXT', 0, None, 0)
(5, 'out_state_tuition', 'TEXT', 0, None, 0)
(6, 'cityID', 'INTEGER', 0, None, 0)

Table Name: majors
(0, 'majorID', 'INTEGER', 0, None, 0)
(1, 'name', 'TEXT', 0, None, 0)
(2, 'description', 'TEXT', 0, None, 0)
(3, 'average_salary', 'TEXT', 0, None, 0)
(4, 'expected_growth', 'TEXT', 0, None, 0)
(5, 'no_of_students', 'TEXT', 0, None, 0)
(6, 'no_of_offering_schools', 'TEXT', 0, None, 0)

Table Name: cities
(0, 'cityID', 'INTEGER', 0, None, 0)
(1, 'state', 'TEXT', 0, None, 0)
(2, 'city', 'TEXT', 0, None, 0)
(3, 'summer_temperature', 'TEXT', 0, None, 0)
(4, 'winter_temperature', 'TEXT', 0, None, 0)

Table Name: careers
(0, 'careerID', 'INTEGER', 0, None, 0)
(1, 'name', 'TEXT', 0, None, 0)
(2, 'salary', 'TEXT', 0, None, 0)
(3, 'growth', 'TEXT', 0, None, 0)
(4, 'employment', 'TEXT', 0, None, 0)

Table Name: majorcareers
(0, 'majorID', 'REAL', 0, None, 0)
(1, 'careerID', 'INTEGER', 0, None, 0)

Table Name: universitymajors
(0, 'universityID', 'REAL', 0, None, 0)
(1, 'majorID', 'INTEGER', 0, None, 0)

Table Name: applications
(0, 'universityID', 'REAL', 0, None, 0)
(1, 'majorID', 'INTEGER', 0, None, 0)
(2, 'degree', 'TEXT', 0, None, 0)
(3, 'decision', 'TEXT', 0, None, 0)
(4, 'decision_method', 'TEXT', 0, None, 0)
(5, 'ug_gpa', 'REAL', 0, None, 0)
(6, 'gre_verbal', 'REAL', 0, None, 0)
(7, 'gre_quant', 'REAL', 0, None, 0)
(8, 'gre_writing', 'REAL', 0, None, 0) """


from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import sqlite3 as lite
import sys
import os
from os import path

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/majors/<int:id>')
def get_major(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "Description", "Average Salary", "Expected Growth", "Number of Students", "Number of Offering Universities"]
	limitCareers = 6
	limitUniversities = 6
	
	cur.execute("select * from majors where majorID = " + str(id))
	majors = cur.fetchall()
	
	cur.execute("select careers.name, careers.careerID from careers, majorcareers where majorID = " + str(id) + " and careers.careerID = majorcareers.careerID limit " + str(limitCareers))
	careers = cur.fetchall()
	
	cur.execute("select universities.name, universities.universityID from universities, universitymajors where majorID = " + str(id) + " and universities.universityID = universitymajors.universityID limit " + str(limitUniversities))
	universities = cur.fetchall()
	
	return render_template("major.html", **locals())

@app.route('/cities/<int:id>')
def get_city(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "State", "City", "Summer Temperature", "Winter Temperature"]
	limitUniversities = 6
	
	cur.execute("select * from cities where cityID = " + str(id))
	cities = cur.fetchall()
	
	cur.execute("select universities.name, universities.universityID from universities where cityID = " + str(id) + " limit " + str(limitUniversities))
	universities = cur.fetchall()
	
	return render_template("city.html", **locals())

@app.route('/universities/<int:id>')
def get_university(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "UG Admissions Rate", "Size", "In-State Tuition", "Out-State Tuition"]
	columnNames_info = ["State", "City"]
	limitMajors = 6
	
	cur.execute("select * from universities where universityID = " + str(id))
	universities = cur.fetchall()
	
	cur.execute("select state, city from universities, cities where universities.universityID = " + str(id) + " and cities.cityID = universities.cityID")
	universities_info = cur.fetchall()
	
	cur.execute("select majors.name, majors.majorID from majors, universitymajors where universitymajors.universityID = " + str(id) + " and universitymajors.majorID = majors.majorID limit " + str(limitMajors))
	majors = cur.fetchall()
	
	return render_template("university.html", **locals())
	
@app.route('/careers/<int:id>')
def get_career(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "Salary", "Growth", "Employment"]
	limitMajors = 6
	
	cur.execute("select * from careers where careerID = " + str(id))
	careers = cur.fetchall()
	
	cur.execute("select majors.name, majors.majorID from majors, majorcareers where majorcareers.careerID = " + str(id) + " and majorcareers.majorID = majors.majorID limit " + str(limitMajors))
	majors = cur.fetchall()
	
	return render_template("career.html", **locals())
	
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

##################################################################################
#Vetted Code Up Till This Point
##################################################################################
	
extra_dirs = ['static',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
app.run(extra_files=extra_files)

# applications

app = Flask(__name__)

import sqlite3 as lite
import sys
 
@app.route("/")
def view_all_applications():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select university, major, degree, decision, decision_method, ug_gpa, gre_verbal, gre_quant, gre_writing from applications")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addapplications", methods=["GET", "POST"])
def add_applications():

	if request.method == "GET":
		return render_template("addapplications.html", **locals())

	else:
		university = request.form["university"]
		major = request.form["major"]
		degree = request.form["degree"]
		decision = request.form["decision"]
		decision_method = request.form["decision_method"]
		ug_gpa = request.form["ug_gpa"]
		gre_verbal = request.form["gre_verbal"]
		gre_quant = request.form["gre_quant"]
		gre_writing = request.form["gre_writing"]

		con = lite.connect("info257app.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into applications (university, major, degree, decision, decision_method, ug_gpa, gre_verbal, gre_quant, gre_writing) values ('{}', '{}')".format(university, major, degree, decision, decision_method, ug_gpa, gre_verbal, gre_quant, gre_writing))

		return redirect("/")


@app.route("/applications/<int:id>")
def get_applications(id):

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select university, major, degree, decision, decision_method, ug_gpa, gre_verbal, gre_quant, gre_writing from applications where id = " + str(id))
	rows = cur.fetchall()
	column_names = ["University","Major","Degree","Decision","Decision_Method","UG_GPA","GRE_Verbal","GRE_Quant","GRE_Writing"]
	return render_template("viewapplications.html", **locals())

if __name__ == "__main__":
    app.run()

# careers
@app.route("/")
def view_all_careers():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select name, salary, growth, employment from careers")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addcareers", methods=["GET", "POST"])
def add_careers():

	if request.method == "GET":
		return render_template("addcareers.html", **locals())

	else:
		name = request.form["name"]
		salary = request.form["salary"]
		growth = request.form["growth"]
		employment = request.form["employment"]

		con = lite.connect("info257app.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into careers (name, salary, growth, employment) values ('{}', '{}')".format(name, salary, growth, employment))

		return redirect("/")


@app.route("/careers/<int:id>")
def get_careers(id):

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select name, salary, growth, employment from careers where id = " + str(id))
	rows = cur.fetchall()
	column_names = ["Name","Salary","Growth","Employment"]
	return render_template("viewcareers.html", **locals())

if __name__ == "__main__":
    app.run()

# cities

@app.route("/")
def view_all_cities():

	con = lite.connect("cities.db")
	cur = con.cursor()
	cur.execute("select state, city, summer_temperature, winter_temperature")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addcities", methods=["GET", "POST"])
def add_cities():

	if request.method == "GET":
		return render_template("cities.html", **locals())

	else:
		state = request.form["city"]
		city = request.form["state"]
		summer_temperature = request.form["summer_temperature"]
		winter_temperature = request.form["winter_temperature"]

		con = lite.connect("cities.db")
		if con:
			cur = con.cursor()
			cur.execute("insert into cities (state, city, summer_temperature, winter_temperature) values ('{}', '{}')").format(state, city, summer_temperature, winter_temperature)
		return redirect("/")


#@app.route("/cities/<int:id>")
def get_cities(id):

	con = lite.connect("cities.db")
	cur = con.cursor()
	cur.execute("select state, city, summer_temperature, winter_temperature from cities where id = " + str(id))
	rows = cur.fetchall()
	column_names = ["state", "city", "summer temperature", "winter temperature"]
	return render_template("viewcities.html", **locals())

# majorcareers

@app.route("/")
def view_all_majorcareers():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select major, career from majorcareers")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addmajorcareers", methods=["GET", "POST"])
def add_majorcareers():

	if request.method == "GET":
		return render_template("addmajorcareers.html", **locals())

	else:
		major = request.form["major"]
		career = request.form["career"]

		con = lite.connect("info257app.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into majorcareers (major, career) values ('{}', '{}')".format(major, career))

		return redirect("/")


@app.route("/majorcareers/<int:id>")
def get_majorcareers(id):

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select id major, career from majorcareers where id = " + str(id))
	rows = cur.fetchall()

	return render_template("viewmajorcareers.html", **locals())
                                    
# majors

@app.route("/")
def view_all_majors():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select name, description, average_salary, expected_growth, no_of_students, no_of_offering_schools from majors")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/addmajorcareers", methods=["GET", "POST"])
def add_majors():

	if request.method == "GET":
		return render_template("addmajors.html", **locals())

	else:
		name = request.form["name"]
		description = request.form["description"]
		average_salary = request.form["average_salary"]
		expected_growth = request.form["expected_growth"]
		no_of_students = request.form["no_of_students"]
		no_of_offering_schools = request.form["no_of_offering_schools"]

		con = lite.connect("info257app.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into Majors (name, description, average_salary, expected_growth, no_of_students, no_of_offering_schools) values ('{}', '{}')".format(name, description, average_salary, expected_growth, no_of_students, no_of_offering_schools))

		return redirect("/")


@app.route("/majors/<int:id>")
def get_majors(id):

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select id name, description, average_salary, expected_growth, no_of_students, no_of_offering_schools from majors where id = " + str(id))
	rows = cur.fetchall()

	return render_template("viewmajors.html", **locals())

# universities

@app.route("/")
def view_all_universities():
	
	con = lite.connect("universities.db")
	cur = con.cursor()
	cur.execute("select name, ug_admissions_rate, size, in_state_tuition, out_state_tuition, state, city from universities")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/adduniversities", methods=["GET", "POST"])
def add_universities():

	if request.method == "GET":
		return render_template("adduniversities.html", **locals())

	else:
		name = request.form["name"]
		ug_admissions_rate = request.form["ug_admissions_rate"]
		size = request.form["size"]
		in_state_tuition = request.form["in_state_tuition"]
		out_state_tuition = request.form["out_state_tuition"]
		city = request.form["city"]
		state = request.form["state"]

		con = lite.connect("universities.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into universities (name, ug_admissions_rate, size, in_state_tuition, out_state_tuition, state, city) values ('{}', '{}')".format(name, ug_admissions_rate, size, in_state_tuition, out_state_tuition, state, city))

		return redirect("/")


#@app.route("/universities/<int:id>")
def get_universities(id):

	con = lite.connect("universities.db")
	cur = con.cursor()
	cur.execute("select name, ug_admissions_rate, size, in_state_tuition, out_state_tuition, state, city from universities where id = " + str(id))
	rows = cur.fetchall()
	column_names = ["name", "UG admissions rate", "size", "in state tuition", "out of state tuition", "state", "city"]
	return render_template("viewuniversities.html", **locals())

# universitymajors

@app.route("/")
def view_all_universitymajors():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select university, major from universitymajors")
	rows = cur.fetchall()

	return render_template("index.html", **locals())

@app.route("/adduniversitymajors", methods=["GET", "POST"])
def add_universitymajors():

	if request.method == "GET":
		return render_template("adduniversitymajors.html", **locals())

	else:
		university = request.form["university"]
		major = request.form["major"]

		con = lite.connect("info257app.db")
		with con:
			cur = con.cursor()
			cur.execute("insert into universitymajors (university, major) values ('{}', '{}')".format(university, major))

		return redirect("/")


@app.route("/universitymajors/<int:id>")
def get_universitymajors(id):

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select id university, major from universitymajors where id = " + str(id))
	rows = cur.fetchall()

	return render_template("viewuniversitymajors.html", **locals())                                   
