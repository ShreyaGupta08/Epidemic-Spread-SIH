[nbvcytreaz import json
import datetime
from twilio.rest import Client
import tweepy
import os

class Alert():
    def __init__(self):
        my_dir = os.path.dirname(__file__)
        self.alert_file_name = os.path.join(my_dir, "alert_data.json")
        self.date_track_file = os.path.join(my_dir, "date_track.json")
        self.THRESHHOLD = 3
        print("obj made")

    def update(self, diseaseid, location):
        print(f"I GOT location: {location}, {diseaseid}")
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
        print(json_data[location][diseaseid])
        if json_data[location][diseaseid] > self.THRESHHOLD:
            send_alert = True
        with open(self.alert_file_name, 'w') as fp:
            json.dump(json_data, fp)
        return send_alert

    def send_sms(self, epidemic):
        account_sid = 'AC31987ba930b2457fb9c8b33e7a9c9787'
        auth_token = 'e21d38f47b597ff5b1d19afa1dc6f6b2'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                 body=f'{epidemic} outbreak detected in nearby areas. Click here to know more forums.epidemic_intelligence.com/',
                 from_='+14064206569',
                 to='+919873957783'
             )
        print("SMS sent to people.")


# consumer_key ="AU1mZxFBAJQdeNae7AaMoJtCa"
# consumer_secret ="2Gs56JeKwrKhG8QaQx30mES55KlTLgg6xo9lbrz5cVsPkVNdtl"
# access_token ="829709201681313793-M6qIHpjFgqTbWj8Snhxx2gF0UrJSfIc"
# access_token_secret ="uVO8Pky12alUaDHPSmDF6BWvhEGTnokN7jGQYopSsRFj0"
#
# # authentication of consumer key and secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#
# # authentication of access token and secret
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
#
# # update the status
# api.update_status(status ="alalalalalal")
Alert().update(213989, "asdasdas")
