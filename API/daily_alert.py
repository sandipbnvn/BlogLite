from main import celery
from application.models.users import User as users_model, db
from application.models.post import Post as post_model, db
from flask import current_app
from datetime import datetime
from datetime import timedelta, time
from httplib2 import Http
from json import dumps
from celery.schedules import crontab



#helper function to get list of inactive users to whom daily alert has to be sent
@celery.task()
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



#user triggered celery task
@celery.task()
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


#celery daily scheduled alerts and monthly report
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=21, minute=35),
            send_webhook_toList.s(),
            name='daily alert'
        )