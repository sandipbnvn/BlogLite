from application.models.users import User as users_model, db
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime
from main import celery
from flask import current_app
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from flask import jsonify
from email import encoders
from xmlrpc.client import SERVER_ERROR

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = 'sandip@gmail.com'
SENDER_PASSWORD = ''

@celery.task
def format_report(template_file, user = {}):
    with open(template_file) as file_:
        template = Template(file_.read())
        current_date = datetime.now()
        date_string = current_date.strftime("%d-%m-%Y, %H:%M")
        followed_length = len(list(user.followed))
        followers_length = len(list(user.followers))
        posts_length = len(list(user.posts))
        return template.render(user=user, followed_length = followed_length, followers_length = followers_length, posts_length = posts_length, date_string = date_string)
    

@celery.task
def create_pdf_report(user):
    message = format_report("monthly_report.html", user=user)
    html = HTML(string=message)
    file_name = str(user.id)+"_"+ str(user.username)+"_monthly_report" + ".pdf"
    print("creating file ",file_name)
    html.write_pdf(target=file_name)


@celery.task
def send_email(to_address="sandip@gmail.com", subject="testing mail hog", message="testing mail hog"):
    current_app.logger.info("inside send email function")
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_ADDRESS
    msg['Subject'] = subject

    msg.attach(MIMEText(message,'html)'))
    s= smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()             
    return jsonify({"message":"email sent"})


@celery.task()
def send_email_with_attachment(to_address="sandip@gmail.com", subject="BlogLite Monthly Engagement Report",
 message="Dear user, please find attached your monthly engagement report",file_name="monthly report", PATH_TO_FILE=None):
    msg = MIMEMultipart()
    body_part = MIMEText(message, 'plain')
    msg['Subject'] = subject
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address

    msg.attach(body_part)

    PATH_TO_FILE = PATH_TO_FILE
    FILE_NAME = "monthly_report.pdf"

    with open(PATH_TO_FILE,'rb') as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
    encoders.encode_base64(part)
        # msg.attach(MIMEApplication(file.read(), Name=FILE_NAME))
    part.add_header("Content-Disposition", f"attachment; filename = monthly_report.pdf")
    msg.attach(part)

    s= smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()  
    return jsonify({"message":"email sent with attachment"})



@celery.task
def generate_allPdf():
    # users = users_model.query.all()
    # for user in users:
    #     create_pdf_report(user)
    user = users_model.query.get(2)
    create_pdf_report(user)



