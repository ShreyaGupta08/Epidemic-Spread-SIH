import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "epidemicalerts@gmail.com"  # Enter your address
receiver_email = "time.traveller.san@gmail.com"  # Enter receiver address
password = "epidemicspreadsih"
message = """\
Subject: Alert

This is to notify that drug availability in your pharmacy is below the predicted requirements."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
