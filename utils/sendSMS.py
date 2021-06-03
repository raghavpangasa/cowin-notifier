from twilio.rest import Client


class SendSMS():
    def __init__(self):
        TWILIO_ACCOUNT_SID = ""
        AUTH_TOKEN = ""
        self.client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self,centre, phoneNumber):
        if phoneNumber[0:3] != "+91":
            phoneNumber = "+91" + phoneNumber
        try:
            message = self.client.messages.create(
                body="Mil Gaya Slot @ " + str(centre),
                from_='+12562026178',
                to=phoneNumber
            )
            print("SMS Sent")
        except Exception as e:
            print(e)
            print("Error sending SMS, contact developer")
            
