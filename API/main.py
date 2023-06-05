from application import create_app
from flask import current_app
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import logging
from application.utils.first_request import create_dev_db, create_prod_db
from application.models.users import User as users_model, db
from application.models.post import Post as post_model, db
# from application import cache
from application.cache import cache
from datetime import datetime
from application.celery_system import make_celery
from sqlalchemy.exc import IntegrityError
import random
from celery.schedules import crontab
from flask import jsonify
from flask_mail import Mail, Message
from json import dumps
from httplib2 import Http
from flask import render_template, request
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from xmlrpc.client import SERVER_ERROR
from flask import jsonify, current_app
from datetime import timedelta, time
from jinja2 import Template
from weasyprint import HTML
from flask_security import auth_required
import pandas as pd
from flask_login import current_user
from werkzeug.exceptions import BadRequest


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = 'sandip@gmail.com'
SENDER_PASSWORD = ''


dev_app = create_app(DevelopmentConfig)
prod_app = create_app(ProductionConfig)
test_app = create_app(TestingConfig)
celery = make_celery(dev_app)
# mail = Mail(dev_app)

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


dev_app.before_first_request(create_dev_db)
test_app.before_first_request(create_dev_db)
prod_app.before_first_request(create_prod_db)


# #testing caching
# @dev_app.route("/home")
# @cache.cached(timeout=50)
# def home():
#     return f"hello friend, {datetime.utcnow()}"


@celery.task
def inactive_users():
    users = users_model.query.all()
    inactive_users = []
    # Current date and time
    now = datetime.now()
    # Midnight today
    midnight = datetime.combine(now.date(), time.min)
    current_app.logger.info(f"today date is {midnight}")
    for user in users:
        if len(list(user.posts))>0:
            current_app.logger.info(f'user:{user.username}, last_post:{user.posts[-1].creation_date}, last_post_old:{midnight>user.posts[-1].creation_date+timedelta(hours=5, minutes=30)}')
            if midnight>user.posts[-1].creation_date+timedelta(hours=5, minutes=30):
                inactive_users.append(user.username)
        else:
            inactive_users.append(user.username)
    current_app.logger.info(f'inactive user: {inactive_users}')
    return inactive_users


@celery.task
def send_webhook_toList():
    user_list = inactive_users()
    for user in user_list:
        url = 'https://chat.googleapis.com/v1/spaces/AAAAnW64g2E/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=i-U_tRlm_-Tl4lLN035i92eBnmE6EYQYZX-UaQ7Ho8A%3D'
        bot_message = {
            'text': f'hey {user}, you have not shared anything in BlogLite today. Please write your mind today'}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
    current_app.logger.info("daily alerts sent")


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
    msg['From'] = "mailer@BlogLite.com"
    msg['To'] = to_address

    msg.attach(body_part)

    PATH_TO_FILE = PATH_TO_FILE
    FILE_NAME = "monthly_report.pdf"

    with open(PATH_TO_FILE,'rb') as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = monthly_report.pdf")
    msg.attach(part)

    s= smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()  
    return jsonify({"message":"email sent with attachment"})

@celery.task
def generate_allPdf():
    users = users_model.query.all()
    for user in users:
        create_pdf_report(user)




@celery.task
def generate_and_send_monthly_report():
    generate_allPdf()
    users = users_model.query.all()
    for user in users:
        send_email_with_attachment(to_address=user.email, PATH_TO_FILE=str(user.id)+"_"+ str(user.username)+"_monthly_report" + ".pdf")


@celery.task
def generate_and_send_user_report(active_user_id):
    generate_allPdf()
    user = users_model.query.get(active_user_id)
    send_email_with_attachment(to_address=user.email, PATH_TO_FILE=str(user.id)+"_"+ str(user.username)+"_monthly_report" + ".pdf")





@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    sender.add_periodic_task(
            # crontab(hour=21, minute=57),
            crontab(minute=54, hour=23, day_of_month=28),
            # 10.0,
            send_webhook_toList.s(),
            name='daily alert'
        )

    sender.add_periodic_task(
            # crontab(hour=22, minute=6),
            crontab(minute=55, hour=23, day_of_month=28),
            # 30.0,
            generate_and_send_monthly_report.s(),
            name='monthly report'
        )


@celery.task
def process_excel(active_user_id):
    df = pd.read_csv("postUpload.csv")
    try:
        for index, row in df.iterrows():
            title=row['title']
            description=row['description']
            current_local_time = datetime.utcnow()
            post = post_model(title=title, description=description, user_id=active_user_id, creation_date=current_local_time)
            db.session.add(post)
            db.session.commit()
            current_app.logger.info(f'post added to the database at {current_local_time}')
            print("one post updated")
    except IntegrityError:
            current_app.logger.warning(
                'Could not add data to database because of conflict')
            db.session.rollback()
            raise BadRequest
    url = 'https://chat.googleapis.com/v1/spaces/AAAAnW64g2E/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=i-U_tRlm_-Tl4lLN035i92eBnmE6EYQYZX-UaQ7Ho8A%3D'
    bot_message = {
        'text': f'hey user, your posts have been uploaded successfully, you can refresh your profile page to view the published posts'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    return df.to_dict()


@auth_required('token')
@dev_app.route("/uploadPosts", methods= ["POST"])
def uploadPosts():
    file = request.files['file']
    file_path = file.save("postUpload.csv")
    result = process_excel.delay(current_user.id)
    return jsonify({'message': "you will get a Google chat notification once the posts are published successfully"})


@auth_required('token')
@dev_app.route("/sendPosts")
def sendPosts():
    result = generate_and_send_user_report.delay(current_user.id)
    return jsonify({'message': "an email will be sent to you"})






