# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
# from email.mime.text import MIMEText
# import smtplib
# from xmlrpc.client import SERVER_ERROR
# from .main import dev_app
# from flask import jsonify, current_app

# SMTP_SERVER_HOST = "localhost"
# SMTP_SERVER_PORT = 1025
# SENDER_ADDRESS = 'sandip@gmail.com'
# SENDER_PASSWORD = ''

# @dev_app.route("/send_email")
# def send_email(to_address="sandip@gmail.com", subject="testing mail hog", message="testing mail hog"):
#     current_app.logger.info("inside send email function")
#     msg = MIMEMultipart()
#     msg['To'] = to_address
#     msg['From'] = SENDER_ADDRESS
#     msg['Subject'] = subject

#     msg.attach(MIMEText(message,'html)'))
#     s= smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
#     s.login(SENDER_ADDRESS,SENDER_PASSWORD)
#     s.send_message(msg)
#     s.quit()             
#     return jsonify({"message":"email sent"})

# def send_email_with_attachment(to_address, subject, message,file_name):
#     msg = MIMEMultipart()
#     body_part = MIMEText(message, 'plain')
#     msg['Subject'] = subject
#     msg['From'] = SENDER_ADDRESS
#     msg['To'] = to_address

#     msg.attach(body_part)

#     PATH_TO_CSV_FILE = 'csv_output/'+ file_name #user_log_20220820.csv'
#     FILE_NAME = file_name # 'user_log_20220820.csv'

#     with open(PATH_TO_CSV_FILE,'rb') as file:
#         msg.attach(MIMEApplication(file.read(), Name=FILE_NAME))

#     s= smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
#     s.login(SENDER_ADDRESS,SENDER_PASSWORD)
#     s.send_message(msg)
#     s.quit()  

#     return True

# #send_email("MK@gmail.com","Report","hello ..................")

# # use to invoke mailhog server in wsl command line
# # ~/go/bin/MailHog