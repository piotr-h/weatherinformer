#! python3
# The aim of this application is to download the weather forecast for my location (currently lat 52.23, lon 21.00 - 
# Palace of Culture and Science) for the following 12 hours, and check wheter it is going to rain. Based on that, I will 
# be sent an email telling me if I should take an umbrella with me or not. If there's going to be rain,
# I will also be informed of the approximate time it'll occurr.

import requests, json, smtplib, email.utils
from email.mime.text import MIMEText


# credentials for accessing APIs
weatherAPIkey = input('Please provide the API key for weatherbit ')
sending_email = input('Please provide the sending email ')
email_password = input('Please provide the sending email account password ')
smtp_server = input('Please provide the smtp address for the sending email ')
receiving_email = input('Please provide the receiving email ')

# getting data from weatherbit
url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly"
querystring = {"lang":"en","hours":"12","lat":"52.23","lon":"21.00"}
headers = {
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
    'x-rapidapi-key': weatherAPIkey
    }
response = requests.request("GET", url, headers=headers, params=querystring)

# transforming json to python dictionary
w_dict = json.loads(response.text)

# processing weather data
message_list = []
for i in range(0, len(w_dict['data'])):
	if w_dict['data'][i]['precip'] > 0:
		message_list.append(w_dict['data'][i]['timestamp_local'][11:16])

# constructing a message
message = ''
if len(message_list) == 0:
	message = 'Today it\'s not going to rain; do not take your umbrella'
else:
	message = 'Take an umbrella, as it\'s going to rain around '
	if len(message_list) == 1:
		message += (message_list[0] + '.')
	elif len(message_list) == 2:
		message += message_list[0] + ' i ' + message_list[1] + '.'
	else:
		for i in message_list[:-2]:
			message += (i + ', ')
		message += (message_list[-2] + ' i ' + message_list[-1] + '.')

# sending a message via email
msg = MIMEText(message)
msg['To'] = email.utils.formataddr(('Recipient', receiving_email))
msg['From'] = email.utils.formataddr(('Sender', sending_email))
msg['Subject'] = 'Prognoza pogody na dziś'

# the below works only with servers using SSL on port 465, i.e. smtp.poczta.onet.pl
server = smtplib.SMTP_SSL(smtp_server, 465)
server.ehlo()
server.login(sending_email, email_password)
try:
	server.sendmail(sending_email, receiving_email, msg.as_string())
finally:
	server.quit()



