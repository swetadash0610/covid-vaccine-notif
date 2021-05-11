import time
from cowin_api import CoWinAPI
import os
from twilio.rest import Client
from dotenv import load_dotenv

starttime = time.time()
load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
from_ =os.environ['FROM']
to =os.environ['TO']

district_id = os.environ['DIST']
min_age_limit = 18
pin_code = os.environ['PIN']
cowin = CoWinAPI()
available_centers = cowin.get_availability_by_district(
    district_id, min_age_limit)
available_centers = available_centers['centers']

while True:
    for value in available_centers:
        for session in value['sessions']:
            body = str(value['name'])+"-"+str(session['date']) + \
                "- "+str(session['available_capacity'])
            if session['min_age_limit'] == 18 and session['available_capacity'] != 0:
                message = client.messages.create(
                    body=body,
                    from_=from_,
                    to=to
                )
                print(message.sid)
    time.sleep(30.0 - ((time.time() - starttime) % 60.0))