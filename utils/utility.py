import os
import json
import requests
import telegram
from django.core.mail import send_mail


def send_application_mail(application):
	try:
		subject = 'Leave Application'
		recipient_list = ['19ucs257@lnmitt.ac.in']
		html_message = '<h1>Leave Application</h1>'
		send_mail(subject=subject, message=application, recipient_list=recipient_list, html_message=html_message)
	except Exception as e:
		print(e)

def custom_alert_slack(message):
	text = ""
	text = "%s" % message
	requests.post(os.getenv('SLACK_WEBHOOK'), data=json.dumps({"text": text}), headers={'Content-type': 'application/json'})

def publish_on_telegram_channel(chat_id, message, token=None, image=None):
	if not token:
		token = os.getenv('TelegramBotsToken')
	bot = telegram.Bot(token=token)
	if image is None:
		bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML', disable_web_page_preview="true")
	else:
		bot.send_photo(chat_id=chat_id, photo=open(image, 'rb'), caption=message, parse_mode='HTML', disable_web_page_preview="true")


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
