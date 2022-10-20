from flask import Flask, render_template, request, url_for
import db

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
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


if __name__ == '__main__':
    app.run(debug=True)
