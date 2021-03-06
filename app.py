
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
resultsDict = []


def getHeaders(table):
	if table == "majors":
		return ["ID", "Name", "Average Salary", "Expected Growth", "No. of Students", "No. Offering Universities"]
	elif table == "cities":
		return ["ID", "City", "State", "Summer Temperature", "Winter Temperature"]
	elif table == "universities":
		return ["ID", "Name", "Admissions Rate", "Size", "In-State Tuition", "Out-State Tuition"]
	elif table == "careers":
		return ["ID", "Name", "Salary", "Growth", "No. Employed"]

def getQuery(myDict):
	# print("\n!!!!!!! MYDICT: " + str(myDict) + " \n")
	myDict = myDict.to_dict()
	category = myDict.pop("category")
	query = "select * from " + category + " c"
	if category == "majors":
		query = "select majorID, name, average_salary, expected_growth, no_of_students, no_of_offering_schools from majors c"
	elif category == "universities":
		query = "select universityID, name, ug_admissions_rate, size, in_state_tuition, out_state_tuition from universities c"
	elif category == "cities":
		query = "select cityID, city, state, summer_temperature, winter_temperature from cities c"
	conjunction_count = 0
	seen = False 
	instate = False
	tuition = "100000"
	state = ""
	if "state" in myDict:
		state = myDict.pop("state")
	if state != "" and state != "Any":
		conjunction_count += 1
		query += " INNER JOIN cities ci on ci.cityID = c.cityID WHERE ci.state = '" + state + "'"
	for term in myDict.items():
		key = term[0]
		value = term[1]
		#process key here (sorry its so messy)
		if value != "":
			conjunction = " AND"
			if conjunction_count == 0:
				conjunction = " WHERE"
			conjunction_count += 1
			if key == "keyword":
				query += " " + conjunction + " c.name like '%" + value + "%'"
			elif key == "admission-min":
				query += " " + conjunction +" c.ug_admissions_rate > " + value
			elif key == "admission-max":
				query += " " + conjunction +" c.ug_admissions_rate < " + value
			elif key == "size":
				query += " " + conjunction +" c.size < " + value
			elif key == "instate":
				if seen and value == "true":
					query += " " + conjunction +" c.in_state_tuition < " + tuition
				elif seen and value == "false":
					query += " " + conjunction +" c.out_state_tuition < " + tuition
				else:
					seen = True
					conjunction_count -= 1
					if instate == "true":
						instate = True
			elif key == "tuition":
				if seen:
					if instate: 
						query += " " + conjunction +" c.in_state_tuition < " + value
					else:
						query += " " + conjunction +" c.out_state_tuition < " + value
				else:
					conjunction_count -= 1
					tuition = value
					seen = True
			elif key == "major-size":
				query += " " + conjunction + " c.no_of_students < " + value
			elif key == "salary-min":
				query += " " + conjunction + " c.average_salary > " + value
			elif key == "salary-max":
				query += " " + conjunction + " c.average_salary < " + value
			elif key == "career-salary-min":
				query += " " + conjunction + " c.salary > " + value
			elif key == "career-salary-max":
				query += " " + conjunction + " c.salary < " + value
	print("\nThis is the query: " + query)
	return query



@app.route('/search', methods=['POST'])
def search():
	values = request.form
	headers = getHeaders(values['category'])
	query = getQuery(values)

	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute(query)
	result = sorted(cur.fetchall(), key=lambda row: row[1]) 
	results = {values['category']: {"results": result, "headers": headers}}
	if len(result) == 0:
		results = {}
	print("!!!! result: " + str(result))
	print("!!!! results: " + str(results))
	return render_template("result.html", **locals())

@app.route('/mini-search', methods=['POST'])
def minisearch():
	values = request.form
	con = lite.connect("info257app.db")
	cur = con.cursor()
	results = {}
	value = values['keyword']
	for table in ["universities", "careers", "majors", "cities"]:
		if table =="cities":
			cur.execute("select cityID, city, state, summer_temperature, winter_temperature from cities where city like  '%" + value + "%'")
		elif table == "universities":
			cur.execute("select universityID, name, ug_admissions_rate, size, in_state_tuition, out_state_tuition from universities where name like '%" + value + "%'")
		elif table =="majors":
			cur.execute("select majorID, name, average_salary, expected_growth, no_of_students, no_of_offering_schools from majors where name like '%" + value + "%'")
		else:
			cur.execute("select * from " + table + " c where  c.name like '%" + value + "%'")
		print(results)
		result = sorted(cur.fetchall(), key=lambda row: row[1]) 
		if result != []:
			results[table] = {"results": result, "headers": getHeaders(table)}
	print("HERE IS RESULTS!!!!!! " + str(results))
	return render_template("result.html", **locals())

@app.route('/')
def home():
	states = ["Any", "Alaska",
                  "Alabama",
                  "Arkansas",
                  "American Samoa",
                  "Arizona",
                  "California",
                  "Colorado",
                  "Connecticut",
                  "District of Columbia",
                  "Delaware",
                  "Florida",
                  "Georgia",
                  "Guam",
                  "Hawaii",
                  "Iowa",
                  "Idaho",
                  "Illinois",
                  "Indiana",
                  "Kansas",
                  "Kentucky",
                  "Louisiana",
                  "Massachusetts",
                  "Maryland",
                  "Maine",
                  "Michigan",
                  "Minnesota",
                  "Missouri",
                  "Mississippi",
                  "Montana",
                  "North Carolina",
                  " North Dakota",
                  "Nebraska",
                  "New Hampshire",
                  "New Jersey",
                  "New Mexico",
                  "Nevada",
                  "New York",
                  "Ohio",
                  "Oklahoma",
                  "Oregon",
                  "Pennsylvania",
                  "Puerto Rico",
                  "Rhode Island",
                  "South Carolina",
                  "South Dakota",
                  "Tennessee",
                  "Texas",
                  "Utah",
                  "Virginia",
                  "Virgin Islands",
                  "Vermont",
                  "Washington",
                  "Wisconsin",
                  "West Virginia",
                  "Wyoming"]
	return render_template("home.html", **locals())

@app.route("/majors")
def view_all_majors():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select majorID, name, average_salary, expected_growth, no_of_students, no_of_offering_schools from majors")
	rows = sorted(cur.fetchall(), key=lambda row: row[1]) 
	results = {"majors": {"results": rows, "headers": getHeaders("majors")}}
	return render_template("result.html", **locals())

@app.route('/majors/<int:id>')
def get_major(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "Description", "Average Salary", "Expected Growth", "Number of Students", "Number of Offering Universities"]
	limitCareers = 25
	limitUniversities = 10
	
	cur.execute("select * from majors where majorID = " + str(id))
	majors = cur.fetchall()
	
	cur.execute("select careers.name, careers.careerID from careers, majorcareers where majorID = " + str(id) + " and careers.careerID = majorcareers.careerID limit " + str(limitCareers))
	careers = cur.fetchall()
	
	cur.execute("select universities.name, universities.universityID from universities, universitymajors where majorID = " + str(id) + " and universities.universityID = universitymajors.universityID")
	universities = cur.fetchall()
	
	return render_template("major.html", **locals())

@app.route('/cities/<int:id>')
def get_city(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = getHeaders("cities")
	limitUniversities = 10
	
	cur.execute("select * from cities where cityID = " + str(id))
	cities = cur.fetchall()
	
	cur.execute("select universities.name, universities.universityID from universities where cityID = " + str(id) + " limit " + str(limitUniversities))
	universities = cur.fetchall()
	
	return render_template("city.html", **locals())

@app.route("/universities")
def view_all_universities():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select universityID, name, ug_admissions_rate, size, in_state_tuition, out_state_tuition from universities")
	rows = sorted(cur.fetchall(), key= lambda row: row[1])
	results = {"universities": {"results": rows, "headers": getHeaders("universities")}}
	return render_template("result.html", **locals())

@app.route('/universities/<int:id>')
def get_university(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "UG Admissions Rate", "Size", "In-State Tuition", "Out-State Tuition"]
	columnNames_info = ["State", "City"]
	limitMajors = 100
	
	cur.execute("select universityID, name, ug_admissions_rate, size, in_state_tuition, out_state_tuition from universities where universityID = " + str(id))
	universities = cur.fetchall()
	
	cur.execute("select state, city from universities, cities where universities.universityID = " + str(id) + " and cities.cityID = universities.cityID")
	universities_info = cur.fetchall()
	
	cur.execute("select majors.name, majors.majorID from majors, universitymajors where universitymajors.universityID = " + str(id) + " and universitymajors.majorID = majors.majorID")
	majors = cur.fetchall()
	
	return render_template("university.html", **locals())

@app.route("/careers")
def view_all_careers():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	cur.execute("select careerID, name, salary, growth, employment from careers")
	rows =  sorted(cur.fetchall(), key=lambda row: row[1]) 
	results = {"careers": {"results": rows, "headers": getHeaders("careers")}}
	return render_template("result.html", **locals())

@app.route('/careers/<int:id>')
def get_career(id):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	columnNames = ["ID", "Name", "Salary", "Growth", "Employment"]
	limitMajors = 25
	
	cur.execute("select * from careers where careerID = " + str(id))
	careers = cur.fetchall()
	
	cur.execute("select majors.name, majors.majorID from majors, majorcareers where majorcareers.careerID = " + str(id) + " and majorcareers.majorID = majors.majorID limit " + str(limitMajors))
	majors = cur.fetchall()
	
	return render_template("career.html", **locals())

@app.route('/search/<keyword>')
def get_search(keyword):
	
	con = lite.connect("info257app.db")
	cur = con.cursor()
	
	def cleanResult(results):
		cleaned = []
		for i in range(len(results)):
			cleaned += [results[i][0]]
		return cleaned
	
	cur.execute("select careerID from careers where name like '%" + keyword + "%'")
	resultsCareers = cleanResult(cur.fetchall())
	
	cur.execute("select universityID from universities where name like '%" + keyword + "%'")
	resultsUniversities = cleanResult(cur.fetchall())
	
	cur.execute("select cityID from cities where state like '%" + keyword + "%' or city like '%" + keyword + "%'")
	resultsCities = cleanResult(cur.fetchall())
	
	cur.execute("select majorID from majors where name like '%" + keyword + "%'")
	resultsMajors = cleanResult(cur.fetchall())
	
	global resultsDict
	resultsDict = {"careers":resultsCareers, "universities":resultsUniversities, "cities":resultsCities, "majors":resultsMajors}

	return "hellooooooo"
	
@app.route('/results/')
def get_result():
	
	con = lite.connect("info257app.db")
	cur = con.cursor()

	displayDict = []
	displayCareers = []
	displayUniversities = []
	displayCities = []
	displayMajors = []
	
	labelsMajors = ["ID", "Name", "Description", "Average Salary", "Expected Growth", "Number of Students", "Number of Offering Universities"]
	labelsCities = ["ID", "State", "City", "Summer Temperature", "Winter Temperature"]
	labelsUniversities = ["ID", "Name", "UG Admissions Rate", "Size", "In-State Tuition", "Out-State Tuition", "City ID"]
	labelsCareers = ["ID", "Name", "Salary", "Growth", "Employment"]

	for i in range(len(resultsDict['careers'])):
		cur.execute("select * from careers where careerID = " + str(resultsDict['careers'][i]))
		displayCareers += cur.fetchall()
	
	for i in range(len(resultsDict['universities'])):
		cur.execute("select * from universities where universityID = " + str(resultsDict['universities'][i]))
		displayUniversities += cur.fetchall()
		
	for i in range(len(resultsDict['cities'])):
		cur.execute("select * from cities where cityID = " + str(resultsDict['cities'][i]))
		displayCities += cur.fetchall()
		
	for i in range(len(resultsDict['majors'])):
		cur.execute("select * from majors where majorID = " + str(resultsDict['majors'][i]))
		displayMajors += cur.fetchall()
	
	displayDict = {"careers":displayCareers, "universities":displayUniversities, "cities":displayCities, "majors":displayMajors}
	print (displayDict)
	
	return "hallooooo"

@app.route('/entrycareer/')
def set_career():
	
	# columnData to be replaced with post data
	# function produces results of data entry (row of entity entered) or errorMsg (non empty)
	
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["Name", "Salary", "Growth", "Employment"]
	columnData = ["name", 1234, 123, 12] 
	errorMsg = ""

	cur.execute("select count(*) from careers where name='{0}'".format(columnData[0]))
	checkRepeats = cur.fetchall()[0][0]
	if (checkRepeats > 0):
		errorMsg = "Career already exists in database! Add another career!"

	if (errorMsg == ""):
		cur.execute("select max(careerID) from careers")
		getNewID = cur.fetchall()[0][0]

		cur.execute("insert into careers (careerID, name, salary, growth, employment) values ({0}, '{1}', {2}, {3}, {4})".format(getNewID+1,columnData[0],columnData[1],columnData[2],columnData[3]))
		cur.execute("select * from careers where name='{0}'".format(columnData[0]))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)

@app.route('/entrymajor/')
def set_major():
	
	# columnData to be replaced with post data
	# function produces results of data entry (row of entity entered) or errorMsg (non empty)
	
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["Name", "Description", "Average Salary", "Expected Growth", "Number of Students", "Number of Offering Universities"]
	columnData = ["name", "description", 123, 12, 12, 123]
	errorMsg = ""

	cur.execute("select count(*) from majors where name='{0}'".format(columnData[0]))
	checkRepeats = cur.fetchall()[0][0]
	if (checkRepeats > 0):
		errorMsg = "Major already exists in database! Add another major!"

	if (errorMsg == ""):
		cur.execute("select max(majorID) from majors")
		getNewID = cur.fetchall()[0][0]
		
		cur.execute("insert into majors (majorID, name, description, average_salary, expected_growth, no_of_students, no_of_offering_schools) values ({0}, '{1}', '{2}', {3}, {4}, {5}, {6})".format(getNewID+1,columnData[0],columnData[1],columnData[2],columnData[3],columnData[4],columnData[5]))
		cur.execute("select * from majors where name='{0}'".format(columnData[0]))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)
		
@app.route('/entrycity/')
def set_city():
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["State", "City", "Summer Temperature", "Winter Temperature"]
	columnData = ["state", "city", 123, 12]
	errorMsg = ""

	cur.execute("select count(*) from cities where state='{0}' and city='{1}'".format(columnData[0], columnData[1]))
	checkRepeats = cur.fetchall()[0][0]
	if (checkRepeats > 0):
		errorMsg = "State/city already exists in database! Add another state/city!"

	if (errorMsg == ""):
		cur.execute("select max(cityID) from cities")
		getNewID = cur.fetchall()[0][0]
		
		cur.execute("insert into cities (cityID, state, city, summer_temperature, winter_temperature) values ({0}, '{1}', '{2}', {3}, {4})".format(getNewID+1,columnData[0],columnData[1],columnData[2],columnData[3]))
		cur.execute("select * from cities where state='{0}' and city='{1}'".format(columnData[0], columnData[1]))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)

@app.route('/entryuniversity/')
def set_university():
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["Name", "UG Admissions Rate", "Size", "In-State Tuition", "Out-State Tuition", "State", "City"]
	columnData = ["name", "udadmitrate", 123, 12, 12, "Georgia", "Brunswick"]
	errorMsg = ""

	cur.execute("select count(*) from universities where name='{0}'".format(columnData[0]))
	checkRepeats = cur.fetchall()[0][0]
	if (checkRepeats > 0):
		errorMsg = "University already exists in database! Add another university!"

	cur.execute("select cityID from cities where state='{0}' and city='{1}'".format(columnData[5], columnData[6]))
	checkID = cur.fetchall()
	if (len(checkID) == 0):
		errorMsg = "University's city does not exist in database! Add the city first!"

	if (errorMsg == ""):
		cityID = checkID[0][0]  
		cur.execute("select max(universityID) from universities")
		getNewID = cur.fetchall()[0][0]

		cur.execute("insert into universities (universityID, name, ug_admissions_rate, size, in_state_tuition, out_state_tuition, cityID) values ({0}, '{1}', '{2}', {3}, {4}, {5}, {6})".format(getNewID+1,columnData[0],columnData[1],columnData[2],columnData[3],columnData[4],cityID))
		cur.execute("select * from universities where name='{0}'".format(columnData[0]))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)

@app.route('/entryuniversitymajor/')
def set_universitymajor():
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["University Name", "Major Name"]
	columnData = ["Massachusetts Maritime Academy", "Accounting"]
	errorMsg = ""

	cur.execute("select universityID from universities where name='{0}'".format(columnData[0]))
	checkUniID = cur.fetchall()
	cur.execute("select majorID from majors where name='{0}'".format(columnData[1]))
	checkMajID = cur.fetchall()

	if (len(checkUniID) == 0):
		errorMsg = "University does not exist in database. Add university first!"
	if (len(checkMajID) == 0):
		errorMsg = "Major does not exist in database. Add major first!"

	if (errorMsg == ""):
		universityID = checkUniID[0][0]
		majorID = checkMajID[0][0]
		cur.execute("select count(*) from universitymajors where majorID={0} and universityID={1}".format(majorID, universityID))
		checkRepeats = cur.fetchall()[0][0]
		if (checkRepeats > 0):
			errorMsg = "Linkage already exists in database! Add another linkage!"

	if (errorMsg == ""):
		cur.execute("insert into universitymajors (universityID, majorID) values ({0}, {1})".format(universityID,majorID))
		cur.execute("select * from universitymajors where universityID='{0}' and majorID='{1}'".format(universityID,majorID))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)
	
@app.route('/entrymajorcareer/')
def set_majorcareer():
	con = lite.connect("info257app.db")
	cur = con.cursor()

	columnNames = ["Career Name", "Major Name"]
	columnData = ["Business Professor", "Animal Genetics"]
	errorMsg = ""

	cur.execute("select careerID from careers where name='{0}'".format(columnData[0]))
	checkCarID = cur.fetchall()
	cur.execute("select majorID from majors where name='{0}'".format(columnData[1]))
	checkMajID = cur.fetchall()

	if (len(checkCarID) == 0):
		errorMsg = "Career does not exist in database. Add career first!"
	if (len(checkMajID) == 0):
		errorMsg = "Major does not exist in database. Add major first!"

	if (errorMsg == ""):
		careerID = checkCarID[0][0]
		majorID = checkMajID[0][0]
		cur.execute("select count(*) from majorCareers where majorID={0} and careerID={1}".format(majorID, careerID))
		checkRepeats = cur.fetchall()[0][0]
		if (checkRepeats > 0):
			errorMsg = "Linkage already exists in database! Add another linkage!"

	if (errorMsg == ""):
		cur.execute("insert into majorCareers (careerID, majorID) values ({0}, {1})".format(careerID,majorID))
		cur.execute("select * from majorCareers where careerID='{0}' and majorID='{1}'".format(careerID,majorID))
		results = cur.fetchall()
		print (results)
	else:
		print(errorMsg)
		

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

if __name__ == "__main__":
    app.run()

# cities

@app.route("/")
def view_all_cities():

	con = lite.connect("cities.db")
	cur = con.cursor()
	cur.execute("select cit, state, summer_temperature, winter_temperature")
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
		with con:
			cur = con.cursor()
			cur.execute("insert into cities (state, city, summer_temperature, winter_temperature) values ('{}', '{}')".format(state, city, summer_temperature, winter_temperature))

		return redirect("/")


#@app.route("/cities/<int:id>")

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


# universities


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

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404                                  
