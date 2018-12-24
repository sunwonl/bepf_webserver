from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def start():
    return render_template('index.html')


@app.route('/exp1')
def exp1():
    return render_template('experiment1.html')


@app.route('/exp2')
def exp2():
    return render_template('experiment2.html')


if __name__ == '__main__':
    app.run()
