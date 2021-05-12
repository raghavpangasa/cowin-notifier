from twilio.rest import Client
from ..utils import config


class SendSMS():
    def __init__(self):
        TWILIO_ACCOUNT_SID = config.TWILIO_ACCOUNT_SID
        AUTH_TOKEN = config.TWILIO_AUTH_TOKEN
        self.client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self,centre, phoneNumber):
        if phoneNumber[0:3] != "+91":
            phoneNumber = "+91" + phoneNumber
        try:
            message = self.client.messages.create(
                body="Mil Gaya Slot @ " + str(centre),
                from_=config.TWILIO_PHONE_NUMBER,
                to="+91" + phoneNumber
            )
            print("SMS Sent")
        except Exception as e:
            print(e)
            print("Error sending SMS, contact developer")
            
