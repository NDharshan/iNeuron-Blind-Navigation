import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("mail@mail.com", "thisismynewpassword")

# message to be sent
message = "SOS test "

# sending the mail
s.sendmail("fokosaf649@gmail.com", "ndarshanraju@gmail.com", message)

# terminating the session
s.quit()
