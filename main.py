import requests
import json
import time
from utils.filterData import FilterData
from utils.sendEmail import SendEmail
from utils.sendSMS import SendSMS
from utils.sendSMS import SendSMS
from utils.alert import Audio
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from multiprocessing import Process
import webbrowser
import datetime
today = datetime.date.today()

fD = FilterData()
sD = SendEmail()
ss = SendSMS()
audio = Audio()
audio.play()

def getAppointMent(pincode, date):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2172.95 Safari/537.36'}
    apiURL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pincode + "&date=" + date
    response = requests.get(apiURL, headers=headers)
    # import pdb; pdb.set_trace()
    try:
        data = json.loads(response.content.decode())
    except:
        print(response)
        data = ""
    return data


def getPossibility(pincode, date, vaccine, fees):
    data = getAppointMent(pincode, date)
    if data:
        for cent in data["centers"]:
        # import pdb; pdb.set_trace()
            if fD.paidFilter(cent, fees):
                for ses in cent["sessions"]:
                    if fD.vaccineFilter(ses,vaccine):
                        return True
    return False



def startSearch(response, phone,emailid,pincode, date, vaccine, fees, sms=True,email=True,alert=True):
    # pincode = "110049"
    # date = "06-05-2021"
    while True:
        print("Searching for your slot!!")
        data = getAppointMent(pincode, date)
        if data:
            for cent in data["centers"]:
            # import pdb; pdb.set_trace()
                if fD.paidFilter(cent, fees):
                    # sD.sendEmail(cent,emailid)
                    mila = False
                    for ses in cent["sessions"]:
                        # mess = "Centre Name: " + str(cent["name"]) + ",\nAddress: " + str(cent["address"]) + ",\nVaccine: " + str(ses["vaccine"])
                        # if cent["fee_type"] == "Paid":
                        #     mess = mess + ",\nFees: " + str(cent["vaccine_fees"])
                        # else:
                        #     mess = mess + ",\nFees: Free" 
                        # sD.sendEmail(mess,emailid)
                        # ss.send_message(mess,phone)
                        if fD.vaccineFilter(ses,vaccine) and fD.ifAvailable(ses):
                            print("Slot mil gaya! @" + cent["name"])
                            mess = "Centre Name: " + str(cent["name"]) + ",\nAddress: " + str(cent["address"]) + ",\nVaccine: " + str(ses["vaccine"])
                            if cent["fee_type"] == "Paid":
                                mess = mess + ",\nFees: " + str(cent["vaccine_fees"])
                            else:
                                mess = mess + ",\nFees: Free" 
                            mila = True
                            if email:
                                sD.sendEmail(mess,emailid)
                            if sms:
                                ss.send_message(mess,phone)
                            if alert:
                                audio.play()
                            response.append(ses)
                            # Send Alert
                    if mila:
                        return response
        else:
            print("error")
        time.sleep(5)


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
RUNNING = False
result = ""

@app.route("/", methods=['GET', 'POST'])
def hello():
    global RUNNING, result
    # print('#########')
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        pincode = request.form['pincode']
        covaxin = False
        covishield = False
        paid = False
        free = False
        smsAlert = False
        emailAlert = False
        soundAlert = False

        if "covaxin" in request.form:
            covaxin = True
        if "covishield" in request.form:
            covishield = True
        if "paid" in request.form:
            paid = True
        if "free" in request.form:
            free = True
        if "smsAlert" in request.form:
            smsAlert = True
        if "emailAlert" in request.form:
            emailAlert = True
        if "soundAlert" in request.form:
            soundAlert = True

        vaccineFilter = ""
        if covishield and not covaxin:
            vaccineFilter = "COVISHIELD"
        if covaxin and not covishield:
            vaccineFilter = "COVAXIN"
        
        feesFilter = -1
        if free and not paid:
            feesFilter = 0
        if paid and not free:
            feesFilter = 1

        date = today.strftime('%d-%m-%Y')
        # date = "10-05-2021"
        # print(name, " ", email, " ", phone,pincode, covaxin,covishield,paid,free,smsAlert,emailAlert,soundAlert)
        
        return_values = []
        possible = getPossibility(pincode,date,vaccineFilter,feesFilter)
        # print(possible,"##########")
        if possible:

            if not RUNNING:
                p1 = Process(target=startSearch(return_values, phone,email,pincode,date,vaccineFilter,feesFilter,smsAlert,emailAlert,soundAlert))
                RUNNING = p1
                # p1.start()
            else:
                RUNNING.terminate()
                p1 = Process(target=startSearch(return_values, phone,email,pincode,date,vaccineFilter,feesFilter,smsAlert,emailAlert,soundAlert))
                RUNNING = p1
                # p1.start()
            result = str(return_values)
            # return render_template('hello.html', form=form, result = result)

        else:
            result = "Please re-enter the details, no centres found for current application."
            # return render_template('hello.html', form=form, result = result)
        try:
            RUNNING.join()
        except:
            pass
    return render_template('hello.html')

def open_browser():
    url = 'http://localhost:8888/'

    # MacOS
    chrome_paths = ['open -a /Applications/Google\ Chrome.app %s','C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s', '/usr/bin/google-chrome %s']

    for cp in chrome_paths:
        try:
            webbrowser.get(cp).open(url)
            webbrowser.open(url)
            break
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    open_browser()
    app.run(port=8888)

    # print("###### Hello!!!!", )

    # app.run()