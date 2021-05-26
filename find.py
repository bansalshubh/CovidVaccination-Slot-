import requests,time
import json
from datetime import datetime,timedelta

def findSlot(age,pin):
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
                            # print(center)
                            for session in center["sessions"]:
                                # if(session['min_age_limt']<=age and session["available_capacity"]>0):
                                print('Pincode : ' + pin)
                                print("Available on: {}".format(given_date))
                                print("\t", center["name"])
                                print("\t",center["block_name"])
                                print("\t Price : ",center["fee_type"])
                                print("\t Availability : ",session["available_capacity"])

                                if(session["vaccine"]!=''):
                                    print("\t Vaccine Type : ",session["vaccine"])
                                print("\n")
                                counter =counter + 1
            else:
                print("No response")
        if counter == 0:
            print("No vaccination slot available !")
        else:
            print("search Completed")
        print(counter)
        dt = datetime.now() + timedelta(minutes = 2)
        while datetime.now()<dt:
            time.sleep(1)


findSlot(52,"332713")