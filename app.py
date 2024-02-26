"""
        ____  _________       ____  ____  _____    __________  __    __    __________________
       / __ )/ ____/   |     / __ \/ __ \/ ___/   / ____/ __ \/ /   / /   / ____/ ____/ ____/
      / __  / /   / /| |    / /_/ / / / /\__ \   / /   / / / / /   / /   / __/ / / __/ __/
     / /_/ / /___/ ___ |   / _, _/ /_/ /___/ /  / /___/ /_/ / /___/ /___/ /___/ /_/ / /___
    /_____/\____/_/  |_|  /_/ |_/_____//____/   \____/\____/_____/_____/_____/\____/_____/

    @file: app.py
    @author: Suraj Kumar Giri
    @init-date: 15th Oct 2022
    @last-modified: 26th Feb 2024

    @description:
        * Module to run the web app and handle all the routes.
"""
__author__ = "Suraj Kumar Giri"
__email__ = 'surajgirioffl@gmail.com'
__version__ = "2.1.7"

from datetime import datetime
from platform import system
import os
import functools
import logging
from http import HTTPStatus
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, Response, make_response, session, redirect, flash
import requests
from db_scripts import results_db as db
from db_scripts import previous_year_questions_db as pyqDb
from db_scripts import userIPDb as ipDB
from db_scripts import registration_db as regDb
from db_scripts import dynamic_contents as dynamicContents
from db_scripts import rds_project_db as rdsDb
from db_scripts import files_db as filesDb
from app_scripts import my_time as myTime
from app_scripts import mail
from app_scripts import validation
from automation_scripts import my_random as myRandom
import setTimeZone as tz
from dotenv import load_dotenv
from utilities import tools
from admin import admin
import auth
from db_scripts2 import admin_db


load_dotenv()  # loading environment variables from .env file
tz.setTimeZone()  # Set timezone to Asia/Kolkata for the web app

# database credentials
databaseCredentials = {
    "host": os.environ.get('DBHOST'),
    "user": os.environ.get('DBUSERNAME'),
    "port": int(os.environ.get('DBPORT')),
    "password": os.environ.get('DBPASSWORD')
}

# mail credentials
mailCredentials: dict = {
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'MAIL_SERVER': os.environ.get('MAIL_SERVER'),
    'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER'),
    'MAIL_PORT': os.environ.get('MAIL_PORT')
}

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

funCall = 0


def isLoggedIn():
    if "username" in session:
        return True
    return False


def authenticate(caller):
    @functools.wraps(caller)
    def wrapper(*args, **kwargs):
        if isLoggedIn():
            return caller(*args, **kwargs)
        else:
            flash("Please Login First")
            return redirect("/login")

    return wrapper


# Context for the base template
def getContextForBaseTemplate():
    return {
        "isLoggedIn": isLoggedIn()
    }


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    logging.info('Home page is called...')
    global funCall
    funCall += 1
    print(f"Home page called {funCall} times")

    # fetching notice from database
    print('Fetching notice from the database...')
    notice = dynamicContents.DynamicContents(**databaseCredentials).notice()

    if notice is not None:
        # if notice is available
        # date is on 13th index of the tuple. We will change MySQL date format to user friendly format.
        print("MySQLDateTime:", notice[13], "Type:", type(notice[13]))
        notice = list(notice)  # typecasting to list for updating a value

        # MySQL connector convert MySQL DATETIME to object of datetime.datetime class.
        # we will convert to datetime.datetime object to readable format.
        notice[13] = myTime.readableDateTime(notice[13])
        return render_template('index.html', isNoticeAvailable=True, notice=notice, **getContextForBaseTemplate())
    return render_template('index.html', **getContextForBaseTemplate())


@app.route('/result', methods=['GET'])
def result():
    logging.info("Result page is called...")
    return render_template('result.html', **getContextForBaseTemplate())


# api route to display result
@app.route('/api/display-result', methods=['POST'])
def displayResult():
    def invalidRequest(errorMessage: str = "Invalid Request", status: int = HTTPStatus.BAD_REQUEST) -> Response:
        """
            Description:
                - Function to send response in case of invalid request or any others issue.

            Args:
                * errorMessage (str, optional):
                    - Error message to be sent along with given status code (shown on the web page).
                    - Defaults to "Invalid Request".
                * status (int, optional):
                    - Status code to be sent along with error message.
                    - Defaults to HTTPStatus.BAD_REQUEST (400).

            Returns:
                * Response:
                    - Response object with given status code and error message in response body/content.
        """
        content = render_template(
            'display-result.html', result=None, isSubmitClicked=True, errorMessage=errorMessage)
        return Response(content, status=status, mimetype='text/html')

    if request.method == "POST":
        clientDataDict = request.json
        print(clientDataDict)
        if validation.isValidSession(clientDataDict.get('session')) and validation.isValidSemester(clientDataDict.get('semester')) and validation.isValidIdName(clientDataDict.get('idName')) and validation.isValidIdValue(clientDataDict.get('idName'), clientDataDict.get('idValue')):
            # if all the data are valid
            print("All data are valid..")
            result = db.Result(clientDataDict.get('session'), clientDataDict.get(
                'semester'), **databaseCredentials)  # creating instance of Result class
            if not result.connectionStatus:
                # means database connection is not established. Invalid session passed.
                return invalidRequest()

            parameterDict = {clientDataDict.get(
                'idName'): clientDataDict.get('idValue')}
            databaseResponse = result.getResult(**parameterDict)

            if databaseResponse is None:
                # if no result found for given credentials due to any reason (either logically invalid credentials or result not yet uploaded/declared/available)
                return invalidRequest(errorMessage="No Result Found For Given Credentials", status=HTTPStatus.NOT_FOUND)
            return render_template('display-result.html', result=databaseResponse, isSubmitClicked=True, subjectsWiseMarks=result.fetchSubjectsWiseMarks(examRoll=databaseResponse.get('ExamRoll'), databaseCredentials=databaseCredentials), **getContextForBaseTemplate())
        else:
            # if user has changed the name using dev tools or changes using interception
            print("Invalid data passed...")
            return invalidRequest()


@app.route("/credits")
def credits():
    logging.info("Credits page is called...")

    # fetching credits data from the database
    credits = dynamicContents.DynamicContents(**databaseCredentials).credits()
    if credits is not None:  # if credits data are available
        return render_template('credits.html', isCreditsAvailable=True, credits=credits, **getContextForBaseTemplate())
    return render_template('credits.html', isCreditsAvailable=False, **getContextForBaseTemplate())


@app.route("/gallery")
def gallery():
    logging.info("Gallery page is called...")
    return render_template('gallery.html', oddNumbers=[odd for odd in range(1, 12) if odd % 2 != 0], **getContextForBaseTemplate())


@app.route("/previousYearQuestions", methods=["GET"])
def previousYearQuestions():
    logging.info("Previous Year Questions page is called...")
    return render_template('previousYearQuestions.html', **getContextForBaseTemplate())


# api route to fetch previous year questions
@app.route('/api/fetch-previous-year-questions', methods=['POST'])
def fetchPreviousYearQuestions():
    def invalidRequest(errorMessage: str = "Invalid Request") -> Response:
        """
            Description:
                - Function to send send invalid request along with status 400 when called.

            Args:
                * errorMessage (str, optional):
                    - Error message to be sent along with status 400 (shown on the web page).

            Returns:
                * Response:
                    - Response object with status 400 and error message in response body/content.
        """
        content = render_template('api/previous-year-questions.html', isSubmitClicked=True,
                                  databaseResponse=None, errorMessage=errorMessage)
        return Response(content, status=HTTPStatus.BAD_REQUEST, headers={'Content-Type': 'text/html'})

    if request.method == "POST":
        logging.info(
            'A post request is received in api of previous year question route...')
        userSelection = request.json
        print(userSelection)

        # credentials received
        semester = userSelection.get('semester')
        source = userSelection.get('source')
        print("semester: ", semester)

        if validation.isValidSource(source) and validation.isValidSemester(semester):
            print("All data are valid...")
            pyqObj = pyqDb.PreviousYearQuestions(**databaseCredentials)
            databaseResponse: tuple = pyqObj.getLinks(
                source=source, semester=semester)
            return render_template('api/previous-year-questions.html', isSubmitClicked=True, databaseResponse=databaseResponse, semester=semester, **getContextForBaseTemplate())
        else:
            print("Invalid data passed...")
            return invalidRequest()


@ app.route("/register", methods=["GET", "POST"])
def register():
    logging.info("Register page is called...")
    return render_template('register.html', **getContextForBaseTemplate())


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
        return render_template('notice.html', isNoticeAvailable=True, notice=notice, **getContextForBaseTemplate())
    else:
        return render_template('notice.html', isNoticeAvailable=False, **getContextForBaseTemplate())


@app.route("/login", methods=["GET", "POST"])
def login():
    if isLoggedIn():
        return "User already logged in..."

    if request.method == "POST":
        print(request.form)
        username: str | None = request.form.get('username')
        password: str | None = request.form.get("password")

        if username and password:
            admin_db_instance = admin_db.AdminDatabase()
            if admin_db_instance.check_login_credentials(username, password):
                session['username'] = username
                if admin_obj := admin_db_instance.is_admin(username):
                    session['admin'] = True
                    session['role'] = admin_obj.role
                return redirect("/dashboard")
            else:
                return render_template('login.html', errorMessage="Invalid Credentials")

    return render_template('login.html')


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard", methods=["GET", "POST"])
@authenticate
def dashboard():
    admin_db_instance = admin_db.AdminDatabase()
    data_dict = admin_db_instance.fetch_admin_details(session.get('username'))
    return render_template("dashboard.html", **data_dict, isAdmin=session.get("admin"), **getContextForBaseTemplate())


@app.route("/sitemap.xml", methods=["GET"])
@app.route("/sitemap.html", methods=["GET"])
@app.route("/ror.xml", methods=["GET"])
@app.route("/urllist.txt", methods=["GET"])
@app.route("/robots.txt", methods=["GET"])
@app.route("/ads.txt", methods=["GET"])
def static_from_root():
    print(app.static_folder)
    return send_from_directory(app.static_folder+'/sitemaps', request.path[1:])


# temporary files serving
@app.route("/notice.pdf", methods=["GET"])
def temp_files():
    return send_from_directory(app.static_folder+'/temp-files', request.path[1:])


@app.route("/studyMaterials", methods=["GET"])
def studyMaterials():
    return render_template('study-materials.html', **getContextForBaseTemplate())


@app.route("/study-materials/sem/<int:semester>", methods=["GET"])
def semesterWiseStudyMaterials(semester):
    # if semester not in [1, 2, 3, 4, 5, 6]:
    # return render_template('404.html', message="Invalid Semester")
    return render_template('semester-wise-study-materials.html', **getContextForBaseTemplate())


@app.route('/sources', methods=['GET'])
def sources():
    # fetching sources data from the database
    sources = dynamicContents.DynamicContents(**databaseCredentials).sources()
    if sources is not None:  # if credits data are available
        return render_template('sources.html', isSourcesAvailable=True, sources=sources)
    return render_template('sources.html', **getContextForBaseTemplate())


@app.route('/teachers', methods=['GET'])
def teachers():
    return render_template('teachers.html', **getContextForBaseTemplate())


@app.route('/studentsCorner', methods=['GET'])
def studentsCorner():
    message = "Hello, Programmers! This page is under development."
    return render_template('students-corner.html', message=message, **getContextForBaseTemplate())


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', **getContextForBaseTemplate())


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', **getContextForBaseTemplate())


@app.route('/about-rds-college', methods=['GET'])
def aboutRdsCollege():
    return render_template('about-rds-college.html', **getContextForBaseTemplate())


@app.route('/files/<string:fileId>', methods=['GET'])
def files(fileId):
    print(
        f"Receive a GET request in the route /files/<fileId> (Here file ID = {fileId})")
    # checking if fileId is valid
    if not validation.isValidFileId(fileId):
        # if fileId is invalid
        print("Invalid fileId is passed...")
        content: str = render_template("error.html", contentHeader="Invalid Request", contentPara="File ID is not valid.",
                                       message="File ID is not valid. Please try again with a valid file ID.")
        return Response(content, status=HTTPStatus.BAD_REQUEST, content_type='text/html')

    filesObj: filesDb.Files = filesDb.Files(**databaseCredentials)
    fileMetadata: dict | None = filesObj.fetchFileMetadata(fileId)
    if fileMetadata:
        driveDownloadLink: str = fileMetadata.get('DownloadLink')

        flag: int = 0  # a flag variable counting number of attempts to fetch the file from drive
        while True:
            try:
                print("Fetching the file from the drive using GET request.")
                response = requests.get(driveDownloadLink)
            except requests.exceptions.ConnectionError:
                print("Connection Error. Internet is not connected.")
                content: str = render_template("error.html", contentHeader="Connection Error", contentPara="Internet is not connected.",
                                               message="Server is not connected to the internet. Server side error. Please try again later.")
                return Response(content, status=HTTPStatus.INTERNAL_SERVER_ERROR, content_type='text/html')
            except Exception as e:
                print("Something went wrong while fetching file from the Google Drive.")
                print("Exception: ", e)
                content: str = render_template("error.html", contentHeader="Something Went Wrong", contentPara="Unable to fetch file.",
                                               message="An unknown error occurred while fetching file from the source. Please try again later.")
                return Response(content, status=HTTPStatus.INTERNAL_SERVER_ERROR, content_type='text/html')
            else:
                if response.status_code == 200:
                    # response is fetched successfully
                    # if content type is 'text/html' then response will not as expected. It means google drive returns any error or warning.
                    # And we can't serve it directly to the user because session id etc generated to the server IP by drive will not work for user and user will not able to interact with the message.
                    # In this case, we will try at least 5 times to fetch the file from the Google Drive to eliminate the issue. But if issue persists then we will serve a custom page to the user.
                    # And user will able to download the file using google drive.

                    content = response.content
                    print("Response is received with status code 200.")
                    print("Response content type:",
                          response.headers['Content-Type'])
                    if response.headers['Content-Type'] == 'application/pdf':
                        # Updating file stats in the database (download count, last download time etc..)
                        filesObj.updateFileStats(fileId)
                        return Response(content, status=HTTPStatus.OK, content_type=response.headers['Content-Type'], headers={'Content-Disposition': f'name={fileMetadata.get("Title")};filename={fileMetadata.get("DownloadName")}.{fileMetadata.get("Extension")}'})
                    elif response.headers['Content-Type'] == 'text/html; charset=utf-8':
                        # This is for content type text/html.
                        # And we know that, we are fetching file but drive returns 'text/html' that states "Google Drive can't scan this file for viruses. This file is executable and may harm your computer. Download Anyway".
                        # So, we will try at least 5 times to fetch the file (server side). If issues persist, then we will return the below response and user need to download the file from drive with the same name as in drive.
                        flag += 1
                        print(f"Flag: {flag}")
                        if flag < 6:
                            # trying again to fetch the file from the drive
                            print("Trying again to fetch the file from the drive...")
                            continue

                        print(
                            "Drive is continuously returning text/html in last 5 requests.")
                        print("Now, serving the file using special template...")
                        # Updating file stats in the database (download count, last download time etc..)
                        filesObj.updateFileStats(fileId)
                        return Response(render_template("/special/download-file.html", message=fileMetadata.get("Title"), fileDownloadLink=fileMetadata.get("DownloadLink"), fileDownloadName=fileMetadata.get("DownloadName"), fileExtension=fileMetadata.get("Extension")), status=HTTPStatus.OK, content_type=response.headers['Content-Type'])
                    else:
                        # Updating file stats in the database (download count, last download time etc..)
                        filesObj.updateFileStats(fileId)
                        return Response(content, status=HTTPStatus.OK, content_type=response.headers['Content-Type'], headers={'Content-Disposition': f'name={fileMetadata.get("Title")};filename={fileMetadata.get("DownloadName")}.{fileMetadata.get("Extension")}'})

                # if status code is not 200.
                # Means file is not fetched successfully then send internal error.
                print("Something went wrong while fetching file from the Google Drive.")
                content: str = render_template("error.html", contentHeader="Something Went Wrong", contentPara="Unable to fetch file.",
                                               message="An unknown error occurred while fetching file from the source. Please try again later.")
                return Response(content, status=HTTPStatus.INTERNAL_SERVER_ERROR, content_type='text/html')
    else:
        # if fileId is valid but file is not found in the database.
        print("File with fileId ", fileId, " is not found in the database.")
        content: str = render_template("error.html", contentHeader="File Not Found", contentPara="File not found in the database.",
                                       message="File with fileId " + fileId + " is not found in the database. Please try again later.")
        return Response(content, status=HTTPStatus.NOT_FOUND, content_type='text/html')


# api routes to fetch file metadata
@app.route('/api/fetch-file-metadata/<string:fileId>', methods=['GET'])
def fileMetadata(fileId: str):
    print("File ID: ", fileId,
          "is received with GET request via the API /api/fetch-file-metadata")
    # checking if fileId is valid
    if not validation.isValidFileId(fileId):
        # if fileId is invalid
        print("Invalid file Id is passed via the API '/api/fetch-file-metadata'")
        content: str = render_template("error.html", contentHeader="Invalid Request", contentPara="File ID is not valid.",
                                       message="File ID is not valid. Please try again with a valid file ID.")
        return Response(content, status=HTTPStatus.BAD_REQUEST, content_type='text/html')

    filesObj: filesDb.Files = filesDb.Files(**databaseCredentials)
    fileMetadata: dict | None = filesObj.fetchFileMetadata(fileId)
    if not fileMetadata:
        print(
            f"Specified file with file id {fileId} is not found in the databases.")
        content: str = render_template("error.html", contentHeader="File Not Found", contentPara="File not found in the database.",
                                       message="File with fileId " + fileId + " is not found in the database. Please try again later.")
        return Response(content, status=HTTPStatus.NOT_FOUND, content_type='text/html')

    # printing a message in the console with the file title
    print(
        f"File ID: {fileId} is found in the database. File title: {fileMetadata.get('Title')}")

    # if everything is OK
    # Actually, fetchFileMetadata() returns all attributes of the specified file by JOINING all the desired tables.
    # If the dictionary (here fileMetadata) which is returned by this method is served directly to the client then it may cause substantial security concerns.
    # So, we will not serve the dictionary directly to the client. Instead, we will create a new dictionary and add only those attributes which are required to be served to the client.
    attributesToBeServed: list = [
        'Title', 'SubmitterName', 'SubmitterContact',
        'SubmitterDesignation', 'SubmitterEmail', 'ApproverContact',
        'ApproverName', 'ApproverDesignation', 'ApproverEmail',
        'Size', 'DownloadCount', 'LastDownloaded', 'DateCreated',
        'DateModified', 'UploadedOn', 'RootSourceName',
        'RootSourceContactLink', 'ViewsCount'
    ]
    metaDataToBeServed: dict = {}
    for key in attributesToBeServed:
        metaDataToBeServed[key] = fileMetadata.get(key)
    return jsonify(metaDataToBeServed)


# api route to fetch file view link
@app.route('/api/fetch-file-view-link/<string:fileId>', methods=['GET'])
def fileViewLink(fileId: str):
    print("File ID: ", fileId,
          "is received with GET request via the API /api/fetch-file-view-link")
    # checking if fileId is valid
    if not validation.isValidFileId(fileId):
        # if fileId is invalid
        print("Invalid file Id is passed via the API '/api/fetch-file-view-link'")
        content: str = render_template("error.html", contentHeader="Invalid Request", contentPara="File ID is not valid.",
                                       message="File ID is not valid. Please try again with a valid file ID.")
        return Response(content, status=HTTPStatus.BAD_REQUEST, content_type='text/html')

    filesObj: filesDb.Files = filesDb.Files(**databaseCredentials)
    specifiedTupleKeyArgs: dict = {
        'tableName': 'drive', 'attributesList': ['ViewLink'],
        'keyAttribute': 'FileId', 'value': fileId
    }
    dbResponse: tuple | None = filesObj.getSpecifiedTuple(
        **specifiedTupleKeyArgs)
    if dbResponse:
        # if file is found in the database and view link is fetched successfully.
        # Updating file stats in the database (view count, last viewed time etc..)
        filesObj.updateFileStats(fileId, tableName="files_views_tracking",
                                 attributeValueToBeIncreaseBy1='ViewsCount', dateTimeAttributeToBeUpdate="LastViewed")
        return jsonify(dbResponse[0])
    return jsonify(None)  # or return jsonify({}) or return jsonify(dbResponse)


@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if request.method == 'GET':
        return render_template('contribute.html', **getContextForBaseTemplate())
    else:  # request.method == 'POST
        dataDict = dict(request.form)
        file = request.files.get('file')
        uniqueID = myRandom.Random(method='epoch').generate(False)
        dataDict['uniqueId'] = uniqueID
        contributionsDict = tools.loadJSONFile(
            'contributions/contributions.json', True)  # Create 'contributions' directory.

        dateTime = tools.getCurrentDateTime()
        if contributionsDict.get(dataDict['email']):
            contributionsDict[dataDict['email']][dateTime] = dataDict
        else:
            contributionsDict[dataDict['email']] = {dateTime: dataDict}

        # Saving data and file
        file.save(f"contributions/{uniqueID}-{file.filename}")
        dataDict['filename'] = f"{uniqueID}-{file.filename}"
        tools.saveDictAsJSON(
            contributionsDict, "contributions/contributions.json")

        # Sending mail
        mail.Mail.configureApp(app, **mailCredentials, MAIL_USE_SSL=True)
        myMail = mail.Mail(app)
        adminMails: list = tools.loadJSONFile("secrets.json")["admin-emails"]
        myMail.sendMessage("New contribution", str(
            dataDict), adminMails, html=render_template("mail-templates/contribution-email-to-admin.html", dataDict=dataDict))

        return render_template('thank-you.html', title="Thanks For Your Contribution!", midMessage="Our team will review your contribution", bottomMessage='You will be informed via email about the', green="approval", red="rejection", **getContextForBaseTemplate())


@app.route("/message")
def message():
    return render_template("message.html")


# API route to fetch different contribution forms for different purposes
@app.route("/api/fetch-contribution-form", methods=["POST"])
def fetchContributionForm():
    print("A POST request received in the API route 'api/fetch-contribution-form'")
    print(request.json)
    selectedOption: str = request.json.get('selectedOption')
    if selectedOption in ['previous-year-questions']:
        return render_template('api/contribution/contribute-previous-year-questions.html')
    return "Hii"


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


# api route 3 (mail service)
@app.route('/api/send-otp', methods=['POST', 'GET'])
def mailService():
    print(request.url)
    if request.url in ['/register']:
        if request.method == 'POST':
            dataDict = request.json()
            email = dataDict.get('email')
            if validation.isValidEmail(email):
                print(f"Email ID {email} is valid.")
                mail.Mail.configureApp(
                    app, **mailCredentials, MAIL_USE_SSL=True)
                myMail = mail.Mail(app)
                otp: int = myRandom.Random.generateOtp()
                recipients = [email]
                status: bool = myMail.sendMessage(subject=f"Verification Code {otp}", message=f"Your OTP is {otp}",
                                                  recipients=recipients, html=render_template('mail-templates/otp.html', otp=otp))
                if status:
                    return "Mail sent successfully"
                else:
                    return "Mail sending failed"
            print(f"Invalid email {email}")
            return "Invalid email ID"
    return "Invalid request"


# special api routes for the college project
@app.route('/api/students-register', methods=['GET', 'POST', 'OPTIONS'])
def registerStudents():
    if request.method == 'OPTIONS':  # Handle preflight requests
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    if request.method == 'POST':
        # validation check will be implemented later.
        dataDict = {
            'firstname': request.json.get('firstname'),
            'middlename': request.json.get('middlename'),
            'lastname': request.json.get('lastname'),
            'course': request.json.get('course'),
            'gender': request.json.get('gender'),
            'country_code': request.json.get('country_code'),
            'phone': request.json.get('phone'),
            'address': request.json.get('address'),
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        print("Data from admission form", dataDict)
        headers = {'mimetype': 'text/html', "Access-Control-Allow-Origin": "*",
                   "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization"}
        return Response("Data added in the database successfully", status=HTTPStatus.OK, headers=headers) if rdsDb.RdsProject(**databaseCredentials).saveStudentDetails(dataDict) else Response("Failed to add data in the database", status=HTTPStatus.BAD_REQUEST, headers=headers)
    else:  # GET request
        return jsonify(rdsDb.RdsProject(**databaseCredentials).fetchAllStudentDetails())


@app.route('/api/students-register/<string:id>', methods=['GET', 'DELETE'])
def registerStudents2(id):
    if request.method == 'GET':
        # return jsonify(rdsDb.RdsProject(**databaseCredentials).fetchStudentDetails(id))
        tableAttributes: list = ['ID', 'First name', 'Middle Name', 'Last Name',
                                 'Gender', 'Email', 'Course', 'Country Code', 'Phone Number', 'Address']
        return render_template('rds-project/detail.html', data=rdsDb.RdsProject(**databaseCredentials).fetchStudentDetails(id), tableAttributes=tableAttributes)
    else:  # DELETE request
        return "Data deleted successfully" if rdsDb.RdsProject(**databaseCredentials).deleteStudent(id) else "Failed to delete data"


@app.route('/api/contact-form', methods=['GET', 'POST', 'OPTIONS'])
def contactUs():
    if request.method == 'OPTIONS':  # Handle preflight requests
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    if request.method == 'POST':
        # validation check will be implemented later.
        dataDict = {
            'firstname': request.json.get('firstname'),
            'lastname': request.json.get('lastname'),
            'country': request.json.get('country'),
            'email': request.json.get('email'),
            'contents': request.json.get('content')
        }
        print("Data from contact form: ", dataDict)

        headers = {'mimetype': 'text/html', "Access-Control-Allow-Origin": "*",
                   "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization"}
        return Response("Data added in the database successfully", status=HTTPStatus.OK, headers=headers) if rdsDb.RdsProject(**databaseCredentials).saveContactFormDetails(dataDict) else Response("Failed to add data in the database", status=HTTPStatus.BAD_REQUEST, headers=headers)
    else:  # GET request
        return jsonify(rdsDb.RdsProject(**databaseCredentials).fetchAllContactFormDetails())


@ app.route('/api/contact-form/<string:sno>', methods=['GET', 'DELETE'])
def contactUs2(sno):
    if request.method == 'GET':
        # return jsonify(rdsDb.RdsProject(**databaseCredentials).fetchContactFormDetails(sno))
        tableAttributes: list = [
            'ID', 'Email', 'First Name', 'Last Name', 'Country', 'Contents']
        return render_template('rds-project/detail.html', data=rdsDb.RdsProject(**databaseCredentials).fetchContactFormDetails(sno), tableAttributes=tableAttributes)
    else:  # DELETE request
        return "Data deleted successfully" if rdsDb.RdsProject(**databaseCredentials).deleteContact(sno) else "Failed to delete data"


# Admin Panel
admin.admin_panel(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - Line %(lineno)s of %(module)s - %(levelname)s -> %(message)s')
    logging.info(
        "\n\n=======================Web app is started=======================")
    app.run(debug=True)
