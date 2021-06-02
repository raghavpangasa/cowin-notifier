from twilio.rest import Client


class SendSMS():
    def __init__(self):
        TWILIO_ACCOUNT_SID = "ACc466d9b37ec9ea6f522e199774e56a1c"
        AUTH_TOKEN = "3bd16147d3dd5a6b16bb1d0235aaca7e"
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
            
