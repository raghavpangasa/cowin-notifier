import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..utils import config

class SendEmail():

    def __init__(self):
        #The mail addresses and password
        self.sender_address = config.YOUR_EMAIL_ID
        self.sender_pass = config.YOUR_EMAIL_PASSWORD
        #Setup the MIME
        self.session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        self.session.starttls() #enable security
        self.session.login(self.sender_address, self.sender_pass) #login with mail_id and password

    def sendEmail(self,centreName, receiver_address):
        try:
            # import pdb; pdb.set_trace()
            # self.session.connect()
            message = MIMEMultipart()
            message['From'] = self.sender_address
            message['To'] = receiver_address
            message['Subject'] = 'COWIN Slot Availability Alert'   #The subject line
            #The body and the attachments for the mail
            mail_content = "A slot is available at the following centre: \n" + str(centreName)
            message.attach(MIMEText(mail_content, 'plain'))
            #Create SMTP session for sending the mail
            text = message.as_string()
            self.session.sendmail(self.sender_address, receiver_address, text)
            # self.session.quit()
            print('Mail Sent')
        except Exception as e:
            print(e)
            print("Error sending email, contact developer")