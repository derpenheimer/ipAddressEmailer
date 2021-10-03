
import smtplib
import ssl
import getpass


def prompt(prompt):
    return input(prompt).strip()

# Get start parameters
hostServer = input("Server: ") #'smtp.gmail.com'
hostPort = input("Port: ") #465
hostUser = input("Username: ") #'your.address.here@gmail.com'
hostPwd = getpass.getpass("Password: ")
addrTo  = input("To: ") #'recv.address.here@live.ca'

# Add the From: and To: headers at the start
msg = ("From: %s\r\nTo: %s\r\n\r\n%s"
       % (hostUser, addrTo, "test message"))

servertest = smtplib.SMTP_SSL(hostServer, hostPort, context=ssl.create_default_context())

with smtplib.SMTP_SSL(hostServer, hostPort, 20, context=ssl.create_default_context()) as server:
    server.ehlo()
    server.login(hostUser, hostPwd)
    server.sendmail(hostUser, addrTo, msg)
