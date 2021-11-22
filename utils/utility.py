import os
from django.core.mail import send_mail

from .alerts import publish_on_telegram_channel


def send_application_mail(person, recipient_list, application):
	try:
		subject = 'Leave Application'
		name = application.person.first_name + ' ' + application.person.last_name
		message = name + ' wants to take a leave.<br>'
		message += '<p>From ' + str(application.start_date) + ' to ' + str(application.end_date) + '</p><br>'
		# message += '<p>Reason: ' + application.comments + '</p><br>'
		message += '<p>Regards<br>' + 'Team LMS<br>'
		from_email = 'Team LNMIIT Leave Management System'
		html_message = '<div>' + message + '</div>'
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
