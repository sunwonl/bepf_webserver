from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy


TOTAL_ROUND = 50

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:elxlfoq123!@127.0.0.1/bepf'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bpef.sqlite3'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)


class exp_log(db.Model):
    email = db.Column('email', db.String(50), primary_key=True)
    ts = db.Column(db.BigInteger, primary_key=True)
    round = db.Column(db.SmallInteger)
    x = db.Column(db.Float)
    y = db.Column(db.Float)

    def __init__(self, email, ts, round, x, y):
        self.email = email
        self.ts = ts
        self.round = round
        self.x = x
        self.y = y


db.create_all()


def processing_click_logs(click_logs):
    print('Processing click logs')
    print(click_logs)
    for l in click_logs:
        log = exp_log(**l)
        db.session.add(log)
        print(l)
    db.session.commit()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def start():
    return render_template('index.html')


@app.route('/initexp', methods=['POST'])
def init_exp():
    email = request.form['email']
    return render_template('experiment1.html', round=1, email=email)


@app.route('/submit_exp1', methods=['POST'])
def submit_exp1():
    import json
    result = request.form['clicklogs']
    round = int(request.form['round'])
    email = request.form['email']

    click_logs = json.loads(result)

    processing_click_logs(click_logs)

    if round < TOTAL_ROUND:
        return render_template('experiment1.html', round=str(round+1), email=email)
    else:
        return render_template('end_exp.html')


if __name__ == '__main__':
    import os
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0')
