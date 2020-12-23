from flask import Flask

app = Flask(__name__)


@app.route('/')
def hi():
    return "Hello World"

@app.route('/interaction-checker/check')
def check_interaction():
    return "checking interactions between drugs"

@app.route('/side-effect-report/send-report')
def send_report():
    return "sending report"

@app.route('/drug-search/search')
def search_drug():
    return "sending report"

if __name__ == '__main__':
    app.run(debug=True)