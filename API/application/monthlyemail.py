from jinja2 import Template
from mail.mail_main import send_email



def call_email(trc_master,loggging,toEmail):
    with open('mail/mail_template/TrackerEmail.html','r') as f:
        template = Template(f.read())
    send_email(toEmail,"Report",template.render(tracker_master=trc_master,loggging=loggging ))