import smtplib
import keyring
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

def send_email():
    date = datetime.datetime.now()
    date = str(date.date())
    subject = "Tally Shows for the Week of %s" % date

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "TallyMusic.net"
    msg['Date'] = formatdate(localtime=True)
    msg['To'] = "dannybrown37@gmail.com"

    msg.attach(MIMEText("Here are this week's shows!"))

    file_name = "concerts-%s.json" % date

    with open("parsed_output/%s" % file_name) as f:
        part = MIMEApplication(
            f.read(),
            Name=file_name
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    msg.attach(part)


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    email = "tallymusicwebmaster@gmail.com"
    server.login(email, keyring.get_password('tmwebmaster', email))
    server.sendmail(
        "TallyMusic.net",
        "dannybrown37@gmail.com",
        msg.as_string()
    )
    server.quit()

if __name__ == '__main__':
    send_email()
