import os

import humanize
from django.core.mail import send_mail

from utils.alerts import publish_on_telegram_channel


def get_message(a):
	try:
		message = {}

		m = '<div class="container container-fluid text-center">'
		m += '<h3>Dear Professor,</h3>'

		message['P'] = f'<div>{a.person.first_name} {a.person.last_name} wants to take a leave.</div>'
		message['A'] = f'<div>Your application that was created <b>{humanize.naturaltime(a.created_at)}</b> has been approved.</div>'
		message['R'] = f'<div>Your application that was created <b>{humanize.naturaltime(a.created_at)}</b> has been rejected by {a.up_next.get_role_display()}.</div>'

		m += str(message[a.status])
		m += '<h2>Application Details</h2>'
		m += '<div>• From ' + str(a.start_date) + ' to ' + str(a.end_date) + '<br>'
		m += '• Reason: ' + a.comments + '<br>'
		m += '• Created at: ' + str(humanize.naturaltime(a.created_at)) + '<br>'
		m += '• Updated at: ' + str(humanize.naturaltime(a.updated_at)) + '</div>'
		m += '<br><br><footer>--<br>Regards<br>' + 'Team LMS</footer>'
		m += '</div>'

		template = '<html><head><style>div{font-size=1.4rem; line-height: 1.4rem;}</style></head><body>' + str(m) + '</body></html>'
		return template
	except Exception as e:
		publish_on_telegram_channel(chat_id=int(os.getenv('TelegramChannel')), message=str(e) + ' \n get_message():30')


def send_application_mail(application):
	try:
		subject = 'Leave Application'
		message = get_message(application)
		from_email = 'Team LNMIIT Leave Management System'
		recipient_list = ['19uec117@lnmiit.ac.in', str(application.up_next.email)]
		html_message = message
		send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, html_message=html_message)
	except Exception as e:
		publish_on_telegram_channel(chat_id=int(os.getenv('TelegramChannel')), message=str(e))
