import smtplib, os, pickle  # smtplib: 메일 전송을 위한 패키지
from email import encoders  # 파일전송을 할 때 이미지나 문서 동영상 등의 파일을 문자열로 변환할 때 사용할 패키지
from email.mime.text import MIMEText   # 본문내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart   # 메시지를 보낼 때 메시지에 대한 모듈
from email.mime.base import MIMEBase     # 파일을 전송할 때 사용되는 모듈

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def make_bepf_report(email, ccei, alpha, rho):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('report.html')

    output = template.render(email=email, ccei=ccei, alpha=alpha, rho=rho)
    #print(output)
    return output


def send_bepf_report(addr, path):

    # pw = "본인의 pw"
    # pickle.dump(pw, open("pw.pickle", 'wb'))

    email = "sun2208@gmail.com"
    pw = 'password'

    smtp = smtplib.SMTP('smtp.gmail.com', 587)   # 587: 서버의 포트번호
    smtp.ehlo()
    smtp.starttls()   # tls방식으로 접속, 그 포트번호가 587
    # smtp.login('hyeshinoh@gmail.com', pickle.load( open('../pw.pickle', 'rb') ))
    smtp.login(email, pw)

    msg = MIMEMultipart()    #msg obj.
    msg['Subject'] = '{}님의 행동경제학 프로파일링 결과 입니다.'.format(addr)

    # text msg
    part = MIMEText('''행동경제학 프로파일링 연구에 참여해주셔서 감사합니다. 
첨부 파일을 다운로드 하신 후, 브라우저로 열어서 결과를 확인해주세요
(다운로드 하지 않는 경우에는 결과가 정상적으로 출력되지 않을 수 있습니다.)''')
    msg.attach(part)   #msg에 part obj.를 추가해줌

    # Attach FILE
    #path = 'tmp.html'
    # ctype = 'application/octet-stream'
    # maintype, subtype = ctype.split('/', 1)
    with open(path, 'rb') as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())  # payload: osi 7-layers
        encoders.encode_base64(part)  # base64 encoding: 영상, 이미지 파일을 문자열 형태로 변환
        part.add_header('Content-Disposition', 'attachment', filename=path)
        msg.attach(part)

    # email 전송
    msg["To"] = addr
    smtp.sendmail(email, addr, msg.as_string())
    print(addr)


if __name__ == '__main__':
    import pandas as pd

    df = pd.read_csv('data/result.csv')
    for index, row in df.iterrows():
        one_res = dict(row)
        email = one_res['email']

        print('sending result {}'.format(email))

        html = make_bepf_report(**one_res)
        with open('report/{}.html'.format(email.split('@')[0]), 'w', encoding='utf-8') as w:
            w.write(html)
        send_bepf_report(email, 'report/{}.html'.format(email.split('@')[0]))
