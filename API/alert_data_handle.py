import json
import datetime
from twilio.rest import Client
import tweepy
import os
import smtplib, ssl
import numpy as np

def to_name(diseaseid):
    con, cursor = make_connection()
    query = f"""
            SELECT * from Diseases
            where id = {diseaseid}
        """
    try:
        cursor.execute(query)
        data = cursor.fetchone()
    except Exception as e:
        print(f"Exception {e} in Pharmacy")
    finally:
        con.close()
    return data[1]

def send_email(amount, state):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "<sender email"  # Enter your address
    receiver_email = "<receiver email>"  # Enter receiver address
    password = "epidemicspreadsih"
    message = f"""\
        Subject: Alert

        This is to notify that spread of epidemic dengue has been predicted to around {amount} cases in your region.
        Please take necessary actions.
    	Thank you.
    	E-pidemic Alerts
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return False

def same(l1, l2, dl1, dl2):
    sum_dif = abs(l1 - dl1) + abs(l2 - dl2)
    if sum_dif < 0.5:
        return True
    return False

def location_to_district(location):
    l1, l2 = location.split()
    l1, l2 = float(l1[1:]), float(l2[:-1])
    my_dir = os.path.dirname(__file__)
    district_file = os.path.join(my_dir, "district.csv")
    with open("district.csv") as handle:
        districts = handle.readlines()
    for line in districts:
        line = line.split(',')
        try:
            dl1, dl2 = float(line[-2]), float(line[-3])
        except:
            continue
        if same(l1, l2, dl1, dl2):
            return line[0]
    return districts[1].split(',')[0]

class Alert():
    def __init__(self):
        my_dir = os.path.dirname(__file__)
        self.alert_file_name = os.path.join(my_dir, "alert_data.json")
        self.correlated_file = os.path.join(my_dir, "correlated.json")
        self.time_predictions = os.path.join(my_dir, "time_predictions.json")
        self.THRESHHOLD = 2

    def update(self, diseaseid, location):
        send_alert = False
        with open(self.alert_file_name) as handle:
            json_data = json.loads(handle.read())
        try:
            json_data[location][diseaseid] += 1
        except:
            try:
                json_data[location][diseaseid] = 1
            except:
                json_data[location] = {}
                json_data[location][diseaseid] = 1
        if json_data[location][diseaseid] > self.THRESHHOLD:
            send_alert = True
        with open(self.alert_file_name, 'w') as fp:
            json.dump(json_data, fp)
        return send_alert

    def send_sms(self, epidemic):
        print("\n\n>>> Sending SMS <<< \n\n")
        account_sid = 'ID'
        auth_token = 'ID'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                 body=f'A {epidemic} outbreak has been detected in your nearby areas. Take caution and click here to know more https://forumepi.createmybb4.com/',
                 from_='<sender>',
                 to='<receiver>'
             )

        print("SMS sent to people.")

    def correlated(self, diseaseid, location):
        district = location_to_district(location)
        with open(self.correlated_file) as handle:
            json_data = json.loads(handle.read())
        try:
            json_data[diseaseid].append(district)
        except:
            json_data[diseaseid] = [district]
        with open(self.correlated_file, 'w') as fp:
            json.dump(json_data, fp)
        return True

    def time_prediction(self, diseaseid):
        val = open("start_month.txt").read()
        if val.strip() != 'n':
            return True
        else:
            with open('start_month.txt', 'w+') as handle:
                handle.write('old')
            with open(self.time_predictions) as handle:
                json_data = json.loads(handle.read())
            send_email(json_data["Delhi"], diseaseid)
            return True


    def get_threshholds(self):
        my_dir = os.path.dirname(__file__)
        population = os.path.join(my_dir, "population.json")
        with open(population) as handle:
            json_data = json.loads(handle.read())
        for key in json_data:
            json_data[key] *= 0.015
        return json_data

    def post_twitter(self, dname, location):
        print("\n\n>>> Sending tweet <<< \n\n")
        consumer_key ="KEY"
        consumer_secret ="KEY"
        access_token ="KEY"
        access_token_secret ="KEY"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        s = f"""
                Widespread of {dname} has been observed in the areas near {location_to_district(location)}. Please, take caution. For more information visit the forums https://forumepi.createmybb4.com/
            	E-pidemic Alerts. {str(np.random.rand())[2]}
        """
        api.update_status(status = s)
