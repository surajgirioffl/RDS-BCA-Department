from flask import Flask, render_template, request, url_for
import db

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
    return render_template('previousYearQuestions.html')


if __name__ == '__main__':
    app.run(debug=True)
