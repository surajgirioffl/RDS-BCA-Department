"""
        ____  _________       ____  ____  _____    __________  __    __    __________________
       / __ )/ ____/   |     / __ \/ __ \/ ___/   / ____/ __ \/ /   / /   / ____/ ____/ ____/
      / __  / /   / /| |    / /_/ / / / /\__ \   / /   / / / / /   / /   / __/ / / __/ __/   
     / /_/ / /___/ ___ |   / _, _/ /_/ /___/ /  / /___/ /_/ / /___/ /___/ /___/ /_/ / /___   
    /_____/\____/_/  |_|  /_/ |_/_____//____/   \____/\____/_____/_____/_____/\____/_____/   
    
    @file: app.py
    @author: Suraj Kumar Giri
    @init-date: 15th Oct 2022
    @last-modified: 20th Jan 2022
    
    @description:
        * Module to run the web app and handle all the routes.
"""
__author__ = "Suraj Kumar Giri"
__email__ = 'surajgirioffl@gmail.com'
__version__ = "2.0.0"


from platform import system
import os
import logging
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from db_scripts import results_db as db
from db_scripts import previous_year_questions_db as pyqDb
from db_scripts import userIPDb as ipDB
from db_scripts import registration_db as regDb
from db_scripts import dynamic_contents as dynamicContents
from app_scripts import my_time as myTime
import setTimeZone as tz
from dotenv import load_dotenv

load_dotenv()  # loading environment variables from .env file
tz.setTimeZone()  # Set timezone to Asia/Kolkata for the web app

# database credentials
databaseCredentials = {
    "host": os.environ.get('DBHOST'),
    "user": os.environ.get('DBUSERNAME'),
    "port": int(os.environ.get('DBPORT')),
    "password": os.environ.get('DBPASSWORD')
}

app = Flask(__name__)


funCall = 0


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    logging.info('Home page is called...')
    global funCall
    funCall += 1
    print(f"Home page called {funCall} times")

    # fetching notice from database
    print('Fetching notice from the database...')
    notice = dynamicContents.DynamicContents().notice()

    if notice is not None:
        # if notice is available
        # date is on 13th index of the tuple. We will change MySQL date format to user friendly format.
        print("MySQLDateTime:", notice[13], "Type:", type(notice[13]))
        notice = list(notice)  # typecasting to list for updating a value

        # MySQL connector convert MySQL DATETIME to object of datetime.datetime class.
        # we will convert to datetime.datetime object to readable format.
        notice[13] = myTime.readableDateTime(notice[13])
        return render_template('index.html', isNoticeAvailable=True, notice=notice)
    return render_template('index.html')


@app.route('/result', methods=['GET'])
def result():
    logging.info("Result page is called...")
    return render_template('result.html')


# api route to display result
@app.route('/api/display-result', methods=['POST'])
def displayResult():
    if request.method == "POST":
        clientDataDict = request.json
        print(clientDataDict)
        if clientDataDict.get('session') == None or clientDataDict.get('semester') == None or clientDataDict.get('idValue') == None or clientDataDict.get('idName') not in ['registrationNo', 'examRoll', 'classRoll']:
            # if user has changed the name using dev tools.
            return render_template('display-result.html', result=None, isSubmitClicked=True, errorMessage="Invalid Request")

        result = db.Result(clientDataDict.get('session'), clientDataDict.get(
            'semester'))  # creating instance of Result class

        parameterDict = {clientDataDict.get(
            'idName'): clientDataDict.get('idValue')}
        databaseResponse = result.getResult(**parameterDict)
        return render_template('display-result.html', result=databaseResponse, isSubmitClicked=True)


@app.route("/credits")
def credits():
    logging.info("Credits page is called...")

    # fetching credits data from the database
    credits = dynamicContents.DynamicContents(**databaseCredentials).credits()
    if credits is not None:  # if credits data are available
        return render_template('credits.html', isCreditsAvailable=True, credits=credits)
    return render_template('credits.html', isCreditsAvailable=False)


@app.route("/gallery")
def gallery():
    logging.info("Gallery page is called...")
    return render_template('404.html', message="Gallery page is under development.")


@app.route("/previousYearQuestions", methods=["GET", "POST"])
def previousYearQuestions():
    logging.info("Previous Year Questions page is called...")
    if request.method == "POST":
        logging.info(
            'A post request is received in previousYearQuestions route...')
        userSelection = request.form
        print(userSelection)
        print("semester: ", userSelection.get('semester'))
        if(userSelection.get('semester') == None or userSelection.get('source') == None):
            # if user has changed the name using dev tools.
            return render_template('previousYearQuestions.html', isSubmitClicked=True, databaseResponse=None, errorMessage="Invalid Request")
        pyqObj = pyqDb.PreviousYearQuestions(userSelection.get('semester'))
        databaseResponse: tuple = pyqObj.getLinks(userSelection.get('source'))
        return render_template('previousYearQuestions.html', isSubmitClicked=True, databaseResponse=databaseResponse, semester=userSelection.get('semester'))
    return render_template('previousYearQuestions.html')


@ app.route("/register", methods=["GET", "POST"])
def register():
    logging.info("Register page is called...")
    return render_template('register.html')


@app.route("/notice")
def notice():
    logging.info("Notice page is called...")

    # fetching notice from database
    notice = dynamicContents.DynamicContents(**databaseCredentials).notice()

    if notice is not None:
        # if notice is available
        # date is on 13th index of the tuple. We will change MySQL date format to user friendly format.
        print("MySQLDateTime:", notice[13], "Type:", type(notice[13]))
        notice = list(notice)  # typecasting to list for updating a value

        # MySQL connector convert MySQL DATETIME to object of datetime.datetime class.
        # we will convert to datetime.datetime object to readable format.
        notice[13] = myTime.readableDateTime(notice[13])
        return render_template('notice.html', isNoticeAvailable=True, notice=notice)
    else:
        return render_template('notice.html', isNoticeAvailable=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')


@app.route("/sitemap.xml", methods=["GET"])
@app.route("/sitemap.html", methods=["GET"])
@app.route("/ror.xml", methods=["GET"])
@app.route("/urllist.txt", methods=["GET"])
@app.route("/robots.txt", methods=["GET"])
def static_from_root():
    print(app.static_folder)
    return send_from_directory(app.static_folder+'/sitemaps', request.path[1:])


# temporary files serving
@app.route("/notice.pdf", methods=["GET"])
def temp_files():
    return send_from_directory(app.static_folder+'/temp-files', request.path[1:])


@app.route("/studyMaterials", methods=["GET"])
def studyMaterials():
    return render_template('study-materials.html')


@app.route("/study-materials/sem/<int:semester>", methods=["GET"])
def semesterWiseStudyMaterials(semester):
    # if semester not in [1, 2, 3, 4, 5, 6]:
    # return render_template('404.html', message="Invalid Semester")
    return render_template('semester-wise-study-materials.html')


@app.route('/sources', methods=['GET'])
def sources():
    # fetching sources data from the database
    sources = dynamicContents.DynamicContents(**databaseCredentials).sources()
    if sources is not None:  # if credits data are available
        return render_template('sources.html', isSourcesAvailable=True, sources=sources)
    return render_template('sources.html')


@app.route('/teachers', methods=['GET'])
def teachers():
    return render_template('teachers.html')


@app.route('/studentsCorner', methods=['GET'])
def studentsCorner():
    message = "Hello, Programmers! This page is under development."
    return render_template('students-corner.html', message=message)


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/about-rds-college', methods=['GET'])
def aboutRdsCollege():
    return render_template('about-rds-college.html')


# api routes
@app.route('/ip', methods=['POST'])
def ip():
    logging.info("IP API route is called (only POST method allow)...")
    if request.method == 'POST':
        logging.info("A post request is received in ip route...")
        print("Gathered Info: ", request.json)
        ipDictionary = {
            'ip': request.json.get('ip'),
            'city': request.json.get('city'),
            'pin': request.json.get('pin'),
            'state': request.json.get('state'),
            'country': request.json.get('country'),
            'isp': request.json.get('isp'),
            'timeZone': request.json.get('timeZone'),
            'platform': request.json.get('platform'),
            'screen': request.json.get('screen'),
            'path': request.json.get('path'),
            'referrer': request.json.get('referrer'),
            # currently feature is not available (After implementing session support, we will add username here.)
            'username': ""
        }

        # let's check if any value in ipDictionary is None or not. If any value will None then we send empty string ("") to database and a null value will be inserted in database.
        # verifiedIpDictionary: dict = {key: value for key, value in ipDictionary.items() if value is not None}
        for key, value in ipDictionary.items():
            if value is None:
                ipDictionary[key] = ""

        # if system is windows then we will use local database. (for testing purpose). It's for my local machine.
        if system() == 'Windows':
            ipObject = ipDB.IP()  # Every parameter will be default. (for local machine)
        else:  # it's for the server which running on linux.
            ipObject = ipDB.IP(**databaseCredentials)
        if ipObject.connectionStatus:
            ipObject.insertInfo(**ipDictionary)
            return 'success'
    return "failed"


# api route 2 (api endpoint)
@app.route('/getDetails/<string:registrationNo>', methods=['GET'])
def getDetails(registrationNo):
    print('API GET Request for details of registration No:', registrationNo)
    response = regDb.FetchDetails().getDetails(registrationNo)
    return jsonify(response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - Line %(lineno)s of %(module)s - %(levelname)s -> %(message)s')
    logging.info(
        "\n\n=======================Web app is started=======================")
    app.run(debug=True)
