import os
from django.core.mail import send_mail

from .alerts import publish_on_telegram_channel

def send_application_mail(user, application):
	try:
		subject = 'Leave Application'
		name = user.person.first_name + ' ' + user.person.last_name
		print(name)
		message = name + ' wants to take a leave.\n'
		message += 'From ' + str(application.cleaned_data['start_date']) + ' to ' + str(application.cleaned_data['end_date'])
		from_email = 'Team LNMIIT Leave Management System'
		recipient_list = ['19ucs257@lnmiit.ac.in']
		html_message = '<h3>' + message + '</h3>'
		send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, html_message=html_message)
	except Exception as e:
		publish_on_telegram_channel(chat_id=int(os.getenv('TelegramChannel')), message=str(e))

#  CHARSET = 'utf-8'
#     body_html = ("""<html>
#         <head></head>
#         <body>
#           <p>%s.</p>
#         </body>
#         </html>
#                     """ % message)
#     response = client.send_email(
#         Destination={
#             'ToAddresses': [
#                 recipient,
#             ],
#         },
#         Message={
#             'Body': {
#                 'Html': {
#                     'Charset': CHARSET,
#                     'Data': body_html,
#                 },
#                 'Text': {
#                     'Charset': CHARSET,
#                     'Data': message,
#                 },
#             },
#             'Subject': {
#                 'Charset': CHARSET,
#                 'Data': subject,
#             },
#         },
#         Source=sender,
#     )
#     return response
