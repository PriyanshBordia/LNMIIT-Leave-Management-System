import os
import json
import requests
import telegram

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
