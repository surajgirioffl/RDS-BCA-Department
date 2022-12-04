from flask import Flask, render_template, request, url_for
import results_db as db
import previous_year_questions_db as pyqDb
import userIPDb as ipDB

app = Flask(__name__)


funCall = 0


@app.route("/", methods=["GET", "POST"])
def home():
    global funCall
    funCall += 1

    if funCall == 1:
        return render_template('index.html', initialStage=True)
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == "POST":
        clientDataDict = request.form
        print(clientDataDict)
        if clientDataDict.get('session') == None or clientDataDict.get('semester') == None or clientDataDict.get('idValue') == None or clientDataDict.get('idName') not in ['registrationNo', 'examRoll', 'classRoll']:
            # if user has changed the name using dev tools.
            return render_template('result.html', result=None, isSubmitClicked=True, errorMessage="Invalid Request")

        result = db.Result(clientDataDict.get('session'), clientDataDict.get(
            'semester'))  # creating instance of Result class

        parameterDict = {clientDataDict.get(
            'idName'): clientDataDict.get('idValue')}
        databaseResponse = result.getResult(**parameterDict)
        return render_template('result.html', result=databaseResponse, isSubmitClicked=True)
    return render_template('result.html')


@app.route("/credits")
def credits():
    return render_template('credits.html')


@app.route("/gallery")
def gallery():
    return render_template('404.html')


@app.route("/previousYearQuestions", methods=["GET", "POST"])
def previousYearQuestions():
    if request.method == "POST":
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
    return render_template('register.html')


@app.route("/notice")
def notice():
    return render_template('notice.html')


# api routes
@app.route('/ip', methods=['POST'])
def ip():
    if request.method == 'POST':
        print(request.json)
        ipDictionary = {
            'ip': request.json.get('ip'),
            'city': request.json.get('city'),
            'pin': request.json.get('pin'),
            'state': request.json.get('state'),
            'country': request.json.get('country'),
            'isp': request.json.get('isp'),
            'timeZone': request.json.get('timeZone')
        }
        ipObject = ipDB.IP(host='rdsbca.mysql.pythonanywhere-services.com', user='rdsbca',
                           database='RdsBca', password='Badam@123')  # port=3307
        if ipObject.connectionStatus:
            ipObject.insertInfo(**ipDictionary)
            return 'success'
    return "failed"


if __name__ == '__main__':
    app.run(debug=True)
