from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from be_factor import *


TOTAL_ROUND = 50

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:elxlfoq123!@127.0.0.1/bepf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)


class participant(db.Model):
    email = db.Column('email', db.String(50), primary_key=True)
    major = db.Column(db.String(20))
    apply_company = db.Column(db.Integer)
    balance = db.Column(db.Integer)
    treat_single = db.Column(db.Float)
    treat_total = db.Column(db.Float)

    def __init__(self, email, major, apply_company, balance, treat_single, treat_total):
        self.email = email
        self.major = major
        self.apply_company = apply_company
        self.balance = balance
        self.treat_single = treat_single
        self.treat_total = treat_total


class exp_log(db.Model):
    email = db.Column('email', db.String(50), primary_key=True)
    ts = db.Column(db.BigInteger, primary_key=True)
    round = db.Column(db.SmallInteger)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    ix = db.Column(db.Float)
    iy = db.Column(db.Float)

    def __init__(self, email, ts, round, x, y, ix, iy):
        self.email = email
        self.ts = ts
        self.round = round
        self.x = x
        self.y = y
        self.ix = ix
        self.iy = iy


class reward_rec(db.Model):
    email = db.Column('email', db.String(50), primary_key=True)
    round = db.Column(db.Integer)
    secure = db.Column(db.String(1))
    reward = db.Column(db.Float)

    def __init__(self, email, round, secure, reward):
        self.email = email
        self.round = round
        self.secure = secure
        self.reward = reward


db.create_all()


def get_last_round(email):
    sql = """
    select round  from exp_log
    where email='{}' order by round desc limit 1""".format(email)

    result = db.engine.execute(sql)
    last_round = [r[0] for r in result]
    if len(last_round) == 0:
        last_round = [0]
    return last_round[0]


def processing_click_logs(click_logs):
    print('Processing click logs')
    print(click_logs)
    for l in click_logs:
        log = exp_log(**l)
        db.session.add(log)
        print(l)
    db.session.commit()


def make_result(email):
    sql = 'select email, round, ts, x, y from (select email, round, ts, x, y, rank() over (partition by email, round order by ts desc) rnk from exp_log where x > 0) x where x.rnk = 1 and email="{}"'.format(email)
    import pandas as pd
    df = pd.read_sql(sql, db.engine.connect())

    import random
    selected_round = min(TOTAL_ROUND, max(round(random.uniform(0, TOTAL_ROUND)), 0))
    secure_idx = round(random.uniform(0, 1))
    selected_secure = ['x', 'y'][secure_idx]

    final_reward = df.loc[int(selected_round)-1][selected_secure]

    return selected_round, selected_secure, final_reward


def process_reward(email, round, secure, reward):
    print('Processing reward')
    reward_rec(email, round, secure, reward)
    db.session.add(reward_rec)

    db.session.commit()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index')
def start():
    return render_template('index.html')


@app.route('/initexp', methods=['POST'])
def init_exp():
    # email = request.form['email']
    input_data = dict(request.form)
    email = input_data['email']
    exists = participant.query.filter_by(email=email).first()
    if not exists:
        p = participant(**input_data)
        db.session.add(p)
        db.session.commit()
    r = get_last_round(email)
    r = int(r)
    return redirect(url_for('exp1', email=email, cur_round=r))


@app.route('/exp1/<email>/<cur_round>')
def exp1(email, cur_round):
    cur_round = int(cur_round)
    if cur_round < TOTAL_ROUND:
        return render_template('experiment1.html', round=str(cur_round+1), email=email)
    else:
        selected_round, secure, reward = make_result(email)
        process_reward(email, selected_round, secure, reward)
        return render_template('end_exp.html',
                               email=email,
                               round=selected_round,
                               secure=secure,
                               reward=reward
                               )


@app.route('/submit_exp1', methods=['POST'])
def submit_exp1():
    import json
    result = request.form['clicklogs']
    cur_round = int(request.form['round'])
    email = request.form['email']
    ix = request.form['ix']
    iy = request.form['iy']
    print(email)
    print(ix, iy)

    click_logs = json.loads(result)

    processing_click_logs(click_logs)

    return redirect('exp1/{}/{}'.format(email, cur_round))


@app.route('/end')
def end_exp():
    return render_template('end_exp.html',
                           email='None',
                           round='None',
                           secure='None',
                           reward='None'
                           )


if __name__ == '__main__':
    import os
    #os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=5001)
