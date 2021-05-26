from flask import Flask,request,session,render_template
import requests,time
from datetime import datetime,timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/CheckSlot')
def check():
    pin = request.args.get("pincode")
    age = request.args.get("age")
    data = list()
    result = findSlot(age,pin,data)
    if(result == 0):
        return render_template("noavailable.html")
    return render_template("slot.html",data = data)

def findSlot(age,pin,data):
    flag = 'y'
    num_days =  2
    actual = datetime.today()
    list_format = [actual + timedelta(days=i) for i in range(num_days)]
    actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
    
    # print(actual_dates)
    while True:
        counter = 0
        for given_date in actual_dates:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pin, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
            result = requests.get(URL,headers = header)
            if(result.ok):
                # print("Ok")
                response_json = result.json()
                if(response_json["centers"]):
                    # print("Ok")
                    if(flag.lower() == 'y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                datas = list()
                                datas.append(pin)
                                datas.append(given_date)
                                datas.append(center["name"])
                                # print("\t", center["name"])
                                datas.append(center["block_name"])
                                # print("\t Price : ",center["fee_type"])
                                datas.append(center["fee_type"])
                                datas.append(session["available_capacity"])
                                if(session["vaccine"]!=''):
                                    datas.append(session["vaccine"])
                                counter =counter + 1
                                # print(datas)
                                if(session["available_capacity"]>0):
                                    data.append(datas)
            else:
                print("No response")
        if counter == 0:
            return 0
        return 1



if __name__ == "__main__":
    app.run()