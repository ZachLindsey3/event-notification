# import smtplib
# from email.mime.text import MIMEText

# with open('test_text.txt', 'r') as input:
#     msg = MIMEText(input.read())

# msg['Subject'] = 'TEST EMAIL'
# msg['From'] = sender
# msg['To'] = recipient

# s = smtplib.SMTP('localhost', 1025)
# s.sendmail(sender, [recipient], msg.as_string())
# s.quit()

import smtplib
import config

carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
	'sprint':   '@page.nextel.com'
}

to_number = config.test_phone_destination.format(carriers['verizon'])
to_email = config.test_email_destination

def send_message(message, to_address):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    auth = (config.test_email_source, config.email_api_key)

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_address, message)
    server.quit()

test_message = 'Test part 2'
send_message(test_message, to_email)

print("goodbye world")