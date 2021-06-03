from flask.wrappers import Response
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
import os, sys
base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)


# App config.
DEBUG = False
app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
RUNNING = False
result = ""


today = datetime.date.today()

fD = FilterData()
sD = SendEmail()
ss = SendSMS()
audio = Audio()
# audio.play()

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



def startSearch(response, phone,emailid,pincodes, date, vaccine, fees, sms=True,email=True,alert=True,dose1=True, dose2=True, age18=True, age45=True):
    # pincode = "110049"
    # date = "06-05-2021"
    while True:
        print("Searching for your slot!!")
        for pincode in pincodes:
            pincode = pincode.replace(" ","")
            data = getAppointMent(pincode, date)
            if data:
                for cent in data["centers"]:
                # import pdb; pdb.set_trace()
                    if fD.paidFilter(cent, fees):
                        # sD.sendEmail(cent,emailid)
                        mila = False
                        final_message = []
                        for ses in cent["sessions"]:
                            if fD.vaccineFilter(ses,vaccine) and fD.ifAvailable(ses, dose1,dose2) and fD.ageFilter(ses, age18,age45):
                                print("Slot mil gaya! @" + cent["name"])
                                # time.sleep(10)
                                mess = "\nCentre Name: " + str(cent["name"]) + ",\nAddress: " + str(cent["address"]) + ",\nDate: " + str(ses["date"]) + ",\nVaccine: " + str(ses["vaccine"])
                                if cent["fee_type"] == "Paid":
                                    mess = mess + ",\nFees: " + str(cent["vaccine_fees"])
                                else:
                                    mess = mess + ",\nFees: Free" 
                                if dose1 and not dose2:
                                    mess = mess + ",\nDose: 1st Dose"
                                if dose2 and not dose1:
                                    mess = mess + ",\nDose: 2nd Dose"
                                if age18 and not age45:
                                    mess = mess + ",\nAge Limit: 18-45"
                                if age45 and not age18:
                                    mess = mess + ",\nAge Limit: 45+"
                                mila = True
                                final_message.append(mess)
                                final_message.append("\n")
                                response.append(mess)
                                response.append("<br/>")
                                # Send Alert
                        if mila:
                            mess = "".join(final_message)
                            if email:
                                sD.sendEmail(mess,emailid)
                            if sms:
                                ss.send_message(mess,phone)
                            if alert:
                                audio.play()
                            return mess
            else:
                print("error")
            time.sleep(4)



@app.route("/", methods=['GET', 'POST'])
def hello():
    global RUNNING, result
    # print('#########')
    if request.method == 'POST':
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        pincodes = request.form['pincode'].split(",")
        covaxin = False
        covishield = False
        paid = False
        free = False
        smsAlert = False
        emailAlert = False
        soundAlert = False
        age18 = False
        age45 = False
        dose1 = False
        dose2 = False

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
        if "age18" in request.form:
            age18 = True
        if "age45" in request.form:
            age45 = True        
        if "dose1" in request.form:
            dose1 = True
        if "dose2" in request.form:
            dose2 = True

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
        progress = True
        for pincode in pincodes:
            pincode = pincode.replace(" ","")
            possible = getPossibility(pincode,date,vaccineFilter,feesFilter)
            if not possible:
                progress = False
        # print(possible,"##########")
        if progress:

            if not RUNNING:
                p1 = Process(target=startSearch(return_values, phone,email,pincodes,date,vaccineFilter,feesFilter,smsAlert,emailAlert,soundAlert, dose1, dose2, age18, age45))
                RUNNING = p1
                # p1.start()
            else:
                try:
                    RUNNING.terminate()
                except:
                    pass
                p1 = Process(target=startSearch(return_values, phone,email,pincodes,date,vaccineFilter,feesFilter,smsAlert,emailAlert,soundAlert))
                RUNNING = p1
                # p1.start()
            result = "Here are the available slots: <br><br><br>" +  "".join(return_values).replace('\n','<br>') + "<br><br><br>Re-enter the form to start again."
            # return render_template('hello.html', form=form, result = result)

        else:
            result = "Please re-enter the details, no centres found for current values."
            # return render_template('hello.html', form=form, result = result)
        try:
            RUNNING.join()
        except:
            pass
    return render_template('hello.html', response=result)

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